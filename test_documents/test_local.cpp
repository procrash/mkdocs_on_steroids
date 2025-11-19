#include <iostream>
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
