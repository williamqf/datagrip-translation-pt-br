import os
import zipfile

JA_JAR = r"C:\Program Files\JetBrains\DataGrip 2026.1.3\plugins\localization-ja\lib\localization-ja.jar"

def check_jar():
    if not os.path.exists(JA_JAR):
        print("Localization JA JAR not found.")
        return
    with zipfile.ZipFile(JA_JAR, 'r') as jar:
        names = sorted([name for name in jar.namelist() if name.endswith(".properties")])
        print("Arquivos no JAR japonês (primeiros 20):")
        for name in names[:20]:
            print(f"  - {name}")

if __name__ == "__main__":
    check_jar()
