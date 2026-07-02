# Windows Event Monitor

This project is a lightweight real-time Windows Event ID monitoring tool written in **PowerShell**. While Python was used for earlier projects, PowerShell is often the native and preferred language for interacting deeply with the Windows OS, especially when querying Event Logs.

## Features

- **Real-Time Polling:** Continuously monitors a specified event log (like `Security` or `System`) for new events.
- **Filtering by ID:** Only triggers on specific Event IDs of interest, filtering out the noise.
- **Color-Coded Output:** Highlights critical events (like Failed Logons or Log Clearings) in red.

## Watched Event IDs (Default)

If you run the script without arguments, it monitors the **Security** log for the following IDs:
- `4624`: Successful Logon
- `4625`: Failed Logon
- `4648`: Logon using explicit credentials
- `4720`: User Account Created
- `4722`: User Account Enabled
- `1102`: Audit log cleared

## Usage

**Important:** To read the `Security` log, you must run your PowerShell terminal as an **Administrator**.

### 1. Basic Execution (Default)

Open an Administrator PowerShell prompt and run:

```powershell
.\monitor.ps1
```

*(Note: If you get an Execution Policy error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### 2. Customizing the Monitor

Monitor the **System** log for service installations (`7045`) and state changes (`7040`):

```powershell
.\monitor.ps1 -LogName System -EventIds 7040, 7045
```

### 3. Testing It Out

To see the tool in action:
1. Start the script in an Admin PowerShell window (`.\monitor.ps1`).
2. Lock your computer (Windows Key + L).
3. Type an incorrect password and hit enter (triggering event `4625`).
4. Type your correct password to log back in (triggering event `4624`).
5. Check your terminal to see the events captured in real-time!
