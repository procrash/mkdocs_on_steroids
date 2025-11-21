# Cross-Linking Feature

## Overview

The Cross-Linking feature automatically creates intelligent connections between related documentation files, making it easier for developers to discover related information and navigate the documentation.

## What It Does

After generating all documentation files, the system:

1. **Analyzes All Markdown Files** for:
   - Shared keywords and topics
   - Common class/function mentions
   - Shared file references
   - Thematic similarity

2. **Builds a Similarity Graph**:
   - Calculates relatedness scores between all documents
   - Identifies the top N most related documents for each file

3. **Automatically Inserts Cross-Links**:
   - Adds "See Also" sections to documents
   - Includes brief explanations of why documents are related
   - Uses relative paths for proper linking

## How It Works

### Similarity Calculation

The system calculates document similarity using multiple signals:

```python
Similarity Score =
    0.4 × Keyword Overlap +
    0.3 × Shared Classes +
    0.2 × Shared Functions +
    0.1 × Shared File References
```

**Example:**

If `threading.md` and `memory-management.md` both mention:
- Keywords: `thread`, `synchronization`, `pool`
- Classes: `ThreadPool`, `WorkerThread`
- Functions: `init()`, `shutdown()`

They'll be identified as related and cross-linked.

### Link Insertion

Cross-links are added as "See Also" sections at the end of documents:

**Before:**
```markdown
# Threading & Concurrency

Thread pool is initialized in `[ThreadPool::init](threadpool.cpp:45-78)`...

## Best Practices
- Always shut down thread pools gracefully
```

**After:**
```markdown
# Threading & Concurrency

Thread pool is initialized in `[ThreadPool::init](threadpool.cpp:45-78)`...

## Best Practices
- Always shut down thread pools gracefully

## See Also

Related documentation:

- **[Memory Management](memory-management.md)** - Related classes: ThreadPool
- **[Performance Optimization](performance.md)** - Related topic
- **[Error Handling](error-handling.md)** - Related classes: ThreadPool
```

## Features

### 1. Automatic Similarity Detection

The system automatically identifies:
- **Thematic Relationships**: Documents covering related topics
- **Code Relationships**: Documents mentioning the same classes/functions
- **Reference Relationships**: Documents referencing the same source files

### 2. Bidirectional Linking

If Document A links to Document B, the system ensures Document B also links back to Document A (when relevant).

### 3. Smart Link Limits

- Maximum 5 links per document (configurable)
- Only links with similarity score > 0.2 are included
- Already existing links are not duplicated

### 4. Relative Path Handling

Links use proper relative paths regardless of directory structure:
```markdown
From: docs/generated/overview/threading.md
To:   docs/generated/overview/performance.md
Link: [Performance](performance.md)

From: docs/generated/overview/threading.md
To:   docs/generated/api/classes/threadpool.md
Link: [ThreadPool](../../api/classes/threadpool.md)
```

### 5. Contextual Snippets

Each link includes a brief explanation:
```markdown
- **[Error Handling](error-handling.md)** - Related classes: ThreadPool, ErrorHandler
```

## Integration

Cross-linking is **Phase 6** of the overview generation process:

```
Phase 1: Topic Extraction (Source + Docs)
    ↓
Phase 2: Topic Synthesis
    ↓
Phase 3: Topic Refinement
    ↓
Phase 4: Dependency Analysis
    ↓
Phase 5: Index Generation
    ↓
Phase 6: Cross-Linking ← NEW!
    ├─ Analyze all generated markdown files
    ├─ Build similarity graph
    ├─ Generate link recommendations
    └─ Insert "See Also" sections
```

## Configuration

Cross-linking is enabled by default when `generate_overview: true`.

To customize:

```yaml
plugins:
  - llm-autodoc:
      generate_overview: true  # Enables cross-linking

      # Cross-linking runs automatically in Phase 6
      # No additional configuration needed
```

To adjust maximum links per document, you would need to modify the code (future enhancement for config option).

## Example Output

### Overview Document: `threading.md`

```markdown
# Threading & Concurrency

## Overview
The project uses a thread pool pattern...

## Threading Model
- Thread pool initialized in `[ThreadPool::init](../../src/threadpool.cpp:45-78)`
- Worker threads spawned in `[ThreadPool::start](../../src/threadpool.cpp:89-120)`

## See Also

Related documentation:

- **[Memory Management](memory-management.md)** - Related classes: ThreadPool, MemoryPool
- **[Performance Optimization](performance.md)** - Related topic
- **[Error Handling](error-handling.md)** - Related classes: ThreadPool
- **[Configuration](configuration.md)** - Related keywords: pool, threads, config
```

### API Document: `classes/threadpool.md`

```markdown
# ThreadPool Class

## Overview
Thread pool implementation for concurrent task execution...

## Methods

### `init()`
Initializes the thread pool...

## See Also

Related documentation:

- **[Threading & Concurrency](../../overview/threading.md)** - Related topic
- **[WorkerThread Class](workerthread.md)** - Related classes: WorkerThread
- **[TaskQueue Class](taskqueue.md)** - Related classes: TaskQueue
```

## Benefits

### 1. Improved Navigation
Developers can easily discover related documentation without searching.

### 2. Better Context
"See Also" links provide context about WHY documents are related.

### 3. Discoverability
Related topics are surfaced automatically, helping developers learn about the codebase.

### 4. Reduced Redundancy
Instead of repeating information, documents can reference each other.

### 5. Maintenance
As documentation changes, cross-links help maintain consistency across related topics.

## Technical Details

### Similarity Thresholds

- **Minimum similarity for linking**: 0.2 (20%)
- **Maximum links per document**: 5
- **Calculation method**: Weighted combination of multiple signals

### Performance

- **Time complexity**: O(n²) where n = number of documents (reasonable for typical projects)
- **Space complexity**: O(n²) for similarity graph
- **Typical execution time**: ~2-5 seconds for 50 documents

### File Analysis

For each document, the system extracts:
- Title (first `#` heading)
- All headings (`##`, `###`, etc.)
- Existing links (to avoid duplication)
- Code references (`[text](file.cpp:123)`)
- Class mentions (`` `ClassName` ``)
- Function mentions (`` `functionName()` ``)
- Keywords (from bold text and code blocks)

## Examples

### Example 1: High Similarity

**Document A** (`testing.md`):
- Keywords: `test`, `unittest`, `coverage`, `mock`
- Classes: `TestRunner`, `MockFactory`
- Functions: `runTests()`, `createMock()`

**Document B** (`ci-cd.md`):
- Keywords: `test`, `coverage`, `pipeline`, `automation`
- Classes: `TestRunner`, `CoverageReport`
- Functions: `runTests()`, `generateReport()`

**Similarity**: ~0.65 (HIGH)

**Result**: Both documents get cross-links to each other with explanation:
```markdown
- **[CI/CD Pipeline](ci-cd.md)** - Related classes: TestRunner
```

### Example 2: Medium Similarity

**Document A** (`architecture.md`):
- Keywords: `design`, `pattern`, `component`, `layer`
- Classes: `Application`, `ServiceLayer`

**Document B** (`build-system.md`):
- Keywords: `cmake`, `build`, `compile`, `configuration`
- Classes: `Application`

**Similarity**: ~0.25 (MEDIUM)

**Result**: Cross-link suggested with generic explanation:
```markdown
- **[Build System](build-system.md)** - Related topic
```

### Example 3: Low Similarity (No Link)

**Document A** (`threading.md`):
- Keywords: `thread`, `concurrent`, `pool`, `mutex`
- Classes: `ThreadPool`, `Mutex`

**Document B** (`i18n.md`):
- Keywords: `locale`, `translation`, `string`, `language`
- Classes: `Translator`, `LocaleManager`

**Similarity**: ~0.05 (LOW)

**Result**: No cross-link created (below 0.2 threshold)

## Limitations

### Current Limitations

1. **Language-Agnostic**: Works for any language but optimized for C++
2. **Keyword-Based**: Relies on keyword extraction, may miss semantic relationships
3. **No Deep Semantic Analysis**: Doesn't understand content meaning deeply
4. **Static Analysis**: Links are created once, not dynamically updated

### Future Enhancements

Planned improvements:

1. **LLM-Enhanced Linking**: Use LLM to suggest context-aware links
2. **Interactive Links**: Generate links based on user navigation patterns
3. **Link Quality Scoring**: Rate link usefulness based on user feedback
4. **Dynamic Updates**: Regenerate links when documents change
5. **Custom Link Rules**: Allow manual link suggestions via config
6. **Link Categories**: Group links by type (related, prerequisite, advanced)

## Troubleshooting

### No Links Generated

**Symptom**: "See Also" sections not appearing in documents

**Possible Causes**:
1. Documents are too dissimilar (all scores < 0.2)
2. Only one document generated
3. Error during cross-linking phase

**Solution**:
```bash
# Check logs for cross-linking phase
mkdocs build 2>&1 | grep "PHASE 6"

# Expected output:
# PHASE 6: CROSS-LINKING
# 🔗 Analyzing 35 documents for cross-linking...
# ✅ Cross-linking complete: 32 files updated with related links
```

### Too Many/Few Links

**Symptom**: Documents have too many or too few cross-links

**Solution**:
Currently requires code modification (future: config option):

```python
# In overview_agent.py, _phase_6_cross_linking():
recommendations = self.cross_linker.generate_cross_links(
    max_links_per_doc=5  # ← Change this number
)
```

### Incorrect Links

**Symptom**: Links point to unrelated documents

**Cause**: Similarity algorithm identified false positives

**Solution**:
1. Check if documents share unexpected keywords
2. Consider adjusting similarity weights (requires code modification)
3. Report as issue for improvement

## Advanced: Custom Similarity Algorithm

To customize the similarity calculation, modify `cross_linker.py`:

```python
def _calculate_similarity(self, doc_a: DocumentNode, doc_b: DocumentNode) -> float:
    score = 0.0

    # Adjust these weights:
    keyword_weight = 0.4  # Currently 40%
    class_weight = 0.3    # Currently 30%
    function_weight = 0.2 # Currently 20%
    file_weight = 0.1     # Currently 10%

    # Your custom logic here...

    return min(score, 1.0)
```

## Integration with RAG

Cross-linked documentation can be uploaded to RAG systems:

```yaml
plugins:
  - llm-autodoc:
      generate_overview: true  # Generates docs with cross-links

      enable_rag_upload: true  # Upload linked docs to RAG
      rag_webhook_url: 'http://localhost:8080/upload'
```

The RAG system will receive documentation with intact internal links, enabling:
- Link-aware retrieval
- Navigation suggestions
- Related document recommendations

## Statistics

After cross-linking, check the logs for statistics:

```
PHASE 6: CROSS-LINKING
🔗 Analyzing 35 documents for cross-linking...
   Loaded 35 markdown documents
   Found 127 potential cross-link relationships
   Generated 158 cross-link recommendations
   Updated 32 files with cross-links
✅ Cross-linking complete: 32 files updated with related links
```

**Interpretation**:
- **35 documents**: Total markdown files analyzed
- **127 relationships**: Document pairs with similarity > 0.2
- **158 recommendations**: Total links to be inserted (some docs get multiple links)
- **32 files updated**: Documents that received new "See Also" sections

## Comparison: Before vs After

### Before Cross-Linking

```
docs/generated/overview/
├── threading.md          (isolated)
├── memory-management.md  (isolated)
├── performance.md        (isolated)
└── error-handling.md     (isolated)
```

**Developer Experience:**
- Must manually search for related topics
- May miss important connections
- Requires prior knowledge of documentation structure

### After Cross-Linking

```
docs/generated/overview/
├── threading.md          ──┐
│                           ├─→ memory-management.md
│                           ├─→ performance.md
│                           └─→ error-handling.md
├── memory-management.md  ──┐
│                           ├─→ threading.md
│                           └─→ performance.md
├── performance.md        ──┐
│                           ├─→ threading.md
│                           └─→ memory-management.md
└── error-handling.md     ───→ threading.md
```

**Developer Experience:**
- Related topics surfaced automatically
- Easy navigation between related documents
- Discover connections you didn't know existed

## Summary

The Cross-Linking feature:

✅ **Automatically** identifies related documentation
✅ **Intelligently** creates cross-links based on multiple signals
✅ **Seamlessly** integrates as Phase 6 of overview generation
✅ **Improves** documentation navigation and discoverability
✅ **Maintains** documentation consistency and coherence

No configuration required - it just works! 🚀
