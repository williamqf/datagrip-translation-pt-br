import zipfile
import os

ZIP_PATH = r"C:\dev\projetos\datagrip\anexo\ij-language-pack-pt-2026.1.1.zip"

def main():
    if not os.path.exists(ZIP_PATH):
        print(f"Error: ZIP not found at {ZIP_PATH}")
        return

    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_file:
        files = zip_file.namelist()
        icons = [f for f in files if 'pluginicon' in f.lower()]
        print(f"Found icons in ZIP:")
        for f in icons:
            print(f"  - {f}")
        print("\nFirst 10 files in ZIP:")
        for f in files[:10]:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
