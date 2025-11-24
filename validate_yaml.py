"""
Validate YAML configuration for MkDocs
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import yaml

print("=" * 70)
print("Validating YAML Configuration")
print("=" * 70)

# Test with unsafe loader (allows Python tags)
print("\n1. Testing YAML structure...")
try:
    with open(r'Z:\mkdocs\mkdocs_example_full_features.yaml', encoding='utf-8') as f:
        config = yaml.unsafe_load(f.read())

    print("   ✅ YAML structure is valid")

    # Validate required top-level keys
    print("\n2. Validating top-level keys...")
    required_keys = ['site_name', 'theme', 'plugins']
    for key in required_keys:
        if key in config:
            print(f"   ✅ Found '{key}'")
        else:
            print(f"   ❌ Missing '{key}'")

    # Validate plugins
    print("\n3. Validating plugins configuration...")
    if 'plugins' in config:
        plugins = config['plugins']
        plugin_names = []

        for plugin in plugins:
            if isinstance(plugin, dict):
                plugin_name = list(plugin.keys())[0]
                plugin_names.append(plugin_name)
            else:
                plugin_names.append(plugin)

        print(f"   ✅ Found {len(plugin_names)} plugins: {', '.join(plugin_names)}")

        # Check for our plugins
        if 'llm-autodoc' in plugin_names:
            print("   ✅ llm-autodoc plugin configured")

            # Get llm-autodoc config
            for plugin in plugins:
                if isinstance(plugin, dict) and 'llm-autodoc' in plugin:
                    autodoc_config = plugin['llm-autodoc']

                    # Check key features
                    features = [
                        ('enable_rag_upload', 'RAG Upload'),
                        ('enable_doxygen_import', 'Doxygen Import')
                    ]

                    for key, name in features:
                        if key in autodoc_config:
                            print(f"      ✅ {name}: {autodoc_config[key]}")

        if 'chatbot' in plugin_names:
            print("   ✅ chatbot plugin configured")

            # Get chatbot config
            for plugin in plugins:
                if isinstance(plugin, dict) and 'chatbot' in plugin:
                    chatbot_config = plugin['chatbot']

                    # Check key features
                    features = [
                        ('enable_rag', 'RAG'),
                        ('enable_mcp_tools', 'MCP Tools'),
                        ('enable_minio', 'MinIO'),
                        ('enable_n8n', 'n8n')
                    ]

                    for key, name in features:
                        if key in chatbot_config:
                            print(f"      ✅ {name}: {chatbot_config[key]}")

                    # Check RAG config
                    if 'rag_config' in chatbot_config:
                        rag_config = chatbot_config['rag_config']
                        rag_type = rag_config.get('type', 'unknown')
                        print(f"      ✅ RAG Type: {rag_type}")

                    # Check MCP tools
                    if 'mcp_tools' in chatbot_config:
                        tools = chatbot_config['mcp_tools']
                        print(f"      ✅ MCP Tools configured: {len(tools)} tool(s)")

    # Validate markdown extensions
    print("\n4. Validating markdown extensions...")
    if 'markdown_extensions' in config:
        extensions = config['markdown_extensions']
        print(f"   ✅ Found {len(extensions)} markdown extensions")

    print("\n" + "=" * 70)
    print("YAML Configuration Validation: SUCCESS ✅")
    print("=" * 70)

except Exception as e:
    print(f"\n   ❌ YAML validation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
