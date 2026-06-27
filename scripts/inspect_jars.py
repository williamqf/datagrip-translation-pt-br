import os
import zipfile

DATAGRIP_DIR = r"C:\Program Files\JetBrains\DataGrip 2026.1.3"

def scan_jars():
    print(f"Buscando arquivos .properties em {DATAGRIP_DIR}...\n")
    
    # We will search in lib and plugins directories
    for root, dirs, files in os.walk(DATAGRIP_DIR):
        for file in files:
            if file.endswith(".jar"):
                jar_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(jar_path, 'r') as jar:
                        properties_files = [
                            name for name in jar.namelist() 
                            if name.startswith("messages/") and name.endswith(".properties")
                        ]
                        if properties_files:
                            rel_path = os.path.relpath(jar_path, DATAGRIP_DIR)
                            print(f"JAR: {rel_path}")
                            for prop in properties_files:
                                print(f"  - {prop}")
                except Exception:
                    # Ignore unreadable/corrupted jars
                    pass

if __name__ == "__main__":
    scan_jars()
