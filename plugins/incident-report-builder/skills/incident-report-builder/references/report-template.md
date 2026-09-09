# Incident report template

Use this structure unless the user specifies another format.

## Incident Summary

**Incident:** <identifier or concise title>
**Status:** <Resolved | Contained | Monitoring | Open | Unknown>
**Affected system:** <system/device/service/account if known>
**Detection source:** <tool, alert, user report, or other source if known>

### Summary
<2–4 sentences describing what was observed, the operational impact if explicitly known, what was done, and the current supported status.>

### Evidence
- <directly observed evidence>
- <logs, alerts, error messages, command output, user reports, or system state>

### Timeline
- **<timestamp>** — <event, observation, action, or result>

If exact timestamps are unavailable, use ordered bullets without invented times and state that the sequence follows the source-note order.

### Actions and Results
| Action | Result |
| --- | --- |
| <action actually performed> | <observed result, or "Result not documented"> |

### Assessment
Include only when the notes contain a supported interpretation or suspected cause. Clearly label uncertainty, for example: **Suspected cause:** or **Assessment:**.

### Unresolved Items
- <missing validation, conflicting evidence, open question, required follow-up>

Omit this section only when the notes establish that no unresolved items remain.
