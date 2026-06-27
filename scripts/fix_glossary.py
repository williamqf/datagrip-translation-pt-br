import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CACHE_FILE = os.path.join(BASE_DIR, "translation_cache.json")

GLOSSARY_CORRECTIONS = {
    # 1. Statement -> Instrução (Database context)
    "action.MoveStatementDown.text": "Mover Instrução P_ara Baixo",
    "action.MoveStatementDown.description": "Mover as instruções selecionadas uma linha para baixo",
    "action.MoveStatementUp.text": "Mover Instrução P_ara Cima",
    "action.MoveStatementUp.description": "Mover as instruções selecionadas uma linha para cima",
    "action.Console.Execute.text": "Executar Instrução Atual no Console",
    "action.Console.Execute.description": "Executa a instrução atual no console",
    "action.Console.Execute.Multiline.text": "Executar Instrução Atual no Console Multilinha",
    "action.Console.Execute.Multiline.description": "Executa a instrução atual no console multilinha",
    "action.EditorChooseLookupItemCompleteStatement.text": "Escolher Item de Busca e Invocar Completar Instrução",
    "action.EditorCompleteStatement.text": "Completar Instrução Atual",
    "scriptGen.option.ConstraintContext.description": "Especificar onde colocar as restrições.\\n<ul>\\n<li><b>Dentro da Coluna</b> na definição da coluna quando a restrição se baseia em uma única coluna.\\nQuando a restrição se baseia em duas ou mais colunas, coloque as restrições\\nna definição da tabela após todas as colunas.</li>\\n<li><b>Dentro da Tabela</b> na definição da tabela, após todas as colunas.</li>\\n<li><b>Após a Tabela</b> após a definição da tabela, usando ALTER TABLE ADD CONSTRAINT.</li>\\n</ul>\\n<p>\\nO processamento de algumas instruções de chave estrangeira pode ser adiado para resolver dependências cíclicas.\\n</p>",
    
    # 2. Commit -> Commit
    "action.Console.TableResult.SubmitAndCommit.text": "Enviar e Commit",
    "action.Console.TableResult.SubmitAndCommit.description": "Enviar e fazer commit de uma transação",
    "dialog.message.failed.to.transaction.in.progress.choice.commit.or.rollback.it.first.try.again": "Falha ao {0}. A transação está em andamento{2, choice, 0# \"{1}\"|1#}. Faça commit ou rollback dela primeiro e tente novamente",
    "notification.content.transaction.choice.committed.rolled.back": "transação {0, choice, 0#comitada|1#com rollback realizado}{1}",

    # 3. Rollback -> Rollback
    "message.text.error.failed.to.rollback.to.a.savepoint": "Falha ao fazer rollback para um savepoint.",
    "action.Console.Transaction.RevertAndRollback.text": "Rollback",
    "action.Console.Transaction.RevertAndRollback.description": "Fazer rollback de uma transação",
    "action.Console.Transaction.Rollback.text": "Rollback",
    "notification.content.rollback.current.transaction.to.undo.changes": "Faça rollback da transação atual para desfazer as alterações.",
    "all.changes.will.be.rolled.back": "Todas as alterações sofrerão rollback.",
    "database.config.rollback.changes": "Descartar Alterações (Rollback)",
    
    # 4. Reticências Omitidas
    "action.sql.ExtractFunctionAction.text": "Extrair Rotina...",
    "action.sql.ImplementMembersAction.text": "Implementar Membros...",
    "action.sql.IntroduceAliasAction.text": "Alias de tabela...",
    "intention.name.change.dialect.to": "Alterar dialeto para...",
    "popup.title.qualify.with": "Qualificar com...",
    "settings.check": "Verificar...",
    "settings.test.rule": "Testar regra..."
}

def main():
    if not os.path.exists(CACHE_FILE):
        print("Erro: Cache file não encontrado.")
        return
        
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
        
    updated = 0
    for key, new_val in GLOSSARY_CORRECTIONS.items():
        if key in cache:
            # Only update if it actually changed
            if cache[key] != new_val:
                print(f"Atualizando {key}:")
                print(f"  Antes: '{cache[key]}'")
                print(f"  Depois: '{new_val}'")
                cache[key] = new_val
                updated += 1
        else:
            # If not in cache, add it anyway for the next translation run to pick it up
            print(f"Inserindo nova chave no cache: {key} -> '{new_val}'")
            cache[key] = new_val
            updated += 1
            
    if updated > 0:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f"\nSucesso: {updated} termos do glossário foram corrigidos no cache!")
    else:
        print("\nNenhuma correção necessária. Todos os termos já estão corretos.")

if __name__ == "__main__":
    main()
