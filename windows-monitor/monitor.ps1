<#
.SYNOPSIS
    Real-time Windows Event Monitor
.DESCRIPTION
    Continuously polls a Windows Event Log (default: Security) for specific Event IDs.
.EXAMPLE
    .\monitor.ps1
.EXAMPLE
    .\monitor.ps1 -LogName System -EventIds 7040, 7045
#>

param (
    [string]$LogName = "Security",
    [int[]]$EventIds = @(
        4624, # Successful Logon
        4625, # Failed Logon
        4648, # Logon using explicit credentials
        4720, # User Account Created
        4722, # User Account Enabled
        1102  # Audit log cleared
    )
)

Write-Host "[*] Starting Real-time Event Monitor on log: $LogName"
Write-Host "[*] Watching for Event IDs: $($EventIds -join ', ')"
Write-Host "[*] Press Ctrl+C to stop.`n"

# Verify Admin rights (Required for Security log)
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin -and $LogName -eq "Security") {
    Write-Host "[-] WARNING: You must run PowerShell as Administrator to read the Security log." -ForegroundColor Red
    exit
}

# Construct the filter hashtable
$filter = @{
    LogName = $LogName
    ID = $EventIds
}

# Keep track of the last checked time so we only get new events
$startTime = Get-Date

try {
    while ($true) {
        $filter["StartTime"] = $startTime
        
        # Suppress errors if no events are found in the short timeframe
        $events = Get-WinEvent -FilterHashtable $filter -ErrorAction SilentlyContinue | Sort-Object TimeCreated
        
        if ($null -ne $events) {
            foreach ($event in $events) {
                $time = $event.TimeCreated.ToString("yyyy-MM-dd HH:mm:ss")
                $id = $event.Id
                # Extract the first meaningful line of the message
                $msg = $event.Message.Split("`n")[0].Trim() 
                
                # Color code based on event severity/type
                if ($id -eq 4625 -or $id -eq 1102) {
                    Write-Host "[!] $time | ID: $id | $msg" -ForegroundColor Red
                } else {
                    Write-Host "[+] $time | ID: $id | $msg" -ForegroundColor Yellow
                }
                
                # Increment start time so we don't process this event again
                # Add 1 millisecond to prevent duplicate processing
                $startTime = $event.TimeCreated.AddMilliseconds(1)
            }
        }
        
        # Pause before checking again to save CPU
        Start-Sleep -Seconds 3
    }
}
catch [System.Management.Automation.PipelineStoppedException] {
    # Expected when user hits Ctrl+C
    Write-Host "`n[*] Monitor stopped gracefully."
}
catch {
    Write-Host "`n[-] An unexpected error occurred: $_" -ForegroundColor Red
}
