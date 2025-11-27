#!/bin/bash
set -e

# Start CORS Proxy in background if PROXY_TARGET_URL is set
if [ ! -z "$PROXY_TARGET_URL" ]; then
    echo "Starting CORS Proxy forwarding to $PROXY_TARGET_URL..."
    # We assume the plugin code is installed in site-packages or /tmp/mkdocs-llm-autodoc
    # But we copied it to /tmp/mkdocs-llm-autodoc in Dockerfile.
    # Let's find where the proxy file is.
    # Since we pip installed it, it should be importable.
    # But to run it as a script, we might need to locate it.
    # Simpler: We can just run it from the source copy in /tmp if we know the path.
    
    # However, for robustness, let's assume we can run it via python -m if it was a module, 
    # but it's not fully packaged as an executable module yet.
    # Let's try to run it from the installed location or the copy.
    
    # Fallback: We know we copied it to /tmp/mkdocs-llm-autodoc
    PROXY_SCRIPT="/tmp/mkdocs-llm-autodoc/mkdocs_llm_autodoc/proxy/cors_proxy.py"
    
    if [ -f "$PROXY_SCRIPT" ]; then
        python "$PROXY_SCRIPT" &
        PROXY_PID=$!
        echo "Proxy started with PID $PROXY_PID"
    else
        echo "Warning: Proxy script not found at $PROXY_SCRIPT"
    fi
fi

# Execute the main command (e.g., mkdocs serve)
exec "$@"
