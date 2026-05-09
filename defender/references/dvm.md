# DVM Reference — Defender Vulnerability Management

## Prioritization Model

DVM scores recommendations using three factors multiplied together:

| Factor | What it measures |
|---|---|
| **Threat** | Active exploitation in the wild, exploit in kit, exploit verified, linked to active alert in your org |
| **Breach likelihood** | How exposed your org is relative to others (device exposure distribution, missing patches, config gaps) |
| **Business value** | Criticality of affected assets (tagged critical assets score higher) |

The **Exposure Score** (0–100) is the org-level aggregate. Lower is better. Each recommendation shows its **delta** — how much fixing it would reduce your Exposure Score.

**Microsoft Secure Score for Devices** is the configuration hygiene counterpart (higher is better) — measures security controls applied, not patching status.

---

## CVE / EPSS Score Interpretation

| Field | Meaning |
|---|---|
| **CVSS** | Severity score (0–10). Base score from NVD. Use as secondary signal only. |
| **EPSS** | Exploit Prediction Scoring System (0–1.0). Probability of exploitation in the next 30 days. Higher = more urgent. |
| **Breach insight** | Icon shown if exploit is being used in active campaigns targeting orgs like yours |
| **Threat insight** | Icon shown if exploit is publicly available or in an exploit kit |
| **Active alerts** | Filter showing if this CVE is linked to an active alert in your environment |

**Prioritization order:** Active alert in org → Breach insight → Threat insight + high EPSS → CVSS

---

## Zero-Day Lifecycle

| Stage | What you see |
|---|---|
| **Pre-patch (zero-day active)** | "Attention required" remediation type. No patch available. Mitigation options shown instead. |
| **Vendor patch released** | Remediation type changes to software update. Zero-day tag retained until patched. |
| **Post-patch (patched in org)** | CVE moves out of zero-day view once device exposure drops to 0. |

Zero-days are tagged across: Vulnerabilities page, Security recommendations, Software page, Device page. Filter by "zero-day" in the Vulnerabilities page filter panel.

---

## Portal Navigation

### Preview UX (newer tenants)
- **Vulnerability management** left nav → Dashboard, Recommendations, Remediation, Weaknesses, Software inventory, Baselines, Event timeline
- Exposure score shown prominently on Dashboard

### Classic UX (existing customers)
- **Threat & Vulnerability Management** left nav — same content, slightly different layout
- Some filter options differ in placement

---

## Security Recommendations Workflow

1. **Find recommendation** → Vulnerability management → Security recommendations → sort by "Exposure score impact" descending
2. **Review flyout** → click recommendation → see: affected devices, CVEs linked, remediation options, exception options
3. **Request remediation** → "Request remediation" → fills Intune ticket with device list, remediation action, due date
4. **Track** → Remediation → Activities tab → shows status, assigned IT admin, due date, progress
5. **Mark exception** if patching isn't possible → Exception types:
   - **Organizational exception** — applies to all affected devices
   - **Device group exception** — applies to specific device group only
   - Duration: 30/60/90 days or indefinite
   - Justification required: Third-party mitigation / Compensating control / Accepted risk / Other

---

## Remediation Ticket via Intune

Requirements: Intune integration enabled in MDE settings + user must have Intune RBAC permissions

1. From recommendation flyout → Request remediation
2. Fill in: remediation type (software update / config change), due date, priority, notes
3. Ticket appears in Intune as a security task
4. IT admin sees in Intune → Security tasks → Accept → remediate → mark complete
5. DVM receives completion signal and closes the activity

Alternate mitigations (when patch unavailable): shown in recommendation flyout as "Configuration change" options — e.g., disable feature, enable protection setting.

---

## Vulnerabilities Page — Filters

| Filter | Values |
|---|---|
| Severity | Critical, High, Medium, Low |
| Exploit type | Exploit available, Exploit verified, Exploit in kit |
| Threat insight | Active alerts, Breach insight |
| Zero-day | Yes/No |
| EPSS score | Range slider |
| OS platform | Windows, macOS, Linux, Android, iOS |
| CVE age | Date range |

**Export limit:** 6,000 records max, 64KB max per export. For larger exports use the API.

**Known limitation:** DVM does not distinguish 32-bit vs 64-bit architecture — can cause false positives on mixed environments.

---

## API Endpoints — Bulk Export

```
GET /api/machines/SoftwareVulnerabilitiesByMachine   # CVEs per device
GET /api/machines/SoftwareInventoryByMachine          # Software per device
GET /api/vulnerabilities/machinesByVulnerability      # Devices affected by CVE
GET /api/recommendations                               # All security recommendations
GET /api/software                                      # Software inventory (global)
GET /api/vulnerabilities                               # All CVEs in your env
```

Export format: JSON. All endpoints paginated — use `$skip` and `$top`. Max page size 10,000.

---

## Software Inventory

- Default view: CPE-matched software only (software with known CVE mappings)
- Enable "Show software without CPE" to see all discovered software
- Detection source: Registry (installed programs) or Disk (file system scan)
- **Linux caveat:** Only RPM/DNF/YUM package manager installed software is detected. Manually compiled binaries are not inventoried.
- Software page per app: vendor, version distribution, vulnerability count, exploit availability, installed devices, event timeline

---

## Block Vulnerable Applications

Feature: Block specific vulnerable software **versions** by device group while patching is in progress.

Location: Security recommendations → select recommendation → "Block vulnerable application" (shown when exploit exists)

Effect: Adds an indicator blocking execution of that specific binary hash on targeted device groups. Removes automatically when recommendation is resolved.

---

## Advanced Inventory Features

| Feature | What it finds |
|---|---|
| Browser extensions | Extension name, permissions, risk level, browser type, installed devices |
| Digital certificates | Expiry date, weak algorithms (MD5/SHA1), issuer, subject, installed devices |
| Hardware & firmware | BIOS version, processor model, system model — for supply chain risk |
| Network shares | Vulnerable SMB share configurations |
| Authenticated scan | Agentless scan for unmanaged Windows devices using domain credentials |
