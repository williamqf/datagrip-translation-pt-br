import os
import sys
import json
import time
import re
import google.generativeai as genai

# Setup API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith("GEMINI_API_KEY="):
                        GEMINI_API_KEY = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                        break
        except Exception as e:
            print(f"Aviso: Erro ao ler .env: {e}")

if not GEMINI_API_KEY:
    print("ERRO: A variável de ambiente GEMINI_API_KEY não está configurada e nenhum arquivo .env foi encontrado.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Directory configurations
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENGLISH_DIR = os.path.join(BASE_DIR, "temp_english_properties")
OUTPUT_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "messages")
CACHE_FILE = os.path.join(BASE_DIR, "translation_cache.json")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load cache
cache = {}
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        print(f"Cache carregado: {len(cache)} traduções existentes.")
    except Exception as e:
        print(f"Erro ao ler cache: {e}. Iniciando cache vazio.")

def save_cache():
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar cache: {e}")

def parse_properties(filepath):
    """
    Parses a Java .properties file.
    Returns: list of dicts with:
      - 'type': 'comment' or 'property'
      - 'key': string (if property)
      - 'val': string (if property, with multiline combined)
      - 'raw': list of raw lines from the file
    """
    entries = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        
        # Comment or empty line
        if not stripped or stripped.startswith('#') or stripped.startswith('!'):
            entries.append({'type': 'comment', 'raw': [line]})
            i += 1
            continue
            
        # Multiline property collector
        raw_lines = [line]
        current_line = line
        while current_line.rstrip().endswith('\\') and i + 1 < n:
            i += 1
            current_line = lines[i]
            raw_lines.append(current_line)
            
        # Combine lines for parsing
        combined = ""
        for rl in raw_lines:
            # strip leading/trailing whitespace and remove backslash continuation if not the last line
            l_strip = rl.strip()
            if l_strip.endswith('\\'):
                l_strip = l_strip[:-1].rstrip()
            combined += l_strip
            
        # Parse key and value
        # Key is everything up to the first unescaped '=' or ':'
        # For simplicity, search for first '=' or ':' that is not preceded by a backslash
        match = re.search(r'(?<!\\)[=:]', combined)
        if match:
            sep_idx = match.start()
            key = combined[:sep_idx].strip()
            val = combined[sep_idx+1:].strip()
            
            # Clean key escape chars if any
            key = key.replace('\\=', '=').replace('\\:', ':')
            entries.append({
                'type': 'property',
                'key': key,
                'val': val,
                'raw': raw_lines
            })
        else:
            # Fallback if no separator found
            entries.append({'type': 'comment', 'raw': raw_lines})
            
        i += 1
        
    return entries

def translate_batch(batch):
    """
    Translates a list of (key, value) pairs.
    """
    prompt = """Você é um tradutor especialista em localização de IDEs JetBrains (DataGrip).
Traduza os seguintes pares de chave-valor de arquivo .properties Java do Inglês para o Português do Brasil (pt-BR).

REGRAS CRÍTICAS:
1. Preserve todos os placeholders exatamente como estão: ex: {0}, {1}, %s, %d, %1$s, etc.
2. Preserve todas as sequências de escape exatamente como estão: ex: \\n, \\t, \\", \\', \\\\, etc. (se no original for \\n, mantenha \\n).
3. Mantenha os termos técnicos de banco de dados em português consagrado de TI:
   - "Table" -> "Tabela"
   - "Query" -> "Consulta" (ou "Query" se for o objeto console)
   - "Schema" -> "Esquema"
   - "Data Source" -> "Fonte de Dados"
   - "Foreign Key" -> "Chave Estrangeira"
   - "Primary Key" -> "Chave Primária"
   - "Console" -> "Console"
   - Não traduza SQL, JDBC, XML, JSON, DDL, DML, etc.
4. Responda APENAS no formato: chave=valor_traduzido. Não adicione nenhuma formatação markdown (como ```properties ou ```), tags HTML adicionais, ou texto explicativo. Apenas as linhas brutas de resultado.
5. Se o valor estiver vazio, mantenha vazio (ex: chave=).

Chave-Valores a traduzir:
"""
    for key, val in batch:
        prompt += f"{key}={val}\n"

    try:
        # Using gemini-flash-lite-latest to avoid low daily quota limits.
        model = genai.GenerativeModel("gemini-flash-lite-latest")
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean markdown wrappers if LLM disobeyed
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
            
        results = {}
        for line in text.splitlines():
            if '=' in line:
                k, v = line.split('=', 1)
                results[k.strip()] = v.strip()
        return results
    except Exception as e:
        print(f"Erro na API do Gemini: {e}")
        return {}

def extract_placeholders(value):
    patterns = [
        r'\{[0-9]+\}',               # MessageFormat braces
        r'%[0-9]*\$?[a-zA-Z%]'        # Formatter percent syntax
    ]
    placeholders = []
    for pattern in patterns:
        placeholders.extend(re.findall(pattern, value))
    return sorted(placeholders)

def placeholders_and_escapes_match(eng_val, pt_val):
    if pt_val is None:
        return False
    # Check placeholders
    if extract_placeholders(eng_val) != extract_placeholders(pt_val):
        return False
    # Check critical escapes (\n, \t)
    eng_esc = sorted(re.findall(r'\\[nt]', eng_val))
    pt_esc = sorted(re.findall(r'\\[nt]', pt_val))
    if eng_esc != pt_esc:
        return False
    return True

def translate_file(filename):
    english_path = os.path.join(ENGLISH_DIR, filename)
    name_without_ext, ext = os.path.splitext(filename)
    portuguese_path = os.path.join(OUTPUT_DIR, f"{name_without_ext}{ext}")
    
    print(f"\nTraduzindo: {filename} -> {os.path.basename(portuguese_path)}")
    entries = parse_properties(english_path)
    
    # Identify properties to translate
    to_translate = []
    for entry in entries:
        if entry['type'] == 'property':
            key = entry['key']
            val = entry['val']
            
            # Lookup logic: check bundle-specific key first, then fallback to general key if signature matches
            bundle_key = f"{filename}:{key}"
            is_cached = False
            if bundle_key in cache:
                is_cached = True
            elif key in cache:
                cached_val = cache[key]
                if placeholders_and_escapes_match(val, cached_val):
                    is_cached = True
            
            # Only translate if not already cached and not empty
            if not is_cached and val:
                to_translate.append((key, val))
            elif not val:
                cache[bundle_key] = ""  # Empty values remain empty
                
    total_to_translate = len(to_translate)
    print(f"Total de chaves no arquivo: {len([e for e in entries if e['type'] == 'property'])}")
    print(f"Precisam de tradução (não cacheado): {total_to_translate}")
    
    # Process in batches of 120 keys
    batch_size = 120
    for idx in range(0, total_to_translate, batch_size):
        batch = to_translate[idx : idx + batch_size]
        print(f"  Traduzindo lote {idx//batch_size + 1} de {((total_to_translate - 1)//batch_size) + 1} ({len(batch)} chaves)...")
        
        # Retry logic
        retries = 3
        translated_batch = {}
        while retries > 0:
            translated_batch = translate_batch(batch)
            if translated_batch:
                break
            retries -= 1
            print("    Erro no lote. Aguardando 20s e tentando novamente...")
            time.sleep(20)
            
        # Update cache
        for key, orig_val in batch:
            if key in translated_batch:
                new_val = translated_batch[key]
                bundle_key = f"{filename}:{key}"
                cache[bundle_key] = new_val
                # Also save to flat key if it doesn't conflict, to help other files
                if key not in cache or placeholders_and_escapes_match(orig_val, cache[key]):
                    cache[key] = new_val
            else:
                print(f"    AVISO: Falha ao traduzir chave '{key}'. Não salva no cache para tentar novamente.")
                
        save_cache()
        # Rate limit safety sleep
        time.sleep(10)
        
    # Write output file
    print(f"Gravando arquivo traduzido: {portuguese_path}")
    with open(portuguese_path, 'w', encoding='utf-8') as out_f:
        for entry in entries:
            if entry['type'] == 'comment':
                out_f.write("".join(entry['raw']))
            elif entry['type'] == 'property':
                key = entry['key']
                val = entry['val']
                bundle_key = f"{filename}:{key}"
                
                # Retrieve translation
                if bundle_key in cache:
                    translated_val = cache[bundle_key]
                else:
                    translated_val = cache.get(key, val)
                
                # Escape key for '=', ':' to avoid breaking property format
                escaped_key = key.replace(':', '\\:').replace('=', '\\=')
                out_f.write(f"{escaped_key}={translated_val}\n")
                
    print(f"Tradução de {filename} concluída!")

def main():
    if not os.path.exists(ENGLISH_DIR):
        print(f"Erro: Pasta {ENGLISH_DIR} não encontrada. Execute extract_bundles.py primeiro.")
        sys.exit(1)
        
    files = [f for f in os.listdir(ENGLISH_DIR) if f.endswith(".properties")]
    # Sort by size to translate smaller files first
    files.sort(key=lambda x: os.path.getsize(os.path.join(ENGLISH_DIR, x)))
    if not files:
        print("Nenhum arquivo .properties encontrado para traduzir.")
        return
        
    print(f"Arquivos para tradução (ordenados por tamanho): {files}")
    for file in files:
        translate_file(file)
        
    print("\nProcesso de tradução completo para todos os arquivos!")

if __name__ == "__main__":
    main()
