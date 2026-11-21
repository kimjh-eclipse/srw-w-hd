Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class SrwSystemAwake {
 [DllImport("kernel32.dll")]
 public static extern uint SetThreadExecutionState(uint flags);
}
"@
$holdFlag = 'C:\Emul\Workshop\SRW_W_HD\test_current\keep_system_awake.flag'
try {
 while (Test-Path -LiteralPath $holdFlag) {
  [void][SrwSystemAwake]::SetThreadExecutionState(2147483649)
  Start-Sleep -Seconds 30
 }
} finally {
 [void][SrwSystemAwake]::SetThreadExecutionState(2147483648)
}
