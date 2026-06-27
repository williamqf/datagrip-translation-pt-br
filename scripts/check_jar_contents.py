import os
import zipfile

JAR_PATH = r"c:\dev\projetos\datagrip\plugin\build\libs\datagrip-translation-pt-br-3.1.0.jar"

def check_jar():
    if not os.path.exists(JAR_PATH):
        print("JAR not found.")
        return
    with zipfile.ZipFile(JAR_PATH, 'r') as jar:
        files = sorted(jar.namelist())
        print(f"Arquivos no JAR ({len(files)} arquivos):")
        for f in files:
            if f.startswith("messages/"):
                print(f"  - {f}")

if __name__ == "__main__":
    check_jar()
