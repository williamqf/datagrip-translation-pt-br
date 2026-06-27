import os
import zipfile

JA_JAR = r"C:\Program Files\JetBrains\DataGrip 2026.1.3\plugins\localization-ja\lib\localization-ja.jar"

def check_xml():
    if not os.path.exists(JA_JAR):
        print("Localization JA JAR not found.")
        return
    with zipfile.ZipFile(JA_JAR, 'r') as jar:
        try:
            xml_content = jar.read("META-INF/plugin.xml").decode('utf-8')
            # Print only ASCII characters
            clean_text = "".join([c if ord(c) < 128 else '?' for c in xml_content])
            print("plugin.xml do JAR japonês:")
            print(clean_text[:1200])
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    check_xml()
