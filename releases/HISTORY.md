# Histórico de Lançamentos - DataGrip Portuguese Pack

Este arquivo contém a cronologia de lançamentos do pacote de tradução em Português do Brasil para o JetBrains DataGrip.

## [v1.0.1] - 2026-06-27
* **Foco:** Atualização de metadados, simplificação da descrição e remoção de termos comunitários.
* **Ajustes:**
  * O nome do plugin foi atualizado para "Portuguese (Brazil) Language Pack".
  * O nome do fornecedor (vendor) foi alterado para "William Q. Fernandes".
  * O texto de descrição (Overview) foi simplificado.

## [v1.0.0] - 2026-06-27
* **Foco:** Primeiro lançamento oficial da tradução no novo padrão de versionamento (1.x).
* **Melhorias:**
  * Tradução integrada de menus, painéis, console SQL e grade de dados (Data Grid).
  * Restrição de compatibilidade exclusiva para o DataGrip.

## [v3.2.0] - 2026-06-24
* **Foco:** Resolução definitiva de termos residuais em inglês e correção de conflitos de chaves.
* **Melhorias:**
  * Implementação de cache de tradução com suporte a namespaces (`filename:key`) e validação de assinatura (placeholders e sequências de escape), resolvendo de vez colisões de chaves idênticas entre diferentes bundles da IDE.
  * Tradução correta de termos gerais retidos pelo whitelist de TI, como `"Default"` e `"Set as Default"`, agora localizados apropriadamente como `"Padrão"` e `"Definir como Padrão"`.
  * Correção do bug de escape de caracteres especiais no salvamento de chaves (como `ignoreTokenType.syntax\:` no `VcsBundle`), garantindo compatibilidade e validação de QA com 0 erros críticos/blockers.

## [v3.1.0] - 2026-06-24
* **Foco:** Tradução completa e pente-fino das configurações.
* **Melhorias:**
  * Mapeamento e tradução dos bundles internos de configurações do IntelliJ (`OptionsBundle`, `ToolsBundle`, `VcsBundle`, `TerminalBundle`, `UIBundle`, `XPathBundle` e debuggers).
  * Correções dos textos em inglês na barra lateral esquerda e categorias de configurações.
  * O tamanho da base traduzida subiu de 10.765 para **13.893 termos**.
  * Correção de erros críticos de QA nos placeholders de chaves no `IdeBundle`, `VcsBundle` e `XPathBundle`.

## [v3.0.0] - 2026-06-24
* **Foco:** Reestruturação física e tradução inicial ampliada.
* **Melhorias:**
  * Reestruturação física do projeto com a pasta de releases permanente (`releases/`) e arquivos de histórico.
  * Tradução ampliada do `IdeBundle` e `ActionsBundle`.
  * Tradução dos pacotes de banco de dados (`SqlBundle`, `DataGridBundle`, `DatabaseDynamicBundle`).

## [v2.4.2] - 2026-06-24
* **Ajustes:** Correções menores e alinhamento de termos no `ActionsBundle` e `DatabaseBundle`.

## [v2.4.1] - 2026-06-24
* **Ajustes:** Correção de pequenos erros de digitação e formatação em mensagens de erro de drivers JDBC.

## [v2.4.0] - 2026-06-24
* **Melhorias:** Expansão das traduções de menus do console SQL e das mensagens de introspecção de bancos de dados.

## [v2.3.0] - 2026-06-24
* **Melhorias:** Adicionadas traduções para menus principais e itens do `ActionsBundle` (menus File, Edit, View, Navigate, Code, etc.).

## [v2.2.0] - 2026-06-24
* **Ajustes:** Correções de placeholders e preservação de tags HTML nas mensagens do `DatabaseBundle`.

## [v2.1.0] - 2026-06-24
* **Melhorias:** Traduções iniciais do gerenciador de conexões de banco de dados (`DatabaseBundle`).

## [v2.0.0] - 2026-06-24
* **Melhorias:** Primeira grande expansão contendo traduções do `DataGripBundle` básico e ativação da localidade `pt_BR`.

## [v1.0.0] - 2026-06-24
* **Melhorias:** Lançamento inicial com a estrutura básica do projeto Gradle e suporte inicial para o JetBrains Language Pack.
