param (
        [string[]] $Servers = "localhost"
      , [string] $Env = "dev"
      , [bool] $Debug = $False
      , [scriptblock] $Cmd = {gci env: | sort name}
)

$Global:Debug=$Debug

$Scriptpath =(Split-Path -parent -Path $MyInvocation.MyCommand.path)

Write-Host "Base Directory: $scriptpath"

Write-Host "Server(s): $Servers"

Write-Host "Environment(s): $Env"

Write-Host "Debug: $Global:Debug"
 
Import-Module $scriptpath\function -force

Get-SystemStatus -Servers $Servers

ExecRemoteCommand -Servers $Servers -Cmd $Cmd
