import os
import zipfile
import re

DATAGRIP_DIR = r"C:\Program Files\JetBrains\DataGrip 2026.1.3"

# Key strings we want to find in properties files
TARGET_STRINGS = [
    "Appearance & Behavior",
    "Appearance \\& Behavior",
    "Appearance \\& Behaviour",
    "Keymap",
    "Version Control",
    "Tools",
    "Backup and Sync",
    "Backup \\& Sync",
    "Advanced Settings",
    "Build Tools",
    "AI Assistant",
    "Coverage",
    "Debugger",
    "Diagrams",
    "Diff & Merge",
    "Diff \\& Merge",
    "External Tools",
    "SSH Configurations",
    "Terminal",
    "XPath Viewer"
]

def search_in_properties(content_str):
    found = []
    for target in TARGET_STRINGS:
        # Match target as complete value after '=' or ':'
        # or as part of settings group name
        pattern = r'(^|[\n\r])[^#!\n\r]*?=\s*.*?' + re.escape(target) + r'.*?([\n\r]|$)'
        matches = re.findall(pattern, content_str, re.IGNORECASE)
        if matches:
            found.append(target)
    return found

def find_bundles():
    print("Iniciando pente fino nos Jars do DataGrip...")
    results = {}
    
    for root, dirs, files in os.walk(DATAGRIP_DIR):
        for file in files:
            if file.endswith(".jar"):
                jar_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(jar_path, 'r') as jar:
                        for name in jar.namelist():
                            if name.startswith("messages/") and name.endswith(".properties") and not name.endswith("_pt.properties") and not name.endswith("_pt_BR.properties"):
                                content = jar.read(name).decode('utf-8', errors='replace')
                                found = search_in_properties(content)
                                if found:
                                    rel_jar = os.path.relpath(jar_path, DATAGRIP_DIR)
                                    if name not in results:
                                        results[name] = []
                                    results[name].append({
                                        'jar': rel_jar,
                                        'targets': found
                                    })
                except Exception:
                    pass
                    
    print("\n--- RESULTADOS DO PENTE FINO ---")
    for prop_name, occurrences in sorted(results.items()):
        print(f"\nArquivo de Recursos: {prop_name}")
        for occ in occurrences:
            print(f"  Localizado em: JAR '{occ['jar']}'")
            print(f"  Termos encontrados: {list(set(occ['targets']))}")

if __name__ == "__main__":
    find_bundles()
