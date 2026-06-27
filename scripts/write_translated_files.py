import os
import json
import re

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
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
print(f"Cache carregado: {len(cache)} traduções disponíveis.")

def parse_properties(filepath):
    entries = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        
        if not stripped or stripped.startswith('#') or stripped.startswith('!'):
            entries.append({'type': 'comment', 'raw': [line]})
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
            entries.append({
                'type': 'property',
                'key': key,
                'val': val,
                'raw': raw_lines
            })
        else:
            entries.append({'type': 'comment', 'raw': raw_lines})
            
        i += 1
    return entries

def generate_pt_br_files():
    if not os.path.exists(ENGLISH_DIR):
        print("Diretório original não encontrado.")
        return
        
    for filename in os.listdir(ENGLISH_DIR):
        if not filename.endswith(".properties"):
            continue
            
        english_path = os.path.join(ENGLISH_DIR, filename)
        name_without_ext, ext = os.path.splitext(filename)
        portuguese_path = os.path.join(OUTPUT_DIR, f"{name_without_ext}_pt{ext}")
        
        entries = parse_properties(english_path)
        
        translated_count = 0
        total_properties = 0
        
        with open(portuguese_path, 'w', encoding='utf-8') as out_f:
            for entry in entries:
                if entry['type'] == 'comment':
                    out_f.write("".join(entry['raw']))
                elif entry['type'] == 'property':
                    total_properties += 1
                    key = entry['key']
                    orig_val = entry['val']
                    
                    val_to_write = cache.get(key, orig_val)
                    if not val_to_write:
                        val_to_write = orig_val
                        
                    # Fix cross-bundle key collisions
                    if key == "action.separator":
                        if filename == "ActionsBundle.properties":
                            val_to_write = "Separador"
                        elif filename == "IdeBundle.properties":
                            val_to_write = "Separador ({0})"
                            
                    out_f.write(f"{key}={val_to_write}\n")
                    if key in cache and cache[key]:
                        translated_count += 1
                        
        print(f"Gerado: {os.path.basename(portuguese_path)} ({translated_count}/{total_properties} chaves traduzidas)")

if __name__ == "__main__":
    generate_pt_br_files()
