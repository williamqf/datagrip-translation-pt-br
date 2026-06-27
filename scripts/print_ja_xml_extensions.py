import os
import zipfile

JA_JAR = r"C:\Program Files\JetBrains\DataGrip 2026.1.3\plugins\localization-ja\lib\localization-ja.jar"

def print_extensions():
    if not os.path.exists(JA_JAR):
        print("Localization JA JAR not found.")
        return
    with zipfile.ZipFile(JA_JAR, 'r') as jar:
        xml_content = jar.read("META-INF/plugin.xml").decode('utf-8')
        import re
        extensions = re.findall(r'<extensions.*?>.*?</extensions>', xml_content, re.DOTALL)
        print("Extensions no JAR japonês:")
        for ext in extensions:
            clean_ext = "".join([c if ord(c) < 128 else '?' for c in ext])
            print(clean_ext)

if __name__ == "__main__":
    print_extensions()
