#
function Get-SystemStatus
{
param (
        [string[]] $Servers = "localhost"
      , [string] $Env
)

Write-Output "Server(s): $Servers"
Write-Host "Debug: $Debug"

foreach ($Server in $Servers)
{ 
   $Command = "Test-Connection -ComputerName $Server -Count 2 -Quiet"
   if ($Debug -eq $True)
   {
      Write-Output "CMD=$Command"
   }
   else
   {
      Write-Output "CMD=$Command"
      Write-Output "Checking...$Server"
      $Result = Invoke-Expression $Command
      Write-Output "Result = $Result"
   }
   If ($Result -eq $True) 
   {
      Write-Output "Server: $Server is up."
   }
   ElseIf ($Result -eq $False) 
   {
      Write-Output "Server: $Server is down."
   }
   Else
   {
      if ($Debug -eq $True)
      {
         Write-Output "Running in Debug mode"
      }
      Else
      {
         Write-Output "Unexpected result from: $Command"
      }
   }
}

}
#
function ExecRemoteCommand
{
param (
        [string[]] $Servers = "localhost"
      , [string] $Env
      , [scriptblock] $Cmd = {gci env: | sort name}
)

Write-Output "Server(s): $Servers"
Write-Host "Debug: $Debug"

foreach ($Server in $Servers)
{
   $s = New-PSSession -computername $Server -credential LOGIN
   Invoke-Command -session $s -scriptblock $Cmd -verbose
   Remove-PSSession $s
}
}
