# Enhanced Chunking Features - Documentation

## Overview

The document chunker has been enhanced with versioning and source tracking capabilities. Each chunk now includes comprehensive metadata that allows LLMs to:
- Reference exact source files
- Track file versions via MD5 hashes
- Identify Git commits, tags, and branches
- Access full source file content for context

---

## New Metadata Fields

### 1. **Source File Content** (`source_file_content`)

**Purpose**: Provides the complete source file content in each chunk's metadata.

**Use Case**: Allows the LLM to:
- Reference the full context when discussing a specific function/class
- Point to specific line numbers in the source file
- Provide more accurate answers based on complete file context

**Example**:
```python
chunk['metadata']['source_file_content'] = """
def example_function():
    '''This is a test function.'''
    return "Hello World"

class TestClass:
    def method1(self):
        return "Method 1"
"""
```

---

### 2. **MD5 Hash** (`file_md5`)

**Purpose**: Unique hash of the source file content for versioning.

**Use Case**: Allows the LLM to:
- Verify if documentation refers to the current version of the file
- Detect if source code has changed since documentation was generated
- Answer questions like "Is this documentation for version X?"

**Example**:
```python
chunk['metadata']['file_md5'] = '30fc73c0d11c1d9187d3c0cf97573ad9'
```

**Calculation**: `hashlib.md5(source_content.encode('utf-8')).hexdigest()`

---

### 3. **Git Commit Hash** (`git_commit`)

**Purpose**: Short (8 character) Git commit hash for the file.

**Use Case**: Allows the LLM to:
- Reference the exact commit that contains this code
- Answer questions like "What commit introduced this feature?"
- Track code evolution over time

**Example**:
```python
chunk['metadata']['git_commit'] = 'f21ab512'
```

**How it works**: Runs `git log -1 --format=%H <file>` and truncates to 8 chars.

---

### 4. **Git Tag** (`git_tag`)

**Purpose**: Git tag for the current commit (if available).

**Use Case**: Allows the LLM to:
- Reference release versions (e.g., "v1.2.3")
- Answer questions like "Which release contains this feature?"
- Provide baseline information for documentation

**Example**:
```python
chunk['metadata']['git_tag'] = 'v1.2.3'
```

**How it works**: Runs `git describe --tags --exact-match HEAD`

---

### 5. **Git Nearest Tag** (`git_nearest_tag`)

**Purpose**: Nearest Git tag if the commit doesn't have an exact tag.

**Use Case**: Provides context when code is between releases.

**Example**:
```python
chunk['metadata']['git_nearest_tag'] = 'v1.2.2'
# Means: This code is based on v1.2.2 but has additional commits
```

**How it works**: Runs `git describe --tags --abbrev=0`

---

### 6. **Git Branch** (`git_branch`)

**Purpose**: Current Git branch name.

**Use Case**: Allows the LLM to:
- Identify if code is from main/develop/feature branch
- Provide context about code stability
- Answer questions about branch-specific features

**Example**:
```python
chunk['metadata']['git_branch'] = 'main'
```

**How it works**: Runs `git rev-parse --abbrev-ref HEAD`

---

## Complete Metadata Structure

```json
{
  "content": "def example_function():\n    return 'Hello'",
  "id": "33348d7576cfb84d3f00236788e80270",
  "metadata": {
    "file_path": "/workspace/source_code/main.py",
    "file_name": "main.py",
    "file_type": "python",
    "chunk_index": 0,
    "total_chunks": 5,
    "source_file_content": "<full source file content>",
    "file_md5": "30fc73c0d11c1d9187d3c0cf97573ad9",
    "git_commit": "f21ab512",
    "git_tag": "v1.2.3",
    "git_branch": "main",
    "type": "function",
    "name": "example_function"
  }
}
```

---

## How LLM Sees the Context

When a user asks a question, the chatbot API formats the RAG results like this:

```markdown
**Relevant Documentation:**

1. def example_function():
    return 'Hello'
   Source: File: /workspace/source_code/main.py, Type: python, MD5: 30fc73c0d11c1d9187d3c0cf97573ad9, Git: f21ab512, Tag: v1.2.3, Branch: main

2. class TestClass:
    def method1(self):
        return "Method 1"
   Source: File: /workspace/source_code/test.py, Type: python, MD5: a72d3bef89..., Git: f21ab512, Tag: v1.2.3, Branch: main
```

This allows the LLM to:
- **Reference specific files**: "According to `/workspace/source_code/main.py`..."
- **Mention versions**: "In version v1.2.3 (commit f21ab512)..."
- **Verify freshness**: "This is from the main branch, MD5: 30fc73c0..."
- **Provide baselines**: "This code is from tag v1.2.3"

---

## Example LLM Responses

### Before (Without Enhanced Metadata):
```
Q: What does example_function do?
A: The example_function returns 'Hello'.
```

### After (With Enhanced Metadata):
```
Q: What does example_function do?
A: The example_function (in main.py, commit f21ab512, tag v1.2.3)
   returns 'Hello'.

   Source file: /workspace/source_code/main.py
   Version: v1.2.3 (f21ab512)
   MD5: 30fc73c0d11c1d9187d3c0cf97573ad9
```

### Versioning Questions:
```
Q: Has this file changed since the documentation was created?
A: Let me check the MD5 hash. The documentation references
   MD5: 30fc73c0d11c1d9187d3c0cf97573ad9. If the current file
   has a different hash, the documentation may be outdated.
```

### Baseline Questions:
```
Q: Which version introduced the TestClass?
A: According to the Git tag in the metadata, TestClass appears in
   tag v1.2.3 (commit f21ab512). You can check earlier tags to
   see when it was first introduced.
```

---

## Implementation Details

### File: `document_chunker.py`

**Key Changes**:

1. **MD5 Calculation** (Line 385-386):
   ```python
   file_md5 = hashlib.md5(source_content.encode('utf-8')).hexdigest()
   ```

2. **Git Info Retrieval** (Lines 415-477):
   ```python
   def _get_git_info(self, file_path: str) -> Dict[str, str]:
       # Runs git commands to get commit, tag, branch
       # Returns dict with git_commit, git_tag, git_branch
   ```

3. **Metadata Addition** (Lines 393-405):
   ```python
   chunk['metadata'].update({
       'file_path': str(path),
       'file_name': path.name,
       'source_file_content': source_content,
       'file_md5': file_md5,
   })

   if git_info:
       chunk['metadata'].update(git_info)
   ```

### File: `api_server.py`

**Key Changes** (Lines 93-109):

Formats source information for LLM context:
```python
source_info = []
if file_path := metadata.get('file_path'):
    source_info.append(f"File: {file_path}")
if md5_hash := metadata.get('file_md5'):
    source_info.append(f"MD5: {md5_hash}")
if git_commit := metadata.get('git_commit'):
    source_info.append(f"Git: {git_commit}")
if git_tag := metadata.get('git_tag'):
    source_info.append(f"Tag: {git_tag}")
# ... etc
```

---

## Error Handling

### Git Not Available
- If Git is not installed or file is not in a Git repository
- Git fields are simply omitted from metadata
- No errors thrown - gracefully degrades

### File Not Readable
- If source file cannot be read
- Chunking still proceeds with available content
- Logged as warning, not fatal error

### Subprocess Timeout
- Git commands have 5-second timeout
- Prevents hanging on slow Git operations
- Returns empty git_info dict on timeout

---

## Performance Considerations

### Git Command Overhead
- Each file requires 3 Git subprocess calls
- Each call has 5-second timeout
- Total max: ~15 seconds per file (worst case)
- **Mitigation**: Commands typically complete in <100ms

### Metadata Size
- `source_file_content` included in every chunk
- For large files (100KB+), metadata can be substantial
- **Impact**: Increased storage requirements in RAG database
- **Benefit**: LLM has full context for accurate responses

### Recommendations
1. **For small projects (<1000 files)**: No issues
2. **For large projects**: Consider:
   - Excluding `source_file_content` for large files
   - Storing source files separately and referencing by path
   - Using file size threshold (e.g., skip content >100KB)

---

## Testing

### Test File: `test_enhanced_chunking.py`

**Tests**:
1. ✅ MD5 hash generation and validation
2. ✅ Source file content inclusion
3. ✅ Git information capture (commit, tag, branch)
4. ✅ Complete metadata structure
5. ✅ Chunk ID generation

**Run tests**:
```bash
python test_enhanced_chunking.py
```

**Expected output**:
```
✅ MD5 hash generation working
✅ Source file content included in metadata
✅ Git information capture implemented (if available)
✅ All required metadata fields present
✅ Chunk ID generation working

🎉 All enhanced chunking features tests completed!
```

---

## Configuration

### Enable/Disable Features

Currently, all features are enabled by default. To customize:

#### Option 1: Modify `document_chunker.py`

```python
class DocumentChunker:
    def __init__(self,
                 max_chunk_size: int = 1000,
                 overlap: int = 100,
                 min_chunk_size: int = 100,
                 include_source_content: bool = True,  # New
                 include_git_info: bool = True):        # New
        self.include_source_content = include_source_content
        self.include_git_info = include_git_info
```

#### Option 2: Add to `mkdocs.yml`

```yaml
plugins:
  - llm-autodoc:
      # ... existing config ...
      document_chunker:
        include_source_content: true  # Include full source in chunks
        include_git_info: true         # Include Git version info
        max_source_size: 100000        # Max file size to include (bytes)
```

---

## Use Cases

### 1. **Version Tracking**
**Scenario**: Documentation generated for v1.2.0, code now at v1.3.0
**Solution**: MD5 hash detects file changes, LLM can warn "documentation may be outdated"

### 2. **Code Reviews**
**Scenario**: Reviewing code changes in a PR
**Solution**: Git commit hash identifies exact version being discussed

### 3. **Regression Debugging**
**Scenario**: Feature worked in v1.2.0, broken in v1.2.3
**Solution**: Git tags help identify which version introduced the bug

### 4. **Baseline Compliance**
**Scenario**: Code must match specific baseline version
**Solution**: Git tag/commit ensures documentation references correct baseline

### 5. **Multi-Branch Development**
**Scenario**: Different features on different branches
**Solution**: Git branch indicates which feature branch the code is from

---

## Future Enhancements

### Potential Additions:
1. **File modification timestamp**: When file was last modified
2. **Author information**: Who last modified the file (from Git)
3. **Commit message**: What change was made (from Git log)
4. **Line numbers**: Map chunks to specific line ranges in source file
5. **Diff generation**: Show what changed between versions
6. **Configurable Git depth**: Get info from last N commits

### Under Consideration:
- Caching Git info to reduce subprocess calls
- Parallel Git info retrieval for performance
- Optional Git info level (minimal/full)
- Integration with Git hosting APIs (GitHub, GitLab)

---

## Troubleshooting

### Git Information Not Appearing

**Problem**: Git fields missing from metadata

**Solutions**:
1. Check Git is installed: `git --version`
2. Verify file is in Git repo: `git status`
3. Check file is committed: `git log -- <file>`
4. Check Git command timeout (default: 5s)

### MD5 Hash Mismatches

**Problem**: MD5 hash changes unexpectedly

**Causes**:
1. Line ending changes (CRLF vs LF)
2. File encoding differences
3. Trailing whitespace changes

**Solutions**:
- Normalize line endings before hashing
- Specify encoding explicitly
- Use `.gitattributes` for consistent line endings

### Performance Issues

**Problem**: Chunking is slow

**Solutions**:
1. Disable Git info for faster processing
2. Exclude large files from source content inclusion
3. Use parallel processing for multiple files
4. Cache Git info at directory level

---

## API Reference

### DocumentChunker.chunk_document()

```python
def chunk_document(self,
                   file_path: str,
                   content: str,
                   file_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Chunk a document with enhanced metadata.

    Args:
        file_path: Path to the file
        content: File content
        file_type: Override file type detection

    Returns:
        List of chunks with metadata including:
        - content: The chunk text
        - id: Unique chunk identifier (MD5 hash)
        - metadata:
            - file_path: Full path to source file
            - file_name: Name of source file
            - file_type: Type of file (python, cpp, markdown, etc.)
            - chunk_index: Index of this chunk
            - total_chunks: Total number of chunks from this file
            - source_file_content: Full source file content for LLM reference
            - file_md5: MD5 hash of source file for versioning
            - git_commit: Git commit hash (short, 8 chars) if available
            - git_tag: Git tag for this commit if available
            - git_nearest_tag: Nearest Git tag if no exact tag
            - git_branch: Current Git branch if available
            - type: Chunk type (function, class, method, section, etc.)
            - name/class/header: Type-specific identifiers
    """
```

---

## Conclusion

The enhanced chunking features provide comprehensive versioning and source tracking capabilities that enable LLMs to:
- Give more accurate, contextual answers
- Reference specific file versions and baselines
- Track code evolution over time
- Verify documentation freshness
- Provide version-specific guidance

All features work seamlessly with existing RAG infrastructure and degrade gracefully when Git is not available.
