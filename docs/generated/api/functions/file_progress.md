# libtorrent::aux::file_progress API Documentation

## file_progress

- **Signature**: `file_progress()`
- **Description**: Default constructor for the file_progress struct. Initializes the object to its default state with no file progress data.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::file_progress progress;
```
- **Preconditions**: None
- **Postconditions**: The file_progress object is in a valid state and can be used with the init() method
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) time, O(1) space
- **See Also**: `init()`, `export_progress()`

## file_progress

- **Signature**: `void init(piece_picker const& picker, file_storage const& fs)`
- **Description**: Initializes the file_progress object with data from a piece_picker and file_storage. This method computes the progress of each file in the torrent by analyzing which pieces are available and how they map to files.
- **Parameters**:
  - `picker` (piece_picker const&): The piece_picker object that contains information about which pieces are available for download. This must be valid and contain the piece availability information for the torrent.
  - `fs` (file_storage const&): The file_storage object that describes the files in the torrent, including their names, sizes, and locations. This must be valid and correspond to the same torrent as the piece_picker.
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::file_progress progress;
progress.init(picker, fs);
```
- **Preconditions**: The picker and fs objects must be valid and correspond to the same torrent. The file_storage must be properly initialized.
- **Postconditions**: The file_progress object contains the calculated progress for each file in the torrent.
- **Thread Safety**: Not thread-safe (modifies internal state)
- **Complexity**: O(n) time where n is the number of files, O(1) space
- **See Also**: `export_progress()`, `total_on_disk()`, `empty()`

## total_on_disk

- **Signature**: `std::int64_t total_on_disk() const`
- **Description**: Returns the total amount of data (in bytes) that is currently on disk for all files in the torrent.
- **Parameters**: None
- **Return Value**: 
  - `std::int64_t`: The total number of bytes on disk for all files. This is the sum of all file sizes that have at least one piece available.
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::file_progress progress;
// ... (init with picker and fs)
std::int64_t on_disk = progress.total_on_disk();
std::cout << "Total data on disk: " << on_disk << " bytes" << std::endl;
```
- **Preconditions**: The `init()` method must have been called to populate the progress data.
- **Postconditions**: Returns the total amount of data on disk at the time of the call.
- **Thread Safety**: Thread-safe (const method)
- **Complexity**: O(1) time, O(1) space
- **See Also**: `export_progress()`, `empty()`

## empty

- **Signature**: `bool empty() const`
- **Description**: Checks if there are any files with progress (i.e., if any files have data on disk). This is useful for determining if the torrent has any downloaded data.
- **Parameters**: None
- **Return Value**:
  - `true`: If no files have any data on disk (all files are completely missing or have no pieces available)
  - `false`: If at least one file has some data on disk
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::file_progress progress;
// ... (init with picker and fs)
if (progress.empty()) {
    std::cout << "No data on disk yet" << std::endl;
} else {
    std::cout << "Some data is on disk" << std::endl;
}
```
- **Preconditions**: The `init()` method must have been called to populate the progress data.
- **Postconditions**: Returns `true` if no files have any data on disk, `false` otherwise.
- **Thread Safety**: Thread-safe (const method)
- **Complexity**: O(1) time, O(1) space
- **See Also**: `total_on_disk()`, `init()`

# Usage Examples

## Basic Usage

```cpp
#include <libtorrent/aux_/file_progress.hpp>
#include <libtorrent/piece_picker.hpp>
#include <libtorrent/file_storage.hpp>

void demonstrate_file_progress() {
    // Create a piece_picker and file_storage (in practice, these would come from a torrent)
    libtorrent::piece_picker picker;
    libtorrent::file_storage fs;
    
    // Initialize file_progress
    libtorrent::aux::file_progress progress;
    progress.init(picker, fs);
    
    // Check if any data is on disk
    if (!progress.empty()) {
        std::cout << "Files have some data on disk" << std::endl;
        std::cout << "Total data on disk: " << progress.total_on_disk() << " bytes" << std::endl;
    } else {
        std::cout << "No data on disk yet" << std::endl;
    }
    
    // Export progress for all files
    std::vector<std::int64_t, file_index_t> file_progress;
    progress.export_progress(file_progress);
    
    // Use the exported progress data
    for (size_t i = 0; i < file_progress.size(); ++i) {
        std::cout << "File " << i << " progress: " << file_progress[i] << " bytes" << std::endl;
    }
}
```

## Error Handling

```cpp
#include <libtorrent/aux_/file_progress.hpp>
#include <libtorrent/piece_picker.hpp>
#include <libtorrent/file_storage.hpp>
#include <iostream>
#include <stdexcept>

void process_file_progress(const libtorrent::piece_picker& picker, const libtorrent::file_storage& fs) {
    try {
        libtorrent::aux::file_progress progress;
        
        // Check if inputs are valid before initializing
        if (picker.empty() || fs.num_files() == 0) {
            throw std::invalid_argument("Invalid piece_picker or file_storage");
        }
        
        progress.init(picker, fs);
        
        // Use the progress data
        if (progress.empty()) {
            std::cout << "No data downloaded yet" << std::endl;
        } else {
            std::cout << "Total downloaded: " << progress.total_on_disk() << " bytes" << std::endl;
        }
    } catch (const std::exception& e) {
        std::cerr << "Error processing file progress: " << e.what() << std::endl;
    }
}
```

## Edge Cases

```cpp
#include <libtorrent/aux_/file_progress.hpp>
#include <libtorrent/piece_picker.hpp>
#include <libtorrent/file_storage.hpp>
#include <iostream>

void demonstrate_edge_cases() {
    // Case 1: Empty torrent (no files)
    libtorrent::file_storage empty_fs;
    libtorrent::piece_picker empty_picker;
    
    libtorrent::aux::file_progress empty_progress;
    empty_progress.init(empty_picker, empty_fs);
    
    std::cout << "Empty torrent - is empty: " << empty_progress.empty() << std::endl;
    std::cout << "Total on disk: " << empty_progress.total_on_disk() << " bytes" << std::endl;
    
    // Case 2: All files fully downloaded
    libtorrent::file_storage fs;
    // Add files to fs...
    libtorrent::piece_picker picker;
    // Fill picker with all pieces available...
    
    libtorrent::aux::file_progress fully_downloaded;
    fully_downloaded.init(picker, fs);
    
    std::cout << "Fully downloaded - is empty: " << fully_downloaded.empty() << std::endl;
    std::cout << "Total on disk: " << fully_downloaded.total_on_disk() << " bytes" << std::endl;
    
    // Case 3: No pieces available
    libtorrent::file_storage partial_fs;
    // Add files to partial_fs...
    libtorrent::piece_picker partial_picker;
    // No pieces available in partial_picker...
    
    libtorrent::aux::file_progress no_data;
    no_data.init(partial_picker, partial_fs);
    
    std::cout << "No data - is empty: " << no_data.empty() << std::endl;
    std::cout << "Total on disk: " << no_data.total_on_disk() << " bytes" << std::endl;
}
```

# Best Practices

1. **Always call init() first**: The file_progress object must be initialized with `init()` before calling any other methods.

2. **Check for empty state**: Use `empty()` to determine if any data is available before processing the progress.

3. **Use total_on_disk for summary**: When you need to know the total amount of data on disk, use `total_on_disk()` instead of summing the export_progress array.

4. **Export only when needed**: The `export_progress()` method is expensive (O(n)) and should only be called when you need individual file progress values.

5. **Thread safety**: The `total_on_disk()` and `empty()` methods are thread-safe, but `init()` is not. Ensure proper synchronization if using across threads.

6. **Avoid repeated export**: If you need to access file progress multiple times, store the exported vector rather than calling `export_progress()` repeatedly.

# Code Review & Improvement Suggestions

## Potential Issues

**Function**: `file_progress()`
**Issue**: No validation that the default constructor initializes the object in a consistent state
**Severity**: Low
**Impact**: Could lead to undefined behavior if the object is used before initialization
**Fix**: Ensure the constructor properly initializes all members:

```cpp
// Ensure all members are properly initialized in the constructor
file_progress() 
    : m_total_on_disk(0)
    , m_file_progress()
{
}
```

**Function**: `init()`
**Issue**: No validation of input parameters
**Severity**: Medium
**Impact**: Could lead to undefined behavior or crashes if invalid input is provided
**Fix**: Add input validation:

```cpp
void init(piece_picker const& picker, file_storage const& fs) {
    if (picker.empty()) {
        throw std::invalid_argument("Piece picker cannot be empty");
    }
    
    if (fs.num_files() == 0) {
        throw std::invalid_argument("File storage cannot be empty");
    }
    
    // Rest of the initialization code
}
```

**Function**: `export_progress()`
**Issue**: No validation of output vector
**Severity**: Medium
**Impact**: Could lead to buffer overflow or undefined behavior
**Fix**: Add validation and possibly use a different approach:

```cpp
void export_progress(vector<std::int64_t, file_index_t>& fp) {
    // Ensure the vector has enough capacity
    if (fp.size() < m_file_progress.size()) {
        throw std::out_of_range("Output vector too small");
    }
    
    // Copy the data
    std::copy(m_file_progress.begin(), m_file_progress.end(), fp.begin());
}
```

**Function**: `total_on_disk()`
**Issue**: No error checking for invalid state
**Severity**: Low
**Impact**: Could return incorrect results if used before initialization
**Fix**: Add a check:

```cpp
std::int64_t total_on_disk() const {
    if (m_file_progress.empty()) {
        return 0;
    }
    return m_total_on_disk;
}
```

## Modernization Opportunities

**Function**: `init()`
**Opportunity**: Use std::span for the file_storage parameter
**Suggestion**: Replace `file_storage const&` with `std::span<const file_storage>` if possible, though this requires more extensive changes.

**Function**: `export_progress()`
**Opportunity**: Use std::expected for error handling
**Suggestion**: Replace the current void return with `std::expected<void, std::errc>` for better error handling:

```cpp
std::expected<void, std::errc> export_progress(
    std::span<std::int64_t, file_index_t> fp) {
    if (fp.size() < m_file_progress.size()) {
        return std::unexpected<std::errc::invalid_argument);
    }
    
    std::copy(m_file_progress.begin(), m_file_progress.end(), fp.begin());
    return {};
}
```

**Function**: `file_progress()`
**Opportunity**: Mark as noexcept
**Suggestion**: Add noexcept specifier since it's a simple constructor:

```cpp
file_progress() noexcept = default;
```

## Refactoring Suggestions

**Function**: `file_progress()`
**Suggestion**: The constructor could be made explicit to prevent implicit conversions:

```cpp
explicit file_progress();
```

**Function**: `export_progress()`
**Suggestion**: Consider splitting into a query method and a separate export method to separate concerns.

## Performance Optimizations

**Function**: `export_progress()`
**Opportunity**: Use move semantics for the output parameter
**Suggestion**: The function could be optimized by taking the vector by value and moving it into the class:

```cpp
void export_progress(std::vector<std::int64_t, file_index_t>&& fp) {
    if (fp.size() <