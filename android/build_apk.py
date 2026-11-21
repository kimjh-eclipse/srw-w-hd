"""Build the Android APK (first version: original screens) without Gradle.

Tools: C:\\Android\\jdk, C:\\Android\\Sdk (platform 35, build-tools 35.0.0), NDK r27d in build/android-toolchain.
Core: build/android-arm64-api24/lib/arm64-v8a/libretro.so (scripts/build/build_android_arm64.ps1).
Output: android/out/SRW_W_HD.apk, signed with a local debug key (android/out/debug.keystore).

  py -3.11 -X utf8 android/build_apk.py
"""
import glob,os,shutil,subprocess,sys,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
JDK=Path(glob.glob(r'C:\Android\jdk\jdk-17*')[0]);SDK=Path(r'C:\Android\Sdk');BT=SDK/'build-tools/35.0.0';JAR=SDK/'platforms/android-35/android.jar'
NDK=ROOT/'build/android-toolchain/android-ndk-r27d';CLANG=NDK/'toolchains/llvm/prebuilt/windows-x86_64/bin/aarch64-linux-android24-clang.cmd'
CORE=ROOT/'build/android-arm64-api24/lib/arm64-v8a/libretro.so'
INC=ROOT/'emulator/desmume/desmume/src/libretro-common/include'
OUT=HERE/'out';env=dict(os.environ,JAVA_HOME=str(JDK),PATH=str(JDK/'bin')+os.pathsep+os.environ['PATH'])


def run(*a):
    print('>',' '.join(str(x) for x in a)[:200],flush=True)
    r=subprocess.run([str(x) for x in a],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if r.returncode:print(r.stdout[-3000:],r.stderr[-3000:]);sys.exit(1)
    return r.stdout


def main():
    if OUT.exists():shutil.rmtree(OUT,ignore_errors=True)
    lib=OUT/'apk/lib/arm64-v8a';lib.mkdir(parents=True);cls=OUT/'classes';cls.mkdir()
    run(CLANG,'-shared','-fPIC','-O2','-I',INC,HERE/'jni/host.c',HERE/'jni/hd.c','-o',lib/'libsrwwhost.so','-lGLESv2','-llog','-ldl','-Wl,-z,max-page-size=16384')
    shutil.copy2(CORE,lib/'libretro.so')
    shutil.copy2(CORE.parent/'libxbrz_compare.so',lib/'libxbrz_compare.so')
    run(BT/'aapt2.exe','link','--manifest',HERE/'AndroidManifest.xml','-I',JAR,'-o',OUT/'base.apk','--min-sdk-version','24','--target-sdk-version','35')
    srcs=[str(p) for p in (HERE/'src').rglob('*.java')]
    run(JDK/'bin/javac.exe','-source','1.8','-target','1.8','-bootclasspath',JAR,'-classpath',JAR,'-encoding','UTF-8','-d',cls,'-Xlint:-options',*srcs)
    classes=[str(p) for p in cls.rglob('*.class')]
    run(BT/'d8.bat','--min-api','24','--lib',JAR,'--output',OUT,*classes)
    unsigned=OUT/'unsigned.apk';shutil.copy2(OUT/'base.apk',unsigned)
    with zipfile.ZipFile(unsigned,'a',zipfile.ZIP_DEFLATED) as z:
        z.write(OUT/'classes.dex','classes.dex')
        for f in lib.iterdir():z.write(f,f'lib/arm64-v8a/{f.name}')
    aligned=OUT/'aligned.apk';run(BT/'zipalign.exe','-f','-p','4',unsigned,aligned)
    ks=HERE/'debug.keystore'
    if not ks.exists():
        run(JDK/'bin/keytool.exe','-genkeypair','-keystore',ks,'-storepass','android','-keypass','android','-alias','debug','-keyalg','RSA','-keysize','2048','-validity','10000','-dname','CN=SRW W HD debug')
    apk=OUT/'SRW_W_HD.apk'
    run(BT/'apksigner.bat','sign','--ks',ks,'--ks-pass','pass:android','--key-pass','pass:android','--out',apk,aligned)
    run(BT/'apksigner.bat','verify',apk)
    print('APK',apk,round(apk.stat().st_size/1e6,1),'MB')


if __name__=='__main__':main()
