import os
import re
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENGLISH_DIR = os.path.join(BASE_DIR, "temp_english_properties")
PT_BR_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "messages")
REPORT_PATH = os.path.join(BASE_DIR, "build", "distributions", "qa_translation_report.md")

# Ensure build/distributions exists
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

PROTECTED_SQL_KEYWORDS = [
    "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", 
    "JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "CROSS JOIN", 
    "WHERE", "FROM", "INTO", "VALUES", "SET", "GROUP BY", "ORDER BY", "HAVING", 
    "LIMIT", "OFFSET", "FETCH", "WITH", "UNION", "INTERSECT", "EXCEPT", 
    "COMMIT", "ROLLBACK", "TRUNCATE", "MERGE", "GRANT", "REVOKE", "EXPLAIN", 
    "PRIMARY KEY", "FOREIGN KEY", "REFERENCES", "CONSTRAINT", "INDEX", "VIEW", 
    "TABLE", "SCHEMA", "DATABASE", "NULL", "TRUE", "FALSE"
]

ALLOWED_HTML_TAGS = [
    'html', 'body', 'b', 'i', 'code', 'a', 'u', 'p', 'span', 'div', 'font', 
    'ul', 'li', 'ol', 'strong', 'table', 'tr', 'td', 'small', 'br', 'hr', 'em', 'h1', 'h2', 'h3'
]

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
        
        # Skip empty lines and comments
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

def extract_placeholders(value):
    patterns = [
        r'\{[0-9]+\}',               # MessageFormat braces
        r'%[0-9]*\$?[a-zA-Z%]'        # Formatter percent syntax
    ]
    placeholders = []
    for pattern in patterns:
        placeholders.extend(re.findall(pattern, value))
    return sorted(placeholders)

def clean_escaped_html(value):
    """
    MessageFormat uses '<' and '>' to escape html tags. Clean these out.
    Also handles row/column placeholders <row> which are not HTML.
    """
    # Remove escaped angle brackets: '<' -> < and '>' -> >
    cleaned = value.replace("'<'", "<").replace("'>'", ">")
    
    # Remove pseudo-tags like <row>, <column>, <duplicate> which are just text placeholders
    cleaned = re.sub(r'<(row|column|duplicate|regexp|t\.\*)>', r'\1', cleaned, flags=re.IGNORECASE)
    return cleaned

def check_html_tags(value):
    """
    Checks if HTML inline tags are balanced and valid.
    """
    issues = []
    cleaned_val = clean_escaped_html(value)
    
    # Find all HTML tags (e.g. <b>, </td>, <a href="...">)
    tags = re.findall(r'<[^>]+>', cleaned_val)
    
    open_tags = []
    for tag in tags:
        tag_content = tag[1:-1].strip()
        # Skip self-closing
        if tag_content.endswith('/') or tag_content.lower().startswith('br') or tag_content.lower().startswith('hr'):
            continue
            
        if tag_content.startswith('/'):
            closing_name = tag_content[1:].strip().split()[0].lower()
            if closing_name in ALLOWED_HTML_TAGS:
                if open_tags and open_tags[-1] == closing_name:
                    open_tags.pop()
                else:
                    issues.append(f"Tag de fechamento '{tag}' sem correspondência de abertura.")
        else:
            opening_name = tag_content.split()[0].lower()
            if opening_name not in ALLOWED_HTML_TAGS:
                # Might be a false positive (e.g. custom database tag <db1>), skip if not standard
                pass
            else:
                open_tags.append(opening_name)
                
    for remaining in open_tags:
        issues.append(f"Tag HTML de abertura '<{remaining}>' não foi fechada.")
        
    return issues

def check_sql_firewall(eng_val, pt_val):
    issues = []
    # Find all SQL keywords in English value
    words = re.findall(r'\b[A-Z_]{3,}\b', eng_val)
    
    for word in words:
        if word in PROTECTED_SQL_KEYWORDS:
            # Check if this keyword is translated
            if not re.search(r'\b' + re.escape(word) + r'\b', pt_val):
                # Common translated words check
                translated = False
                common_translations = {
                    "SELECT": ["SELECIONAR"],
                    "DROP": ["DESCARTAR", "REMOVER", "APAGAR"],
                    "COMMIT": ["CONFIRMAR"],
                    "ROLLBACK": ["REVERTER"],
                    "WHERE": ["ONDE"],
                    "JOIN": ["JUNTAR"],
                    "TABLE": ["TABELA"],
                    "SCHEMA": ["ESQUEMA"],
                    "DATABASE": ["BANCO DE DADOS"],
                    "NULL": ["NULO"],
                    "TRUE": ["VERDADEIRO"],
                    "FALSE": ["FALSO"],
                    "WITH": ["COM"]
                }
                pt_upper = pt_val.upper()
                if word in common_translations:
                    for trans in common_translations[word]:
                        if trans in pt_upper:
                            translated = True
                            break
                if translated:
                    issues.append(f"Palavra-chave SQL protegida '{word}' foi traduzida na interface.")
                else:
                    # If it's just missing, check if the whole sentence is translated differently
                    # For SQL keywords like WITH/FROM in UI texts, they might be translated to Portuguese if not syntax
                    # but if it matches a translation word, raise it
                    pass
    return issues

def main():
    if not os.path.exists(ENGLISH_DIR):
        print(f"Erro: Diretorio original {ENGLISH_DIR} nao existe.")
        return

    # Inventory
    eng_files = sorted([f for f in os.listdir(ENGLISH_DIR) if f.endswith(".properties")])
    
    inventory_data = []
    all_findings = []
    
    blocker_count = 0
    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0
    
    for filename in eng_files:
        eng_path = os.path.join(ENGLISH_DIR, filename)
        pt_filename = filename
        pt_path = os.path.join(PT_BR_DIR, pt_filename)
        
        eng_props = parse_properties(eng_path)
        pt_props = parse_properties(pt_path)
        
        missing_keys = []
        extra_keys = []
        status = "PASS"
        
        # Check key parity
        for key in eng_props:
            if key not in pt_props:
                missing_keys.append(key)
                
        for key in pt_props:
            if key not in eng_props:
                extra_keys.append(key)
                
        if missing_keys or extra_keys:
            status = "FAIL"
            
        inventory_data.append({
            'file': filename,
            'eng_keys': len(eng_props),
            'pt_keys': len(pt_props),
            'missing': len(missing_keys),
            'extra': len(extra_keys),
            'status': status
        })
        
        # Detail checks per key
        for key in eng_props:
            if key not in pt_props:
                all_findings.append({
                    'bundle': filename,
                    'key': key,
                    'type': 'MISSING_KEY',
                    'severity': 'CRITICAL',
                    'original': eng_props[key],
                    'translation': '',
                    'issue': 'Chave ausente no arquivo traduzido pt-BR.'
                })
                critical_count += 1
                continue
                
            eng_val = eng_props[key]
            pt_val = pt_props[key]
            
            # 1. Placeholders Parity
            eng_pl = extract_placeholders(eng_val)
            pt_pl = extract_placeholders(pt_val)
            if eng_pl != pt_pl:
                all_findings.append({
                    'bundle': filename,
                    'key': key,
                    'type': 'PLACEHOLDER_MISMATCH',
                    'severity': 'CRITICAL',
                    'original': eng_val,
                    'translation': pt_val,
                    'issue': f"Placeholders não coincidem. Original: {eng_pl} | Traduzido: {pt_pl}"
                })
                critical_count += 1
                
            # 2. Escape Parity (Checking critical formatting escapes like \n, \t)
            # Only count \n and \t to avoid flagging translated shortcut escapes like \&
            eng_esc_chars = re.findall(r'\\[nt]', eng_val)
            pt_esc_chars = re.findall(r'\\[nt]', pt_val)
            if sorted(eng_esc_chars) != sorted(pt_esc_chars):
                all_findings.append({
                    'bundle': filename,
                    'key': key,
                    'type': 'ESCAPE_MISMATCH',
                    'severity': 'CRITICAL',
                    'original': eng_val,
                    'translation': pt_val,
                    'issue': f"Sequências de escape críticas (\\n, \\t) não coincidem. Original: {sorted(eng_esc_chars)} | Traduzido: {sorted(pt_esc_chars)}"
                })
                critical_count += 1
                
            # 3. HTML integrity (Only report if original has balanced tags and pt-BR broke them)
            eng_html_issues = check_html_tags(eng_val)
            pt_html_issues = check_html_tags(pt_val)
            # If pt-BR has issues that were NOT present in original, report them
            new_html_issues = [x for x in pt_html_issues if x not in eng_html_issues]
            for issue in new_html_issues:
                all_findings.append({
                    'bundle': filename,
                    'key': key,
                    'type': 'HTML_INTEGRITY',
                    'severity': 'HIGH',
                    'original': eng_val,
                    'translation': pt_val,
                    'issue': issue
                })
                high_count += 1
                
            # 4. SQL Syntax Firewall
            sql_issues = check_sql_firewall(eng_val, pt_val)
            for issue in sql_issues:
                all_findings.append({
                    'bundle': filename,
                    'key': key,
                    'type': 'SQL_FIREWALL_VIOLATION',
                    'severity': 'CRITICAL',
                    'original': eng_val,
                    'translation': pt_val,
                    'issue': issue
                })
                critical_count += 1
                
            # 5. UI Length check
            if len(eng_val) > 0:
                ratio = len(pt_val) / len(eng_val)
                if ratio > 1.8 and len(pt_val) > 15:
                    all_findings.append({
                        'bundle': filename,
                        'key': key,
                        'type': 'LAYOUT_RISK',
                        'severity': 'MEDIUM',
                        'original': eng_val,
                        'translation': pt_val,
                        'issue': f"Texto pt-BR {ratio:.2f}x maior do que o original em inglês (potencial quebra de layout)."
                    })
                    medium_count += 1

    # Write report Markdown
    decision = "APPROVED_FOR_IDE_SMOKE_TEST"
    if blocker_count > 0 or critical_count > 0:
        decision = "NEEDS_FIX_BEFORE_IDE_TEST"
        
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("# DataGrip pt-BR Localization QA Report\n\n")
        f.write("## Scope\n")
        f.write("Auditoria estática programática dos arquivos de propriedades de tradução do DataGrip.\n\n")
        
        f.write("## Files Checked\n")
        f.write(f"Diretório Original: `{ENGLISH_DIR}`\n")
        f.write(f"Diretório Traduzido: `{PT_BR_DIR}`\n\n")
        
        f.write("## Summary\n")
        f.write(f"- **Blockers**: {blocker_count}\n")
        f.write(f"- **Critical Issues**: {critical_count}\n")
        f.write(f"- **High Issues**: {high_count}\n")
        f.write(f"- **Medium Issues**: {medium_count}\n")
        f.write(f"- **Low Issues**: {low_count}\n\n")
        f.write(f"### Decisão Recomendada: **`{decision}`**\n\n")
        
        f.write("## Localization QA Inventory\n\n")
        f.write("| Bundle | Original Keys | pt-BR Keys | Missing | Extra | Status |\n")
        f.write("|---|---:|---:|---:|---:|---|\n")
        for item in inventory_data:
            f.write(f"| {item['file']} | {item['eng_keys']} | {item['pt_keys']} | {item['missing']} | {item['extra']} | {item['status']} |\n")
        f.write("\n")
        
        # Details of failures
        f.write("## Blockers\n\n")
        blockers = [x for x in all_findings if x['severity'] == 'BLOCKER']
        if blockers:
            for b in blockers:
                f.write(f"### `{b['bundle']}` - `{b['key']}`\n")
                f.write(f"- **Tipo**: {b['type']}\n")
                f.write(f"- **Original**: `{b['original']}`\n")
                f.write(f"- **Tradução**: `{b['translation']}`\n")
                f.write(f"- **Problema**: {b['issue']}\n\n")
        else:
            f.write("Nenhum blocker encontrado.\n\n")
            
        f.write("## Critical Issues\n\n")
        criticals = [x for x in all_findings if x['severity'] == 'CRITICAL']
        if criticals:
            for c in criticals:
                f.write(f"### `{c['bundle']}` - `{c['key']}`\n")
                f.write(f"- **Tipo**: {c['type']}\n")
                f.write(f"- **Original**: `{c['original']}`\n")
                f.write(f"- **Tradução**: `{c['translation']}`\n")
                f.write(f"- **Problema**: {c['issue']}\n\n")
        else:
            f.write("Nenhuma issue crítica encontrada.\n\n")
            
        f.write("## High Issues (HTML/Tooltip Integrity)\n\n")
        highs = [x for x in all_findings if x['severity'] == 'HIGH']
        if highs:
            for h in highs:
                f.write(f"### `{h['bundle']}` - `{h['key']}`\n")
                f.write(f"- **Original**: `{h['original']}`\n")
                f.write(f"- **Tradução**: `{h['translation']}`\n")
                f.write(f"- **Problema**: {h['issue']}\n\n")
        else:
            f.write("Nenhuma issue de gravidade Alta encontrada.\n\n")
            
        f.write("## Medium Issues (Layout & Style)\n\n")
        mediums = [x for x in all_findings if x['severity'] == 'MEDIUM']
        if mediums:
            for m in mediums:
                f.write(f"### `{m['bundle']}` - `{m['key']}`\n")
                f.write(f"- **Original**: `{m['original']}`\n")
                f.write(f"- **Tradução**: `{m['translation']}`\n")
                f.write(f"- **Problema**: {m['issue']}\n\n")
        else:
            f.write("Nenhuma issue de gravidade Média encontrada.\n\n")
            
        f.write("## Decision\n")
        f.write(f"Recomendação de aprovação: **`{decision}`**\n\n")
        
        f.write("## Next Actions\n")
        if decision == "NEEDS_FIX_BEFORE_IDE_TEST":
            f.write("1. Corrigir as inconsistências críticas listadas acima.\n")
            f.write("2. Rodar o script de QA novamente.\n")
        else:
            f.write("1. Instalar o plugin ZIP e prosseguir com o Smoke Test em tempo de execução.\n")

    print(f"Auditoria concluida com sucesso!")
    print(f"Relatorio salvo em: {REPORT_PATH}")
    print(f"Resultados: Blockers={blocker_count}, Critical={critical_count}, High={high_count}, Medium={medium_count}")

if __name__ == "__main__":
    main()
