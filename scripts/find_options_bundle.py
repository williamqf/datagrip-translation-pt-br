import os
import zipfile

DATAGRIP_DIR = r"C:\Program Files\JetBrains\DataGrip 2026.1.3"

BUNDLES_TO_FIND = [
    "messages/OptionsBundle.properties",
    "messages/ToolsBundle.properties",
    "messages/VcsBundle.properties",
    "messages/TerminalBundle.properties",
    "messages/XPathBundle.properties",
    "messages/UIBundle.properties",
    "messages/XDebuggerBundle.properties",
    "messages/XDebuggerImplBundle.properties",
    "messages/XDebuggerUiBundle.properties"
]

def find_jars():
    print("Mapeando JARs que contêm os bundles que precisamos:")
    found_map = {}
    
    for root, dirs, files in os.walk(DATAGRIP_DIR):
        for file in files:
            if file.endswith(".jar"):
                jar_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(jar_path, 'r') as jar:
                        for name in jar.namelist():
                            if name in BUNDLES_TO_FIND:
                                rel_jar = os.path.relpath(jar_path, DATAGRIP_DIR)
                                if name not in found_map:
                                    found_map[name] = []
                                found_map[name].append(rel_jar)
                except Exception:
                    pass
                    
    for bundle, jars in sorted(found_map.items()):
        print(f"\nBundle: {bundle}")
        for jar in jars:
            print(f"  - No JAR: {jar}")

if __name__ == "__main__":
    find_jars()
