# Test Markdown Document

This is a comprehensive test document for the markdown splitter.

## Introduction

The document upload service automatically processes markdown files using the
specialized MarkdownTextSplitter from LangChain. This ensures that the document
structure is preserved during chunking.

## Features

### Automatic Detection

The system automatically detects file types based on their extension:

- `.md` and `.markdown` files use MarkdownTextSplitter
- `.cpp`, `.h`, `.hpp` files use C++ language splitter
- `.py` files use Python language splitter
- `.pdf` files extract text and split intelligently

### Smart Splitting

Each splitter understands the structure of its content type:

```python
# Python code is preserved properly
def example_function():
    return "This stays together in a chunk"
```

### Configuration

You can configure:
1. Chunk size (default: 1000)
2. Chunk overlap (default: 200)
3. Custom webhook URL

## Conclusion

The markdown splitter ensures your documentation maintains its hierarchical structure
even after being split into chunks for the RAG system.
