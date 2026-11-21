param(
    [Parameter(Mandatory)]
    [string] $NdkPath,
    [ValidateRange(21, 35)]
    [int] $ApiLevel = 24,
    [ValidateRange(1, 64)]
    [int] $Jobs = 6
)

$ErrorActionPreference = 'Stop'
$project = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$ndk = (Resolve-Path -LiteralPath $NdkPath).Path
$ndkBuild = Join-Path $ndk 'ndk-build.cmd'
$llvm = Join-Path $ndk 'toolchains/llvm/prebuilt/windows-x86_64/bin'
$readElf = Join-Path $llvm 'llvm-readelf.exe'
$clang = Join-Path $llvm 'clang.exe'
$clangCpp = Join-Path $llvm 'clang++.exe'
foreach ($tool in @($ndkBuild, $readElf, $clang, $clangCpp)) {
    if (!(Test-Path -LiteralPath $tool -PathType Leaf)) {
        throw "Missing Android NDK tool: $tool"
    }
}

$source = Join-Path $project 'emulator/desmume/desmume/src'
$coreProject = Join-Path $source 'frontend/libretro'
$build = Join-Path $project "build/android-arm64-api$ApiLevel"
$objects = Join-Path $build 'obj'
$libraries = Join-Path $build 'lib'
$abiDirectory = Join-Path $libraries 'arm64-v8a'
New-Item -ItemType Directory -Force -Path $abiDirectory | Out-Null

& $ndkBuild -C $coreProject "APP_ABI=arm64-v8a" "APP_PLATFORM=android-$ApiLevel" "NDK_OUT=$objects" "NDK_LIBS_OUT=$libraries" "-j$Jobs"
if ($LASTEXITCODE -ne 0) { throw 'DeSmuME Android build failed' }

$core = Join-Path $abiDirectory 'libretro.so'
$symbols = & $readElf --dyn-syms --wide $core
if ($LASTEXITCODE -ne 0) { throw 'Could not read Android core exports' }
$symbols = $symbols -notmatch '\bUND\b'

# Verify the HD functions used by the existing frontend, including optional ones.
$adapter = Get-Content -Raw -LiteralPath (Join-Path $project 'emulator/hd_core.py')
$hdExports = [regex]::Matches($adapter, '\bretro_srw_\w+') |
    ForEach-Object Value | Sort-Object -Unique
$required = @('retro_init', 'retro_load_game', 'retro_run', 'retro_serialize', 'retro_unserialize') + $hdExports
foreach ($symbol in $required) {
    if (!($symbols -match "\b$symbol\s*$")) { throw "Missing Android core export: $symbol" }
}

$target = "--target=aarch64-linux-android$ApiLevel"
$nativeModules = @('native_composition', 'native_font_pixels', 'native_font_scan')
foreach ($module in $nativeModules) {
    $inputFile = Join-Path $project "emulator/$module.c"
    $outputFile = Join-Path $abiDirectory "lib$module.so"
    & $clang $target -std=c11 -O3 -fPIC -shared '-Wl,-z,max-page-size=16384' $inputFile -o $outputFile
    if ($LASTEXITCODE -ne 0) { throw "Android build failed: $module" }
}

$filter = Join-Path $source 'filter'
$bridge = Join-Path $project 'tools/xbrz_compare_bridge.cpp'
$xbrz = Join-Path $abiDirectory 'libxbrz_compare.so'
& $clangCpp $target -std=c++11 -O3 -fPIC -shared -static-libstdc++ '-Wl,-z,max-page-size=16384' "-I$filter" $bridge (Join-Path $filter 'xbrz.cpp') -o $xbrz
if ($LASTEXITCODE -ne 0) { throw 'Android build failed: xBRZ bridge' }

$artifacts = @($core, $xbrz) + @($nativeModules | ForEach-Object { Join-Path $abiDirectory "lib$_.so" })
foreach ($artifact in $artifacts) {
    $elfHeader = & $readElf -h $artifact
    if ($LASTEXITCODE -ne 0 -or !($elfHeader -match 'Machine:\s+AArch64')) {
        throw "Expected an ARM64 ELF library: $artifact"
    }
    $segments = & $readElf --program-headers --wide $artifact
    if ($LASTEXITCODE -ne 0) { throw "Could not read ELF segments: $artifact" }
    $loads = $segments -match '^\s+LOAD\s'
    if (!$loads -or ($loads -notmatch '\s0x4000\s*$')) {
        throw "Expected 16 KB load segment alignment: $artifact"
    }
}

$xbrzSymbols = & $readElf --dyn-syms --wide $xbrz
if ($LASTEXITCODE -ne 0) { throw 'Could not read Android xBRZ exports' }
$xbrzSymbols = $xbrzSymbols -notmatch '\bUND\b'
foreach ($symbol in @('srww_xbrz4_argb', 'srww_xbrz4_rgb')) {
    if (!($xbrzSymbols -match "\b$symbol\s*$")) { throw "Missing xBRZ export: $symbol" }
}

$artifacts | ForEach-Object { Get-FileHash -LiteralPath $_ -Algorithm SHA256 } |
    Select-Object Path, Hash | Format-Table -AutoSize
Write-Output "Verified $($required.Count) required core exports, two xBRZ exports and $($artifacts.Count) ARM64 ELF libraries."
