# XDR Reference — Defender XDR / Advanced Hunting

## Advanced Hunting — Limits

| Limit | Value |
|---|---|
| Data window | 30 days |
| Max result rows | 100,000 |
| Query timeout | 10 minutes |
| Max result size | 64 MB |
| Max queries/minute | 15 (portal), 45 (API) |
| Custom detection frequency | Every 1h, 3h, 12h, or 24h |

---

## Advanced Hunting — Table Schema Reference

### Device tables (MDE)

**DeviceProcessEvents**
`Timestamp, DeviceId, DeviceName, ActionType, FileName, FolderPath, SHA1, SHA256, MD5, FileSize, ProcessVersionInfoCompanyName, ProcessVersionInfoProductName, ProcessVersionInfoProductVersion, ProcessVersionInfoInternalFileName, ProcessVersionInfoOriginalFileName, ProcessVersionInfoFileDescription, ProcessId, ProcessCommandLine, ProcessIntegrityLevel, ProcessTokenElevation, ProcessCreationTime, AccountDomain, AccountName, AccountSid, AccountUpn, AccountObjectId, LogonId, InitiatingProcessAccountDomain, InitiatingProcessAccountName, InitiatingProcessAccountSid, InitiatingProcessAccountUpn, InitiatingProcessAccountObjectId, InitiatingProcessLogonId, InitiatingProcessIntegrityLevel, InitiatingProcessTokenElevation, InitiatingProcessSHA1, InitiatingProcessSHA256, InitiatingProcessMD5, InitiatingProcessFileName, InitiatingProcessFileSize, InitiatingProcessVersionInfoCompanyName, InitiatingProcessVersionInfoProductName, InitiatingProcessVersionInfoProductVersion, InitiatingProcessVersionInfoInternalFileName, InitiatingProcessVersionInfoOriginalFileName, InitiatingProcessVersionInfoFileDescription, InitiatingProcessId, InitiatingProcessCommandLine, InitiatingProcessCreationTime, InitiatingProcessFolderPath, InitiatingProcessParentId, InitiatingProcessParentFileName, InitiatingProcessParentCreationTime, InitiatingProcessSignerType, InitiatingProcessSignatureStatus, ReportId, AppGuardContainerId, AdditionalFields`

**DeviceNetworkEvents**
`Timestamp, DeviceId, DeviceName, ActionType, RemoteIP, RemotePort, RemoteUrl, LocalIP, LocalPort, Protocol, LocalIPType, RemoteIPType, InitiatingProcessSHA1, InitiatingProcessSHA256, InitiatingProcessMD5, InitiatingProcessFileName, InitiatingProcessFileSize, InitiatingProcessVersionInfoCompanyName, InitiatingProcessVersionInfoProductName, InitiatingProcessVersionInfoProductVersion, InitiatingProcessVersionInfoInternalFileName, InitiatingProcessVersionInfoOriginalFileName, InitiatingProcessVersionInfoFileDescription, InitiatingProcessId, InitiatingProcessCommandLine, InitiatingProcessCreationTime, InitiatingProcessFolderPath, InitiatingProcessParentFileName, InitiatingProcessParentId, InitiatingProcessParentCreationTime, InitiatingProcessAccountDomain, InitiatingProcessAccountName, InitiatingProcessAccountSid, InitiatingProcessAccountUpn, InitiatingProcessAccountObjectId, InitiatingProcessLogonId, InitiatingProcessIntegrityLevel, InitiatingProcessTokenElevation, ReportId, AppGuardContainerId, AdditionalFields`

**DeviceFileEvents**
`Timestamp, DeviceId, DeviceName, ActionType, FileName, FolderPath, SHA1, SHA256, MD5, FileOriginUrl, FileOriginReferrerUrl, FileOriginIP, PreviousFolderPath, PreviousFileName, FileSize, InitiatingProcessAccountDomain, InitiatingProcessAccountName, InitiatingProcessAccountSid, InitiatingProcessAccountUpn, InitiatingProcessAccountObjectId, InitiatingProcessMD5, InitiatingProcessSHA1, InitiatingProcessSHA256, InitiatingProcessFileName, InitiatingProcessFileSize, InitiatingProcessVersionInfoCompanyName, InitiatingProcessVersionInfoProductName, InitiatingProcessVersionInfoProductVersion, InitiatingProcessVersionInfoInternalFileName, InitiatingProcessVersionInfoOriginalFileName, InitiatingProcessVersionInfoFileDescription, InitiatingProcessId, InitiatingProcessCommandLine, InitiatingProcessCreationTime, InitiatingProcessFolderPath, InitiatingProcessParentFileName, InitiatingProcessParentId, InitiatingProcessParentCreationTime, InitiatingProcessIntegrityLevel, InitiatingProcessTokenElevation, RequestProtocol, RequestSourceIP, RequestSourcePort, RequestAccountName, RequestAccountDomain, RequestAccountSid, ShareName, InitiatingProcessLogonId, ReportId, AppGuardContainerId, SensitivityLabel, SensitivitySubLabel, IsAzureInfoProtectionApplied, AdditionalFields`

**DeviceRegistryEvents**
`Timestamp, DeviceId, DeviceName, ActionType, RegistryKey, RegistryValueType, RegistryValueName, RegistryValueData, PreviousRegistryKey, PreviousRegistryValueName, PreviousRegistryValueData, InitiatingProcessAccountDomain, InitiatingProcessAccountName, InitiatingProcessAccountSid, InitiatingProcessAccountUpn, InitiatingProcessAccountObjectId, InitiatingProcessLogonId, InitiatingProcessIntegrityLevel, InitiatingProcessTokenElevation, InitiatingProcessSHA1, InitiatingProcessSHA256, InitiatingProcessMD5, InitiatingProcessFileName, InitiatingProcessFileSize, InitiatingProcessVersionInfoCompanyName, InitiatingProcessVersionInfoProductName, InitiatingProcessVersionInfoProductVersion, InitiatingProcessVersionInfoInternalFileName, InitiatingProcessVersionInfoOriginalFileName, InitiatingProcessVersionInfoFileDescription, InitiatingProcessId, InitiatingProcessCommandLine, InitiatingProcessCreationTime, InitiatingProcessFolderPath, InitiatingProcessParentId, InitiatingProcessParentFileName, InitiatingProcessParentCreationTime, ReportId, AppGuardContainerId`

**DeviceLogonEvents**
`Timestamp, DeviceId, DeviceName, ActionType, AccountDomain, AccountName, AccountSid, AccountUpn, AccountObjectId, LogonType, LogonId, RemoteDeviceName, IsLocalAdmin, FailureReason, IsInteractive, Protocol, ReportId, AdditionalFields, InitiatingProcessAccountDomain, InitiatingProcessAccountName, InitiatingProcessAccountSid, InitiatingProcessAccountUpn, InitiatingProcessAccountObjectId, InitiatingProcessLogonId, InitiatingProcessIntegrityLevel, InitiatingProcessTokenElevation, InitiatingProcessSHA1, InitiatingProcessSHA256, InitiatingProcessMD5, InitiatingProcessFileName, InitiatingProcessFileSize, InitiatingProcessId, InitiatingProcessCommandLine, InitiatingProcessCreationTime, InitiatingProcessFolderPath, InitiatingProcessParentId, InitiatingProcessParentFileName, InitiatingProcessParentCreationTime`

**DeviceImageLoadEvents** — DLL/image load events, same column structure as DeviceProcessEvents

**DeviceEvents** — Catch-all for other device events (ASR triggers, tamper events, network protection, etc.)
`ActionType` values include: `AntivirusDetection`, `ExploitGuardNetworkProtectionBlocked`, `AttackSurfaceReductionRuleTriggered`, `TamperProtectionBlocked`, `ControlledFolderAccessViolationAudited`, etc.

**DeviceInfo**
`Timestamp, DeviceId, DeviceName, ClientVersion, PublicIP, OSArchitecture, OSPlatform, OSBuild, IsAzureADJoined, LoggedOnUsers, RegistryDeviceTag, OSVersion, MachineGroup, ReportId, OnboardingStatus, AdditionalFields, DeviceCategory, DeviceType, DeviceSubType, Model, Vendor, OSDistribution, OSVersionInfo, MergedDeviceIds, MergedToDeviceId`

**DeviceNetworkInfo**
`Timestamp, DeviceId, DeviceName, ReportId, NetworkAdapterName, MacAddress, NetworkAdapterType, NetworkAdapterStatus, TunnelType, ConnectedNetworks, DnsAddresses, IPv4Dhcp, IPv6Dhcp, DefaultGateways, IPAddresses, AdditionalFields`

---

### Identity tables (MDI)

**IdentityLogonEvents**
`Timestamp, ActionType, Application, LogonType, Protocol, FailureReason, AccountName, AccountDomain, AccountUpn, AccountSid, AccountObjectId, TargetAccountName, TargetAccountDomain, TargetAccountUpn, TargetAccountSid, TargetAccountObjectId, TargetDeviceName, DestinationDeviceName, DestinationIPAddress, DestinationPort, DestinationLocation, IPAddress, Port, Location, ISP, ReportId, AdditionalFields`

**IdentityQueryEvents** — LDAP queries, DNS lookups
**IdentityDirectoryEvents** — AD changes: password resets, group modifications, account enable/disable
**IdentityInfo** — User account attributes snapshot

---

### Email tables (MDO)

**EmailEvents**
`Timestamp, NetworkMessageId, InternetMessageId, SenderMailFromAddress, SenderFromAddress, SenderDisplayName, SenderObjectId, SenderMailFromDomain, SenderFromDomain, SenderIPv4, SenderIPv6, RecipientEmailAddress, RecipientObjectId, Subject, EmailClusterId, EmailDirection, DeliveryAction, DeliveryLocation, SpamFilteringVerdict, BulkFilteringVerdict, PhishFilteringVerdict, MalwareFilteringVerdict, UrlFilteringVerdict, AttachmentFilteringVerdict, OrgLevelPolicy, OrgLevelAction, UserLevelPolicy, UserLevelAction, Directionality, ConnectorId, AuthenticationDetails, AttachmentCount, UrlCount, EmailLanguage, ReportId, AdditionalFields`

**EmailAttachmentInfo** — `NetworkMessageId, AttachmentCount, FileName, FileType, SHA256, MalwareFamily, DetectionMethods, ThreatNames, ReportId`

**EmailUrlInfo** — `NetworkMessageId, Url, UrlDomain, UrlLocation, ReportId`

**EmailPostDeliveryEvents** — Actions taken after delivery (ZAP, manual remediation)

---

### Cloud tables (MDA)

**CloudAppEvents** — User activity in cloud apps (O365, Teams, SharePoint, etc.)
`Timestamp, ActionType, Application, ApplicationId, AccountObjectId, AccountDisplayName, AccountCountry, AccountCity, AccountType, IsAdminOperation, DeviceType, OSPlatform, IPAddress, IPTags, IPCategory, UserAgentTags, UserAgent, ActivityType, ActivityObjects, ObjectName, ObjectType, ObjectId, ReportId, AdditionalFields`

**AADSignInEventsBeta** — Azure AD sign-in logs (available in advanced hunting)

---

### Threat & Vulnerability tables

**DeviceTvmSoftwareInventory** — Software per device with CPE
**DeviceTvmSoftwareVulnerabilities** — CVEs per device
**DeviceTvmSoftwareVulnerabilitiesKB** — CVE knowledge base (CVSS, exploit availability)
**DeviceTvmSecureConfigurationAssessment** — Security baseline config checks per device
**DeviceTvmSecureConfigurationAssessmentKB** — Config check knowledge base
**DeviceTvmBrowserExtensions** — Browser extensions per device
**DeviceTvmCertificateInfo** — Certificates per device

---

### Other tables

**AlertEvidence** — All entities linked to alerts (files, processes, IPs, URLs, users, devices)
`Timestamp, AlertId, ServiceSource, EntityType, EvidenceDirection, FileName, FolderPath, SHA1, SHA256, FileSize, ThreatFamily, RemoteIP, RemoteUrl, AccountName, AccountDomain, AccountSid, AccountObjectId, AccountUpn, DeviceId, DeviceName, LocalIP, NetworkMessageId, EmailSubject, AttachmentName, AdditionalFields`

**AlertInfo** — Alert metadata
`Timestamp, AlertId, Title, Category, Severity, ServiceSource, DetectionSource, AttackTechniques, ReportId`

**ExposureGraphEdges** / **ExposureGraphNodes** — Attack path / blast radius graph (requires Exposure Management)

---

## KQL Query Patterns

### Custom detection required columns
Every custom detection query MUST return:
- `Timestamp`
- At least one entity column: `DeviceId`, `DeviceName`, `AccountObjectId`, `AccountUpn`, `AccountSid`, `SHA1`, `SHA256`, `RemoteUrl`, `RemoteIP`
- `ReportId` (for most device tables — not required for identity/email tables)

### Performance best practices
- Filter early: put `where Timestamp > ago(1d)` and `where DeviceName == "..."` before joins
- Avoid `contains` — use `has` or `startswith` instead (much faster)
- Avoid `!has` on large tables — reformulate as anti-join
- Use `summarize` before `join` to reduce rows
- `project` only columns you need before expensive operations
- For file hash lookups: always use SHA1 or SHA256, not MD5 (less unique)

---

## Ransomware Hunting Queries

### Stage 1: Initial access — RDP brute force
```kql
DeviceLogonEvents
| where Timestamp > ago(7d)
| where LogonType == "Network" and ActionType == "LogonFailed"
| summarize FailCount = count() by DeviceName, RemoteDeviceName, bin(Timestamp, 1h)
| where FailCount > 20
```

### Stage 2: Credential theft — LSASS access
```kql
DeviceEvents
| where Timestamp > ago(7d)
| where ActionType == "OpenProcessApiCall"
| where FileName =~ "lsass.exe"
| where InitiatingProcessFileName !in~ ("MsMpEng.exe", "svchost.exe", "csrss.exe")
```

### Stage 3: Lateral movement — PsExec / WMI
```kql
DeviceProcessEvents
| where Timestamp > ago(7d)
| where (FileName =~ "psexec.exe" or FileName =~ "psexesvc.exe")
    or (InitiatingProcessFileName =~ "wmiprvse.exe" and FileName !in~ ("WmiPrvSE.exe","scrcons.exe"))
```

### Stage 4: Defense evasion — shadow copy deletion
```kql
DeviceProcessEvents
| where Timestamp > ago(7d)
| where (FileName =~ "vssadmin.exe" and ProcessCommandLine has "delete")
    or (FileName =~ "wbadmin.exe" and ProcessCommandLine has "delete")
    or (ProcessCommandLine has "shadowcopy" and ProcessCommandLine has "delete")
```

### Stage 5: Ransomware file writes (high-volume rename/create)
```kql
DeviceFileEvents
| where Timestamp > ago(1d)
| where ActionType in ("FileCreated", "FileRenamed")
| summarize FileCount = count() by DeviceId, DeviceName, bin(Timestamp, 5m)
| where FileCount > 500
```

### Combined multi-indicator ransomware score
```kql
let RDPBrute = DeviceLogonEvents
    | where Timestamp > ago(1d) and LogonType == "Network" and ActionType == "LogonFailed"
    | summarize count() by DeviceId | where count_ > 50 | extend Score = 1;
let LsassAccess = DeviceEvents
    | where Timestamp > ago(1d) and ActionType == "OpenProcessApiCall" and FileName =~ "lsass.exe"
    | summarize count() by DeviceId | where count_ > 0 | extend Score = 3;
let ShadowDelete = DeviceProcessEvents
    | where Timestamp > ago(1d)
    | where FileName =~ "vssadmin.exe" and ProcessCommandLine has "delete"
    | summarize count() by DeviceId | extend Score = 5;
RDPBrute | union LsassAccess | union ShadowDelete
| summarize TotalScore = sum(Score) by DeviceId
| where TotalScore >= 5
| join kind=inner (DeviceInfo | summarize arg_max(Timestamp, DeviceName) by DeviceId) on DeviceId
```

---

## Custom Detection Rules

**Location:** Advanced Hunting → Custom detection rules → Create rule

**Required settings:**
- Query (must return required columns above)
- Alert title and severity (Informational / Low / Medium / High)
- MITRE tactic and technique
- Impacted entities (which column maps to which entity type)
- Actions (optional — run automatically when triggered):
  - Generate alert only (default)
  - Quarantine file
  - Stop and quarantine process
  - Kill process
  - Collect investigation package
  - Restrict app execution
  - Isolate device
  - Block URL
  - Block IP address

**Run frequency:** Every 1h, 3h, 12h, 24h

**Scope:** All devices, or specific device groups

---

## Automatic Attack Disruption

**How it works:** XDR correlates signals across all Defender workloads. When confidence exceeds 99% (measured by signal-to-noise ratio on production data), it automatically contains the attack.

**Action types:**
| Action | What it does |
|---|---|
| **Contain device** | Blocks all inbound/outbound traffic except Defender service endpoints. Device stays in Defender management. |
| **Contain IP** | Blocks all undiscovered (unmanaged) devices at that IP from communicating with managed devices |
| **Disable user (cloud)** | Disables Entra ID account via Microsoft-managed app `60ca1954-583c-4d1f-86de-39d835f3e452` |
| **Contain user (endpoint)** | Blocks user logon on endpoints without disabling the AD account |

**Visual indicators:** Yellow banner on incident page, "Attack Disruption" tag on incident, graph shows action status, "Policy status" column in Activities tab.

**Reversibility:** All actions fully reversible by security team from the incident page.

---

## Incident Investigation Workflow

1. **Triage** → Incidents queue → sort by severity/updated time → review attack story summary
2. **Attack story graph** → visual node graph of all correlated alerts, entities, actions → click nodes to pivot
3. **Blast Radius Analysis** → shows laterally reachable assets (requires Sentinel data lake + Exposure Management)
4. **Go Hunt** → right-click any entity in graph → opens Advanced Hunting pre-filtered to that entity
5. **Evidence tab** → all entities (files, processes, IPs, users, devices) linked to incident
6. **Timeline** → chronological event view across all workloads
7. **Respond** → Isolate device, collect package, run AV scan, restrict apps — all from incident page
8. **Close** → classify as True Positive / False Positive / Informational, set determination

---

## Alert Classification Playbooks

### Inbox forwarding rules (BEC indicator)
Hunt: `CloudAppEvents | where ActionType == "New-InboxRule" | where AdditionalFields has "ForwardTo"`

### Inbox manipulation rules (hiding breach)
Hunt: `CloudAppEvents | where ActionType == "New-InboxRule" | where AdditionalFields has_any ("MoveToFolder","Delete","MarkAsRead") and AdditionalFields has_any ("Phish","Malware","Hack")`

### Password spray
Hunt: `IdentityLogonEvents | where ActionType == "LogonFailed" | summarize count(), dcount(AccountUpn) by IPAddress, bin(Timestamp, 1h) | where count_ > 50 and dcount_AccountUpn > 10`

### Malicious exchange connectors
Hunt: `CloudAppEvents | where ActionType in ("New-SendConnector","Set-SendConnector") | where AdditionalFields has "SmartHosts"`
