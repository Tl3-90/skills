---
name: datacamp-learning-builder
description: Use the connected DataCamp app as the primary learning-content source for researching a topic and turning the retrieved material into structured, reusable learning workflows, course plans, or skill specifications. Use when the user asks to learn a technical topic through DataCamp, extract a curriculum from DataCamp, compare DataCamp learning resources, or build a reusable skill/course structure from DataCamp content.
---

# DataCamp Learning Builder

## Source rule

Use the connected DataCamp app as the primary source whenever the task depends on DataCamp content. Do not invent course names, chapter names, exercise details, or DataCamp coverage from memory.

Available DataCamp operations may include catalog search plus retrieval of courses, exercises, tutorials, webinars, and code-alongs. Use only operations actually exposed in the current runtime.

## Workflow

1. Convert the user's request into a precise DataCamp catalog query.
2. Search DataCamp at the appropriate level and technology.
3. Retrieve the strongest matching course or content details when needed.
4. Retrieve representative exercises when they materially improve understanding of what is actually taught.
5. Separate source facts from your own instructional organization.
6. Build the requested output from the retrieved material.
7. Preserve progression: fundamentals before dependent concepts, then applied practice, then integration.
8. Avoid padding the result with unrelated topics merely because they are available in the catalog.

## Reusable learning output

When the user asks for a reusable learning skill, course, or curriculum, structure the result around:

- Purpose
- Prerequisites
- Learning outcomes
- Ordered modules or sections
- DataCamp source mapping for each module
- Guided practice
- Independent practice
- Validation or pass criteria
- Troubleshooting or misconception checks where useful
- Cumulative project or capstone when the requested scope justifies one

Keep source identifiers such as course slugs, course IDs, chapter IDs, tutorial IDs, webinar IDs, or code-along IDs when available so future runs can retrieve the source again instead of relying on copied text.

## Content handling

Do not reproduce DataCamp course content wholesale. Summarize and transform retrieved material into an original learning workflow. Prefer durable references to DataCamp resources over embedding large amounts of provider content.

If DataCamp returns several plausible sources, choose based on direct topical fit, appropriate level, and progression rather than popularity alone.

If the requested topic is not adequately covered by DataCamp, state that directly instead of fabricating coverage.

## Skill-building behavior

When the user asks to turn DataCamp material into a skill specification:

1. Identify the stable workflow the skill should perform.
2. Distill only the knowledge and sequence required for that workflow.
3. Keep DataCamp as a runtime dependency when current information or detailed course retrieval is important.
4. Put static instructions in the skill and leave provider-specific retrieval to the DataCamp app.
5. Make the resulting skill portable: it should describe what to retrieve and how to use it, not depend on one chat transcript.
6. Include explicit failure behavior for missing, unavailable, or weak DataCamp results.

## Accuracy audit

Before finalizing:

- Confirm every named DataCamp resource came from the DataCamp app in the current workflow.
- Confirm the proposed sequence does not require concepts that have not yet been introduced.
- Confirm the output matches the user's requested depth and level.
- Remove unsupported claims about what a course teaches.
- Remove duplicated modules and unnecessary prerequisites.

## Invocation examples

- "Use DataCamp to build me a progressive Python fundamentals course."
- "Find DataCamp material on AI engineering and turn it into a reusable skill."
- "Compare the DataCamp courses that teach Power BI modeling and build a learning path."
- "Use DataCamp exercises to verify what this course actually teaches before making the curriculum."
