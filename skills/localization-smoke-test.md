---
name: localization-smoke-test
description: Use for manual and semi-automated smoke testing of a JetBrains DataGrip pt-BR Language Pack after build and QA. Focus on installing the plugin from disk, restarting DataGrip, verifying UI localization, preserving SQL editor behavior, autocomplete, generated SQL, database explorer, settings, dialogs, tooltips, and safe non-destructive SQL execution. Do not run destructive SQL or alter databases.
---

# Localization Smoke Test

## Mission

Validate the DataGrip pt-BR Language Pack inside the actual DataGrip IDE after file-level QA and plugin build.

This skill is for runtime validation.

It answers:

1. Does the plugin install?
2. Does DataGrip restart?
3. Does the UI load in pt-BR?
4. Does the IDE remain stable?
5. Does SQL behavior remain intact?
6. Are translations usable in real screens?
7. Are there visible layout, tooltip, or terminology problems?

This skill does not replace file-level QA.

Use this after:

- `.properties` QA
- SQL syntax firewall
- placeholder validation
- `plugin.xml` validation
- Gradle build/package validation

---

## Dependencies

* `datagrip-ptbr-localization-qa`: This smoke test depends on a successful QA audit and build before runtime validation can begin.

---

## Quick Start

To execute this skill, use the following prompt pattern:
> "Use the `localization-smoke-test` skill to verify the packaged DataGrip pt-BR Language Pack plugin. Prepare the smoke test checklist and report findings."

---

## Common Mistakes

* **Running Destructive Commands**: Executing modifying statements (like `DROP`, `DELETE`, or `ALTER`) during testing on a production or non-disposable database.
* **Ignoring QA Status**: Installing the plugin when the QA phase reported `NEEDS_FIX_BEFORE_IDE_TEST` or `REJECTED_UNSAFE_SQL_TRANSLATION`.
* **Failing to Verify Autocomplete**: Neglecting to type partial keywords (e.g., `SEL`) to ensure suggestion options remain in English SQL syntax rather than translated.

---

## JetBrains Documentation Boundary

DataGrip supports installing plugins manually from a ZIP or JAR through:

```text
Settings / Plugins / Install Plugin from Disk
```

The tested artifact should be the packaged plugin archive produced by the build, usually under:

```text
build/distributions/
```

A Language Pack must behave as a localization plugin. It must not change SQL language behavior, parser behavior, database behavior, or generated SQL syntax.

---

## Non-Destructive Rule

Never run destructive SQL during smoke testing.

Forbidden against real databases:

```sql
DROP
DELETE
TRUNCATE
ALTER
UPDATE
INSERT
CREATE
MERGE
GRANT
REVOKE
COMMIT
ROLLBACK
```

Allowed only in a disposable sandbox if explicitly authorized.

Default allowed smoke queries:

```sql
SELECT 1;
SELECT CURRENT_DATE;
SELECT CURRENT_TIMESTAMP;
```

If no safe connection exists, test editor/autocomplete behavior without executing against a real database.

---

## Preconditions

Before smoke testing, confirm:

```text
Plugin ZIP exists:
Gradle build succeeded:
QA report status:
DataGrip version:
Plugin version:
Installation method:
Backup/rollback plan:
```

Do not install if QA decision is:

```text
NEEDS_FIX_BEFORE_IDE_TEST
NEEDS_BUILD_FIX
REJECTED_UNSAFE_SQL_TRANSLATION
```

Only install if QA decision is:

```text
APPROVED_FOR_IDE_SMOKE_TEST
```

or user explicitly overrides.

---

## Smoke Test Levels

Use three levels.

### Level 1 - Startup Safety

Goal: prove the IDE starts and plugin does not crash.

Checks:

1. Install plugin from disk.
2. Restart DataGrip.
3. Confirm DataGrip opens.
4. Confirm no startup crash.
5. Confirm no plugin error notification.
6. Confirm plugin appears installed.

### Level 2 - UI Localization Coverage

Goal: verify visible localization.

Checks:

1. Settings.
2. Plugins page.
3. Database Explorer.
4. SQL Console.
5. Data Editor.
6. Context menus.
7. Toolbars.
8. Tooltips.
9. Dialogs.
10. Status messages.

### Level 3 - SQL Behavior Integrity

Goal: verify SQL remains SQL.

Checks:

1. SQL editor opens.
2. Syntax highlighting remains normal.
3. Autocomplete suggests SQL keywords in English SQL syntax.
4. Generated SQL remains valid SQL.
5. Harmless `SELECT 1;` runs if safe connection exists.
6. Dialogs mentioning SQL preserve SQL tokens.
7. No SQL keyword appears translated inside code editor or generated snippets.

---

## Manual Installation Steps

Use the documented manual installation path:

```text
Ctrl + Alt + S
Plugins
Gear icon
Install Plugin from Disk
Select ZIP/JAR
OK
Restart IDE
```

Record:

```text
Plugin archive path:
Install result:
Restart result:
Plugin appears installed: yes/no
Language applied: yes/no/partial
Errors observed:
```

---

## Rollback Plan

Before installing, know how to remove the plugin:

```text
Settings
Plugins
Installed
Find plugin
Disable or Uninstall
Restart IDE
```

If DataGrip cannot start after installation, use safe mode or remove the plugin from the IDE plugins directory according to the local environment.

Do not delete unrelated plugin directories.

---

## Required Evidence

For each screen tested, collect:

```text
Screen:
Expected:
Observed:
Status:
Issue:
Severity:
Screenshot path, if available:
```

Status values:

```text
PASS
FAIL
PARTIAL
NOT_TESTED
```

Severity values:

```text
BLOCKER
CRITICAL
HIGH
MEDIUM
LOW
```

---

## Startup Checklist

```text
[ ] Plugin archive exists
[ ] Plugin installs from disk
[ ] Restart requested
[ ] DataGrip restarts successfully
[ ] No startup crash
[ ] No plugin error notification
[ ] Plugin appears in Installed plugins
[ ] UI language appears pt-BR
```

Any startup crash is `BLOCKER`.

---

## UI Screen Checklist

Check these screens:

```text
Welcome screen
Settings
Plugins
Database Explorer
Data Sources and Drivers
SQL Console
Query result grid
Data Editor
Context menus
Navigation/search actions
Notifications
Inspection messages
Tooltips
Confirmation dialogs
```

For each screen, classify:

```text
Localization coverage:
Terminology quality:
Layout risk:
Broken HTML:
Untranslated critical text:
```

Untranslated text is not automatically a failure unless it is central, confusing, or inconsistent.

Broken UI rendering is higher priority than incomplete coverage.

---

## SQL Editor Integrity Checklist

Check:

```text
[ ] SQL keywords remain SQL
[ ] Autocomplete uses SQL syntax
[ ] Generated SQL remains executable
[ ] Templates do not insert translated SQL
[ ] Syntax highlighting works
[ ] Inspections do not corrupt SQL wording
[ ] Quick fixes do not generate translated SQL
```

Examples of failures:

```text
SELECT appears as SELECIONAR in editor insertion
DROP TABLE generated as DESCARTAR TABELA
WHERE generated as ONDE
JOIN generated as JUNTAR
NULL generated as NULO
```

These are `CRITICAL` or `BLOCKER`.

---

## Safe Query Test

Only if a safe connection exists.

Run:

```sql
SELECT 1;
```

Optional:

```sql
SELECT CURRENT_DATE;
SELECT CURRENT_TIMESTAMP;
```

Record:

```text
Connection:
Dialect:
Query:
Result:
Errors:
```

Do not run destructive SQL.

If no connection exists, mark as:

```text
NOT_TESTED - no safe connection
```

This is acceptable.

---

## Autocomplete Test

In SQL console, type partial tokens:

```text
SEL
WHE
JOI
GRO
ORD
```

Expected suggestions:

```text
SELECT
WHERE
JOIN
GROUP BY
ORDER BY
```

Failure if suggestions are translated as Portuguese SQL tokens.

Record:

```text
Input:
Expected:
Observed:
Status:
```

---

## Generated SQL Test

Use only non-destructive generation paths where possible.

Examples:

- generate SELECT statement
- preview query
- copy generated SELECT
- inspect DDL preview without executing

Expected:

```text
SQL keywords remain in SQL.
UI labels may be pt-BR.
```

Do not execute destructive generated SQL.

---

## Dialog and Tooltip Test

Check dialogs that mention SQL operations.

Allowed:

```text
Deseja executar a instrução DROP?
```

Forbidden:

```text
Deseja executar a instrução DESCARTAR?
```

Validate:

- SQL tokens preserved
- HTML not broken
- placeholders rendered correctly
- dialog buttons are concise
- no truncated critical action labels

---

## Layout Risk Rules

Classify layout problems:

```text
LOW:
minor longer wording, still readable

MEDIUM:
noticeable overflow or cramped label

HIGH:
button/menu/dialog becomes hard to use

CRITICAL:
text hides controls or blocks workflow
```

Prefer concise UI wording over literal completeness.

---

## Smoke Test Report Template

Every smoke test must produce:

```markdown
# DataGrip pt-BR Language Pack Smoke Test Report

## Test Environment

## Plugin Artifact

## Installation Result

## Startup Result

## UI Localization Results

## SQL Editor Integrity Results

## Autocomplete Results

## Generated SQL Results

## Safe Query Execution Results

## Dialog and Tooltip Results

## Layout Risks

## Issues Found

| Severity | Area | Description | Evidence | Recommendation |
|---|---|---|---|---|

## Final Decision

## Rollback Needed

## Next Actions
```

Final decision must be exactly one:

```text
APPROVED_FOR_DAILY_USE_TEST
APPROVED_WITH_MINOR_ISSUES
NEEDS_TRANSLATION_FIX
NEEDS_BUILD_FIX
REJECTED_SQL_INTEGRITY_RISK
REJECTED_STARTUP_RISK
```

---

## Decision Rules

Use:

```text
APPROVED_FOR_DAILY_USE_TEST
```

only if:

- DataGrip starts
- plugin loads
- core UI is pt-BR
- SQL editor works
- autocomplete is not corrupted
- no BLOCKER/CRITICAL issues

Use:

```text
REJECTED_SQL_INTEGRITY_RISK
```

if any SQL syntax is translated in editor, generated SQL, autocomplete, template, or executable context.

Use:

```text
REJECTED_STARTUP_RISK
```

if IDE startup fails, plugin fails to load, or severe plugin exception occurs.

---

## Relationship With Other Skills

Use before this skill:

```text
localization-translation-engine
datagrip-ptbr-localization-qa
```

Use this skill only after file-level and build-level confidence exists.

If smoke test finds translation problems, return to:

```text
localization-translation-engine
```

If smoke test finds structural or build problems, return to:

```text
datagrip-ptbr-localization-qa
```

---

## Prompt Usage Pattern

```text
Use the localization-smoke-test skill.

Goal:
Prepare and execute a safe smoke test plan for the DataGrip pt-BR Language Pack.

Rules:
- Do not run destructive SQL.
- Do not alter real databases.
- Verify plugin install, IDE startup, UI localization, SQL editor, autocomplete, generated SQL, and harmless SELECT behavior.
- Produce a smoke test report with final decision.
```

---

## Final Principle

The smoke test exists to answer one question:

Can a real DataGrip user install this Language Pack and work safely without corrupting SQL behavior?

If not, reject it.
