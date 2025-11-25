#!/usr/bin/env python3
"""
Automatisiertes Setup-Script für MkDocs LLM AutoDoc Plugin

Dieses Script führt Sie durch die Konfiguration des LLM AutoDoc Plugins
und aktualisiert automatisch Ihre mkdocs.yml Datei.
"""

import os
import sys
import yaml
from pathlib import Path


def print_header(text):
    """Drucke eine formatierte Überschrift"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_option(num, text, description):
    """Drucke eine nummerierte Option"""
    print(f"[{num}] {text}")
    print(f"    {description}\n")


def get_choice(prompt, options):
    """Fordere den Benutzer auf, eine Option auszuwählen"""
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return choice
            print(f"Bitte wählen Sie eine Zahl zwischen 1 und {len(options)}")
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")
        except KeyboardInterrupt:
            print("\n\nAbgebrochen.")
            sys.exit(0)


def get_yes_no(prompt):
    """Fordere den Benutzer auf, Ja oder Nein zu antworten"""
    while True:
        response = input(f"{prompt} (j/n): ").lower().strip()
        if response in ['j', 'ja', 'y', 'yes']:
            return True
        elif response in ['n', 'nein', 'no']:
            return False
        print("Bitte antworten Sie mit 'j' oder 'n'")


def get_input(prompt, default=None):
    """Fordere den Benutzer zur Eingabe auf"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    response = input(prompt).strip()
    return response if response else default


def main():
    print_header("MkDocs LLM AutoDoc Plugin - Automatisches Setup")

    print("Dieses Script hilft Ihnen bei der Konfiguration des LLM AutoDoc Plugins.")
    print("Es wird Ihre mkdocs.yml Datei automatisch aktualisieren.\n")

    # Schritt 1: LLM Provider auswählen
    print_header("Schritt 1: LLM Provider")

    print_option(1, "Anthropic Claude",
                 "Beste Code-Verständnis, empfohlen. Benötigt API-Key (~$2-5 für typisches Projekt)")
    print_option(2, "OpenAI GPT-4",
                 "Gute Qualität. Benötigt API-Key (~$10-20 für typisches Projekt)")
    print_option(3, "Ollama",
                 "Kostenlos, läuft lokal. Benötigt Ollama Installation")
    print_option(4, "LM Studio",
                 "Kostenlos, läuft lokal mit GUI. Benötigt LM Studio Installation")

    provider_choice = get_choice("Wählen Sie Ihren LLM Provider (1-4): ", range(1, 5))

    provider_map = {
        1: ('anthropic', 'claude-3-5-sonnet-20241022', None),
        2: ('openai', 'gpt-4', None),
        3: ('ollama', 'llama3', 'http://localhost:11434/v1'),
        4: ('lmstudio', 'local-model', 'http://localhost:1234/v1')
    }

    llm_provider, llm_model, llm_base_url = provider_map[provider_choice]

    # API Key für Cloud-Provider
    llm_api_key = 'not-needed'
    if llm_provider in ['anthropic', 'openai']:
        api_key_name = f"{'ANTHROPIC' if llm_provider == 'anthropic' else 'OPENAI'}_API_KEY"
        llm_api_key = f"!ENV {api_key_name}"
        print(f"\nHinweis: Stellen Sie sicher, dass Sie die Umgebungsvariable {api_key_name} gesetzt haben.")
        print(f"export {api_key_name}='your-api-key-here'")

    # Modellname anpassen
    if provider_choice in [3, 4]:
        custom_model = get_input(f"Modellname", llm_model)
        if custom_model:
            llm_model = custom_model

    if llm_base_url:
        custom_url = get_input(f"Server URL", llm_base_url)
        if custom_url:
            llm_base_url = custom_url

    # Schritt 2: C++ Projekt-Pfad
    print_header("Schritt 2: C++ Projekt-Pfad")

    print_option(1, "../cpp-project", "Das C++ Projekt liegt im übergeordneten Ordner")
    print_option(2, "./cpp-project", "Das C++ Projekt liegt im mkdocs Ordner")
    print_option(3, "../src", "Nur der src Ordner im übergeordneten Verzeichnis")
    print_option(4, "Eigener Pfad", "Geben Sie einen eigenen Pfad ein")

    path_choice = get_choice("Wo befindet sich Ihr C++ Projekt? (1-4): ", range(1, 5))

    path_map = {
        1: '../cpp-project',
        2: './cpp-project',
        3: '../src'
    }

    if path_choice == 4:
        cpp_project_path = get_input("Geben Sie den Pfad zu Ihrem C++ Projekt ein", "./cpp-project")
    else:
        cpp_project_path = path_map[path_choice]

    # Schritt 3: Dokumentationsebenen
    print_header("Schritt 3: Dokumentationsebenen")

    print("Welche Dokumentationsebenen möchten Sie generieren?\n")

    generate_high_level = get_yes_no("  [1] High-Level: Projektübersicht & Architektur mit Diagrammen")
    generate_mid_level = get_yes_no("  [2] Mid-Level: Modul-Dokumentation mit Klassen und Dependencies")
    generate_detailed_level = get_yes_no("  [3] Detailed-Level: Vollständige API-Referenz mit Beispielen (dauert am längsten)")

    # Schritt 4: Code-Review
    print_header("Schritt 4: Code-Review & Verbesserungsvorschläge")

    enable_code_review = get_yes_no("Möchten Sie Code-Review & Verbesserungsvorschläge aktivieren?")

    # Zusammenfassung
    print_header("Zusammenfassung Ihrer Konfiguration")

    print(f"LLM Provider:        {llm_provider}")
    print(f"LLM Modell:          {llm_model}")
    if llm_base_url:
        print(f"LLM Server URL:      {llm_base_url}")
    print(f"C++ Projekt-Pfad:    {cpp_project_path}")
    print(f"High-Level Docs:     {'✓' if generate_high_level else '✗'}")
    print(f"Mid-Level Docs:      {'✓' if generate_mid_level else '✗'}")
    print(f"Detailed-Level Docs: {'✓' if generate_detailed_level else '✗'}")
    print(f"Code-Review:         {'✓' if enable_code_review else '✗'}")

    if not get_yes_no("\nMöchten Sie mit dieser Konfiguration fortfahren?"):
        print("Abgebrochen.")
        sys.exit(0)

    # mkdocs.yml aktualisieren
    print_header("mkdocs.yml wird aktualisiert...")

    mkdocs_yml_path = Path('mkdocs.yml')
    if not mkdocs_yml_path.exists():
        print(f"FEHLER: mkdocs.yml nicht gefunden in {mkdocs_yml_path.absolute()}")
        sys.exit(1)

    # YAML laden
    with open(mkdocs_yml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Plugin-Konfiguration erstellen
    plugin_config = {
        'llm-autodoc': {
            'enabled': True,
            'cpp_project_path': cpp_project_path,
            'llm_provider': llm_provider,
            'llm_model': llm_model,
            'llm_api_key': llm_api_key,
            'generate_high_level': generate_high_level,
            'generate_mid_level': generate_mid_level,
            'generate_detailed_level': generate_detailed_level,
            'high_level_output': 'generated',
            'mid_level_output': 'generated/modules',
            'detailed_level_output': 'generated/api',
            'enable_quality_check': True,
            'enable_cross_references': True,
            'enable_code_review': enable_code_review,
            'enable_cache': True,
            'cache_dir': '.cache/llm-autodoc',
            'force_regenerate': False,
            'include_patterns': ['**/*.h', '**/*.hpp', '**/*.cpp', '**/*.cc'],
            'exclude_patterns': ['**/build/**', '**/third_party/**', '**/external/**', '**/test/**', '**/tests/**', '**/.git/**'],
            'max_concurrent_llm_calls': 3,
            'retry_failed': True,
            'verbose': False
        }
    }

    if llm_base_url:
        plugin_config['llm-autodoc']['llm_base_url'] = llm_base_url

    # Prüfen, ob das Plugin bereits konfiguriert ist
    if '# - llm-autodoc:' in content or '  - llm-autodoc:' in content:
        print("\nDas Plugin ist bereits in mkdocs.yml vorhanden.")
        if get_yes_no("Möchten Sie die bestehende Konfiguration ersetzen?"):
            # Entferne die alte Konfiguration (kommentiert oder aktiv)
            lines = content.split('\n')
            new_lines = []
            skip_until = None

            for i, line in enumerate(lines):
                if skip_until and i < skip_until:
                    continue
                if '# - llm-autodoc:' in line or '  - llm-autodoc:' in line:
                    # Finde das Ende der Plugin-Konfiguration
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith('  #     ') or lines[j].startswith('      ')):
                        j += 1
                    skip_until = j
                    continue
                new_lines.append(line)

            content = '\n'.join(new_lines)

    # Füge die neue Plugin-Konfiguration hinzu
    # Finde die Position nach git-revision-date-localized
    lines = content.split('\n')
    insert_pos = None

    for i, line in enumerate(lines):
        if 'git-revision-date-localized:' in line:
            # Finde das Ende dieses Plugins
            j = i + 1
            while j < len(lines) and (lines[j].startswith('      ') or lines[j].strip() == ''):
                j += 1
            insert_pos = j
            break

    if insert_pos is None:
        print("FEHLER: Konnte die Position für das Plugin in mkdocs.yml nicht finden.")
        sys.exit(1)

    # Erstelle die Plugin-Konfiguration als String
    plugin_str = "  - llm-autodoc:\n"
    plugin_str += "      # Required Settings\n"
    plugin_str += f"      enabled: {str(plugin_config['llm-autodoc']['enabled']).lower()}\n"
    plugin_str += f"      cpp_project_path: '{plugin_config['llm-autodoc']['cpp_project_path']}'\n\n"
    plugin_str += f"      # LLM Configuration\n"
    plugin_str += f"      llm_provider: '{plugin_config['llm-autodoc']['llm_provider']}'\n"
    plugin_str += f"      llm_model: '{plugin_config['llm-autodoc']['llm_model']}'\n"

    if 'llm_base_url' in plugin_config['llm-autodoc']:
        plugin_str += f"      llm_base_url: '{plugin_config['llm-autodoc']['llm_base_url']}'\n"

    if plugin_config['llm-autodoc']['llm_api_key'] == 'not-needed':
        plugin_str += f"      llm_api_key: 'not-needed'\n\n"
    else:
        plugin_str += f"      llm_api_key: {plugin_config['llm-autodoc']['llm_api_key']}\n\n"

    plugin_str += f"      # Documentation Levels\n"
    plugin_str += f"      generate_high_level: {str(plugin_config['llm-autodoc']['generate_high_level']).lower()}\n"
    plugin_str += f"      generate_mid_level: {str(plugin_config['llm-autodoc']['generate_mid_level']).lower()}\n"
    plugin_str += f"      generate_detailed_level: {str(plugin_config['llm-autodoc']['generate_detailed_level']).lower()}\n\n"

    plugin_str += f"      # Output Paths\n"
    plugin_str += f"      high_level_output: '{plugin_config['llm-autodoc']['high_level_output']}'\n"
    plugin_str += f"      mid_level_output: '{plugin_config['llm-autodoc']['mid_level_output']}'\n"
    plugin_str += f"      detailed_level_output: '{plugin_config['llm-autodoc']['detailed_level_output']}'\n\n"

    plugin_str += f"      # Quality Control\n"
    plugin_str += f"      enable_quality_check: {str(plugin_config['llm-autodoc']['enable_quality_check']).lower()}\n"
    plugin_str += f"      enable_cross_references: {str(plugin_config['llm-autodoc']['enable_cross_references']).lower()}\n"
    plugin_str += f"      enable_code_review: {str(plugin_config['llm-autodoc']['enable_code_review']).lower()}\n\n"

    plugin_str += f"      # Caching\n"
    plugin_str += f"      enable_cache: {str(plugin_config['llm-autodoc']['enable_cache']).lower()}\n"
    plugin_str += f"      cache_dir: '{plugin_config['llm-autodoc']['cache_dir']}'\n"
    plugin_str += f"      force_regenerate: {str(plugin_config['llm-autodoc']['force_regenerate']).lower()}\n\n"

    plugin_str += f"      # File Patterns\n"
    plugin_str += f"      include_patterns:\n"
    for pattern in plugin_config['llm-autodoc']['include_patterns']:
        plugin_str += f"        - '{pattern}'\n"
    plugin_str += f"      exclude_patterns:\n"
    for pattern in plugin_config['llm-autodoc']['exclude_patterns']:
        plugin_str += f"        - '{pattern}'\n"
    plugin_str += "\n"

    plugin_str += f"      # Advanced\n"
    plugin_str += f"      max_concurrent_llm_calls: {plugin_config['llm-autodoc']['max_concurrent_llm_calls']}\n"
    plugin_str += f"      retry_failed: {str(plugin_config['llm-autodoc']['retry_failed']).lower()}\n"
    plugin_str += f"      verbose: {str(plugin_config['llm-autodoc']['verbose']).lower()}\n"

    # Füge die Plugin-Konfiguration ein
    lines.insert(insert_pos, plugin_str)

    # Speichere die aktualisierte mkdocs.yml
    new_content = '\n'.join(lines)
    with open(mkdocs_yml_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✓ mkdocs.yml wurde erfolgreich aktualisiert!")

    # Nächste Schritte
    print_header("Nächste Schritte")

    print("1. Stellen Sie sicher, dass das Plugin installiert ist:")
    print("   cd plugins/mkdocs-llm-autodoc && pip install -e .")
    print()

    if llm_provider in ['anthropic', 'openai']:
        api_key_name = f"{'ANTHROPIC' if llm_provider == 'anthropic' else 'OPENAI'}_API_KEY"
        print(f"2. Setzen Sie Ihren API-Key:")
        print(f"   export {api_key_name}='your-api-key-here'")
        print()

    if llm_provider in ['ollama', 'lmstudio']:
        print(f"2. Stellen Sie sicher, dass Ihr {llm_provider} Server läuft:")
        if llm_provider == 'ollama':
            print(f"   ollama serve")
        else:
            print(f"   LM Studio → Developer → Start Server")
        print()

    print("3. Generieren Sie die Dokumentation:")
    print("   mkdocs build")
    print()

    print("4. Sehen Sie sich das Ergebnis an:")
    print("   mkdocs serve")
    print()

    print_header("Setup abgeschlossen!")
    print("Viel Erfolg mit Ihrer automatisch generierten Dokumentation!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup abgebrochen.")
        sys.exit(0)
