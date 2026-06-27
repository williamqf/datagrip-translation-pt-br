---
name: localization-translation-engine
description: Use for producing, reviewing, standardizing, and correcting pt-BR translations for a JetBrains DataGrip Language Pack. Focus on consistent terminology, professional Brazilian Portuguese for database/IDE users, preservation of SQL syntax, placeholders, escapes, HTML, resource bundle semantics, and JetBrains Language Pack boundaries. Do not translate SQL keywords, SQL snippets, database identifiers, generated code, or executable syntax.
---

# Localization Translation Engine

## Mission

Produce and refine Brazilian Portuguese translations for a JetBrains DataGrip Language Pack.

The goal is a professional, consistent, safe UI localization for DataGrip.

This skill defines how translations should be written.

It does not replace QA.

It complements the QA skill.

Primary objectives:

1. Translate only user-facing IDE interface text.
2. Preserve SQL syntax and executable code.
3. Maintain consistent DataGrip/database terminology.
4. Avoid literal, awkward, or AI-like translations.
5. Respect placeholders, escapes, and markup.
6. Keep UI text concise enough for IDE layouts.
7. Follow the JetBrains Language Pack model.

---

## Dependencies

* `datagrip-ptbr-localization-qa`: This translation engine relies on the QA skill to validate the safety and integrity of the translations generated.

---

## Quick Start

To execute this skill, use the following prompt pattern:
> "Use the `localization-translation-engine` skill to translate the pending keys in the English property files to Brazilian Portuguese (pt-BR)."

---

## Common Mistakes

* **Awkward Literal Translations**: Translating terms literally (e.g., translating `driver` as `motorista`, `query` as `interrogação`, `view` as `vista`, or `drop` as `derrubar`). Always consult the core glossary.
* **Corrupting Executable Code**: Translating SQL commands (`SELECT`, `INSERT`, etc.) in autocomplete, templates, or code generation contexts.
* **Broken formatting/escapes**: Removing or misplacing placeholder brackets (`{0}`) or escape characters (`\n`, `\t`) which breaks runtime interpolation.

---

## JetBrains Language Pack Boundary

A JetBrains Language Pack localizes UI text through resource bundles.

It must not change:

- SQL language behavior
- SQL parser behavior
- autocomplete logic
- generated SQL syntax
- editor semantics
- DataGrip runtime behavior

The plugin descriptor must declare the language pack using the official extension pattern:

```xml
<extensions defaultExtensionNs="com.intellij">
  <languageBundle locale="pt_BR"/>
</extensions>
```

Use `pt_BR` for Brazilian Portuguese in this project unless the project itself intentionally standardizes another locale format.

---

## Non-Negotiable Rule

Translate the IDE.

Do not translate SQL.

A translation is wrong if it converts executable SQL into Portuguese.

Forbidden examples:

```text
SELECT -> SELECIONAR
INSERT -> INSERIR
UPDATE -> ATUALIZAR
DELETE -> EXCLUIR
DROP -> DESCARTAR
ALTER -> ALTERAR
CREATE -> CRIAR
JOIN -> JUNTAR
WHERE -> ONDE
COMMIT -> CONFIRMAR
ROLLBACK -> REVERTER
NULL -> NULO
```

Allowed examples:

```text
Run SELECT query -> Executar consulta SELECT
Generate DROP statement -> Gerar instrução DROP
Commit transaction -> Fazer commit da transação
Rollback transaction -> Fazer rollback da transação
```

When a token can be SQL syntax, preserve it.

---

## Translation Scope

Translate:

- menu labels
- action names
- dialog labels
- settings text
- error descriptions
- warnings
- tooltips
- status messages
- UI explanations
- inspection descriptions
- non-executable examples where safe

Do not translate:

- SQL keywords used as syntax
- SQL templates
- generated code snippets
- live template bodies
- autocomplete insert text
- database identifiers
- file paths
- command-line options
- API names
- class names
- package names
- XML/HTML tag names
- placeholders
- escape sequences
- product names

---

## Required Translation Decision

For each non-trivial string, classify it before translating:

```text
UI_TEXT
MIXED_UI_WITH_SQL_TOKEN
SQL_SYNTAX_OR_TEMPLATE
CODE_OR_IDENTIFIER
PLACEHOLDER_HEAVY
HTML_TOOLTIP
UNKNOWN_NEEDS_REVIEW
```

Translation rules by class:

```text
UI_TEXT:
Translate naturally.

MIXED_UI_WITH_SQL_TOKEN:
Translate surrounding text and preserve SQL tokens.

SQL_SYNTAX_OR_TEMPLATE:
Do not translate executable syntax.

CODE_OR_IDENTIFIER:
Preserve code and identifiers.

PLACEHOLDER_HEAVY:
Translate carefully while preserving placeholder order and meaning.

HTML_TOOLTIP:
Translate visible text only. Preserve tags and entities.

UNKNOWN_NEEDS_REVIEW:
Prefer conservative preservation.
```

---

## Core Terminology Glossary

Use these preferred translations consistently:

```text
Action -> Ação
Apply -> Aplicar
Cancel -> Cancelar
Close -> Fechar
Copy -> Copiar
Create -> Criar
Delete -> Excluir
Edit -> Editar
Execute -> Executar
Export -> Exportar
Import -> Importar
Open -> Abrir
Refresh -> Atualizar
Remove -> Remover
Rename -> Renomear
Run -> Executar
Save -> Salvar
Search -> Pesquisar
Settings -> Configurações
View -> Exibir
```

Database and DataGrip terminology:

```text
Database -> Banco de dados
Data source -> Fonte de dados
Schema -> Esquema
Table -> Tabela
View -> Visão
Column -> Coluna
Row -> Linha
Cell -> Célula
Index -> Índice
Key -> Chave
Primary key -> Chave primária
Foreign key -> Chave estrangeira
Constraint -> Restrição
Trigger -> Trigger
Procedure -> Procedimento
Function -> Função
Sequence -> Sequência
Query -> Consulta
Statement -> Instrução
Script -> Script
Console -> Console
Editor -> Editor
Result set -> Conjunto de resultados
Data grid -> Grade de dados
Data editor -> Editor de dados
Database Explorer -> Explorador de banco de dados
Connection -> Conexão
Driver -> Driver
Dialect -> Dialeto
Transaction -> Transação
Commit -> Commit
Rollback -> Rollback
DDL -> DDL
DML -> DML
Data Definition Language -> Linguagem de definição de dados
Data Manipulation Language -> Linguagem de manipulação de dados
```

Keep these terms in English when they are established technical terms or syntax-bearing concepts:

```text
commit
rollback
driver
console
schema
query
script
SQL
DDL
DML
JDBC
NoSQL
CSV
JSON
XML
HTML
```

Use judgment: `schema` may be translated as `esquema` in UI descriptions, but preserve `schema` if it is part of a code-like expression or product-specific wording.

---

## Terms to Avoid

Avoid awkward or misleading translations:

```text
Query -> Interrogação
Statement -> Declaração
Data source -> Origem de dados
Driver -> Motorista
Schema -> Esquema visual
View -> Vista
Commit -> Confirmar
Rollback -> Reverter
Join -> Juntar
Drop -> Derrubar
```

Preferred alternatives:

```text
Query -> Consulta
Statement -> Instrução
Data source -> Fonte de dados
Driver -> Driver
Schema -> Esquema
View -> Visão
Commit -> Commit
Rollback -> Rollback
JOIN -> JOIN
DROP -> DROP
```

---

## Style Guide

Use Brazilian Portuguese.

Tone:

- professional
- direct
- concise
- technical
- natural for IT/database users

Avoid:

- overly formal legalistic phrasing
- childish wording
- verbose paraphrases
- machine-translation artifacts
- unnecessary anglicisms when a good pt-BR term exists
- forced Portuguese for established database terms

Prefer:

```text
Executar consulta
Fonte de dados
Conexão com banco de dados
Editor de dados
Grade de resultados
Aplicar alterações
Descartar alterações
```

Avoid:

```text
Rodar uma pergunta
Origem dos dados
Motorista do banco
Vista da tabela
Efetuar a realização da execução
```

---

## UI Length Rules

DataGrip UI has dense panels, compact buttons, and toolbars.

Translations must be concise.

Risk thresholds:

```text
LOW:
pt-BR length <= 1.4x English length

MEDIUM:
pt-BR length > 1.4x and <= 1.8x

HIGH:
pt-BR length > 1.8x
```

For buttons and short actions, prefer one or two words.

Examples:

```text
Apply -> Aplicar
Run -> Executar
Cancel -> Cancelar
Reload -> Recarregar
Reset -> Redefinir
```

Do not turn button labels into sentences.

---

## Placeholder Rules

Never add, remove, rename, or reorder placeholders unless the original MessageFormat semantics require a different grammatical order and all placeholders are preserved.

Preserve:

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

If reordering placeholders for Portuguese grammar, ensure all placeholders remain present exactly once unless repeated in original.

Before finalizing a translation:

```text
Original placeholders == translated placeholders
```

If not, stop and fix.

---

## Escape Rules

Preserve escape sequences:

```text
\n
\t
\r
\'
\"
\\
\uXXXX
```

Do not insert spaces after backslashes.

Do not convert literal escapes into actual line breaks unless the project format explicitly expects that.

Do not alter Unicode escapes casually.

---

## HTML and Markup Rules

Translate visible text only.

Preserve:

- tag names
- attributes
- entities
- opening/closing structure

Examples:

```html
<b>Warning</b>
```

May become:

```html
<b>Aviso</b>
```

Forbidden:

```html
<negrito>Aviso</negrito>
```

For tooltips, preserve semantic clarity and avoid overlong phrasing.

---

## Product and Brand Names

Do not translate:

```text
DataGrip
JetBrains
IntelliJ
IntelliJ Platform
JDBC
Gradle
Kotlin
Java
PostgreSQL
MySQL
Oracle
SQL Server
SQLite
MariaDB
MongoDB
Redis
Snowflake
BigQuery
ClickHouse
Cassandra
```

Preserve database product names exactly.

---

## SQL Token Firewall

Maintain a protected token list.

Protected tokens include:

```text
SELECT
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
JOIN
INNER JOIN
LEFT JOIN
RIGHT JOIN
FULL JOIN
CROSS JOIN
WHERE
FROM
INTO
VALUES
SET
GROUP BY
ORDER BY
HAVING
LIMIT
OFFSET
FETCH
WITH
UNION
INTERSECT
EXCEPT
CASE
WHEN
THEN
ELSE
END
NULL
TRUE
FALSE
COMMIT
ROLLBACK
SAVEPOINT
TRUNCATE
MERGE
GRANT
REVOKE
EXPLAIN
ANALYZE
PRIMARY KEY
FOREIGN KEY
REFERENCES
CONSTRAINT
INDEX
VIEW
TABLE
SCHEMA
DATABASE
```

If these appear in uppercase in the source, preserve them.

If they appear in code-like context, preserve them regardless of case.

---

## High-Risk Bundle Areas

Be extra conservative in keys or files related to:

```text
SqlBundle
DatabaseBundle
DatabaseDynamicBundle
DataGripBundle
DataGridBundle
```

High-risk key fragments:

```text
sql
query
statement
generate
template
completion
lookup
inspection
quickfix
intention
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

When these appear, classify the string before translating.

---

## Translation Examples

Safe UI translation:

```text
Original:
Execute selected statement

Translation:
Executar instrução selecionada
```

Mixed UI and SQL token:

```text
Original:
Generate SELECT statement

Translation:
Gerar instrução SELECT
```

Syntax must remain:

```text
Original:
SELECT * FROM table

Translation:
SELECT * FROM table
```

Dangerous and forbidden:

```text
SELECT * FROM table -> SELECIONAR * DE tabela
```

Tooltip:

```text
Original:
<b>Commit</b> current transaction

Translation:
Fazer <b>commit</b> da transação atual
```

---

## Consistency Rules

If a term appears across bundles, translate it consistently.

Preferred consistency examples:

```text
Data source -> Fonte de dados
Database Explorer -> Explorador de banco de dados
Result set -> Conjunto de resultados
Execution plan -> Plano de execução
Explain plan -> Plano EXPLAIN
Query console -> Console de consulta
Database console -> Console do banco de dados
```

Do not alternate between:

```text
Fonte de dados
Origem de dados
Fonte dos dados
```

Pick one: `Fonte de dados`.

---

## Review Checklist for Each Translation

Before accepting a translation, verify:

- Does it translate UI, not syntax?
- Are SQL tokens preserved?
- Are placeholders preserved?
- Are escapes preserved?
- Is HTML preserved?
- Is terminology consistent?
- Is it concise enough for UI?
- Is it natural pt-BR for database professionals?
- Could it alter generated code or autocomplete?
- If uncertain, did it choose the safer conservative option?

---

## Output Format for Translation Review

When reviewing strings, use:

```markdown
| Bundle | Key | Original | Current pt-BR | Issue | Proposed pt-BR | Severity |
|---|---|---|---|---|---|---|
```

Severity values:

```text
BLOCKER
CRITICAL
HIGH
MEDIUM
LOW
```

Use `BLOCKER` or `CRITICAL` when SQL syntax or placeholders are at risk.

---

## Automation Guidance

When building translation tooling, maintain:

```text
glossary.json
protected_sql_tokens.json
translation_memory.json
qa_translation_report.md
```

Recommended automated checks:

1. SQL token preservation.
2. glossary consistency.
3. placeholder parity.
4. escape parity.
5. HTML preservation.
6. length ratio.
7. suspicious literal translations.

The engine may suggest corrections, but QA must still validate high-risk entries.

---

## Relationship With QA Skill

Use this skill to decide how text should be translated.

Use `datagrip-ptbr-localization-qa` to decide whether the plugin is safe to test, build, and install.

Recommended pairing:

```text
localization-translation-engine
datagrip-ptbr-localization-qa
```

The translation engine improves language quality.

The QA skill protects runtime safety.

---

## Final Principle

If a translation makes the IDE more Brazilian but the SQL less SQL, it is wrong.

Preserve executable meaning first.

Polish UI wording second.
