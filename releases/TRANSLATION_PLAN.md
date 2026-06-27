# Plano de Tradução e Cobertura - DataGrip Portuguese Pack

Este documento descreve o status atual das traduções e o planejamento para atingir a cobertura máxima (100%) da IDE na versão `v3.0.0`.

## 1. Estatísticas de Tradução Atuais (Base: v2.4.2)

De acordo com a auditoria dos arquivos de recursos (.properties) sob `temp_english_properties` e `src/main/resources/messages/`:

| Bundle (.properties) | Total Chaves (Inglês) | Traduzidas | Idênticas ao Inglês (Não Traduzidas) | Cobertura (%) |
|---|---:|---:|---:|---:|
| **ActionsBundle** | 2.809 | 1.890 | 919 | 67.2% |
| **DataGridBundle** | 428 | 1 | 427 | 0.2% |
| **DataGripBundle** | 29 | 28 | 1 | 96.5% |
| **DatabaseBundle** | 3.298 | 2.006 | 1.292 | 60.8% |
| **DatabaseDynamicBundle** | 505 | 0 | 505 | 0.0% |
| **IdeBundle** | 2.904 | 71 | 2.833 | 2.4% |
| **SqlBundle** | 792 | 2 | 790 | 0.2% |
| **TOTAL** | **10.765** | **3.998** | **6.767** | **37.1%** |

* **Status:** Atualmente, apenas **37.1%** da IDE está traduzida. Os painéis de configurações, consoles de banco de dados e ações contextuais específicas de SQL/Grids ainda estão majoritariamente em inglês.

---

## 2. Escopo Planejado para v3.0.0 (100% de Cobertura)

### Fase A: Menus Principais e Configurações
* **IdeBundle.properties (2.833 chaves):** Tradução dos menus de preferência como *Appearance & Behavior*, *Version Control*, *Tools*, *Backup and Sync*, *Advanced Settings*, bem como o *AI Assistant*.
* **ActionsBundle.properties (919 chaves):** Tradução de itens do menu superior ("Settings...", "Local History", etc.).

### Fase B: Console SQL e Grades de Dados
* **SqlBundle.properties (790 chaves):** Destaque de sintaxe, mensagens do console SQL e autocompletar.
* **DataGridBundle.properties (427 chaves):** Painel de exportação de dados (CSV, JSON), edição inline de células de tabelas.
* **DatabaseDynamicBundle.properties (505 chaves):** Menus dinâmicos de tabelas e esquemas.

### Fase C: Mensagens de Sistema e Drivers
* **DatabaseBundle.properties (1.292 chaves):** Localização de metadados profundos, diálogos de introspecção e erros JDBC.

---

## 3. Diretrizes de Qualidade e Segurança (QA Firewall)

Durante a tradução automatizada de lotes, o mecanismo do script `scripts/validate_translation.py` garantirá que:
1. **Preservação de Placeholders:** Placeholders como `{0}`, `%s`, `%1$s` permaneçam idênticos.
2. **Preservação de Escapes:** Sequências como `\n`, `\t` e aspas escapadas sejam idênticas.
3. **Firewall SQL:** Palavras-chave SQL reservadas em caixa alta (como `SELECT`, `DROP`, `WHERE`, `COMMIT`) não sejam traduzidas nas mensagens do console ou modelos de geração de código.
