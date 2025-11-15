# API Documentation

## main

- **Signature**: `int main(int argc, char const* argv[])`
- **Description**: The main entry point of the bt-get application, which downloads a torrent from a magnet URL. This function initializes the libtorrent session, adds the torrent, and monitors the download progress until completion.
- **Parameters**:
  - `argc` (int): The number of command line arguments. Must be exactly 2 for proper operation.
  - `argv` (char const*[]): Array of command line arguments. The first argument is the program name, the second must be a valid magnet URL.
- **Return Value**:
  - `0`: Success - the download completed successfully.
  - `1`: Failure - the function returned due to invalid arguments or other errors.
- **Exceptions/Errors**:
  - Throws `std::exception` if libtorrent initialization fails.
  - Throws `std::invalid_argument` if the magnet URL is invalid.
  - Throws `std::runtime_error` if torrent addition fails.
- **Example**:
```cpp
int main(int argc, char const* argv[]) try {
    if (argc != 2) {
        std::cerr << "usage: " << argv[0] << " <magnet-url>" << std::endl;
        return 1;
    }
    // ... rest of the function
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
    return 1;
}
```
- **Preconditions**: 
  - The program must be called with exactly two arguments.
  - The second argument must be a valid magnet URL string.
  - The libtorrent library must be properly linked and initialized.
- **Postconditions**: 
  - The function returns 0 if the download completes successfully.
  - The function returns 1 if it fails to initialize or add the torrent.
  - The downloaded torrent data is saved to the default download directory.
- **Thread Safety**: This function is not thread-safe as it creates and uses a single libtorrent session.
- **Complexity**: 
  - Time: O(n) where n is the number of pieces in the torrent.
  - Space: O(m) where m is the total size of the torrent data.

## Usage Examples

### Basic Usage
```cpp
// Download a torrent from a magnet URL
./bt-get "magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678"
```

### Error Handling
```cpp
int main(int argc, char const* argv[]) try {
    if (argc != 2) {
        std::cerr << "usage: " << argv[0] << " <magnet-url>" << std::endl;
        return 1;
    }
    
    // Validate magnet URL format
    if (!isValidMagnetUrl(argv[1])) {
        std::cerr << "Invalid magnet URL format" << std::endl;
        return 1;
    }
    
    lt::settings_pack p;
    p.set_int(lt::alert_category::status | lt::alert_category::error);
    lt::session ses(p);
    
    lt::add_torrent_params params;
    params.url = argv[1];
    lt::torrent_handle h = ses.add_torrent(params);
    
    // Monitor download progress
    while (!h.is_seed()) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        // Print download progress
    }
    
    std::cout << "Download completed successfully" << std::endl;
    return 0;
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
    return 1;
}
```

### Edge Cases
```cpp
int main(int argc, char const* argv[]) try {
    if (argc != 2) {
        std::cerr << "usage: " << argv[0] << " <magnet-url>" << std::endl;
        return 1;
    }
    
    // Handle empty magnet URL
    if (std::string(argv[1]).empty()) {
        std::cerr << "Error: Empty magnet URL" << std::endl;
        return 1;
    }
    
    // Handle invalid magnet URL
    if (!isMagnetUrlValid(argv[1])) {
        std::cerr << "Error: Invalid magnet URL format" << std::endl;
        return 1;
    }
    
    // Handle very large torrents
    if (getTorrentSize(argv[1]) > 1000 * 1024 * 1024) {
        std::cout << "Warning: This is a large torrent (>1GB)" << std::endl;
    }
    
    lt::settings_pack p;
    p.set_int(lt::alert_mask, lt::alert_category::status | lt::alert_category::error);
    lt::session ses(p);
    
    lt::add_torrent_params params;
    params.url = argv[1];
    lt::torrent_handle h = ses.add_torrent(params);
    
    // Handle case where torrent is already added
    if (h.is_valid()) {
        std::cout << "Torrent already added" << std::endl;
        return 0;
    }
    
    // Monitor download
    while (!h.is_seed()) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    
    std::cout << "Download completed" << std::endl;
    return 0;
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
    return 1;
}
```

## Best Practices

1. **Always validate input parameters** - Check argc/argv validity and magnet URL format.
2. **Use try-catch blocks** - Wrap the main function in exception handling to gracefully handle errors.
3. **Add proper error messages** - Provide clear usage instructions and error descriptions.
4. **Monitor download progress** - Implement a loop to check download status and provide feedback.
5. **Handle edge cases** - Consider empty URLs, invalid URLs, and very large torrents.
6. **Use const correctness** - Mark parameters as const where appropriate.
7. **Avoid magic numbers** - Use named constants for configuration values.

## Code Review & Improvement Suggestions

### Potential Issues

**Security:**
- **Function**: `main`
- **Issue**: Insufficient input validation for magnet URLs
- **Severity**: Medium
- **Impact**: Could lead to parsing errors or security vulnerabilities with malformed URLs
- **Fix**: Add proper validation for magnet URL format:
```cpp
bool isValidMagnetUrl(const char* url) {
    return url && std::string(url).find("magnet:?xt=urn:btih:") == 0;
}
```

**Performance:**
- **Function**: `main`
- **Issue**: Inefficient download monitoring loop
- **Severity**: Medium
- **Impact**: High CPU usage due to busy-waiting
- **Fix**: Use proper sleep intervals and add more sophisticated monitoring:
```cpp
while (!h.is_seed()) {
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    // Check for alerts and update UI if needed
}
```

**Correctness:**
- **Function**: `main`
- **Issue**: Unchecked return value from ses.add_torrent()
- **Severity**: High
- **Impact**: Could fail silently if torrent addition fails
- **Fix**: Check the return value from add_torrent:
```cpp
lt::add_torrent_params params;
params.url = argv[1];
lt::torrent_handle h = ses.add_torrent(params);
if (!h.is_valid()) {
    std::cerr << "Failed to add torrent" << std::endl;
    return 1;
}
```

**Code Quality:**
- **Function**: `main`
- **Issue**: Missing proper error handling for libtorrent functions
- **Severity**: Medium
- **Impact**: Poor user experience with vague error messages
- **Fix**: Add specific error handling and use descriptive error messages:
```cpp
try {
    // ... torrent addition code
} catch (const lt::invalid_handle& e) {
    std::cerr << "Invalid torrent handle: " << e.what() << std::endl;
    return 1;
} catch (const lt::alert_exception& e) {
    std::cerr << "Alert exception: " << e.what() << std::endl;
    return 1;
}
```

### Modernization Opportunities

- **Add [[nodiscard]] attribute** to the function to indicate that the return value is important:
```cpp
[[nodiscard]] int main(int argc, char const* argv[])
```

- **Use std::string_view** for command line arguments to avoid string copying:
```cpp
int main(int argc, std::string_view argv[])
```

- **Use constexpr for constants** where appropriate:
```cpp
constexpr int MIN_ARGS = 2;
```

- **Use std::expected (C++23) or std::optional** for error handling:
```cpp
std::expected<int, std::string> runDownload(std::string_view magnetUrl)
```

### Refactoring Suggestions

1. **Split into smaller functions**:
   - `parseArguments(int argc, char const* argv[])`
   - `validateMagnetUrl(std::string_view url)`
   - `createSession()`
   - `addTorrent(lt::session& ses, std::string_view url)`
   - `monitorDownload(lt::torrent_handle& handle)`
   - `handleErrors(std::exception const& e)`

2. **Move torrent handling logic into a separate class**:
   - Create a `TorrentDownloader` class with methods for adding, monitoring, and managing torrents.

3. **Extract configuration into a separate function**:
   - Move session configuration to a `createSessionSettings()` function.

### Performance Optimizations

1. **Use move semantics** for string parameters:
```cpp
int main(int argc, std::string_view argv)
```

2. **Return by value for RVO** where appropriate:
```cpp
std::optional<std::string> getDownloadPath() const
```

3. **Use string_view for read-only string parameters**:
```cpp
void processMagnetUrl(std::string_view url)
```

4. **Add noexcept where applicable**:
```cpp
int main(int argc, char const* argv[]) noexcept
```