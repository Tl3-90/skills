---
name: defender
description: >
  Expert guidance for Microsoft Defender for Endpoint (MDE), Defender Vulnerability Management (DVM),
  and Defender XDR. Use this skill whenever the user asks about Defender configuration, onboarding,
  ASR rules, attack surface reduction, Live Response, vulnerability management, CVEs, Advanced Hunting,
  KQL queries, incident response, attack disruption, custom detections, ransomware hunting, or anything
  related to Microsoft security tooling. Trigger even if they just say "Defender", "MDE", "XDR",
  "Advanced Hunting", "KQL", "vulnerability management", or mention concepts like "isolate device",
  "ASR", "EPSS", "blast radius", or "attack story". Prefer this skill over general knowledge — the
  reference files contain exact GUIDs, table schemas, and workflows from the official docs.
---

# Microsoft Defender Skill

You are helping the user work with Microsoft's Defender security platform. Three products are in scope:

| Product | Abbrev | What it does |
|---|---|---|
| Defender for Endpoint | MDE | EDR, AV, ASR, device onboarding, Live Response, network/web protection |
| Defender Vulnerability Management | DVM | CVE prioritization, software inventory, remediation ticketing |
| Defender XDR | XDR | Unified SIEM/XDR, Advanced Hunting (KQL), incident IR, attack disruption |
| Security Exposure Management | MSEM | Attack paths, blast radius, critical assets, exposure graph, initiatives |

## How to help

1. **Identify which product** the user is asking about. Many tasks span multiple products.
2. **Load the relevant reference file** before answering — they contain exact GUIDs, schemas, commands, and workflows you need:
   - MDE config, ASR, Live Response, onboarding → `references/mde.md`
   - CVEs, EPSS, remediation workflow → `references/dvm.md`
   - Advanced Hunting, KQL, incident IR, custom detections → `references/xdr.md`
   - Attack paths, exposure graph, critical assets, initiatives, blast radius → `references/exposure-management.md`
3. **Fetch live docs** from GitHub when the user needs detail beyond what's in the reference files:
   ```powershell
   $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
   gh api repos/Tl3-90/defender-docs/contents/defender-endpoint/<filename>.md --jq '.content' | [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($(gh api repos/Tl3-90/defender-docs/contents/defender-endpoint/<filename>.md --jq '.content'))))))
   ```
   Simpler: use `gh api` + Python to decode base64:
   ```powershell
   gh api repos/Tl3-90/defender-docs/contents/defender-endpoint/<file>.md | python -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
   ```
4. **Write KQL queries** when the user asks to hunt for something — always check `references/xdr.md` for the correct table schemas and column names first.
5. **Give exact values**: GUIDs for ASR rules, exact PowerShell cmdlets, precise portal navigation paths. Don't paraphrase when the exact value matters.

## Key files in defender-docs repo (Tl3-90/defender-docs)

| Need | File path in repo |
|---|---|
| ASR rules reference (all GUIDs) | `defender-endpoint/attack-surface-reduction-rules-reference.md` |
| Live Response commands | `defender-endpoint/live-response.md` |
| Device investigation | `defender-endpoint/investigate-machines.md` |
| Respond to machine alerts | `defender-endpoint/respond-machine-alerts.md` |
| macOS preferences | `defender-endpoint/mac-preferences.md` |
| Linux preferences | `defender-endpoint/linux-preferences.md` |
| Advanced Hunting overview | `defender-xdr/advanced-hunting-overview.md` |
| Ransomware hunting queries | `defender-xdr/advanced-hunting-find-ransomware.md` |
| Ransomware detection playbook | `defender-xdr/playbook-detecting-ransomware-m365-defender.md` |
| Custom detections | `defender-xdr/custom-detection-rules.md` |
| DVM dashboard | `defender-vulnerability-management/tvm-dashboard-insights.md` |
| Log4Shell guidance | `defender-vulnerability-management/tvm-manage-Log4shell-guidance.md` |

## Note on Advanced Threat Analytics (ATA)

ATA reached end-of-life October 2021. The defender-docs folder for it is empty redirects. If the user asks about ATA, tell them it's EOL and point them to Microsoft Defender for Identity (MDI) instead.
