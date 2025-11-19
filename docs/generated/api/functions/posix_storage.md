# POSIX Storage API Documentation

## posix_storage

### Signature
```cpp
struct TORRENT_EXTRA_EXPORT posix_storage
```

### Description
The `posix_storage` class implements a POSIX-compliant file storage backend for the libtorrent library. It provides a platform-independent interface for reading and writing torrent data to the file system using standard POSIX file operations. This storage implementation is designed for Unix-like systems and handles file operations for torrent files, including piece-level access and error reporting.

The class is designed to be used as a storage backend for torrent operations, allowing libtorrent to read and write data from/to the file system in a standardized way. It provides methods for accessing file information, reading data from specific pieces, and managing the storage lifecycle.

### Class Members

#### Constructor
```cpp
explicit posix_storage(storage_params const& p);
```
**Description**: Constructs a new POSIX storage instance with the specified storage parameters. This constructor initializes the storage system with the given configuration, including file paths, storage mode, and other parameters.

**Parameters**:
- `p` (storage_params const&): Configuration parameters for the storage system. This includes the directory path where files will be stored, the storage mode (e.g., sparse files, pre-allocating space), and other relevant settings.

**Return Value**: None (constructor)

**Exceptions/Errors**:
- Throws std::system_error if the storage directory cannot be accessed or created
- Throws std::invalid_argument if the provided parameters are invalid
- May throw exceptions related to file system operations (e.g., insufficient permissions)

**Preconditions**:
- The storage parameters must be valid and complete
- The specified directory path must be accessible
- The storage mode must be supported

**Postconditions**:
- The storage system is initialized and ready for use
- File system operations can be performed
- The storage system is in a consistent state

**Thread Safety**: Not thread-safe during construction. Once constructed, the object can be used by multiple threads, but concurrent access to the same storage must be synchronized.

**Complexity**: O(1) - The constructor performs initialization but does not perform any I/O operations that scale with the size of the data.

**See Also**: `storage_params`, `file_storage`

#### files() Method
```cpp
file_storage const& files() const;
```
**Description**: Returns a reference to the file storage object that contains information about the torrent files. This method provides access to the metadata about the files in the torrent, including their names, sizes, and piece assignments.

**Parameters**: None

**Return Value**:
- `file_storage const&`: A constant reference to the file storage object containing information about the torrent files.

**Exceptions/Errors**: None

**Preconditions**: The `posix_storage` object must be properly initialized.

**Postconditions**: The returned reference remains valid as long as the `posix_storage` object exists.

**Thread Safety**: Thread-safe (read-only access to the file storage)

**Complexity**: O(1) - Returns a reference to an existing object

**See Also**: `file_storage`, `storage_params`

#### Destructor
```cpp
~posix_storage();
```
**Description**: Destructor that cleans up the POSIX storage system. This method closes any open file handles, releases allocated resources, and ensures that any pending operations are completed before the storage system is destroyed.

**Parameters**: None

**Return Value**: None

**Exceptions/Errors**: May throw std::system_error if there are issues with closing files or releasing resources.

**Preconditions**: The `posix_storage` object must be properly constructed.

**Postconditions**: All resources are released, file handles are closed, and the storage system is in a clean state.

**Thread Safety**: Not thread-safe during destruction. Should not be called while other threads are using the storage.

**Complexity**: O(n) where n is the number of files, as it may need to close multiple file handles.

**See Also**: `files()`, `read()`

#### read() Method
```cpp
int read(settings_interface const& sett
    , span<char> bufs
    , piece_index_t const piece, int const offset
    , storage_error& error);
```
**Description**: Reads data from a specific piece and offset in the torrent storage. This method reads the requested data from the specified piece and offset, applying any necessary transformations based on the settings provided.

**Parameters**:
- `sett` (settings_interface const&): Interface to access configuration settings that may affect the reading behavior (e.g., encryption settings, compression).
- `bufs` (span<char>): Buffer where the read data will be stored. The span provides a safe, non-owning view of the buffer.
- `piece` (piece_index_t const): Index of the piece to read from. This must be a valid piece index within the torrent's file layout.
- `offset` (int const): Offset within the piece where reading should start. This must be within the bounds of the piece size.
- `error` (storage_error&): Reference to a storage_error object where any errors during the read operation will be recorded.

**Return Value**:
- `int`: The number of bytes successfully read, or -1 if an error occurred.

**Exceptions/Errors**:
- Throws std::system_error if there are file system errors during reading
- Throws std::invalid_argument if the piece index or offset is invalid
- The `error` parameter will be populated with details about any storage-related errors

**Preconditions**:
- The `posix_storage` object must be properly initialized
- The `bufs` span must point to a valid buffer of sufficient size
- The `piece` index must be valid (0 ≤ piece < total number of pieces)
- The `offset` must be within the bounds of the piece (0 ≤ offset < piece size)
- The `error` parameter must be a valid reference

**Postconditions**:
- The buffer will contain the requested data if the read was successful
- The `error` parameter will contain information about any errors that occurred
- The file position is not modified (this is a random-access read operation)

**Thread Safety**: Not thread-safe. Concurrent read operations should be synchronized.

**Complexity**: O(1) - The method performs a direct file read operation that is independent of the data size, though the actual I/O time depends on the amount of data read.

**See Also**: `file_storage`, `storage_error`, `span`

### Usage Examples

#### Basic Usage
```cpp
#include <libtorrent/aux_/posix_storage.hpp>
#include <libtorrent/storage_params.hpp>
#include <libtorrent/storage_error.hpp>

// Create storage parameters
libtorrent::storage_params params;
params.save_path = "/path/to/torrent/files";
params.torrent_file = "example.torrent";

// Create POSIX storage
libtorrent::posix_storage storage(params);

// Get file information
auto& file_info = storage.files();

// Read data from piece 5, offset 1024
char buffer[1024];
libtorrent::storage_error error;
int bytes_read = storage.read(
    params.settings,
    libtorrent::span<char>(buffer, sizeof(buffer)),
    libtorrent::piece_index_t(5),
    1024,
    error
);

if (bytes_read != -1) {
    // Process the read data
    // buffer contains the data read from the torrent
}
```

#### Error Handling
```cpp
#include <libtorrent/aux_/posix_storage.hpp>
#include <libtorrent/storage_params.hpp>
#include <libtorrent/storage_error.hpp>
#include <iostream>

void read_with_error_handling() {
    libtorrent::storage_params params;
    params.save_path = "/path/to/torrent/files";
    
    try {
        libtorrent::posix_storage storage(params);
        
        char buffer[4096];
        libtorrent::storage_error error;
        int bytes_read = storage.read(
            params.settings,
            libtorrent::span<char>(buffer, sizeof(buffer)),
            libtorrent::piece_index_t(10),
            0,
            error
        );
        
        if (bytes_read == -1) {
            std::cerr << "Read failed: " << error.ec.message() << std::endl;
            std::cerr << "Error code: " << error.ec.value() << std::endl;
            if (error.operation == libtorrent::storage_error::read) {
                std::cerr << "Failed to read from storage" << std::endl;
            }
            return;
        }
        
        // Process successful read
        std::cout << "Read " << bytes_read << " bytes successfully" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Storage initialization failed: " << e.what() << std::endl;
    }
}
```

#### Edge Cases
```cpp
#include <libtorrent/aux_/posix_storage.hpp>
#include <libtorrent/storage_params.hpp>
#include <libtorrent/storage_error.hpp>
#include <iostream>

void handle_edge_cases() {
    libtorrent::storage_params params;
    params.save_path = "/path/to/torrent/files";
    
    try {
        libtorrent::posix_storage storage(params);
        
        // Test with invalid piece index
        char buffer[1];
        libtorrent::storage_error error;
        int bytes_read = storage.read(
            params.settings,
            libtorrent::span<char>(buffer, sizeof(buffer)),
            libtorrent::piece_index_t(1000000), // Invalid piece index
            0,
            error
        );
        
        if (bytes_read == -1) {
            std::cerr << "Invalid piece index error: " << error.ec.message() << std::endl;
        }
        
        // Test with offset beyond piece size
        char buffer2[1];
        error = libtorrent::storage_error(); // Reset error
        bytes_read = storage.read(
            params.settings,
            libtorrent::span<char>(buffer2, sizeof(buffer2)),
            libtorrent::piece_index_t(5),
            1000000000, // Offset beyond piece size
            error
        );
        
        if (bytes_read == -1) {
            std::cerr << "Invalid offset error: " << error.ec.message() << std::endl;
        }
        
        // Test with empty buffer
        char buffer3[0];
        error = libtorrent::storage_error(); // Reset error
        bytes_read = storage.read(
            params.settings,
            libtorrent::span<char>(buffer3, sizeof(buffer3)),
            libtorrent::piece_index_t(0),
            0,
            error
        );
        
        if (bytes_read == -1) {
            std::cerr << "Empty buffer error: " << error.ec.message() << std::endl;
        }
        
    } catch (const std::exception& e) {
        std::cerr << "Storage error: " << e.what() << std::endl;
    }
}
```

### Best Practices

1. **Proper Error Handling**: Always check the return value of `read()` and examine the `storage_error` object for details about any failures.

2. **Buffer Size Management**: Ensure that the buffer provided to `read()` is large enough to hold the requested data and that the `span` correctly represents the buffer size.

3. **Thread Safety**: Use appropriate synchronization mechanisms when accessing `posix_storage` objects from multiple threads.

4. **Resource Management**: Ensure that the storage object is properly destroyed and that all file handles are closed before the program terminates.

5. **Parameter Validation**: Validate piece indices and offsets before calling `read()` to avoid runtime errors.

6. **Memory Alignment**: Ensure that the buffer provided to `read()` is properly aligned for the target architecture, especially when dealing with large amounts of data.

### Code Review & Improvement Suggestions

#### Function: `posix_storage::posix_storage`
**Issue**: No explicit exception specification for the constructor
**Severity**: Medium
**Impact**: Lack of exception specification could lead to unexpected behavior in exception handling
**Fix**: Add explicit exception specification
```cpp
explicit posix_storage(storage_params const& p) noexcept(false);
```

#### Function: `posix_storage::files()`
**Issue**: Returns a reference to internal data without clear ownership semantics
**Severity**: Medium
**Impact**: Could lead to confusion about object lifetime and ownership
**Fix**: Add documentation about the lifetime of the returned reference
```cpp
/**
 * Returns a reference to the file storage object.
 * The returned reference is valid for the lifetime of this posix_storage object.
 */
file_storage const& files() const;
```

#### Function: `posix_storage::~posix_storage()`
**Issue**: No noexcept specification for the destructor
**Severity**: Medium
**Impact**: Could prevent the use of this class in noexcept contexts
**Fix**: Add noexcept specification
```cpp
~posix_storage() noexcept;
```

#### Function: `posix_storage::read()`
**Issue**: The `error` parameter is passed by reference but not marked as const
**Severity**: Low
**Impact**: Could lead to confusion about whether the error object can be modified
**Fix**: Mark as const reference
```cpp
int read(settings_interface const& sett
    , span<char> bufs
    , piece_index_t const piece, int const offset
    , storage_error& error) const;
```

### Modernization Opportunities

1. **Use of [[nodiscard]]**: The `read()` function should be marked as `[[nodiscard]]` since its return value is important:
```cpp
[[nodiscard]] int read(settings_interface const& sett
    , span<char> bufs
    , piece_index_t const piece, int const offset
    , storage_error& error);
```

2. **Use of std::expected**: Replace the error-handling pattern with `std::expected` if available in the C++ standard:
```cpp
// Using std::expected (C++23)
std::expected<int, storage_error> read(settings_interface const& sett
    , span<char> bufs
    , piece_index_t const piece, int const offset);
```

3. **Use of std::span**: The function already uses `std::span`, which is good practice. This should be maintained.

4. **Use of concepts**: Consider adding constraints for the parameters to improve type safety:
```cpp
template<typename Settings>
requires std::is_same_v<Settings, settings_interface>
int read(Settings const& sett
    ,