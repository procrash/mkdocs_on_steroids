FROM python:3.11-slim

# Install system dependencies
# git is often needed for mkdocs plugins
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install MkDocs and Material theme
RUN pip install --no-cache-dir \
    mkdocs \
    mkdocs-material \
    pymdown-extensions

# Copy plugin code
# In a real scenario, we might install from pypi, but here we install the local plugin
COPY plugins/mkdocs-llm-autodoc /tmp/mkdocs-llm-autodoc
RUN pip install --no-cache-dir /tmp/mkdocs-llm-autodoc

# Install additional dependencies for the plugin
RUN pip install --no-cache-dir \
    openai \
    anthropic \
    chromadb \
    tiktoken \
    tqdm \
    pyyaml \
    flask \
    requests

# Expose MkDocs development server port
EXPOSE 8000

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Default command (can be overridden by docker-compose)
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
