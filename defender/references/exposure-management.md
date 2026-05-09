# Exposure Management Reference — Microsoft Security Exposure Management (MSEM)

## What it is

MSEM is a **proactive security posture management** tool in the Defender XDR portal (`security.microsoft.com`). It unifies endpoint, identity, cloud (Azure/AWS/GCP), and external attack surface data into a single property graph. Aligns with Gartner's CTEM (Continuous Threat Exposure Management) framework.

**Not a detection/response tool** — it surfaces attack paths, prioritizes remediation, and tracks posture over time.

**Not available in:** GCC, GCC High, DoD government clouds.

---

## Licensing

### Licenses that unlock full MSEM
- Microsoft 365 E5 or A5
- Microsoft 365 E3 + E5 Security add-on
- Microsoft 365 E3 + EMS E5 add-on
- Windows 10/11 Enterprise E5 or A5
- EMS E5 or A5
- Office 365 E5 or A5
- Defender for Endpoint (standalone)
- Defender for Identity (standalone)
- Defender for Cloud Apps / Cloud App Discovery
- Defender for Office 365 Plan 2
- Microsoft 365 Business Premium
- Defender for Business
- Defender for Cloud

### Licenses that unlock Secure Score only (NOT full MSEM)
- Microsoft 365 E3, A3
- Defender for Office 365 Plan 1

### Data connector pricing
Currently **free (public preview)**. At GA: consumption-based per third-party asset ingested.

### Data freshness
- Graph updates within **72 hours** of changes at source products
- **14-day retention** in exposure graph (only latest snapshot, no historical graph)
- MDE sensor **≥ 10.3740.XXXX** required for critical asset classification

---

## RBAC Permissions

### Defender Unified RBAC (preferred)
Under **Security posture** category:

| Permission | Access |
|---|---|
| `Exposure Management (read)` | Read all MSEM |
| `Exposure Management (manage)` | Read + set initiative targets, edit metric weights (requires ALL device groups) |
| `Core security settings (manage)` | Configure EASM vendor connection |

Role must be assigned to **Microsoft Security Exposure Management** data source.

### Entra ID role equivalents
- **Full read + write:** Global Admin, Security Admin
- **Read + limited write:** Security Operator (can change criticality, toggle rules)
- **Read only:** Global Reader, Security Reader, Helpdesk Admin, User Admin, Exchange Admin, SharePoint Admin

---

## Portal Navigation

All under `Exposure Management` in `security.microsoft.com`:

```
Exposure Management
├── Overview (dashboard)
├── Attack surface
│   ├── Attack paths
│   └── Map (attack surface map)
├── Vulnerability management
│   ├── Overview
│   ├── Vulnerabilities (Devices tab + Cloud tab)
│   └── Remediation
├── Exposure insights
│   ├── Initiatives
│   ├── Metrics
│   ├── Recommendations
│   └── Events
└── Data Connectors
Settings > Microsoft XDR > Rules > Critical asset management
```

---

## Enterprise Exposure Graph

Property graph ingesting assets and relationships from:
- Defender for Endpoint (devices)
- Defender for Identity (users, groups, AD roles)
- Defender Vulnerability Management (CVEs, software)
- Defender for Cloud (Azure/AWS/GCP resources)
- Defender for Cloud Apps (SaaS apps)
- Defender for Office (email/collaboration)
- Defender for IoT / OT
- Microsoft Entra ID
- Defender EASM (external attack surface)
- External connectors: ServiceNow CMDB, Qualys, Rapid7, Tenable, Wiz, Palo Alto Prisma

### Advanced Hunting Tables

#### ExposureGraphNodes — entities and their properties

| Column | Type | Notes |
|---|---|---|
| `NodeId` | string | Unique GUID-format ID |
| `NodeLabel` | string | Entity type. e.g. `"microsoft.compute/virtualmachines"`, `"elasticloadbalancing.loadbalancer"` |
| `NodeName` | string | Display name |
| `Categories` | dynamic (array) | e.g. `["compute","virtual_machine"]` |
| `NodeProperties` | dynamic (json) | Contains `rawData` with: `osType`, `exposedToInternet`, `vulnerableToRCE`, `criticalityLevel`, `IsInternetFacing`, `VulnerableToPrivilegeEscalation`, `containsSensitiveData`, etc. |
| `EntityIds` | dynamic | All known IDs. e.g. `{"AzureResourceId":"...","MdeMachineId":"..."}` |

#### ExposureGraphEdges — relationships between entities

| Column | Type | Notes |
|---|---|---|
| `EdgeId` | string | Unique edge ID |
| `EdgeLabel` | string | Relationship type. e.g. `"affecting"`, `"routes traffic to"`, `"is running"`, `"contains"`, `"Can Authenticate As"`, `"CanRemoteInteractiveLogonTo"` |
| `SourceNodeId` | string | |
| `SourceNodeName` | string | |
| `SourceNodeLabel` | string | |
| `SourceNodeCategories` | dynamic | |
| `TargetNodeId` | string | |
| `TargetNodeName` | string | |
| `TargetNodeLabel` | string | |
| `TargetNodeCategories` | dynamic | |
| `EdgeProperties` | dynamic | Optional data per edge type. For `"routes traffic to"`: contains `networkReachability` with port/protocol ranges |

### Graph KQL Operators
- `make-graph` — builds graph from tabular edge + node data
- `graph-match` — pattern search across graph
- Path length: `[edge*1..3]` = 1 to 3 hops

### Performance tips
- Extract needed columns from `NodeProperties` BEFORE `make-graph` (NodeProperties is large)
- Use `has()` for dynamic columns (uses smart index)
- Pattern: `Categories has 'virtual_machine' and set_has_element(Categories, 'virtual_machine')` — `has` for performance, `set_has_element` for precision

---

## KQL Query Examples

```kusto
// VMs exposed to internet with RCE vulnerability
ExposureGraphNodes
| where isnotnull(NodeProperties.rawData.exposedToInternet)
| where isnotnull(NodeProperties.rawData.vulnerableToRCE)
| where Categories has "virtual_machine" and set_has_element(Categories, "virtual_machine")

// Internet-facing devices with privilege escalation vuln
ExposureGraphNodes
| where isnotnull(NodeProperties.rawData.IsInternetFacing)
| where isnotnull(NodeProperties.rawData.VulnerableToPrivilegeEscalation)
| where set_has_element(Categories, "device")

// Users logged into more than one critical device
let IdentitiesAndCriticalDevices = ExposureGraphNodes
| where (set_has_element(Categories, "device") and isnotnull(NodeProperties.rawData.criticalityLevel) and NodeProperties.rawData.criticalityLevel.criticalityLevel < 4)
  or set_has_element(Categories, "identity");
ExposureGraphEdges
| where EdgeLabel == "Can Authenticate As"
| make-graph SourceNodeId --> TargetNodeId with IdentitiesAndCriticalDevices on NodeId
| graph-match (Device)-[canConnectAs]->(Identity)
  where set_has_element(Identity.Categories, "identity") and set_has_element(Device.Categories, "device")
  project IdentityIds=Identity.EntityIds, DeviceIds=Device.EntityIds
| mv-apply DeviceIds on (where DeviceIds.type == "DeviceInventoryId")
| mv-apply IdentityIds on (where IdentityIds.type == "SecurityIdentifier")
| summarize NumberOfDevicesUserLoggedinTo=count() by tostring(IdentityIds.id)
| where NumberOfDevicesUserLoggedinTo > 1

// Multi-hop path from IP to VM (up to 3 hops)
let IPsAndVMs = ExposureGraphNodes
| where (set_has_element(Categories, "ip_address") or set_has_element(Categories, "virtual_machine"));
ExposureGraphEdges
| make-graph SourceNodeId --> TargetNodeId with IPsAndVMs on NodeId
| graph-match (IP)-[anyEdge*1..3]->(VM)
  where set_has_element(IP.Categories, "ip_address") and set_has_element(VM.Categories, "virtual_machine")
  project IpIds=IP.EntityIds, VmIds=VM.EntityIds, VmProperties=VM.NodeProperties.rawData

// CVEs from Rapid7 connector
ExposureGraphEdges
| where EdgeLabel == "affecting" and SourceNodeLabel == "Cve"
| where isnotempty(EdgeProperties.rawData.rapid7ReportInfo)
| project AssetName = TargetNodeName, CVE = SourceNodeName

// CVEs from Tenable connector
ExposureGraphEdges
| where EdgeLabel == "affecting" and SourceNodeLabel == "Cve"
| where isnotempty(EdgeProperties.rawData.tenableReportInfo)
| project AssetName = TargetNodeName, CVE = SourceNodeName
```

---

## Critical Asset Management

### Four criticality levels (highest takes precedence when multiple rules match)
| Level | Impact |
|---|---|
| Very High | Catastrophic if compromised — business survival at risk |
| High | Significant disruption to core operations |
| Medium | Moderate impact on some functions |
| Low | Minimal impact |

### Key predefined classifiers

**Devices — Very High / High:**
Domain Controller (VH), Entra ID Connect (H), ADFS (H), ADCS (H), VMware ESXi (H), VMware vCenter (H), Hyper-V Server (H), Domain Admin Device (H), Global Admin Workstation (H), Devices with Sensitive Information/Keys (H)

**Devices — Medium:**
Exchange Server, SharePoint Server, Database Server, IT Admin Device, Security Ops Admin Device, Network Admin Device, WSUS Server, Backup Server

**Identities — Very High:**
Global Admin, Domain Administrator, Enterprise Administrator, Privileged Role Administrator, Privileged Authentication Administrator, Authentication Administrator, Hybrid Identity Administrator, Directory Sync Accounts, Senior Executives (all)

**Identities — High:**
Security Admin, Security Operator, Security Reader, Global Reader, Application Developer, Cloud Device Administrator, Conditional Access Administrator, Exchange Admin, SharePoint Admin, Teams Admin, Billing Admin, Identity Governance Admin

**Cloud — High:**
Databases with Sensitive Data, Confidential Azure VM, Azure VM with Critical User, Azure Key Vault (many identities or high ops volume), Premium/multi-node AKS cluster, Immutable+Locked Azure Storage

### Custom classification
Path: **Settings > Microsoft XDR > Rules > Critical asset management**
- Query builder with Boolean filters per asset type
- AD groups supported for identity rules (Entra ID groups not yet supported)
- Preview affected assets before saving

---

## Attack Paths

**How generated:** MSEM simulates adversary routes using graph data. Paths update dynamically as environment changes (new devices, user logons, group membership, config changes).

**Key concepts:**
- **Attack path**: End-to-end route from entry point → critical asset
- **Choke point**: Node where multiple paths converge — highest-leverage hardening target
- **Blast radius**: Visual of downstream assets reachable if choke point is compromised
- **Entry point**: Internet-facing or externally reachable asset where attack begins
- **End Game assets (on-prem)**: Domain Admins, Enterprise Admins, Domain Controllers — paths auto-terminate here

**Cloud attack paths** (requires Defender for Cloud):
- Cover Azure, AWS, GCP: VMs, storage, containers, serverless, APIs, AI agents
- Validated via active reachability scans (not just theoretical config review)
- Support hybrid paths spanning on-prem + cloud

### Portal workflow
1. Attack surface > Attack paths — list view (sort by risk level, target criticality)
2. Select path → graph visualization
3. Recommendations tab → per-path mitigations
4. Choke points tab → select node → **View blast radius**
5. **View in map** → open in attack surface map

---

## Exposure Insights

### Initiatives (built-in catalog)
| Initiative | Focus |
|---|---|
| Ransomware Protection | Controls reducing ransomware success |
| Critical Asset Protection | Resilience of critical assets |
| Endpoint Security | Endpoint coverage and configuration |
| Identity Security | Credential, auth, password protection |
| Cloud Security [Preview] | Cloud coverage, config, performance |
| SaaS Security | SaaS app connectors and config |
| Zero Trust (Foundational) | Zero Trust adoption alignment |
| External Attack Surface Protection | EASM-integrated external footprint |
| Business Email Compromise | BEC financial fraud posture |
| Vulnerability Assessment | Cross-infrastructure vulnerability tracking |
| CIS M365 Foundations Benchmark | CIS M365 v3.0.0 compliance |
| Enterprise IoT Security | IoT device risk visibility |
| OT Security [Preview] | OT network monitoring |

**Scoring:** 0 (worst) to 100 (best). Weighted average of metric values. History tracked for changes >2.5%.

### Metrics
- Group recommendations by asset scope within an initiative
- Progress: 0 (high exposure) → 100 (no exposure)
- Weight: High/Medium/Low (or Risk Accepted)
- Editing weight affects ALL initiatives that metric belongs to; propagates in ~2 hours

### Recommendations (unified catalog)
Sources: Microsoft Secure Score + MSEM + Defender for Cloud + MDVM
Tabs: Devices (Misconfigs / Vulns) | Cloud (Misconfigs / Vulns / Exposed Secrets) | SaaS | Identities | Data
Remediate: Manage button → links to source workload

### Events
- Trigger on: metric score drop ≥2%, initiative score drop ≥2%, new initiative available
- Past 7 days shown on Overview dashboard

---

## Data Connectors

| Connector | Type | What it adds to graph |
|---|---|---|
| ServiceNow CMDB | CMDB | Assets, criticality, business context |
| Qualys | VM scanner | Devices + CVE findings |
| Rapid7 InsightVM | VM scanner | Devices + CVE findings |
| Tenable | VM scanner | Devices + CVE findings |
| Wiz | Cloud security | Cloud resources, CVEs, network config, exposure |
| Palo Alto Prisma | Cloud security | Cloud resources |

**What connector data enables:** Assets in Device Inventory, in Exposure Graph (AH queryable), in Attack Surface Map, new attack path discovery, criticality auto-mapped to MSEM levels.

**Limitation:** Third-party vuln data appears in Exposure Graph only — not yet in MDVM vulnerability table directly.

**IP allowlist:** Microsoft "Scuba" IP ranges — see `https://www.microsoft.com/download/details.aspx?id=56519`

---

## EASM Initiative (External Attack Surface)

Two modes:
| Mode | Requirements | Detail level | Availability |
|---|---|---|---|
| Pre-built footprint | No MDEASM subscription | High-level metrics only | ~1 hour |
| Full MDEASM | Active Azure MDEASM subscription (30-day free trial) | Asset-level detail, full exposure | ~32 hours |

Full mode requires: Resource Name, Subscription ID, Resource Group Name, Region from Azure MDEASM resource.
Permission required: Global Admin or `Core security settings (manage)`.

---

## Integration Summary

| Product | What it contributes to MSEM |
|---|---|
| MDE | Endpoint/device data, device groups scope MSEM, sensor ≥10.3740 for criticality |
| DVM | Vulnerability/CVE data; MDVM now lives inside MSEM portal |
| Defender XDR | AH tables ExposureGraphNodes/Edges; critical asset info in XDR device inventory |
| Defender for Cloud | Azure/AWS/GCP cloud assets, cloud attack paths, cloud recommendations |
| Defender for Identity | User/group/AD role data, identity attack path edges, End Game asset detection |
| Secure Score | Ingested as recommendation source; both Secure Score + Cloud Secure Score visible |

---

## Practical Workflows

### Find and fix highest-risk attack paths
1. Exposure Management > Attack surface > Attack paths
2. Sort by risk level or target criticality
3. Select path → Recommendations tab → Manage
4. Choke points tab → View blast radius → prioritize that node

### Prioritize via initiatives
1. Exposure insights > Initiatives → star key initiatives
2. Open initiative → Set target score
3. Metrics tab → worst metrics → drill to recommendations → Manage

### Hunt risky assets in Advanced Hunting
```kusto
// Quick start — see what's in your graph
ExposureGraphNodes | summarize count() by NodeLabel | order by count_ desc
ExposureGraphEdges | summarize count() by EdgeLabel | order by count_ desc
```

### Connect third-party scanner
1. Exposure Management > Data Connectors → select vendor
2. Authenticate (API key/service account) → allowlist Scuba IPs
3. Wait several hours → query in AH or explore in Map

### Classify custom critical assets
1. Settings > Microsoft XDR > Rules > Critical asset management
2. New rule → query builder → preview affected assets → assign criticality level
