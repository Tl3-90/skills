# MDE Reference — Defender for Endpoint

## ASR Rules — Full Reference

All rules support modes: **Block**, **Audit**, **Warn**, **Disabled**. Configure via Intune, GPO, PowerShell, or ConfigMgr.

| Rule Name | GUID | Min OS | Notes |
|---|---|---|---|
| Block abuse of exploited vulnerable signed drivers | 56a863a9-875e-4185-98a7-b882c64b5ce5 | Win10 1709 | |
| Block Adobe Reader from creating child processes | 7674ba52-37eb-4a4f-a9a1-f0f9a1619a2c | Win10 1709 | |
| Block all Office applications from creating child processes | d4f940ab-401b-4efc-aadc-ad5f3c50688a | Win10 1709 | |
| Block credential stealing from LSASS | 9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2 | Win10 1709 | Requires LSASS protection; may conflict with some AV products |
| Block executable content from email client and webmail | be9ba2d9-53ea-4cdc-84e5-9b1eeee46550 | Win10 1709 | |
| Block executable files from running unless they meet prevalence, age, or trusted list criteria | 01443614-cd74-433a-b99e-2ecdc07bfc25 | Win10 1709 | Cloud protection required |
| Block execution of potentially obfuscated scripts | 5beb7efe-fd9a-4556-801d-275e5ffc04cc | Win10 1709 | PowerShell/JS/VBS |
| Block JavaScript or VBScript from launching downloaded executable content | d3e037e1-3eb8-44c8-a917-57927947596d | Win10 1709 | |
| Block Office applications from creating executable content | 3b576869-a4ec-4529-8536-b80a7769e899 | Win10 1709 | |
| Block Office applications from injecting code into other processes | 75668c1f-73b5-4cf0-bb93-3ecf5cb7cc84 | Win10 1709 | |
| Block Office communication application from creating child processes | 26190899-1602-49e8-8b27-eb1d0a1ce869 | Win10 1709 | Outlook child processes |
| Block persistence through WMI event subscription | e6db77e5-3df2-4cf1-b95a-636979351e5b | Win10 1709 | File/folder exclusions not supported |
| Block process creations from PSExec and WMI commands | d1e49aac-8f56-4280-b9ba-993a6d77406c | Win10 1709 | May conflict with SCCM |
| Block rebooting machine in safe mode | 33ddedf1-c6e0-47cb-833e-de6133960387 | Win10 1709+ | |
| Block untrusted and unsigned processes from USB | b2b3f03d-6a65-4f7b-a9c7-1c7ef74a9ba4 | Win10 1709 | |
| Block use of copied or impersonated system tools | c0033c00-d16d-4114-a5a0-dc9b3a7d2ceb | Win10 1709 | |
| Block Webshell creation for Servers | a8f5898e-1dc8-49a9-9878-85004b8a61e6 | Server only | |
| Block Win32 API calls from Office macros | 92e97fa1-2edf-4476-bdd6-9dd0b4dddc7b | Win10 1709 | |
| Use advanced protection against ransomware | c1db55ab-c21a-4637-bb3f-a12568109d35 | Win10 1709 | Cloud protection required |

**PowerShell — set ASR rule:**
```powershell
Set-MpPreference -AttackSurfaceReductionRules_Ids <GUID> -AttackSurfaceReductionRules_Actions Enabled
# Actions: Enabled (Block), AuditMode, Warn, Disabled
# Multiple rules: comma-separate GUIDs and actions
```

**Event IDs for ASR:** 1121 (rule triggered/blocked), 1122 (rule in audit mode), 5007 (settings changed)

---

## Live Response

**Limits:** 50 concurrent sessions max | 30-minute session timeout | 10-minute per-command timeout

### Basic commands (all platforms)
| Command | Description |
|---|---|
| `cd` | Change directory |
| `cls` | Clear console |
| `connect` | Initiate session |
| `connections` | Show active connections |
| `dir` | List directory contents |
| `drivers` | List installed drivers |
| `fg <job_id>` | Bring background job to foreground |
| `fileinfo` | Get file metadata |
| `findfile <name>` | Search by filename |
| `getfile <path>` | Download file from device |
| `help` | Show available commands |
| `jobs` | List running background jobs |
| `persistence` | Show persistence mechanisms |
| `processes` | List running processes |
| `registry` | Registry operations |
| `scheduledtasks` | List scheduled tasks |
| `services` | List services |
| `trace` | Enable session logging |

### Advanced commands (Windows only — requires EnableLiveResponseUnsafeCommands)
| Command | Description |
|---|---|
| `analyze` | Analyze entity, return verdict |
| `cancel <job_id>` | Cancel background job |
| `isolate <device>` | Isolate device from network |
| `putfile <path>` | Upload file to device (from library) |
| `remediate` | Remediate entity on device |
| `run <script>` | Execute PowerShell script from library |
| `undo` | Reverse remediation action |

**Script library:** Upload scripts via portal → Endpoints → Response → Live Response Library. Scripts run via `run script.ps1 -parameters`.

---

## Investigation Package Contents (Windows)

When you collect an investigation package, the zip contains:

| File | Contents |
|---|---|
| `autoruns.txt` | Autorun entries (registry, startup, scheduled tasks) |
| `installed_programs.txt` | All installed applications |
| `network_connections.txt` | Active TCP/UDP connections |
| `processes_and_services.txt` | Running processes and services |
| `prefetch/` | Windows prefetch files (execution evidence) |
| `temp_directories/` | Contents of user and system temp folders |
| `user_account_control.txt` | UAC settings |
| `windows_event_logs/` | Security, System, Application event logs |
| `MpCmdRun.log` | Defender AV log |
| `MpCmdRunSigUpdateLog.log` | Signature update log |
| `registry_hives/` | SYSTEM, SOFTWARE, SAM, NTUSER.dat |

---

## Onboarding Methods by OS

| OS | Recommended Method | Alternatives |
|---|---|---|
| Windows 10/11 (Intune-managed) | Microsoft Intune | GPO, local script |
| Windows 10/11 (domain-joined) | Group Policy | SCCM, local script |
| Windows Server 2019/2022 | Unified MDE agent via Intune/SCCM | Local script |
| Windows Server 2012 R2 / 2016 | Unified MDE downlevel agent | MMA agent (legacy) |
| macOS (Intune) | Intune MDM profile | JAMF, other MDM, manual |
| macOS (JAMF) | JAMF Pro profile + policy | Intune, manual |
| Linux | Ansible/Puppet/Chef/SaltStack | Manual + bash script, installer |
| Android | Intune MAM or MDM | |
| iOS | Intune supervised/unsupervised | |
| VDI (non-persistent) | Golden image onboarding script | |
| Azure VMs | Azure Security Center integration | |

---

## Exclusions — Types and Common Mistakes

### Exclusion types
- **Extension exclusions** — exclude by file extension (e.g., `.log`) — applies to all locations
- **Path exclusions** — exclude specific folders/files — use full absolute path
- **Process exclusions** — exclude files opened by specific process — use full executable path
- **Contextual exclusions** — exclude based on path + process combination (most precise)

### Common mistakes
- Using folder exclusions that are too broad (e.g., `C:\Windows\`) — creates massive blind spots
- Excluding by extension system-wide when process-specific exclusion would suffice
- Not using contextual exclusions when both path and process are known
- Excluding temp directories entirely instead of specific app temp paths
- Forgetting to add exclusions on both the AV and EDR side when applicable
- Using relative paths instead of absolute paths

### Server-specific
- Don't exclude `%windir%\SysWow64\` — use specific subpaths
- SQL Server: exclude `.mdf`, `.ldf`, `.ndf` files and SQL binaries directory, not the entire data directory

---

## False Positive / Negative Handling

### False Positive (legitimate file/process flagged)
1. Check alert details → determine if detection is from cloud, signature, or behavioral
2. Review the file/process context in the device timeline
3. If legitimate: Submit as FP via portal alert → "Submit feedback" → False positive
4. Add indicator: Security → Indicators → Add indicator (file hash, domain, IP, cert)
5. Add exclusion if needed (after confirming it's safe — use most specific exclusion type)
6. For AV detections: MpCmdRun.exe -RestoreQuarantinedItems or portal restore

### False Negative (missed detection)
1. Collect investigation package from device
2. Submit file for deep analysis: Alert/file page → Submit for deep analysis
3. Submit to Microsoft: Security portal → Threat Intelligence → Submit
4. Check if exclusion is too broad (covering the malicious path)
5. Verify cloud protection is enabled and device can reach cloud endpoints

---

## Platform Configuration Keys

### Linux — key JSON preference fields (`/etc/opt/microsoft/mdatp/mdatp_managed.json`)
```json
{
  "antivirusEngine": {
    "enableRealTimeProtection": true,
    "enablePassiveMode": false,
    "exclusionsMergePolicy": "merge",
    "exclusions": [{"$type": "excludedPath", "isDirectory": true, "path": "/path"}],
    "threatTypeSettings": [{"key": "potentially_unwanted_application", "value": "block"}],
    "scanAfterDefinitionUpdate": true,
    "scanArchives": true,
    "maximumOnDemandScanThreads": 2,
    "cloudService": {"enabled": true, "diagnosticLevel": "optional", "automaticSampleSubmissionConsent": "safe"}
  },
  "edr": {
    "tags": [{"key": "GROUP", "value": "my-group"}]
  },
  "userInterface": {
    "hideStatusMenuIcon": false
  }
}
```

### macOS — key plist preference keys (`/Library/Managed Preferences/com.microsoft.wdav.plist`)
Key paths follow the same structure as Linux JSON but in plist format. Key fields:
- `antivirusEngine > enableRealTimeProtection` (bool)
- `antivirusEngine > passiveMode` (bool)
- `antivirusEngine > exclusions` (array of dicts with `$type`, `path`, `isDirectory`)
- `cloudService > enabled` (bool)
- `cloudService > automaticSampleSubmission` (bool)
- `edr > tags` (array)
- `userInterface > hideStatusMenuIcon` (bool)
- `tamperProtection > enforcementLevel` (string: `audit`/`block`)
- `networkProtection > enforcementLevel` (string: `disabled`/`audit`/`block`)
