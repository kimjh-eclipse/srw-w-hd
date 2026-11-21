Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class WorkshopMonitorPower {
[DllImport("user32.dll",SetLastError=true)] public static extern IntPtr SendMessageTimeout(IntPtr window,uint message,IntPtr parameter,IntPtr value,uint flags,uint timeout,out IntPtr result);
}
"@
$monitorFlag=Join-Path $PSScriptRoot 'keep_monitor_off.flag'
$workFlag=Join-Path $PSScriptRoot 'keep_system_awake.flag'
while ((Test-Path -LiteralPath $monitorFlag) -and (Test-Path -LiteralPath $workFlag)) {
 $monitorResult=[IntPtr]::Zero
 [void][WorkshopMonitorPower]::SendMessageTimeout([IntPtr]0xffff,0x0112,[IntPtr]0xF170,[IntPtr]2,2,1000,[ref]$monitorResult)
 Start-Sleep -Seconds 15
}
