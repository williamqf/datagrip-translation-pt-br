import os
import sys
import json
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENGLISH_DIR = os.path.join(BASE_DIR, "temp_english_properties")
CACHE_FILE = os.path.join(BASE_DIR, "translation_cache.json")
REPORT_PATH = os.path.join(BASE_DIR, "build", "distributions", "prune_cache_report.json")

# Ensure build/distributions exists
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

# Whitelist of terms that are legitimately identical in English and pt-BR
LEGITIMATE_IDENTICAL_WORDS = {
    # Acronyms & technical terms
    "sql", "json", "xml", "html", "csv", "url", "uri", "uuid", "ip", "tcp", "ssh", "vm", "tls", "ssl", "jdbc", "nosql",
    "ddl", "dml", "jvm", "jre", "jdk", "api", "os", "ide", "lob", "clob", "blob", "db", "dbms", "na", "nan", "tsv", "xlsx",
    "utc", "ui", "ascii", "hex", "utf8", "utf", "kms", "ram", "mb", "gb", "tb", "ssh", "ssl", "tls", "crl", "pkcs12", "x509",
    "pkcs", "oid", "oids", "bidi", "ltr", "rtl", "cte", "ctes", "rls", "fk", "pk",
    # Brand/product names & Cloud tools
    "datagrip", "jetbrains", "intellij", "gradle", "kotlin", "java", "oracle", "mysql", "redis", "postgres", "postgresql",
    "mariadb", "sqlite", "cassandra", "mongodb", "redshift", "bigquery", "snowflake", "clickhouse", "h2", "derby", "db2",
    "sybase", "exasol", "teradata", "hive", "presto", "trino", "vertica", "hsqldb", "informix", "firebird", "greenplum",
    "aws", "azure", "gcp", "git", "github", "docker", "kubernetes", "couchbase", "dynamodb", "cockroach", "duckdb", 
    "hana", "spanner", "tidb",
    # SQL Keywords (only if they are raw syntax)
    "select", "insert", "update", "delete", "drop", "alter", "create", "join", "where", "from", "into", "values", "set",
    "commit", "rollback", "null", "true", "false", "default", "with", "union", "intersect", "except", "grant", "revoke",
    # Technical UI terms that remain identical in pt-BR
    "menu", "console", "editor", "plugin", "plugins", "terminal", "total", "host", "hosts", "online", "offline",
    "tablespace", "tablespaces", "warehouse", "regex",
    # Short symbols/words
    "ok", "id", "up", "to", "in", "on", "as", "by", "n", "t", "r"
}

def parse_properties(filepath):
    properties = {}
    if not os.path.exists(filepath):
        return properties
        
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        
        if not stripped or stripped.startswith('#') or stripped.startswith('!'):
            i += 1
            continue
            
        raw_lines = [line]
        current_line = line
        while current_line.rstrip().endswith('\\') and i + 1 < n:
            i += 1
            current_line = lines[i]
            raw_lines.append(current_line)
            
        combined = ""
        for rl in raw_lines:
            l_strip = rl.strip()
            if l_strip.endswith('\\'):
                l_strip = l_strip[:-1].rstrip()
            combined += l_strip
            
        match = re.search(r'(?<!\\)[=:]', combined)
        if match:
            sep_idx = match.start()
            key = combined[:sep_idx].strip()
            val = combined[sep_idx+1:].strip()
            key = key.replace('\\=', '=').replace('\\:', ':')
            properties[key] = val
        i += 1
    return properties

def is_legitimately_identical(value):
    # Strip formatting and punctuation
    cleaned = value.strip().lower()
    
    # Handle pure numbers or punctuation
    word_only = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    words = word_only.split()
    
    if not words:
        return True # Just numbers, symbols, or empty
        
    for w in words:
        # Check if the word is numeric or in our whitelist
        if w.isdigit():
            continue
        if w in LEGITIMATE_IDENTICAL_WORDS:
            continue
        # If any word is not in the whitelist and is >= 3 chars, it's not legitimately identical
        if len(w) >= 3:
            return False
            
    return True

def main():
    dry_run = "--commit" not in sys.argv
    print(f"=== SCRIPT DE LIMPEZA DE CACHE (PRUNING) ===")
    print(f"Modo: {'DRY RUN (Simulação - nenhuma alteração será salva)' if dry_run else 'COMMIT (O cache será atualizado!)'}")
    
    if not os.path.exists(CACHE_FILE):
        print("Erro: Cache de tradução não encontrado.")
        sys.exit(1)
        
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
        
    eng_files = sorted([f for f in os.listdir(ENGLISH_DIR) if f.endswith(".properties")])
    
    # Gather all original properties
    original_properties = {}
    for filename in eng_files:
        eng_path = os.path.join(ENGLISH_DIR, filename)
        props = parse_properties(eng_path)
        original_properties.update(props)
        
    to_prune = []
    to_keep = []
    obsolete = []
    
    for key, cached_val in cache.items():
        if key not in original_properties:
            obsolete.append(key)
            continue
            
        eng_val = original_properties[key]
        
        if cached_val == eng_val:
            if not is_legitimately_identical(eng_val):
                to_prune.append({
                    "key": key,
                    "original": eng_val,
                    "cached": cached_val
                })
            else:
                to_keep.append({
                    "key": key,
                    "val": cached_val,
                    "reason": "Legitimamente idêntico (termo técnico/símbolo)"
                })
        else:
            # Different value, keep it in cache
            to_keep.append({
                "key": key,
                "val": cached_val,
                "reason": "Traduzido"
            })
            
    print(f"\nEstatísticas da análise:")
    print(f"  Total de chaves no cache atualmente: {len(cache)}")
    print(f"  Chaves obsoletas (removidas da IDE original): {len(obsolete)}")
    print(f"  Chaves traduzidas ou legitimamente idênticas a manter: {len(to_keep)}")
    print(f"  Chaves em inglês para LIMPAR (pruning): {len(to_prune)}")
    
    # Report sample of pruned keys
    if to_prune:
        print("\nAmostra de chaves que serão limpas (primeiras 10):")
        for item in to_prune[:10]:
            print(f"  - {item['key']}: '{item['original']}'")
            
    # Save report JSON
    report = {
        "total_cache": len(cache),
        "obsolete_count": len(obsolete),
        "kept_count": len(to_keep),
        "pruned_count": len(to_prune),
        "obsolete": obsolete,
        "pruned": to_prune
    }
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
        
    print(f"\nRelatório de simulação salvo em: {REPORT_PATH}")
    
    if not dry_run:
        # Perform actual pruning
        new_cache = {}
        for item in to_keep:
            new_cache[item["key"]] = item["val"]
            
        with open(CACHE_FILE, 'w', encoding='utf-8') as cf:
            json.dump(new_cache, cf, ensure_ascii=False, indent=2)
        print("SUCESSO: O arquivo translation_cache.json foi atualizado!")
    else:
        print("\nPara aplicar as mudanças no cache, execute novamente com a flag '--commit'")

if __name__ == "__main__":
    main()
