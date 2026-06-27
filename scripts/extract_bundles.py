import os
import zipfile
import shutil

# Paths configuration
DATAGRIP_DIR = r"C:\Program Files\JetBrains\DataGrip 2026.1.3"
TEMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp_english_properties"))

# Bundles to extract mapping: { jar_relative_path: [files_to_extract] }
BUNDLES_TO_EXTRACT = {
    os.path.join("lib", "product.jar"): [
        "messages/DataGripBundle.properties",
        "messages/SshBundle.properties",
        "messages/UltimateFeaturesBundle.properties",
        "messages/LspBundle.properties",
        "messages/CommercialBundle.properties",
        "messages/LicenseBundle.properties"
    ],
    os.path.join("plugins", "DatabaseTools", "lib", "database-plugin.jar"): [
        "messages/DatabaseBundle.properties",
        "messages/DatabaseDynamicBundle.properties"
    ],
    os.path.join("plugins", "DatabaseTools", "lib", "modules", "intellij.database.sql.jar"): [
        "messages/SqlBundle.properties"
    ],
    os.path.join("lib", "intellij.grid.core.impl.jar"): [
        "messages/DataGridBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.ide.impl.jar"): [
        "messages/ActionsBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.ide.jar"): [
        "messages/IdeBundle.properties",
        "messages/UIBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.ide.core.jar"): [
        "messages/OptionsBundle.properties",
        "messages/ApplicationBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.lang.impl.jar"): [
        "messages/ToolsBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.vcs.core.jar"): [
        "messages/VcsBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.debugger.jar"): [
        "messages/XDebuggerBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.debugger.impl.jar"): [
        "messages/XDebuggerImplBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.debugger.impl.ui.jar"): [
        "messages/XDebuggerUiBundle.properties"
    ],
    os.path.join("plugins", "terminal", "lib", "terminal.jar"): [
        "messages/TerminalBundle.properties"
    ],
    os.path.join("plugins", "xpath", "lib", "xpath.jar"): [
        "messages/XPathBundle.properties"
    ],
    # ---- Novos bundles v3.3.0 ----
    os.path.join("lib", "intellij.platform.externalSystem.jar"): [
        "messages/ExternalSystemBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.diff.jar"): [
        "messages/DiffBundle.properties"
    ],
    os.path.join("lib", "intellij.settingsSync.core.jar"): [
        "messages/SettingsSyncBundle.properties"
    ],
    os.path.join("plugins", "settingsSync", "lib", "settingsSync.jar"): [
        "messages/SettingsSyncJbaBundle.properties"
    ],
    os.path.join("plugins", "mcpserver", "lib", "mcpserver.jar"): [
        "messages/McpServerBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.coverage.jar"): [
        "messages/CoverageBundle.properties"
    ],
    os.path.join("plugins", "uml", "lib", "uml-support.jar"): [
        "messages/DiagramBundle.properties"
    ],
    # ---- Novos bundles v3.4.0 (Pente Fino Final) ----
    os.path.join("lib", "intellij.platform.credentialStore.impl.jar"): [
        "messages/CredentialStoreBundle.properties"
    ],
    os.path.join("lib", "intellij.platform.lang.jar"): [
        "messages/CodeInsightBundle.properties"
    ],
    os.path.join("plugins", "fullLine", "lib", "fullLine.jar"): [
        "messages/MLInlineCompletionBundle.properties"
    ],
    os.path.join("plugins", "markdown", "lib", "markdown.jar"): [
        "messages/MarkdownImagesBundle.properties",
        "messages/MarkdownBundle.properties"
    ],
    os.path.join("plugins", "grazie", "lib", "grazie.jar"): [
        "messages/GrazieBundle.properties"
    ],
    # User plugins (AI Assistant)
    os.path.join(os.environ.get("APPDATA", r"C:\Users\hm007073\AppData\Roaming"), "JetBrains", "DataGrip2026.1", "plugins", "ml-llm", "lib", "ml-llm.jar"): [
        "messages/*.properties"
    ],
    # ---- Novos bundles v3.5.0 (Git, JSON, XML, Sistema) ----
    os.path.join("plugins", "vcs-git", "lib", "vcs-git.jar"): [
        "messages/*.properties"
    ],
    os.path.join("plugins", "vcs-git-commit-modal", "lib", "vcs-git-commit-modal.jar"): [
        "messages/ModalCommitBundle.properties"
    ],
    os.path.join("plugins", "json", "lib", "json.jar"): [
        "messages/JsonBundle.properties",
        "messages/JsonPathBundle.properties"
    ],
    os.path.join("lib", "intellij.xml.impl.jar"): [
        "messages/XmlBundle.properties"
    ],
    os.path.join("plugins", "platform-images", "lib", "platform-images.jar"): [
        "messages/ImagesBundle.properties"
    ],
    os.path.join("plugins", "searchEverywhereMl", "lib", "searchEverywhereMl.jar"): [
        "messages/searchEverywhereMlCoreBundle.properties"
    ]
}

def extract_bundles():
    print(f"Iniciando extração de chaves a partir de: {DATAGRIP_DIR}")
    print(f"Pasta temporária de destino: {TEMP_DIR}")
    
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    for jar_rel_path, files in BUNDLES_TO_EXTRACT.items():
        if os.path.isabs(jar_rel_path):
            jar_path = jar_rel_path
        else:
            jar_path = os.path.join(DATAGRIP_DIR, jar_rel_path)
            
        if not os.path.exists(jar_path):
            print(f"ERRO: Arquivo JAR não encontrado: {jar_path}")
            continue
            
        print(f"Lendo JAR: {os.path.basename(jar_path)}")
        try:
            with zipfile.ZipFile(jar_path, 'r') as jar:
                # Resolve wildcards
                actual_files = []
                for f_pattern in files:
                    if f_pattern.endswith('*.properties'):
                        prefix = f_pattern.replace('*.properties', '')
                        for entry in jar.namelist():
                            if entry.startswith(prefix) and entry.endswith('.properties'):
                                actual_files.append(entry)
                    else:
                        actual_files.append(f_pattern)
                
                for file_in_zip in actual_files:
                    try:
                        # Extract file
                        data = jar.read(file_in_zip)
                        
                        # Target filename (flattened structure or keeping messages/)
                        dest_filename = os.path.basename(file_in_zip)
                        dest_path = os.path.join(TEMP_DIR, dest_filename)
                        
                        with open(dest_path, 'wb') as f:
                            f.write(data)
                        
                        print(f"  - Extraído: {file_in_zip} -> {dest_filename}")
                    except KeyError:
                        print(f"  - AVISO: Arquivo {file_in_zip} não encontrado no JAR.")
        except Exception as e:
            print(f"ERRO ao processar JAR {jar_path}: {e}")

    print("Extração concluída!")

if __name__ == "__main__":
    extract_bundles()
