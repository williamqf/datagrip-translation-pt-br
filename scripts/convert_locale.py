import os
import re

BASE_DIR = r"D:\dev\antigravity\datagrip"

# 1. Rename files in src/main/resources/messages/
messages_dir = os.path.join(BASE_DIR, "src", "main", "resources", "messages")
if os.path.exists(messages_dir):
    for filename in os.listdir(messages_dir):
        if filename.endswith("_pt_BR.properties"):
            old_path = os.path.join(messages_dir, filename)
            new_filename = filename.replace("_pt_BR.properties", "_pt.properties")
            new_path = os.path.join(messages_dir, new_filename)
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

# 2. Update plugin.xml
plugin_xml_path = os.path.join(BASE_DIR, "src", "main", "resources", "META-INF", "plugin.xml")
if os.path.exists(plugin_xml_path):
    with open(plugin_xml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace locale="pt_BR" with locale="pt"
    content = content.replace('locale="pt_BR"', 'locale="pt"')
    # Also update version to 2.1.0
    content = re.sub(r'<version>.*?</version>', '<version>2.1.0</version>', content)
    with open(plugin_xml_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated plugin.xml")

# 3. Update gradle.properties
gradle_properties_path = os.path.join(BASE_DIR, "gradle.properties")
if os.path.exists(gradle_properties_path):
    with open(gradle_properties_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'pluginVersion = .*', 'pluginVersion = 2.1.0', content)
    with open(gradle_properties_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated gradle.properties")

# 4. Update scripts/translate_bundles.py
translate_script = os.path.join(BASE_DIR, "scripts", "translate_bundles.py")
if os.path.exists(translate_script):
    with open(translate_script, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('_pt_BR', '_pt')
    with open(translate_script, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated translate_bundles.py")

# 5. Update scripts/write_translated_files.py
write_script = os.path.join(BASE_DIR, "scripts", "write_translated_files.py")
if os.path.exists(write_script):
    with open(write_script, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('_pt_BR', '_pt')
    with open(write_script, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated write_translated_files.py")

# 6. Update scripts/validate_translation.py
validate_script = os.path.join(BASE_DIR, "scripts", "validate_translation.py")
if os.path.exists(validate_script):
    with open(validate_script, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('_pt_BR', '_pt')
    with open(validate_script, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated validate_translation.py")

print("Conversion to 'pt' locale completed successfully!")
