---
name: datagrip-ptbr-localization-qa
description: Use for QA, testing, validation, and correction of a JetBrains DataGrip pt-BR Language Pack. Focus on preserving SQL syntax, validating .properties structure, placeholders, escapes, HTML/tooltips, UI terminology, plugin.xml languageBundle, Gradle verification, build packaging, and manual IDE smoke testing. Do not translate SQL commands, SQL keywords, generated code snippets, or database identifiers.
---

# DataGrip pt-BR Localization QA

## Mission

Act as the final QA gate for the DataGrip pt-BR Language Pack.

The goal is to validate that the plugin translates the DataGrip IDE interface into Brazilian Portuguese without breaking:

1. SQL syntax
2. code generation
3. autocomplete
4. placeholders
5. escaped sequences
6. HTML/tooltips
7. plugin structure
8. Gradle verification
9. IDE runtime behavior

This skill exists to protect the IDE, not to maximize translation coverage.

A partial but safe translation is better than a complete translation that corrupts SQL, code generation, or runtime behavior.

---

## Dependencies

* None (This skill is self-contained and does not rely on other external skills).

---

## Quick Start

To execute this skill, use the following prompt pattern:
> "Use the `datagrip-ptbr-localization-qa` skill to audit the DataGrip pt-BR Language Pack. Run all checks, report findings, and verify if it is safe for IDE smoke testing."

---

## Common Mistakes

* **Translating SQL Keywords**: Translating executable SQL commands (e.g., changing `SELECT` to `SELECIONAR` or `COMMIT` to `CONFIRMAR`) inside code generation, autocomplete, or template bundles.
* **Placeholder/Escape Sequence Mismatch**: Modifying or removing variables (like `{0}`, `%s`) or escape sequences (like `\n`, `\t`) during translation, which breaks Java runtime string formatting.
* **Corrupting HTML Tags**: Translating HTML tag names, leaving tags open, or breaking attribute quotes inside tooltips and descriptions, resulting in rendering glitches.
* **Bypassing Build Errors**: Ignoring compilation or verification warnings from Gradle tasks, leading to broken plugin packages.

---

## Critical Boundary

Translate the IDE.

Do not translate SQL.

The plugin may translate UI text, labels, dialogs, menus, tooltips, and user-facing descriptions.

The plugin must not translate:

- SQL reserved words
- SQL commands
- generated SQL snippets
- autocomplete code fragments
- templates that insert SQL into the editor
- database object identifiers
- JDBC/driver-specific syntax
- function names when used as executable syntax
- code examples where translation changes executable meaning

Examples that must remain unchanged when used as syntax:

```text
SELECT
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
JOIN
WHERE
GROUP BY
ORDER BY
HAVING
COMMIT
ROLLBACK
TRUNCATE
MERGE
WITH
FROM
INTO
VALUES
NULL
TRUE
FALSE
```

Allowed:

```text
Run SELECT statement
```

May become:

```text
Executar instrução SELECT
```

Forbidden:

```text
Executar instrução SELECIONAR
```

---

## Project Context

This project is a JetBrains DataGrip Language Pack for Portuguese Brazil (`pt_BR`).

Known localized bundles may include:

```text
DataGripBundle_pt_BR.properties
DatabaseDynamicBundle_pt_BR.properties
DataGridBundle_pt_BR.properties
SqlBundle_pt_BR.properties
DatabaseBundle_pt_BR.properties
```

Known implementation details may include:

```text
plugin.xml
build.gradle.kts
settings.gradle.kts
gradle.properties
translation_cache.json
scripts/extract_bundles.py
scripts/translate_bundles.py
```

The plugin descriptor must preserve:

```xml
<languageBundle locale="pt_BR"/>
```

---

## Evidence and Safety Rules

Before changing translations, identify:

1. original English key/value
2. current pt-BR value
3. bundle file
4. key name
5. why the translation is unsafe, incorrect, or acceptable
6. proposed correction

Do not rewrite large groups blindly.

Do not normalize SQL keywords into Portuguese.

Do not alter placeholders.

Do not alter escape semantics.

Do not alter HTML structure unless fixing a broken tag.

Do not change build configuration unless QA evidence requires it.

---

## QA Priority Order

Validate in this order:

1. SQL syntax preservation
2. placeholder parity
3. escape parity
4. HTML/tooltips integrity
5. key parity between original and pt-BR bundles
6. plugin.xml languageBundle
7. semantic quality of pt-BR UI text
8. UI length and layout risk
9. Gradle verification
10. packaged plugin smoke test

If a higher-priority failure exists, fix it before cosmetic translation improvements.

---

## Phase 1 - Inventory

First, locate and document:

```text
Original bundle directory:
pt-BR bundle directory:
Number of original bundle files:
Number of pt-BR bundle files:
Number of keys per bundle:
plugin.xml path:
Gradle wrapper/path:
JDK used:
Build artifact path:
```

Expected report:

```markdown
# Localization QA Inventory

| Bundle | Original Keys | pt-BR Keys | Missing | Extra | Status |
|---|---:|---:|---:|---:|---|
```

---

## Phase 2 - Key Parity

For each original `.properties` file and matching `_pt_BR.properties` file:

Validate:

- no missing keys
- no unexpected extra keys unless justified
- no duplicate keys
- encoding can be read safely
- comments do not break parsing
- line continuations remain valid

Failure severity:

```text
CRITICAL:
missing runtime key, malformed properties file, duplicate causing ambiguity

HIGH:
extra/obsolete key likely ignored but confusing

MEDIUM:
comment/format inconsistency

LOW:
style-only issue
```

---

## Phase 3 - Placeholder Parity

Placeholders must match exactly between original and localized value.

Validate these patterns:

```text
{0}
{1}
{2}
%s
%d
%f
%1$s
%2$d
```

Also preserve MessageFormat quoting rules:

```text
''
'{0}'
```

For every mismatch, report:

```text
Bundle:
Key:
Original:
Translation:
Original placeholders:
Translation placeholders:
Severity:
Fix:
```

Default severity: `CRITICAL`.

Do not guess missing placeholders. Restore them exactly.

---

## Phase 4 - Escape Sequence Parity

Validate escape sequences:

```text
\n
\t
\r
\'
\"
\\
\uXXXX
```

Rules:

- preserve intentional newlines
- preserve tabs if used structurally
- do not add spaces after backslashes
- do not double-unescape
- do not convert literal escape sequences into real control characters unless format requires it
- preserve Unicode escapes if the project standard uses them

Report:

```text
Bundle:
Key:
Original escapes:
Translation escapes:
Problem:
Fix:
```

Severity: `CRITICAL` when it can break parsing or runtime rendering.

---

## Phase 5 - HTML and Tooltip Integrity

Some DataGrip/Database/DataGrid strings may include HTML fragments.

Validate:

- balanced tags
- no broken `<b>`, `<i>`, `<code>`, `<a>`, `<br>`
- no translated tag names
- no broken entities
- no malformed attributes
- no missing closing tags where required
- no inserted angle brackets from translation

Allowed tags must remain tags.

Forbidden:

```text
<b>Importante
```

Required:

```text
<b>Importante</b>
```

Report:

```text
Bundle:
Key:
Original HTML:
Translation HTML:
Issue:
Fix:
```

Severity: `HIGH` or `CRITICAL` depending on rendering risk.

---

## Phase 6 - SQL Syntax Firewall

This is the most important localization rule.

Analyze keys and values in:

```text
SqlBundle
DatabaseBundle
DatabaseDynamicBundle
DataGripBundle
DataGridBundle
```

High-risk key patterns:

```text
sql
query
statement
generate
template
completion
inspection
quickfix
intention
live.template
console
ddl
dml
select
insert
update
delete
drop
alter
create
join
where
commit
rollback
```

A translation is unsafe if it changes executable syntax.

Examples of unsafe changes:

```text
SELECT -> SELECIONAR
DROP -> DESCARTAR
COMMIT -> CONFIRMAR
ROLLBACK -> REVERTER
JOIN -> JUNTAR
WHERE -> ONDE
NULL -> NULO
```

Valid UI translation keeps SQL keywords intact:

```text
Drop table -> Remover tabela
DROP TABLE -> DROP TABLE
Generate SELECT -> Gerar SELECT
```

Classification:

```text
SAFE_UI_TEXT
SQL_SYNTAX_MUST_REMAIN
MIXED_UI_WITH_SQL_TOKEN
UNKNOWN_NEEDS_REVIEW
```

For every risky string, report:

```text
Bundle:
Key:
Original:
Translation:
Classification:
Risk:
Fix:
```

Default fix: preserve SQL tokens exactly and translate only surrounding UI text.

---

## Phase 7 - Autocomplete and Code Generation Protection

Treat strings used for code insertion as code.

If a key appears to produce SQL snippets or templates, do not translate executable parts.

High-risk indicators:

```text
action.generate.*
template.*
completion.*
lookup.*
intention.*
quickfix.*
sql.*
ddl.*
dml.*
```

If uncertain, classify as:

```text
UNKNOWN_NEEDS_REVIEW
```

and prefer preserving the original syntax.

Rule:

When unsure whether a string is UI or generated code, do not translate the syntax-bearing part.

---

## Phase 8 - Semantic UI Review

After structural safety is clean, review Portuguese quality.

Prioritize DataGrip user profile:

- database developers
- DBAs
- data analysts
- system analysts
- infrastructure professionals

Prefer established Brazilian technical terminology:

```text
database -> banco de dados
schema -> esquema
table -> tabela
view -> visão
index -> índice
constraint -> restrição
foreign key -> chave estrangeira
primary key -> chave primária
query -> consulta
statement -> instrução
connection -> conexão
data source -> fonte de dados
driver -> driver
console -> console
transaction -> transação
commit -> commit
rollback -> rollback
```

Avoid awkward literal AI translations.

Examples:

```text
Apply -> Aplicar
Cancel -> Cancelar
Execute -> Executar
Run -> Executar
Data Source -> Fonte de dados
Database Explorer -> Explorador de banco de dados
```

Do not over-translate accepted technical terms.

---

## Phase 9 - UI Length and Layout Risk

Short UI controls must remain short.

Pay attention to:

- buttons
- tabs
- toolbars
- context menu items
- status labels
- small dialogs
- grid actions

Risk indicators:

- pt-BR value is more than 1.8x original length
- button label becomes a sentence
- menu item becomes too verbose
- tooltip loses clarity
- repeated nouns create visual clutter

Report as:

```text
LAYOUT_RISK_LOW
LAYOUT_RISK_MEDIUM
LAYOUT_RISK_HIGH
```

Prefer concise wording.

---

## Phase 10 - Plugin Descriptor QA

Validate `plugin.xml`.

Required:

```xml
<languageBundle locale="pt_BR"/>
```

Check:

- locale is exactly `pt_BR`
- plugin ID is stable
- version is present
- languageBundle is not duplicated incorrectly
- descriptor remains valid XML
- no unrelated plugin behavior was added

Do not add features to the plugin.

This project is a Language Pack.

---

## Phase 11 - Build and Packaging QA

When authorized to run tests, execute:

```text
./gradlew verifyPlugin
./gradlew buildPlugin
```

If Windows local Gradle/JDK paths are used, respect the project setup.

Do not install or download dependencies unless explicitly authorized.

Record:

```text
Command:
Working directory:
JDK:
Gradle:
Exit code:
Key output:
Artifact path:
```

Build output must not be treated as successful unless exit code is 0 and expected artifact exists.

---

## Phase 12 - Manual IDE Smoke Test Plan

Before testing inside DataGrip, create a smoke test checklist.

Minimum checks:

1. Plugin installs from disk.
2. IDE restarts successfully.
3. UI language changes to pt-BR.
4. DataGrip opens without crash.
5. Settings opens.
6. Database Explorer opens.
7. SQL console opens.
8. Autocomplete still suggests SQL keywords correctly.
9. Generated SQL remains SQL.
10. Running a harmless query still works.
11. Dialogs containing SQL keep SQL keywords intact.
12. Tooltips render without broken HTML.

Harmless query examples:

```sql
SELECT 1;
SELECT CURRENT_DATE;
```

Do not test destructive SQL such as `DROP`, `DELETE`, `TRUNCATE`, or `ALTER` against real databases.

---

## Severity Model

Use this severity scale:

```text
BLOCKER:
IDE crash, broken plugin loading, malformed properties, broken plugin.xml, SQL syntax corruption.

CRITICAL:
placeholder mismatch, broken escapes, SQL keyword translated in syntax context, build failure.

HIGH:
HTML broken, autocomplete/code generation risk, missing keys, major semantic error.

MEDIUM:
awkward technical translation, layout risk, inconsistent terminology.

LOW:
style preference, minor wording improvement.
```

---

## Required QA Output

Every QA pass must produce:

```markdown
# DataGrip pt-BR Localization QA Report

## Scope

## Files Checked

## Summary

## Blockers

## Critical Issues

## SQL Syntax Firewall Findings

## Placeholder Findings

## Escape Findings

## HTML Findings

## Semantic UI Findings

## Layout Risk Findings

## Build/Packaging Status

## Manual Smoke Test Plan

## Decision

## Next Actions
```

Decision must be one of:

```text
APPROVED_FOR_IDE_SMOKE_TEST
NEEDS_FIX_BEFORE_IDE_TEST
NEEDS_BUILD_FIX
REJECTED_UNSAFE_SQL_TRANSLATION
```

---

## Automation Recommendations

Prefer creating or improving QA scripts when repeated checks are needed.

Useful scripts:

```text
scripts/qa_check_properties.py
scripts/qa_sql_firewall.py
scripts/qa_html_placeholders.py
scripts/qa_generate_report.py
```

Scripts should:

- compare original vs pt-BR bundles
- check key parity
- check placeholders
- check escapes
- check HTML
- flag SQL keyword translations
- generate Markdown and JSON reports

Do not rely only on manual review.

---

## Guardrails for Automated Fixes

Automated fixes may:

- restore missing placeholders
- restore SQL tokens
- fix obvious broken HTML tags
- normalize accepted terminology
- reduce overly verbose button labels

Automated fixes must not:

- alter SQL code snippets semantically
- invent missing context
- rewrite whole bundles blindly
- change original source bundles
- remove keys
- modify build files without reason
- touch plugin artifact unless building

---

## Recommended Workflow

1. Inventory files.
2. Run structural checks.
3. Run SQL syntax firewall.
4. Fix BLOCKER and CRITICAL issues first.
5. Run semantic UI review.
6. Run layout risk review.
7. Validate `plugin.xml`.
8. Run `verifyPlugin`.
9. Run `buildPlugin`.
10. Generate QA report.
11. Only then perform IDE smoke test.

---

## Prompt Usage Pattern

When invoked, prefer this pattern:

```text
Use the datagrip-ptbr-localization-qa skill.

Goal:
Audit the DataGrip pt-BR Language Pack before IDE smoke testing.

Do not install the plugin yet.
Do not change SQL syntax.
Do not translate SQL keywords.
First produce a QA plan and then run safe file-level checks.
```

---

## Final Principle

A localization plugin can sound less polished and still be acceptable.

It cannot corrupt SQL.

It cannot break placeholders.

It cannot break IDE startup.

Protect those first.