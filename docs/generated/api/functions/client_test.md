```markdown
# libtorrent Client Test API Documentation

## sleep_and_input

- **Signature**: `bool sleep_and_input(int* c, lt::time_duration const sleep)`
- **Description**: Checks for keyboard input with a timeout, returning true if input is available.
- **Parameters**:
  - `c` (int*): Pointer to store the pressed key character. The function stores the pressed character here.
  - `sleep` (lt::time_duration const): Duration to wait for input before returning.
- **Return Value**:
  - `true`: Input was received during the timeout period.
  - `false`: No input was received within the specified time.
- **Exceptions/Errors**:
  - No exceptions thrown. Returns false if no input is detected.
- **Example**:
```cpp
int key;
if (sleep_and_input(&key, lt::seconds(1))) {
    std::printf("Key pressed: %d\n", key);
} else {
    std::printf("No input received\n");
}
```
- **Preconditions**:
  - `c` must be a valid pointer.
  - `sleep` must be a positive duration.
- **Postconditions**:
  - If input is received, `*c` contains the pressed key.
  - Returns false if no input is received within the timeout period.
- **Thread Safety**: Not thread-safe. Uses `_kbhit()` and `_getch()` which are not thread-safe.
- **Complexity**: O(1) time complexity.
- **See Also**: `set_keypress`, `sleep_and_input` (alternative implementation)

## set_keypress

- **Signature**: `set_keypress(std::uint8_t const mode = 0)`
- **Description**: Constructor for the `set_keypress` class. Configures terminal settings to enable single-character input mode.
- **Parameters**:
  - `mode` (std::uint8_t const): Bitmask indicating which terminal settings to modify (e.g., echo control).
- **Return Value**: None.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
{
    set_keypress s_; // Sets terminal to single-character mode
    // ... use single-character input
} // Destructor restores terminal settings
```
- **Preconditions**: Must be called in a terminal environment.
- **Postconditions**:
  - Terminal is configured for single-character input mode.
  - Destructor restores original terminal settings.
- **Thread Safety**: Not thread-safe. Changes terminal state globally.
- **Complexity**: O(1) time complexity.
- **See Also**: `~set_keypress`, `sleep_and_input`

## set_keypress

- **Signature**: `~set_keypress()`
- **Description**: Destructor for the `set_keypress` class. Restores original terminal settings.
- **Parameters**: None.
- **Return Value**: None.
- **Exceptions/Errors**: None.
- **Example**:
```cpp
{
    set_keypress s_; // Sets terminal settings
    // ... use terminal
} // Destructor restores original settings
```
- **Preconditions**: `set_keypress` object must have been constructed.
- **Postconditions**: Terminal settings are restored to original state.
- **Thread Safety**: Not thread-safe. Changes terminal state globally.
- **Complexity**: O(1) time complexity.
- **See Also**: `set_keypress`

## sleep_and_input

- **Signature**: `bool sleep_and_input(int* c, lt::time_duration const sleep)`
- **Description**: Checks for keyboard input with a timeout using select() system call, returning true if input is available.
- **Parameters**:
  - `c` (int*): Pointer to store the pressed key character.
  - `sleep` (lt::time_duration const): Duration to wait for input before returning.
- **Return Value**:
  - `true`: Input was received during the timeout period.
  - `false`: No input was received within the specified time.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
int key;
if (sleep_and_input(&key, lt::seconds(1))) {
    std::printf("Key pressed: %d\n", key);
} else {
    std::printf("No input received\n");
}
```
- **Preconditions**:
  - `c` must be a valid pointer.
  - `sleep` must be a positive duration.
- **Postconditions**:
  - If input is received, `*c` contains the pressed key.
  - Returns false if no input is received within the timeout period.
- **Thread Safety**: Not thread-safe. Uses `select()` and file descriptor operations.
- **Complexity**: O(1) time complexity.
- **See Also**: `set_keypress`, `sleep_and_input` (alternative implementation)

## to_hex

- **Signature**: `std::string to_hex(lt::sha1_hash const& s)`
- **Description**: Converts a SHA-1 hash to its hexadecimal string representation.
- **Parameters**:
  - `s` (lt::sha1_hash const&): The SHA-1 hash to convert.
- **Return Value**: A string containing the hexadecimal representation of the hash.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
lt::sha1_hash hash = lt::sha1_hash::from_string("a1b2c3d4e5f6g7h8i9j0");
std::string hex = to_hex(hash);
std::printf("Hex: %s\n", hex.c_str());
```
- **Preconditions**: `s` must be a valid SHA-1 hash.
- **Postconditions**: Returns a string with the hexadecimal representation of the hash.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time complexity.
- **See Also**: `lt::sha1_hash`, `to_hex`

## load_file

- **Signature**: `bool load_file(std::string const& filename, std::vector<char>& v, int limit = 8000000)`
- **Description**: Loads a file into a vector, with size limit checking.
- **Parameters**:
  - `filename` (std::string const&): Path to the file to load.
  - `v` (std::vector<char>&): Vector to store the file contents.
  - `limit` (int): Maximum file size allowed (default: 8,000,000 bytes).
- **Return Value**:
  - `true`: File loaded successfully.
  - `false`: File could not be loaded (too large or file not found).
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::vector<char> data;
if (load_file("example.txt", data)) {
    std::printf("File loaded successfully\n");
} else {
    std::printf("Failed to load file\n");
}
```
- **Preconditions**:
  - `filename` must be a valid file path.
  - `v` must be a valid vector.
- **Postconditions**:
  - If successful, `v` contains the file contents.
  - Returns false if the file is too large or cannot be opened.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time complexity, where n is file size.
- **See Also**: `save_file`, `std::vector`

## is_absolute_path

- **Signature**: `bool is_absolute_path(std::string const& f)`
- **Description**: Checks if a path is absolute.
- **Parameters**:
  - `f` (std::string const&): Path to check.
- **Return Value**:
  - `true`: Path is absolute.
  - `false`: Path is relative.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
if (is_absolute_path("C:\\Windows\\system32")) {
    std::printf("Path is absolute\n");
} else {
    std::printf("Path is relative\n");
}
```
- **Preconditions**: `f` must be a valid string.
- **Postconditions**: Returns true if the path is absolute, false otherwise.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time complexity, where n is path length.
- **See Also**: `make_absolute_path`, `path_append`

## path_append

- **Signature**: `std::string path_append(std::string const& lhs, std::string const& rhs)`
- **Description**: Appends two path components, handling platform-specific path separators.
- **Parameters**:
  - `lhs` (std::string const&): Base path.
  - `rhs` (std::string const&): Path to append.
- **Return Value**: Combined path string.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::string path = path_append("C:\\Users", "Documents");
std::printf("Path: %s\n", path.c_str());
```
- **Preconditions**:
  - `lhs` and `rhs` must be valid strings.
  - `rhs` should not be empty unless `lhs` is also empty.
- **Postconditions**: Returns a properly formatted path with appropriate separator.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time complexity, where n is total path length.
- **See Also**: `make_absolute_path`, `is_absolute_path`

## make_absolute_path

- **Signature**: `std::string make_absolute_path(std::string const& p)`
- **Description**: Converts a relative path to an absolute path.
- **Parameters**:
  - `p` (std::string const&): Relative path to convert.
- **Return Value**: Absolute path.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::string absolute = make_absolute_path("Documents\\file.txt");
std::printf("Absolute path: %s\n", absolute.c_str());
```
- **Preconditions**: `p` must be a valid string.
- **Postconditions**: Returns the absolute path equivalent of the input.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time complexity, where n is path length.
- **See Also**: `path_append`, `is_absolute_path`

## print_endpoint

- **Signature**: `std::string print_endpoint(lt::tcp::endpoint const& ep)`
- **Description**: Converts a TCP endpoint to a string representation with proper formatting for IPv6 addresses.
- **Parameters**:
  - `ep` (lt::tcp::endpoint const&): Endpoint to convert.
- **Return Value**: String representation of the endpoint.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
lt::tcp::endpoint ep(lt::address_v4::from_string("192.168.1.1"), 8080);
std::string str = print_endpoint(ep);
std::printf("Endpoint: %s\n", str.c_str());
```
- **Preconditions**: `ep` must be a valid endpoint.
- **Postconditions**: Returns a string representation of the endpoint.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time complexity.
- **See Also**: `lt::tcp::endpoint`, `print_endpoint`

## peer_index

- **Signature**: `int peer_index(lt::tcp::endpoint addr, std::vector<lt::peer_info> const& peers)`
- **Description**: Finds the index of a specific peer in a vector of peers.
- **Parameters**:
  - `addr` (lt::tcp::endpoint): The peer endpoint to find.
  - `peers` (std::vector<lt::peer_info> const&): Vector of peer information.
- **Return Value**:
  - Index of the peer if found.
  - `-1` if the peer is not found.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
int index = peer_index(ep, peers);
if (index != -1) {
    std::printf("Peer found at index: %d\n", index);
} else {
    std::printf("Peer not found\n");
}
```
- **Preconditions**:
  - `peers` must be a valid vector.
  - `addr` must be a valid endpoint.
- **Postconditions**: Returns the index of the peer, or -1 if not found.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time complexity, where n is the number of peers.
- **See Also**: `lt::peer_info`, `std::vector`

## base32encode_i2p

- **Signature**: `void base32encode_i2p(lt::sha256_hash const& s, std::string& out, int limit)`
- **Description**: Encodes a SHA-256 hash to base32 format for I2P addresses.
- **Parameters**:
  - `s` (lt::sha256_hash const&): Hash to encode.
  - `out` (std::string&): Output string to store the encoded result.
  - `limit` (int): Maximum length of output.
- **Return Value**: None.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
lt::sha256_hash hash = lt::sha256_hash::from_string("a1b2c3d4e5f6g7h8i9j0");
std::string result;
base32encode_i2p(hash, result, 50);
std::printf("Base32: %s\n", result.c_str());
```
- **Preconditions**:
  - `s` must be a valid SHA-256 hash.
  - `out` must be a valid string.
  - `limit` must be positive.
- **Postconditions**: `out` contains the base32-encoded hash.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time complexity, where n is hash size.
- **See Also**: `lt::sha256_hash`, `base32encode_i2p`

## print_peer_info

- **Signature**: `int print_peer_info(std::string& out, std::vector<lt::peer_info> const& peers, int max_lines)`
- **Description**: Prints peer information to a string with formatting.
- **Parameters**:
  - `out` (std::string&): Output string to append results.
  - `peers` (std::vector<lt::peer_info> const&): Vector of peer information.
  - `max_lines` (int): Maximum number of lines to print.
- **Return Value**: Number of lines printed.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::string output;
int lines = print_peer_info(output, peers, 10);
std::printf("Printed %d lines\n", lines);
```
- **Preconditions**:
  - `out` must be a valid string.
  - `peers` must be a valid vector.
  - `max_lines` must be positive.
- **Postconditions**: Appends peer information to `out` string.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time complexity, where n is number of peers.
- **See Also**: `lt::peer_info`, `std::vector`

## print_peer_legend

- **Signature**: `int print_peer_legend(std::string& out, int max_lines)`
- **Description**: Prints a legend for peer information display.
- **Parameters**:
  - `out` (std::string&): Output string to append results.
  - `max_lines` (int): Maximum number of lines to print.
- **Return Value**: Number of lines printed.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::string output;
int lines = print_peer_legend(output, 5);
std::printf("Printed %d lines\n", lines);
```
- **Preconditions**:
  - `out` must be a valid string.
  - `max_lines` must be positive.
- **Postconditions**: Appends legend information to `out` string.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time complexity.
- **See Also**: `print_peer_info`

## signal_handler

- **Signature**: `void signal_handler(int)`
- **Description**: Signal handler function that sets a global flag to terminate the main loop.
- **Parameters**:
  - `int`: Signal number (not used).
- **Return Value**: None.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
// Set up signal handler
signal(SIGINT, signal_handler);
```
- **Preconditions**: Must be called as a signal handler.
- **Postconditions**: Sets global `quit` flag to true.
- **Thread Safety**: Thread-safe only if `quit` is atomic or properly synchronized.
- **Complexity**: O(1) time complexity.
- **See Also**: `main`, `quit`

## print_settings

- **Signature**: `void print_settings(int const start, int const num, char const* const type)`
- **Description**: Prints settings names and types for the specified range.
- **Parameters**:
  - `start` (int const): Starting index of settings to print.
  - `num` (int const): Number of settings to print.
  - `type` (char const* const): Type string to append to each setting.
- **Return Value**: None.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
print_settings(0, 10, "string");
```
- **Preconditions**:
  - `start` must be non-negative.
  - `num` must be non-negative.
- **Postconditions**: Prints settings information to stdout.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time complexity, where n is number of settings.
- **See Also**: `lt::name_for_setting`

## assign_setting

- **Signature**: `void assign_setting(lt::settings_pack& settings, std::string const& key, char const* value)`
- **Description**: Assigns a value to a libtorrent setting by name.
- **Parameters**:
  - `settings` (lt::settings_pack&): Settings pack to modify.
  - `key` (std::string const&): Name of the setting.
  - `value` (char const*): Value to assign