import os
import zipfile

def parse_properties(content: str):
    properties = {}
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('!'):
            continue
        
        split_idx = -1
        for idx, char in enumerate(line):
            if char in ('=', ':'):
                bs_count = 0
                for c in reversed(line[:idx]):
                    if c == '\\':
                        bs_count += 1
                    else:
                        break
                if bs_count % 2 == 0:
                    split_idx = idx
                    break
        if split_idx != -1:
            key = line[:split_idx].strip()
            value = line[split_idx+1:].strip()
            properties[key] = value
        else:
            key = line.strip()
            properties[key] = ""
    return properties

def main():
    jar_path = r"C:\dev\projetos\datagrip\anexo\extracted\ij-language-pack-pt\lib\ij-language-pack-pt-2026.1.1.jar"
    plugin_dir = r"c:\dev\projetos\datagrip\plugin\src\main\resources\messages"
    
    if not os.path.exists(jar_path):
        print(f"Error: JAR file not found at {jar_path}")
        return
        
    if not os.path.exists(plugin_dir):
        print(f"Error: Plugin messages directory not found at {plugin_dir}")
        return

    # Find common bundles
    with zipfile.ZipFile(jar_path, 'r') as jar:
        jar_files = {os.path.basename(f): f for f in jar.namelist() if f.startswith('messages/') and f.endswith('.properties')}
        
    plugin_files = {f for f in os.listdir(plugin_dir) if f.endswith('.properties')}
    
    common_filenames = sorted(list(jar_files.keys() & plugin_files))
    
    print(f"Found {len(common_filenames)} common bundles to merge.")
    
    total_added = 0
    total_updated = 0
    total_preserved = 0
    bundles_merged = 0
    
    with zipfile.ZipFile(jar_path, 'r') as jar:
        for filename in common_filenames:
            jar_zip_path = jar_files[filename]
            plugin_file_path = os.path.join(plugin_dir, filename)
            
            # Read official properties
            official_content = jar.read(jar_zip_path).decode('utf-8')
            official_props = parse_properties(official_content)
            
            # Read plugin properties
            with open(plugin_file_path, 'r', encoding='utf-8') as f:
                plugin_content = f.read()
            plugin_props = parse_properties(plugin_content)
            
            # Statistics calculation
            plugin_keys = set(plugin_props.keys())
            official_keys = set(official_props.keys())
            
            added_keys = official_keys - plugin_keys
            updated_keys = plugin_keys & official_keys
            preserved_keys = plugin_keys - official_keys
            
            total_added += len(added_keys)
            total_updated += len(updated_keys)
            total_preserved += len(preserved_keys)
            
            # Merge logic
            official_keys_to_add = set(official_keys)
            output_lines = []
            
            for line in plugin_content.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith('#') or stripped.startswith('!'):
                    output_lines.append(line)
                    continue
                
                split_idx = -1
                for idx, char in enumerate(line):
                    if char in ('=', ':'):
                        bs_count = 0
                        for c in reversed(line[:idx]):
                            if c == '\\':
                                bs_count += 1
                            else:
                                break
                        if bs_count % 2 == 0:
                            split_idx = idx
                            break
                
                if split_idx != -1:
                    key = line[:split_idx].strip()
                    key_part = line[:split_idx + 1]
                    
                    if key in official_props:
                        after_sep = line[split_idx+1:]
                        leading_ws_len = len(after_sep) - len(after_sep.lstrip())
                        leading_ws = after_sep[:leading_ws_len]
                        
                        output_lines.append(key_part + leading_ws + official_props[key])
                        if key in official_keys_to_add:
                            official_keys_to_add.remove(key)
                    else:
                        output_lines.append(line)
                else:
                    key = line.strip()
                    if key in official_props:
                        output_lines.append(f"{key}={official_props[key]}")
                        if key in official_keys_to_add:
                            official_keys_to_add.remove(key)
                    else:
                        output_lines.append(line)
            
            # Append remaining official keys
            if official_keys_to_add:
                output_lines.append("")
                output_lines.append("# Keys added from official JAR")
                for key in sorted(official_keys_to_add):
                    output_lines.append(f"{key}={official_props[key]}")
            
            # Write back
            new_content = "\n".join(output_lines) + "\n"
            with open(plugin_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            bundles_merged += 1
            
    print("\n--- Merge Summary ---")
    print(f"Number of bundles merged: {bundles_merged}")
    print(f"Total keys added: {total_added}")
    print(f"Total keys updated: {total_updated}")
    print(f"Total keys preserved: {total_preserved}")

if __name__ == '__main__':
    main()
