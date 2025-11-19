```markdown
# C++ Library API Documentation

## load_torrent_file1

- **Signature**: `lt::add_torrent_params load_torrent_file1(std::string filename, dict cfg)`
- **Description**: Loads a torrent file from the specified filename and converts it into an `lt::add_torrent_params` object. The function processes the torrent file and applies configuration settings from the provided dictionary. This is a wrapper around the core `lt::load_torrent_file` function with additional configuration parsing.
- **Parameters**:
  - `filename` (std::string): The path to the torrent file to load. The file must exist and be a valid .torrent file. Must be a UTF-8 encoded string.
  - `cfg` (dict): Configuration dictionary containing parameters to limit or modify the torrent loading process. This dictionary is converted to limits using `dict_to_limits` function.
- **Return Value**:
  - `lt::add_torrent_params`: An object containing the parsed torrent information that can be used to add the torrent to a session. Returns an empty object if the file cannot be loaded.
- **Exceptions/Errors**:
  - `std::filesystem::filesystem_error`: Thrown if the file cannot be accessed or read.
  - `lt::invalid_torrent_file`: Thrown if the torrent file is corrupted or invalid.
  - `std::bad_alloc`: Thrown if memory allocation fails.
- **Example**:
```cpp
try {
    auto params = load_torrent_file1("/path/to/torrent.torrent", {});
    // Use params to add torrent to session
} catch (const std::exception& e) {
    std::cerr << "Error loading torrent: " << e.what() << std::endl;
}
```
- **Preconditions**: The file at `filename` must exist and be a valid .torrent file. The `cfg` dictionary must be properly formatted.
- **Postconditions**: Returns a valid `lt::add_torrent_params` object if successful, or throws an exception if the file cannot be loaded.
- **Thread Safety**: Thread-safe, as it only reads from disk and performs parsing.
- **Complexity**: O(n) where n is the size of the torrent file, as it requires reading and parsing the entire file.
- **See Also**: `lt::load_torrent_file`, `dict_to_limits`

## load_torrent_buffer0

- **Signature**: `lt::add_torrent_params load_torrent_buffer0(bytes b)`
- **Description**: Loads a torrent from a binary buffer containing the .torrent file data. This function is designed for in-memory torrent data processing, such as when torrent files are received over a network.
- **Parameters**:
  - `b` (bytes): A bytes object containing the raw binary data of the torrent file. The data must be a valid .torrent file in bencode format.
- **Return Value**:
  - `lt::add_torrent_params`: An object containing the parsed torrent information. Returns an empty object if the buffer contains invalid data.
- **Exceptions/Errors**:
  - `lt::invalid_torrent_file`: Thrown if the buffer contains invalid or corrupt torrent data.
  - `std::bad_alloc`: Thrown if memory allocation fails.
- **Example**:
```cpp
auto torrent_data = bytes{...}; // Initialize with actual torrent data
try {
    auto params = load_torrent_buffer0(torrent_data);
    // Use params to add torrent to session
} catch (const std::exception& e) {
    std::cerr << "Error parsing torrent buffer: " << e.what() << std::endl;
}
```
- **Preconditions**: The `bytes` object must contain valid .torrent file data in bencode format.
- **Postconditions**: Returns a valid `lt::add_torrent_params` object if successful, or throws an exception if the data is invalid.
- **Thread Safety**: Thread-safe, as it only processes the provided buffer.
- **Complexity**: O(n) where n is the size of the buffer, as it requires parsing the entire buffer.
- **See Also**: `lt::load_torrent_buffer`, `bytes`

## load_torrent_buffer1

- **Signature**: `lt::add_torrent_params load_torrent_buffer1(bytes b, dict cfg)`
- **Description**: Loads a torrent from a binary buffer with optional configuration settings. This function combines the functionality of `load_torrent_buffer` with configuration options from a dictionary.
- **Parameters**:
  - `b` (bytes): A bytes object containing the raw binary data of the torrent file. The data must be a valid .torrent file in bencode format.
  - `cfg` (dict): Configuration dictionary containing parameters to limit or modify the torrent loading process. This dictionary is converted to limits using `dict_to_limits` function.
- **Return Value**:
  - `lt::add_torrent_params`: An object containing the parsed torrent information with applied configuration. Returns an empty object if the buffer contains invalid data.
- **Exceptions/Errors**:
  - `lt::invalid_torrent_file`: Thrown if the buffer contains invalid or corrupt torrent data.
  - `std::bad_alloc`: Thrown if memory allocation fails.
- **Example**:
```cpp
auto torrent_data = bytes{...}; // Initialize with actual torrent data
auto config = dict{{"max_connections", 100}, {"priority", "high"}};
try {
    auto params = load_torrent_buffer1(torrent_data, config);
    // Use params to add torrent to session
} catch (const std::exception& e) {
    std::cerr << "Error parsing torrent buffer: " << e.what() << std::endl;
}
```
- **Preconditions**: The `bytes` object must contain valid .torrent file data in bencode format. The `cfg` dictionary must be properly formatted.
- **Postconditions**: Returns a valid `lt::add_torrent_params` object with applied configuration if successful, or throws an exception if the data is invalid.
- **Thread Safety**: Thread-safe, as it only processes the provided buffer.
- **Complexity**: O(n) where n is the size of the buffer, as it requires parsing the entire buffer.
- **See Also**: `load_torrent_buffer0`, `dict_to_limits`

## load_torrent_parsed1

- **Signature**: `lt::add_torrent_params load_torrent_parsed1(lt::bdecode_node const& n, dict cfg)`
- **Description**: Loads a torrent from a pre-parsed bdecode_node object with optional configuration settings. This function is useful when torrent data has already been decoded and needs to be converted to `lt::add_torrent_params`.
- **Parameters**:
  - `n` (lt::bdecode_node const&): A reference to a bdecode_node object that contains the parsed torrent data. The node must represent a valid torrent dictionary.
  - `cfg` (dict): Configuration dictionary containing parameters to limit or modify the torrent loading process. This dictionary is converted to limits using `dict_to_limits` function.
- **Return Value**:
  - `lt::add_torrent_params`: An object containing the parsed torrent information with applied configuration. Returns an empty object if the node is invalid.
- **Exceptions/Errors**:
  - `lt::invalid_torrent_file`: Thrown if the bdecode_node does not represent a valid torrent.
  - `std::bad_alloc`: Thrown if memory allocation fails.
- **Example**:
```cpp
// Assume torrent_data is a bdecode_node object
auto config = dict{{"max_connections", 100}, {"priority", "high"}};
try {
    auto params = load_torrent_parsed1(torrent_data, config);
    // Use params to add torrent to session
} catch (const std::exception& e) {
    std::cerr << "Error parsing torrent data: " << e.what() << std::endl;
}
```
- **Preconditions**: The `bdecode_node` must contain valid torrent data. The `cfg` dictionary must be properly formatted.
- **Postconditions**: Returns a valid `lt::add_torrent_params` object with applied configuration if successful, or throws an exception if the data is invalid.
- **Thread Safety**: Thread-safe, as it only processes the provided node.
- **Complexity**: O(1) for the function call, but parsing the node is O(n) where n is the complexity of the bdecode_node structure.
- **See Also**: `lt::load_torrent_parsed`, `bdecode_node`, `dict_to_limits`

## bind_load_torrent

- **Signature**: `void bind_load_torrent()`
- **Description**: Binds the `load_torrent_file` and `load_torrent_parsed` functions to a scripting interface (likely Python) by creating function pointers and registering them. This function is typically called during library initialization to make the C++ functions accessible from the scripting environment.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None (should not throw exceptions in initialization code)
- **Example**:
```cpp
// This function is typically called once during library initialization
bind_load_torrent();
// Now the functions are available in the scripting interface
```
- **Preconditions**: The functions `lt::load_torrent_file` and `lt::load_torrent_parsed` must be defined and accessible.
- **Postconditions**: The functions are registered in the scripting interface and can be called from the scripting language.
- **Thread Safety**: Thread-safe only if called before any other thread uses the functions.
- **Complexity**: O(1), as it only creates function pointers and registers them.
- **See Also**: `def`, `lt::load_torrent_file`, `lt::load_torrent_parsed`

# Usage Examples

## Basic Usage

```cpp
#include <iostream>
#include <string>

// Assume these functions are available
// #include "load_torrent.hpp"

int main() {
    try {
        // Load from file
        auto params1 = load_torrent_file1("/path/to/torrent.torrent", {});
        
        // Load from buffer
        auto torrent_data = bytes{...}; // Initialize with actual torrent data
        auto params2 = load_torrent_buffer1(torrent_data, {});
        
        // Load from parsed data
        auto parsed_data = lt::bdecode_node{}; // Initialize with actual parsed data
        auto params3 = load_torrent_parsed1(parsed_data, {});
        
        std::cout << "Torrent loaded successfully" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

## Error Handling

```cpp
#include <iostream>
#include <string>

void load_torrent_with_error_handling() {
    try {
        // Try loading from file
        auto params = load_torrent_file1("/path/to/torrent.torrent", {});
        
        // Process successfully loaded torrent
        std::cout << "Torrent loaded: " << params.name() << std::endl;
    } catch (const std::filesystem::filesystem_error& e) {
        std::cerr << "File system error: " << e.what() << std::endl;
    } catch (const lt::invalid_torrent_file& e) {
        std::cerr << "Invalid torrent file: " << e.what() << std::endl;
    } catch (const std::bad_alloc& e) {
        std::cerr << "Memory allocation failed: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Unexpected error: " << e.what() << std::endl;
    }
}
```

## Edge Cases

```cpp
#include <iostream>
#include <string>

void test_edge_cases() {
    // Empty filename
    try {
        auto params = load_torrent_file1("", {});
    } catch (const std::filesystem::filesystem_error& e) {
        std::cout << "Empty filename handled correctly: " << e.what() << std::endl;
    }
    
    // Non-existent file
    try {
        auto params = load_torrent_file1("/non/existent/torrent.torrent", {});
    } catch (const std::filesystem::filesystem_error& e) {
        std::cout << "Non-existent file handled correctly: " << e.what() << std::endl;
    }
    
    // Corrupt torrent file
    try {
        auto params = load_torrent_file1("/path/to/corrupt.torrent", {});
    } catch (const lt::invalid_torrent_file& e) {
        std::cout << "Corrupt torrent file handled correctly: " << e.what() << std::endl;
    }
}
```

# Best Practices

1. **Always check for errors**: Wrap calls to these functions in try-catch blocks to handle filesystem errors, invalid torrent files, and memory allocation issues.

2. **Use appropriate loading method**: 
   - Use `load_torrent_file1` for files stored on disk
   -