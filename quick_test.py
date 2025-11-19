"""
Quick test script to verify the document uploader setup without actually uploading.
Tests the splitting functionality locally.
"""

import sys
from pathlib import Path

# Create a simple test file
test_content_cpp = """#include <iostream>
#include <vector>
#include <string>

// This is a test C++ file for the document upload service
// It demonstrates the C++ code splitting capabilities

class DocumentProcessor {
private:
    std::vector<std::string> chunks;
    int chunkSize;

public:
    DocumentProcessor(int size) : chunkSize(size) {
        std::cout << "DocumentProcessor initialized with chunk size: " << size << std::endl;
    }

    void processDocument(const std::string& content) {
        // Process the document and split into chunks
        std::cout << "Processing document of size: " << content.length() << std::endl;

        // Split logic would go here
        for (size_t i = 0; i < content.length(); i += chunkSize) {
            chunks.push_back(content.substr(i, chunkSize));
        }
    }

    void printChunks() {
        std::cout << "Total chunks: " << chunks.size() << std::endl;
        for (size_t i = 0; i < chunks.size(); ++i) {
            std::cout << "Chunk " << i << ": " << chunks[i].length() << " chars" << std::endl;
        }
    }
};

int main() {
    DocumentProcessor processor(1000);
    processor.processDocument("Sample document content here...");
    processor.printChunks();
    return 0;
}
"""

test_content_md = """# Test Markdown Document

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
"""

def test_without_upload():
    """Test the document processor without uploading to n8n."""
    try:
        from document_uploader import DocumentProcessor

        print("\n" + "="*80)
        print("  Document Upload Service - Local Test (No Upload)")
        print("="*80 + "\n")

        # Create test files
        test_dir = Path("test_documents")
        test_dir.mkdir(exist_ok=True)

        cpp_file = test_dir / "test_local.cpp"
        md_file = test_dir / "test_local.md"

        print("[1/4] Creating test files...")
        cpp_file.write_text(test_content_cpp, encoding='utf-8')
        md_file.write_text(test_content_md, encoding='utf-8')
        print(f"      [OK] Created {cpp_file}")
        print(f"      [OK] Created {md_file}\n")

        # Test C++ processing
        print("[2/4] Testing C++ file processing...")
        processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
        cpp_chunks = processor.process_file(str(cpp_file))
        print(f"      [OK] Split C++ file into {len(cpp_chunks)} chunks")
        print(f"      [OK] First chunk preview: {cpp_chunks[0][:100]}...\n")

        # Test Markdown processing
        print("[3/4] Testing Markdown file processing...")
        md_chunks = processor.process_file(str(md_file))
        print(f"      [OK] Split Markdown file into {len(md_chunks)} chunks")
        print(f"      [OK] First chunk preview: {md_chunks[0][:100]}...\n")

        # Show chunk details
        print("[4/4] Chunk Details:")
        print(f"\n  C++ File ({cpp_file.name}):")
        for i, chunk in enumerate(cpp_chunks):
            print(f"    Chunk {i+1}: {len(chunk)} characters")

        print(f"\n  Markdown File ({md_file.name}):")
        for i, chunk in enumerate(md_chunks):
            print(f"    Chunk {i+1}: {len(chunk)} characters")

        print("\n" + "="*80)
        print("  Local Test Successful!")
        print("="*80)
        print("\n  Next Steps:")
        print("  1. Configure your n8n webhook URL in .env")
        print("  2. Run test_upload.bat to test uploading to n8n")
        print("  3. Use upload_document.bat to upload your files")
        print("\n" + "="*80 + "\n")

        return 0

    except ImportError as e:
        print(f"\n[ERROR] Missing dependencies: {e}")
        print("        Please run: setup_document_uploader.bat\n")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(test_without_upload())
