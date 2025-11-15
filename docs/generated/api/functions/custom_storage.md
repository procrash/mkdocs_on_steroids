# Custom Storage API Documentation

## temp_storage

- **Signature**: `explicit temp_storage(lt::file_storage const& fs)`
- **Description**: Constructs a temporary storage object that holds file data in memory. This is a simple in-memory storage implementation that stores file data in a map from piece indices to byte arrays. The storage is designed to be used with libtorrent's custom storage interface.
- **Parameters**:
  - `fs` (lt::file_storage const&): The file storage object that describes the torrent's file layout. This must be valid and cannot be modified during the storage's lifetime.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
lt::file_storage fs;
// populate fs with file information
auto storage = temp_storage(fs);
```
- **Preconditions**: `fs` must be a valid file storage object
- **Postconditions**: The storage object is initialized with the file storage information
- **Thread Safety**: Not thread-safe (constructors are not thread-safe)
- **Complexity**: O(n) where n is the number of files
- **See Also**: `temp_disk_io`, `new_torrent`

## readv

- **Signature**: `lt::span<char const> readv(lt::peer_request const r, lt::storage_error& ec) const`
- **Description**: Reads a block of data from the specified piece and offset. This function is part of the custom storage interface and is called by libtorrent to retrieve data from the storage.
- **Parameters**:
  - `r` (lt::peer_request const): The request specifying which piece and offset to read from. The piece index must be valid.
  - `ec` (lt::storage_error&): Error code that will be set if an error occurs during the read operation.
- **Return Value**: 
  - `lt::span<char const>`: A span containing the requested data, or an empty span if an error occurs.
- **Exceptions/Errors**: 
  - `lt::operation_t::file_read`: Operation failed due to missing piece data
  - `boost::asio::error::eof`: The requested piece does not exist in the storage
- **Example**:
```cpp
lt::peer_request req{0, 0, 1024};
lt::storage_error ec;
auto data = storage.readv(req, ec);
if (data.empty()) {
    std::cerr << "Error reading data: " << ec.ec.message() << std::endl;
}
```
- **Preconditions**: The storage must be initialized and the piece index must be valid
- **Postconditions**: Returns the requested data or an empty span if an error occurs
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) average case, O(log n) worst case for map lookup
- **See Also**: `writev`, `hash`, `hash2`

## writev

- **Signature**: `void writev(lt::span<char const> const b, lt::piece_index_t const piece, int const offset)`
- **Description**: Writes data to the specified piece and offset. This function is part of the custom storage interface and is called by libtorrent to store data in the storage.
- **Parameters**:
  - `b` (lt::span<char const> const): The data to write, must not be null
  - `piece` (lt::piece_index_t const): The piece index to write to, must be valid
  - `offset` (int const): The offset within the piece to start writing, must be within bounds
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
lt::span<char const> data = ...; // data to write
storage.writev(data, 0, 0);
```
- **Preconditions**: The storage must be initialized and the piece index must be valid
- **Postconditions**: The data is written to the specified location in the storage
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) average case, O(log n) worst case for map lookup
- **See Also**: `readv`, `hash`, `hash2`

## hash

- **Signature**: `lt::sha1_hash hash(lt::piece_index_t const piece, lt::span<lt::sha256_hash> const block_hashes, lt::storage_error& ec) const`
- **Description**: Computes the SHA-1 hash of a piece. This function is part of the custom storage interface and is called by libtorrent to verify the integrity of pieces.
- **Parameters**:
  - `piece` (lt::piece_index_t const): The piece index to hash, must be valid
  - `block_hashes` (lt::span<lt::sha256_hash> const): The span of SHA-256 hashes for the piece blocks, must be valid
  - `ec` (lt::storage_error&): Error code that will be set if an error occurs during the hash computation
- **Return Value**: 
  - `lt::sha1_hash`: The computed SHA-1 hash of the piece, or a zero hash if an error occurs
- **Exceptions/Errors**: 
  - `lt::operation_t::file_read`: Operation failed due to missing piece data
  - `boost::asio::error::eof`: The requested piece does not exist in the storage
- **Example**:
```cpp
lt::sha1_hash hash = storage.hash(0, block_hashes, ec);
if (hash == lt::sha1_hash{}) {
    std::cerr << "Error computing hash: " << ec.ec.message() << std::endl;
}
```
- **Preconditions**: The storage must be initialized and the piece index must be valid
- **Postconditions**: Returns the SHA-1 hash of the piece or a zero hash if an error occurs
- **Thread Safety**: Thread-safe
- **Complexity**: O(n) where n is the number of bytes in the piece
- **See Also**: `hash2`, `readv`, `writev`

## hash2

- **Signature**: `lt::sha256_hash hash2(lt::piece_index_t const piece, int const offset, lt::storage_error& ec)`
- **Description**: Computes the SHA-256 hash of a specific block within a piece. This function is part of the custom storage interface and is called by libtorrent to verify the integrity of piece blocks.
- **Parameters**:
  - `piece` (lt::piece_index_t const): The piece index to hash, must be valid
  - `offset` (int const): The offset within the piece to start hashing, must be within bounds
  - `ec` (lt::storage_error&): Error code that will be set if an error occurs during the hash computation
- **Return Value**: 
  - `lt::sha256_hash`: The computed SHA-256 hash of the block, or a zero hash if an error occurs
- **Exceptions/Errors**: 
  - `lt::operation_t::file_read`: Operation failed due to missing piece data
  - `boost::asio::error::eof`: The requested piece does not exist in the storage
- **Example**:
```cpp
lt::sha256_hash hash = storage.hash2(0, 0, ec);
if (hash == lt::sha256_hash{}) {
    std::cerr << "Error computing hash: " << ec.ec.message() << std::endl;
}
```
- **Preconditions**: The storage must be initialized and the piece index must be valid
- **Postconditions**: Returns the SHA-256 hash of the block or a zero hash if an error occurs
- **Thread Safety**: Thread-safe
- **Complexity**: O(n) where n is the number of bytes in the block
- **See Also**: `hash`, `readv`, `writev`

## piece_size

- **Signature**: `int piece_size(lt::piece_index_t piece) const`
- **Description**: Returns the size of a piece in bytes. This function is part of the custom storage interface and is called by libtorrent to determine the size of pieces.
- **Parameters**:
  - `piece` (lt::piece_index_t): The piece index to query, must be valid
- **Return Value**: 
  - `int`: The size of the piece in bytes, or the size of the last piece if it's smaller
- **Exceptions/Errors**: None
- **Example**:
```cpp
int size = storage.piece_size(0);
std::cout << "Piece 0 size: " << size << " bytes" << std::endl;
```
- **Preconditions**: The storage must be initialized and the piece index must be valid
- **Postconditions**: Returns the size of the specified piece
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `temp_storage`, `readv`, `writev`

## pop

- **Signature**: `lt::storage_index_t pop(std::vector<lt::storage_index_t>& q)`
- **Description**: Removes and returns the last element from a vector of storage indices. This function is used to manage the free slots pool in the temp_disk_io class.
- **Parameters**:
  - `q` (std::vector<lt::storage_index_t>&): The vector of storage indices to pop from, must not be empty
- **Return Value**: 
  - `lt::storage_index_t`: The storage index that was removed from the vector
- **Exceptions/Errors**: 
  - `TORRENT_ASSERT`: Throws an assertion failure if the vector is empty
- **Example**:
```cpp
std::vector<lt::storage_index_t> free_slots = {0, 1, 2};
lt::storage_index_t idx = pop(free_slots);
// free_slots now contains {0, 1}
```
- **Preconditions**: The vector must not be empty
- **Postconditions**: The last element is removed from the vector and returned
- **Thread Safety**: Not thread-safe (no synchronization)
- **Complexity**: O(1)
- **See Also**: `new_torrent`, `remove_torrent`

## temp_disk_io

- **Signature**: `explicit temp_disk_io(lt::io_context& ioc)`
- **Description**: Constructs a disk I/O interface for temporary storage. This class manages the lifetime of temporary storage objects and handles asynchronous operations.
- **Parameters**:
  - `ioc` (lt::io_context&): The I/O context to use for asynchronous operations, must be valid
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
lt::io_context ioc;
auto disk_io = temp_disk_io(ioc);
```
- **Preconditions**: The I/O context must be valid and cannot be destroyed while the disk_io object is in use
- **Postconditions**: The disk I/O interface is initialized with the specified I/O context
- **Thread Safety**: Not thread-safe (constructors are not thread-safe)
- **Complexity**: O(1)
- **See Also**: `temp_disk_constructor`, `new_torrent`, `remove_torrent`

## settings_updated

- **Signature**: `void settings_updated() override`
- **Description**: Called when settings are updated. This function is part of the disk interface and is overridden to handle setting updates. In this implementation, it does nothing.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
// This function is called automatically when settings change
```
- **Preconditions**: The disk interface must be properly initialized
- **Postconditions**: No changes to the state of the disk interface
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `temp_disk_io`, `temp_disk_constructor`

## new_torrent

- **Signature**: `lt::storage_holder new_torrent(lt::storage_params const& params, std::shared_ptr<void> const&) override`
- **Description**: Creates a new storage object for a torrent. This function is part of the disk interface and is called by libtorrent to create storage for a new torrent.
- **Parameters**:
  - `params` (lt::storage_params const&): The storage parameters for the torrent, must be valid
  - `shared_ptr<void> const&`: Optional shared pointer to additional data, currently unused
- **Return Value**: 
  - `lt::storage_holder`: A holder for the new storage object
- **Exceptions/Errors**: 
  - `lt::storage_error`: If there's an error creating the storage
- **Example**:
```cpp
lt::storage_params params;
auto storage = new_torrent(params, nullptr);
```
- **Preconditions**: The disk interface must be properly initialized
- **Postconditions**: A new storage object is created and returned
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) average case, O(log n) worst case for map lookup
- **See Also**: `remove_torrent`, `temp_storage`, `temp_disk_io`

## remove_torrent

- **Signature**: `void remove_torrent(lt::storage_index_t const idx) override`
- **Description**: Removes a torrent storage object. This function is part of the disk interface and is called by libtorrent to remove a torrent's storage.
- **Parameters**:
  - `idx` (lt::storage_index_t const): The index of the torrent to remove, must be valid
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
remove_torrent(0);
```
- **Preconditions**: The disk interface must be properly initialized and the index must be valid
- **Postconditions**: The storage object at the specified index is removed and the slot is marked as free
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `new_torrent`, `temp_disk_io`, `pop`

## abort

- **Signature**: `void abort(bool) override`
- **Description**: Aborts any ongoing operations. This function is part of the disk interface and is called by libtorrent when the session is shutting down or when operations need to be canceled.
- **Parameters**:
  - `bool`: Indicates whether to abort all operations (true) or just the current one (false), currently unused
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
abort(true);
```
- **Preconditions**: The disk interface must be properly initialized
- **Postconditions**: Any ongoing operations are aborted
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `temp_disk_io`, `temp_disk_constructor`

## async_read

- **Signature**: `void async_read(lt::storage_index_t storage, lt::peer_request const& r, std::function<void(lt::disk_buffer_holder block, lt::storage_error const& se)> handler, lt::disk_job_flags_t)`
- **Description**: Asynchronously reads data from the storage. This function is part of the disk interface and is called by libtorrent to read data from a torrent.
- **Parameters**:
  - `storage` (lt::storage_index_t): The index of the storage object to read from, must be valid
  - `r` (lt::peer_request const&): The request specifying which piece and offset to read from, must be valid
  - `handler` (std::function<void(lt::disk_buffer_holder block, lt::storage_error const& se)>): The callback to call when the read is complete
  - `lt::disk_job_flags_t`: Flags controlling the behavior of the read operation, currently unused
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
async_read(0, request, [](lt::disk_buffer_holder block, lt::storage_error const& se) {
    if (!se.ec) {
        // process data
    }
}, lt::disk_job_flags_t::default_flags);
```
- **Preconditions**: The disk interface must be properly initialized and the storage index must be valid
- **Postconditions**: The read operation is initiated and the handler will be called when complete
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) average case, O(log n) worst case for map lookup
- **See Also**: `async_write`, `async_hash`, `async_hash2`

## async_write

- **Signature**: `bool async_write(lt::storage_index_t storage, lt::peer_request const& r, char const* buf, std::shared_ptr<lt::disk_observer>, std::function<void(lt::storage_error const&)> handler, lt::disk_job_flags_t)`
- **Description**: Asynchronously writes data to the storage. This function is part of the disk interface and is called by libtorrent to write data to a torrent.
- **Parameters**:
  - `storage` (lt::storage_index_t): The index of the storage object to write to, must be valid
  - `r` (lt::peer_request const&): The request specifying which piece and offset to write to, must be valid
  - `buf` (char const*): The buffer containing the data to write, must not be null
  - `std::shared_ptr<lt::disk_observer>`: Observer for the write operation, currently unused
  - `handler` (std::function<void(lt::storage_error const&)>): The callback to call when the write is complete
  - `lt::disk_job_flags_t`: Flags controlling the behavior of the write operation, currently unused
- **Return Value**: 
  - `bool`: True if the write operation was successfully started
- **Exceptions/Errors**: None
- **Example**:
```cpp
async_write(0, request, data, nullptr, [](lt::storage_error const& se) {
    if (se.ec) {
        std::cerr << "Write failed: " << se.ec.message() << std::endl;
    }
}, lt::disk_job_flags_t::default_flags);
```
- **Preconditions**: The disk interface must be properly initialized and the storage index must be valid
- **Postconditions**: The write operation is initiated and the handler will be called when complete
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) average case, O(log n) worst case for map lookup
- **See Also**: `async_read`, `async_hash`, `async_hash2`

## async_hash

- **Signature**: `void async_hash(lt