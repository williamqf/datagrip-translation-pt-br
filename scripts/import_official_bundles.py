import os
import zipfile
import shutil

JAR_PATH = r"C:\dev\projetos\datagrip\anexo\extracted\ij-language-pack-pt\lib\ij-language-pack-pt-2026.1.1.jar"
RESOURCES_DIR = r"c:\dev\projetos\datagrip\plugin\src\main\resources"

def clean_zip_path(path):
    # Normalize zip paths to use forward slashes
    return path.replace('\\', '/')

def main():
    if not os.path.exists(JAR_PATH):
        print(f"Error: JAR not found at {JAR_PATH}")
        return

    # Check if target messages directory exists
    target_messages_dir = os.path.join(RESOURCES_DIR, "messages")
    
    # We will count files and categorize them
    copied_count = 0
    skipped_count = 0
    breakdown = {}

    print(f"Reading official JAR: {JAR_PATH}")
    with zipfile.ZipFile(JAR_PATH, 'r') as jar:
        for zip_info in jar.infolist():
            # Skip directories
            if zip_info.is_dir():
                continue

            path = clean_zip_path(zip_info.filename)
            parts = path.split('/')

            # Filter 1: Exclude files in "ai/" folder
            if parts[0] == 'ai':
                skipped_count += 1
                continue

            # Filter 2: Exclude files in "localization/" folder
            if parts[0] == 'localization':
                skipped_count += 1
                continue

            # Filter 3: Exclude files in "META-INF/" folder
            if parts[0] == 'META-INF':
                skipped_count += 1
                continue

            # Filter 4: Exclude any ".class" files
            if path.endswith('.class'):
                skipped_count += 1
                continue

            # Filter 5: Exclude "README.md"
            if parts[-1].lower() == 'readme.md':
                skipped_count += 1
                continue

            # Filter 6: Exclude files in "messages/" that already exist in our messages/ directory
            if parts[0] == 'messages':
                dest_file_path = os.path.join(target_messages_dir, '/'.join(parts[1:]))
                if os.path.exists(dest_file_path):
                    skipped_count += 1
                    continue

            # Check if there are other language files included in the copy list
            # Usually, other language files would have suffixes like _ja, _zh_CN, _zh, _ko, etc.
            is_non_portuguese = False
            for suffix in ['_ja.properties', '_zh_CN.properties', '_zh.properties', '_ko.properties', '_de.properties', '_fr.properties']:
                if path.endswith(suffix):
                    is_non_portuguese = True
                    break
            
            if is_non_portuguese:
                print(f"Skipping non-Portuguese file: {path}")
                skipped_count += 1
                continue

            # Copy/extract the file
            target_path = os.path.join(RESOURCES_DIR, *parts)
            target_parent = os.path.dirname(target_path)
            if not os.path.exists(target_parent):
                os.makedirs(target_parent, exist_ok=True)

            with jar.open(zip_info) as source, open(target_path, 'wb') as dest:
                shutil.copyfileobj(source, dest)

            copied_count += 1
            
            # Determine directory breakdown category
            category = parts[0]
            if len(parts) > 1 and parts[0] in ['com', 'org', 'net', 'gov']:
                # For package structures like com/android/..., let's aggregate under com/ or similar
                category = parts[0] + '/'
            
            breakdown[category] = breakdown.get(category, 0) + 1

    print("\nExtraction Summary:")
    print(f"Total files copied: {copied_count}")
    print(f"Total files skipped: {skipped_count}")
    print("\nDirectory breakdown of copied files:")
    for cat, count in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat}: {count} files")

if __name__ == '__main__':
    main()
