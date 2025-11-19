# C++ API Documentation: Custom Storage Implementation

## temp_storage

- **Signature**: `explicit temp_storage(lt::file_storage const& fs)`
- **Description**: Constructor for a temporary storage implementation that uses in-memory storage. This class implements the `lt::storage_interface` concept and manages file data in memory.
- **Parameters**:
  - `fs` (lt::file_storage const&): The file storage object describing the torrent's file layout. This must be valid and cannot be modified while the storage is in use.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
lt::file_storage fs;
// populate fs with file information
auto storage = temp_storage(fs);
```
- **Preconditions**: The `fs` parameter must be valid and remain valid for the lifetime of the storage object.
- **Postconditions**: The storage object is initialized with the provided file storage configuration.
- **Thread Safety**: Not thread-safe (constructor)
- **Complexity**: O(1) time, O(n) space where n is the number of files
- **See Also**: `temp_disk_io`, `temp_disk_constructor`

## readv

- **Signature**: `lt::span<char const> readv(lt::peer_request const r, lt::storage_error& ec) const`
- **Description**: Reads data from the specified piece and offset into a buffer. This function is called by libtorrent when a peer requests data.
- **Parameters**:
  - `r` (lt::peer_request const&): The request specifying which piece and offset to read from.
  - `ec` (lt::storage_error&): Error code that will be set if an error occurs.
- **Return Value**: A span of const char representing the data read. Returns an empty span if no data is available or an error occurs.
- **Exceptions/Errors**: Sets error code to `boost::asio::error::eof` if the requested piece doesn't exist in memory.
- **Example**:
```cpp
lt::peer_request req{0, 0, 1024};
lt::storage_error ec;
auto data = storage.readv(req, ec);
if (ec.ec) {
    // handle error
}
```
- **Preconditions**: The storage object must be properly initialized and the requested piece must exist.
- **Postconditions**: Returns data from the specified piece and offset, or an empty span if the piece doesn't exist.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) time, O(1) space
- **See Also**: `writev`, `hash`, `hash2`

## writev

- **Signature**: `void writev(lt::span<char const> const b, lt::piece_index_t const piece, int const offset)`
- **Description**: Writes data to the specified piece and offset. This function is called by libtorrent when a peer sends data that needs to be stored.
- **Parameters**:
  - `b` (lt::span<char const> const&): The data to write to storage.
 