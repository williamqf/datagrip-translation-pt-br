import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CACHE_FILE = os.path.join(BASE_DIR, "translation_cache.json")

def main():
    if not os.path.exists(CACHE_FILE):
        print("Erro: Cache file não encontrado.")
        return
        
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
        
    cache["unwrap.with"] = "Desembrulhar WITH"
    cache["action.separator"] = "Separador ({0})"
    
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
        
    print("Sucesso: Chaves críticas corrigidas no cache!")

if __name__ == "__main__":
    main()
