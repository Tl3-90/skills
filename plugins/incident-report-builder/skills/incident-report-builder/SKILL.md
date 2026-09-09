---
name: incident-report-builder
description: Convert rough IT troubleshooting notes, timelines, alerts, ticket notes, chat logs, or remediation notes into a structured incident report. Use when the user wants an evidence-based incident summary that clearly separates observations, actions, results, assumptions, and unresolved items.
---

# Incident Report Builder

Create concise, operationally useful IT incident reports from incomplete or messy source notes without inventing facts.

## Core rules

1. Treat user-provided notes as the source of truth.
2. Never convert an assumption into a fact.
3. Separate observed evidence from interpretation.
4. Preserve timestamps, hostnames, usernames, alert names, error messages, commands, and tool names exactly when provided.
5. Do not fabricate missing timestamps, root causes, remediation results, ticket IDs, severity levels, or affected systems.
6. If notes conflict, preserve the conflict and mark it unresolved instead of choosing one version without evidence.
7. Prefer concise operational language over narrative prose.

## Workflow

### 1. Parse the source notes

Extract only information explicitly present in the input:

- incident identifier, if provided
- date and time
- affected device, service, account, application, or location
- detection source
- observed symptoms or alerts
- technical evidence
- actions taken
- result of each action
- current status
- unresolved questions
- suspected cause or interpretation, when explicitly stated

### 2. Classify every material statement

Internally classify information as one of:

- **Observed** — directly seen in an alert, log, system, command output, screenshot, or user report
- **Action** — a troubleshooting or remediation step that was actually performed
- **Result** — what happened after an action
- **Reported** — information supplied by another person but not independently verified in the notes
- **Inference** — a possible explanation or suspected cause
- **Unresolved** — information that is missing, contradictory, or still requires verification

Do not present an inference as observed evidence.

### 3. Build the timeline

When timestamps are available, order events chronologically.

Use the exact timestamp precision provided. Do not invent missing minutes, seconds, dates, or time zones.

When ordering cannot be established, state that sequence is based on note order rather than confirmed timestamps.

### 4. Determine incident status

Use only the strongest status supported by the notes:

- **Resolved** — evidence shows the issue is no longer occurring and required remediation is complete
- **Contained** — immediate risk or impact was stopped, but follow-up remains
- **Monitoring** — remediation occurred and validation is still underway
- **Open** — issue or investigation remains active
- **Unknown** — the notes do not establish current status

Do not label an incident resolved merely because an action was performed.

### 5. Produce the report

Use the structure in `references/report-template.md`.

Omit empty optional sections rather than filling them with invented content. Keep unresolved items visible.

### 6. Run an evidence audit

Before finalizing, verify:

- Every factual claim is traceable to the supplied notes.
- Suspected causes are labeled as suspected or inferred.
- Actions are not confused with successful outcomes.
- Timeline ordering is supported by timestamps or explicitly marked as note-order only.
- No unsupported severity, impact, root cause, or resolution claim was added.
- Sensitive credentials, secrets, or authentication tokens are not repeated unnecessarily.

If the audit finds unsupported wording, correct it before returning the report.

## Output behavior

When the source notes are sufficient, produce the completed incident report directly.

When one missing fact prevents a materially correct report, ask only for that fact. Otherwise, preserve the gap under **Unresolved Items** and complete the report with the available evidence.

When the user asks for a shorter version, preserve the distinction between evidence, actions, results, and unresolved items even when condensing.
