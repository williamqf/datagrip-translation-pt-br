import zipfile
import os

JAR_PATH = r"C:\Users\hm007073\AppData\Roaming\JetBrains\DataGrip2026.1\plugins\ml-llm\lib\ml-llm.jar"

def main():
    if not os.path.exists(JAR_PATH):
        print(f"Error: JAR not found at {JAR_PATH}")
        return

    with zipfile.ZipFile(JAR_PATH, 'r') as jar:
        files = jar.namelist()
        icons = [f for f in files if 'pluginicon' in f.lower()]
        print(f"Found icons in {os.path.basename(JAR_PATH)}:")
        for f in icons:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
