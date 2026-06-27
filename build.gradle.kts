plugins {
    id("java")
    id("org.jetbrains.intellij.platform") version "2.1.0"
}

group = providers.gradleProperty("pluginGroup").get()
version = providers.gradleProperty("pluginVersion").get()

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        // Target DataGrip 2026.1.3 locally
        local(file("C:/Program Files/JetBrains/DataGrip 2026.1.3"))
        
        // Instrumentator is required by the plugin
        instrumentationTools()
        
        // Marketplace ZIP Signer for signing packages
        zipSigner()
    }
}

intellijPlatform {
    pluginConfiguration {
        id = providers.gradleProperty("pluginGroup")
        name = providers.gradleProperty("pluginName")
        version = providers.gradleProperty("pluginVersion")
        
        description = """
            Pacote de tradução para Português do Brasil (pt-br), desenvolvido para o DataGrip.

            <h3>Diferenciais e Funcionalidades Traduzidas:</h3>
            <ul>
                <li><b>Interface e Menus:</b> Tradução completa dos menus de navegação (File, Edit, View, Navigate, Tools, etc.), barra de status, atalhos de teclado e janelas de diálogo de sistema.</li>
                <li><b>Console SQL e Editores:</b> Localização completa do console de consultas, mensagens do analisador SQL, destaque de sintaxe, autocompletar e plano de execução (Explain Plan).</li>
                <li><b>Gerenciamento de Dados:</b> Tradução do visualizador de tabelas (Data Grid), importação e exportação de formatos (CSV, JSON, XML), filtros e ordenações.</li>
                <li><b>Segurança de Código:</b> Passou por validação automatizada rígida para garantir que tags de sistema, placeholders ({0}, %s) e palavras-chave de banco de dados permaneçam funcionais e seguros.</li>
            </ul>

            <h3>Como Ativar:</h3>
            <ol>
                <li>Acesse <b>Settings</b> | <b>Appearance &amp; Behavior</b> | <b>System Settings</b> | <b>Language and Region</b>.</li>
                <li>Selecione <b>Português (Brasil)</b> nas opções de idioma.</li>
                <li>Clique em <b>Apply/OK</b> e reinicie o DataGrip.</li>
            </ol>
        """.trimIndent()

        changeNotes = """
            Lançamento oficial (Versão 1.0.1) do pacote de tradução para o DataGrip.
            <ul>
                <li>Ajuste e simplificação da descrição do plugin e remoção de termos de marca comunitária.</li>
                <li>Tradução integrada de menus, painéis, console SQL e grade de dados (Data Grid).</li>
                <li>Restrição de compatibilidade exclusiva para o DataGrip, garantindo estabilidade e prevenindo erros em outras IDEs.</li>
                <li>Revisão ortográfica e sintática de todos os termos técnicos de banco de dados.</li>
            </ul>
        """.trimIndent()
        
        vendor {
            name = "William Q. Fernandes"
            email = "williamqfernandes@gmail.com"
        }
    }

    signing {
        val certFile = file("secrets/certificate-chain.crt")
        val keyFile = file("secrets/private-key.pem")
        val pwdFile = file("secrets/password.txt")

        if (certFile.exists() && keyFile.exists() && pwdFile.exists()) {
            certificateChainFile.set(certFile)
            privateKeyFile.set(keyFile)
            password.set(pwdFile.readText().trim())
        }
    }
}

tasks {
    buildSearchableOptions {
        enabled = false
    }
}
