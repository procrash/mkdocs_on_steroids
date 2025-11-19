# libtorrent C++ Library API Documentation

## Function: find_handle

- **Signature**: `int find_handle(lt::torrent_handle h)`
- **Description**: Searches for a torrent handle in the global handles vector and returns its index if found.
- **Parameters**:
  - `h` (lt::torrent_handle): The torrent handle to search for in the global handles vector.
- **Return Value**:
  - Returns the index of the handle in the handles vector if found.
  - Returns -1 if the handle is not found in the handles vector.
- **Exceptions/Errors**:
  - No exceptions are thrown.
- **Example**:
```cpp
int index = find_handle(my_handle);
if (index != -1) {
    // Handle found at index
}
```
- **Preconditions**: The handles vector must be initialized and contain valid torrent handles.
- **Postconditions**: The function returns the index of the handle if found, or -1 if not found.
- **Thread Safety**: Not thread-safe - requires external synchronization.
- **Complexity**: O(n) where n is the number of handles in the vector.
- **See Also**: `get_handle()`, `add_handle()`

## Function: get_handle

- **Signature**: `lt::torrent_handle get_handle(int i)`
- **Description**: Retrieves a torrent handle from the global handles vector by index.
- **Parameters**:
  - `i` (int): The index of the handle to retrieve. Must be within the bounds of the handles vector.
- **Return Value**:
  - Returns the torrent handle at index i if it exists.
  - Returns a default-constructed torrent handle if the index is invalid.
- **Exceptions/Errors**:
  - No exceptions are thrown.
- **Example**:
```cpp
lt::torrent_handle handle = get_handle(5);
if (handle.is_valid()) {
    // Handle is valid, use it
}
```
- **Preconditions**: The handles vector must be initialized and contain valid torrent handles.
- **Postconditions**: Returns the torrent handle at the specified index or a default-constructed handle if index is invalid.
- **Thread Safety**: Not thread-safe - requires external synchronization.
- **Complexity**: O(1) - constant time.
- **See Also**: `find_handle()`, `add_handle()`

## Function: add_handle

- **Signature**: `int add_handle(lt::torrent_handle const& h)`
- **Description**: Adds a torrent handle to the global handles vector, either by overwriting an invalid handle or by appending to the end.
- **Parameters**:
  - `h` (lt::torrent_handle const&): The torrent handle to add to the handles vector.
- **Return Value**:
  - Returns the index of the added handle.
  - Returns -1 if no invalid handle was found and the vector cannot be extended (though this shouldn't happen given the implementation).
- **Exceptions/Errors**:
  - No exceptions are thrown.
- **Example**:
```cpp
int index = add_handle(new_handle);
if (index != -1) {
    // Handle was successfully added
}
```
- **Preconditions**: The handles vector must be initialized.
- **Postconditions**: The torrent handle is added to the handles vector at the first invalid handle position or at the end.
- **Thread Safety**: Not thread-safe - requires external synchronization.
- **Complexity**: O(n) where n is the number of handles in the vector.
- **See Also**: `find_handle()`, `get_handle()`

## Function: set_int_value

- **Signature**: `int set_int_value(void* dst, int* size, int val)`
- **Description**: Copies an integer value to a destination buffer, ensuring the buffer is large enough.
- **Parameters**:
  - `dst` (void*): Pointer to the destination buffer where the integer will be stored.
  - `size` (int*): Pointer to the size of the destination buffer. This will be updated to the actual size used.
  - `val` (int): The integer value to copy to the destination buffer.
- **Return Value**:
  - Returns 0 if the value was successfully copied.
  - Returns -2 if the destination buffer is too small to hold the integer.
- **Exceptions/Errors**:
  - No exceptions are thrown.
- **Example**:
```cpp
int result;
int buffer[2];
int buffer_size = sizeof(buffer);
int status = set_int_value(buffer, &buffer_size, 42);
if (status == 0) {
    // Value was successfully set
}
```
- **Preconditions**: `dst` must be a valid pointer to a buffer, and `size` must be a valid pointer to a size value.
- **Postconditions**: The integer value is copied to the destination buffer, and the size parameter is updated to the actual size used.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) - constant time.
- **See Also**: None

## Function: copy_proxy_setting

- **Signature**: `void copy_proxy_setting(lt::proxy_settings* s, proxy_setting const* ps)`
- **Description**: Copies proxy settings from a C-style proxy setting structure to a libtorrent proxy settings structure.
- **Parameters**:
  - `s` (lt::proxy_settings*): Pointer to the destination libtorrent proxy settings structure.
  - `ps` (proxy_setting const*): Pointer to the source C-style proxy setting structure.
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions are thrown.
- **Example**:
```cpp
lt::proxy_settings proxy_settings;
proxy_setting c_style_settings = {/* initialize */};
copy_proxy_setting(&proxy_settings, &c_style_settings);
```
- **Preconditions**: Both `s` and `ps` must be valid pointers, and the structures they point to must be properly initialized.
- **Postconditions**: The proxy settings from `ps` are copied to `s`.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) - constant time.
- **See Also**: None

## Function: session_create

- **Signature**: `TORRENT_EXPORT void* session_create(int tag, ...)`
- **Description**: Creates a new libtorrent session with the specified configuration parameters.
- **Parameters**:
  - `tag` (int): The first tag in the variable argument list, used to identify the configuration parameter to follow.
  - `...`: Variable arguments containing configuration parameters and their values.
- **Return Value**:
  - Returns a pointer to the newly created session if successful.
  - Returns nullptr if session creation fails.
- **Exceptions/Errors**:
  - No exceptions are thrown.
- **Example**:
```cpp
void* session = session_create(SET_UPLOAD_RATE_LIMIT, 100, SET_DOWNLOAD_RATE_LIMIT, 50, TAG_END);
if (session != nullptr) {
    // Session created successfully
}
```
- **Preconditions**: The tag values must be valid session configuration tags, and the arguments must follow the correct format.
- **Postconditions**: A new session is created and initialized with the specified configuration.
- **Thread Safety**: Not thread-safe - requires external synchronization.
- **Complexity**: O(1) - constant time.
- **See Also**: `session_close()`, `session_set_settings()`

## Function: session_close

- **Signature**: `TORRENT_EXPORT void session_close(void* ses)`
- **Description**: Closes and destroys a libtorrent session.
- **Parameters**:
  - `ses` (void*):