# libtorrent File Mapping API Documentation

## file_mapping_handle

- **Signature**: `file_mapping_handle(file_handle file, open_mode_t mode, std::int64_t size)`
- **Description**: Constructs a file_mapping_handle object that manages a file mapping. This constructor creates a file mapping object that allows memory-mapped access to a file.
- **Parameters**:
  - `file` (file_handle): The file handle to map. This must be a valid file handle that has been opened with appropriate permissions.
  - `mode` (open_mode_t): The access mode for the file mapping (read, write, etc.). Valid values depend on the implementation but typically include read-only, read-write, etc.
  - `size` (std::int64_t): The size of the file mapping in bytes. This must be a non-negative value.
- **Return Value**:
  - None. This is a constructor and does not return a value.
- **Exceptions/Errors**:
  - May throw exceptions if file mapping cannot be created (e.g., insufficient permissions, invalid file handle, out of memory).
- **Example**:
```cpp
file_handle file = /* obtain file handle */;
auto mapping = file_mapping_handle(file, open_mode_t::read_write, 1024 * 1024);
```
- **Preconditions**:
  - `file` must be a valid file handle.
  - `size` must be non-negative.
- **Postconditions**:
  - A file_mapping_handle object is created and initialized with the specified parameters.
- **Thread Safety**: Not thread-safe during construction.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `~file_mapping_handle()`, `handle()`, `fd()`

## file_mapping_handle (copy constructor)

- **Signature**: `file_mapping_handle(file_mapping_handle const&) = delete`
- **Description**: Deleted copy constructor prevents copying of file_mapping_handle objects. This is because file mappings are unique resources that cannot be duplicated.
- **Parameters**: None (deleted function).
- **Return Value**: None.
- **Exceptions/Errors**: None (function is deleted).
- **Example**: 
```cpp
// This code will not compile:
file_mapping_handle original(file, mode, size);
file_mapping_handle copy = original; // Error: copy constructor deleted
```
- **Preconditions**: None.
- **Postconditions**: None.
- **Thread Safety**: N/A (function is deleted).
- **Complexity**: N/A (function is deleted).
- **See Also**: `operator=()`, `file_mapping_handle()`

## handle

- **Signature**: `HANDLE handle() const`
- **Description**: Returns the underlying Windows handle to the file mapping object. This can be used for Windows-specific operations that require access to the file mapping handle.
- **Parameters**: None.
- **Return Value**:
  - `HANDLE`: The Windows handle to the file mapping object. Returns `nullptr` if no mapping exists.
- **Exceptions/Errors**: None.
- **Example**:
```cpp
auto mapping = file_mapping_handle(file, mode, size);
HANDLE handle = mapping.handle();
if (handle != nullptr) {
    // Use the handle for Windows API calls
}
```
- **Preconditions**:
  - The file_mapping_handle must be constructed and valid.
- **Postconditions**:
  - Returns a valid handle if the file mapping was successfully created.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time complexity.
- **See Also**: `fd()`, `has_memory_map()`

## fd

- **Signature**: `handle_type fd() const`
- **Description**: Returns the file descriptor associated with the underlying file. This is useful for file operations that require the file descriptor but not the memory mapping.
- **Parameters**: None.
- **Return Value**:
  - `handle_type`: The file descriptor of the underlying file. This is typically an integer representing the file descriptor.
- **Exceptions/Errors**: None.
- **Example**:
```cpp
auto mapping = file_mapping_handle(file, mode, size);
handle_type file_fd = mapping.fd();
// Use file_fd for standard file operations
```
- **Preconditions**:
  - The file_mapping_handle must be constructed and valid.
- **Postconditions**:
  - Returns the file descriptor of the underlying file.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time complexity.
- **See Also**: `handle()`, `has_memory_map()`

## file_mapping (constructor)

- **Signature**: `file_mapping(file_handle file, open_mode_t mode, std::int64_t file_size, std::shared_ptr<std::mutex> open_unmap_lock = {})`
- **Description**: Constructs a file_mapping object that manages a memory-mapped file. This constructor creates a file mapping that allows memory-mapped access to a file.
- **Parameters**:
  - `file` (file_handle): The file handle to map. This must be a valid file handle that has been opened with appropriate permissions.
  - `mode` (open_mode_t): The access mode for the file mapping (read, write, etc.).
  - `file_size` (std::int64_t): The size of the file in bytes. This must be non-negative.
  - `open_unmap_lock` (std::shared_ptr<std::mutex>): Optional mutex for synchronizing access during mapping and unmapping operations.
- **Return Value**: None. This is a constructor and does not return a value.
- **Exceptions/Errors**:
  - May throw exceptions if file mapping cannot be created (e.g., insufficient permissions, invalid file handle, out of memory).
- **Example**:
```cpp
file_handle file = /* obtain file handle */;
auto mapping = file_mapping(file, open_mode_t::read_write, 1024 * 1024);
```
- **Preconditions**:
  - `file` must be a valid file handle.
  - `file_size` must be non-negative.
- **Postconditions**:
  - A file_mapping object is created and initialized with the specified parameters.
- **Thread Safety**: Not thread-safe during construction.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `~file_mapping()`, `fd()`, `has_memory_map()`

## file_mapping (copy constructor)

- **Signature**: `file_mapping(file_mapping const&) = delete`
- **Description**: Deleted copy constructor prevents copying of file_mapping objects. This is because file mappings are unique resources that cannot be duplicated.
- **Parameters**: None (deleted function).
- **Return Value**: None.
- **Exceptions/Errors**: None (function is deleted).
- **Example**:
```cpp
// This code will not compile:
file_mapping original(file, mode, size);
file_mapping copy = original; // Error: copy constructor deleted
```
- **Preconditions**: None.
- **Postconditions**: None.
- **Thread Safety**: N/A (function is deleted).
- **Complexity**: N/A (function is deleted).
- **See Also**: `operator=()`, `file_mapping()`

## fd (file_mapping version)

- **Signature**: `handle_type fd() const`
- **Description**: Returns the file descriptor associated with the underlying file. This is useful for file operations that require the file descriptor but not the memory mapping.
- **Parameters**: None.
- **Return Value**:
  - `handle_type`: The file descriptor of the underlying file. This is typically an integer representing the file descriptor.
- **Exceptions/Errors**: None.
- **Example**:
```cpp
auto mapping = file_mapping(file, mode, size);
handle_type file_fd = mapping.fd();
// Use file_fd for standard file operations
```
- **Preconditions**:
  - The file_mapping must be constructed and valid.
- **Postconditions**:
  - Returns the file descriptor of the underlying file.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time complexity.
- **See Also**: `handle()`, `has_memory_map()`

## has_memory_map

- **Signature**: `bool has_memory_map() const`
- **Description**: Checks whether the file_mapping object has an active memory mapping. This function returns true if a memory mapping has been successfully created and is currently active.
- **Parameters**: None.
- **Return Value**:
  - `bool`: Returns `true` if a memory mapping exists, `false` otherwise.
- **Exceptions/Errors**: None.
- **Example**:
```cpp
auto mapping = file_mapping(file, mode, size);
if (mapping.has_memory_map()) {
    // Memory mapping is active
} else {
    // No memory mapping available
}
```
- **Preconditions**:
  - The file_mapping must be constructed and valid.
- **Postconditions**:
  - Returns the current state of the memory mapping.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time complexity.
- **See Also**: `handle()`, `range()`

## range

- **Signature**: `span<byte> range()`
- **Description**: Returns a span representing the memory-mapped region of the file. This function provides direct access to the mapped memory area.
- **Parameters**: None.
- **Return Value**:
  - `span<byte>`: A span object representing the memory-mapped region. The span is valid only if the file mapping exists and is not null.
- **Exceptions/Errors**:
  - Throws an assertion error if `m_mapping` is null (indicating the file mapping is not valid).
- **Example**:
```cpp
auto mapping = file_mapping(file, mode, size);
auto mem_region = mapping.range();
// Use mem_region for direct memory access
```
- **Preconditions**:
  - The file_mapping must be constructed and have a valid memory mapping.
- **Postconditions**:
  - Returns a span pointing to the memory-mapped region if the mapping exists.
- **Thread Safety**: Thread-safe as long as no other thread is modifying the memory mapping.
- **Complexity**: O(1) time complexity.
- **See Also**: `has_memory_map()`, `handle()`

# Usage Examples

## Basic Usage

```cpp
#include "libtorrent/aux_/mmap.hpp"
#include "libtorrent/file.hpp"

// Create a file handle
file_handle file = file_handle::open("example.txt", file_handle::read_write);

// Create a file mapping
auto mapping = file_mapping(file, open_mode_t::read_write, 1024 * 1024);

// Get access to the mapped memory
if (mapping.has_memory_map()) {
    auto region = mapping.range();
    // Use the memory region
    std::fill(region.begin(), region.end(), 0);
}

// The mapping is automatically cleaned up when the object goes out of scope
```

## Error Handling

```cpp
#include "libtorrent/aux_/mmap.hpp"
#include "libtorrent/file.hpp"
#include <iostream>

try {
    file_handle file = file_handle::open("example.txt", file_handle::read_write);
    
    if (!file) {
        std::cerr << "Failed to open file" << std::endl;
        return;
    }
    
    auto mapping = file_mapping(file, open_mode_t::read_write, 1024 * 1024);
    
    if (!mapping.has_memory_map()) {
        std::cerr << "Failed to create memory mapping" << std::endl;
        return;
    }
    
    auto region = mapping.range();
    // Process the mapped region
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
}
```

## Edge Cases

```cpp
#include "libtorrent/aux_/mmap.hpp"
#include "libtorrent/file.hpp"

// Handle very large files
std::int64_t large_file_size = 1024 * 1024 * 1024; // 1GB
auto large_mapping = file_mapping(file, open_mode_t::read_write, large_file_size);

// Handle zero-sized files
std::int64_t zero_size = 0;
auto zero_mapping = file_mapping(file, open_mode_t::read_write, zero_size);

// Check for successful mapping
if (zero_mapping.has_memory_map()) {
    auto region = zero_mapping.range();
    // region will be a span of length 0
}
```

# Best Practices

## Effective Usage

1. **Always check if