# libtorrent Python Bindings API Documentation

## set_hash

- **Signature**: `void set_hash(create_torrent& c, piece_index_t p, bytes const& b)`
- **Description**: Sets the SHA1 hash for a specific piece in the torrent. This function is used to manually specify the hash of a piece in the torrent metadata, which is essential for creating a valid torrent file.
- **Parameters**:
  - `c` (create_torrent&): Reference to the create_torrent object that will have the hash set.
  - `p` (piece_index_t): The index of the piece to set the hash for. Must be a valid piece index within the torrent's piece count.
  - `b` (bytes const&): The SHA1 hash bytes for the piece. This must be exactly 20 bytes long, which is the standard length for SHA1 hashes.
- **Return Value**: None. The function does not return a value.
- **Exceptions/Errors**: 
  - The function does not throw exceptions. However, if the provided hash is not exactly 20 bytes, it may result in undefined behavior or runtime errors.
  - The function relies on the underlying `create_torrent::set_hash` method, which may throw exceptions if the piece index is invalid.
- **Example**:
```cpp
// Set the hash for piece 0 in a torrent
bytes hash_data = create_bytes(20, 0); // Create a 20-byte array of zeros
set_hash(torrent, 0, hash_data);
```
- **Preconditions**: 
  - The `create_torrent` object must be properly initialized.
  - The piece index must be valid (less than the total number of pieces).
  - The hash data must be exactly 20 bytes long.
- **Postconditions**: 
  - The specified piece will have the provided SHA1 hash set.
  - The torrent metadata will be updated to reflect this hash.
- **Thread Safety**: Not thread-safe. Concurrent access to the same `create_torrent` object may result in undefined behavior.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `set_file_hash`, `create_torrent::set_hash`

## set_file_hash

- **Signature**: `void set_file_hash(create_torrent& c, file_index_t f, bytes const& b)`
- **Description**: Sets the SHA1 hash for a specific file in the torrent. This function is used to manually specify the hash of a file in the torrent metadata, which is essential for creating a valid torrent file.
- **Parameters**:
  - `c` (create_torrent&): Reference to the create_torrent object that will have the file hash set.
  - `f` (file_index_t): The index of the file to set the hash for. Must be a valid file index within the torrent's file count.
  - `b` (bytes const&): The SHA1 hash bytes for the file. This must be exactly 20 bytes long, which is the standard length for SHA1 hashes.
- **Return Value**: None. The function does not return a value.
- **Exceptions/Errors**: 
  - The function does not throw exceptions. However, if the provided hash is not exactly 20 bytes, it may result in undefined behavior or runtime errors.
  - The function relies on the underlying `create_torrent::set_file_hash` method, which may throw exceptions if the file index is invalid.
- **Example**:
```cpp
// Set the hash for file 0 in a torrent
bytes hash_data = create_bytes(20, 0); // Create a 20-byte array of zeros
set_file_hash(torrent, 0, hash_data);
```
- **Preconditions**: 
  - The `create_torrent` object must be properly initialized.
  - The file index must be valid (less than the total number of files).
  - The hash data must be exactly 20 bytes long.
- **Postconditions**: 
  - The specified file will have the provided SHA1 hash set.
  - The torrent metadata will be updated to reflect this hash.
- **Thread Safety**: Not thread-safe. Concurrent access to the same `create_torrent` object may result in undefined behavior.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `set_hash`, `create_torrent::set_file_hash`

## set_piece_hashes_callback

- **Signature**: `void set_piece_hashes_callback(create_torrent& c, std::string const& p, boost::python::object cb)`
- **Description**: Sets piece hashes for a torrent using a callback function. This function computes the SHA1 hash for each piece of the torrent data and calls the provided callback function for each piece processed. This is useful for providing progress updates during the hash computation process.
- **Parameters**:
  - `c` (create_torrent&): Reference to the create_torrent object that will have piece hashes computed.
  - `p` (std::string const&): The path to the directory containing the torrent files. This is used to locate the files to hash.
  - `cb` (boost::python::object): A Python callable object that will be called with the piece index as an argument for each piece processed. This allows the caller to track progress.
- **Return Value**: None. The function does not return a value.
- **Exceptions/Errors**: 
  - The function may throw exceptions if the file system operations fail (e.g., file not found, permission denied).
  - The callback function may throw exceptions if it is not properly implemented.
- **Example**:
```cpp
// Set piece hashes with a callback for progress tracking
void progress_callback(piece_index_t piece) {
    std::cout << "Processing piece " << piece << std::endl;
}
set_piece_hashes_callback(torrent, "/path/to/files", boost::python::object(progress_callback));
```
- **Preconditions**: 
  - The `create_torrent` object must be properly initialized with file information.
  - The specified path must exist and contain the torrent files.
  - The callback function must be callable and accept a single piece_index_t parameter.
- **Postconditions**: 
  - All pieces in the torrent will have their SHA1 hashes computed and set.
  - The callback function will be called for each piece processed.
- **Thread Safety**: Not thread-safe. Concurrent access to the same `create_torrent` object may result in undefined behavior.
- **Complexity**: O(n) time complexity, where n is the total number of pieces, O(1) space complexity.
- **See Also**: `set_piece_hashes`, `set_piece_hashes_callback` (overloaded version)

## set_piece_hashes_callback

- **Signature**: `void set_piece_hashes_callback(create_torrent& c, std::string const& p, boost::python::object cb)`
- **Description**: Sets piece hashes for a torrent using a callback function with error handling. This function computes the SHA1 hash for each piece of the torrent data and calls the provided callback function for each piece processed, while also handling errors through an error code parameter.
- **Parameters**:
  - `c` (create_torrent&): Reference to the create_torrent object that will have piece hashes computed.
  - `p` (std::string const&): The path to the directory containing the torrent files. This is used to locate the files to hash.
  - `cb` (boost::python::object): A Python callable object that will be called with the piece index as an argument for each piece processed. This allows the caller to track progress.
- **Return Value**: None. The function does not return a value.
- **Exceptions/Errors**: 
  - The function may throw exceptions if the file system operations fail (e.g., file not found, permission denied).
  - The callback function may throw exceptions if it is not properly implemented.
  - The error code parameter allows the caller to check for errors after the function returns.
- **Example**:
```cpp
// Set piece hashes with error handling and progress tracking
error_code ec;
void progress_callback(piece_index_t piece) {
    std::cout << "Processing piece " << piece << std::endl;
}
set_piece_hashes_callback(torrent, "/path/to/files", boost::python::object(progress_callback));
if (ec) {
    std::cerr << "Error setting piece hashes: " << ec.message() << std::endl;
}
```
- **Preconditions**: 
  - The `create_torrent` object must be properly initialized with file information.
  - The specified path must exist and contain the torrent files.
  - The callback function must be callable and accept a single piece_index_t parameter.
- **Postconditions**: 
  - All pieces in the torrent will have their SHA1 hashes computed and set if no errors occur.
  - The callback function will be called for each piece processed.
  - The error code will be set if any errors occur during the process.
- **Thread Safety**: Not thread-safe. Concurrent access to the same `create_torrent` object may result in undefined behavior.
- **Complexity**: O(n) time complexity, where n is the total number of pieces, O(1) space complexity.
- **See Also**: `set_piece_hashes`, `set_piece_hashes_callback` (overloaded version)

## set_piece_hashes0

- **Signature**: `void set_piece_hashes0(create_torrent& c, std::string const & s)`
- **Description**: Sets piece hashes for a torrent using a default callback and error handling. This function computes the SHA1 hash for each piece of the torrent data and stores the results in the create_torrent object. It is a simplified version of the more complex set_piece_hashes functions, using default error handling and no callback.
- **Parameters**:
  - `c` (create_torrent&