# Connection Tester API Documentation

## generate_block

- **Signature**: `void generate_block(span<std::uint32_t> buffer, piece_index_t const piece, int const offset)`
- **Description**: Fills a buffer with a pattern based on the piece index and offset. This function generates a block of data with a specific pattern that can be used for testing purposes. The pattern is derived from the piece index and the offset within the piece.
- **Parameters**:
  - `buffer` (span<std::uint32_t>): The buffer to fill with the generated data. This must be a valid span that can hold at least `buffer.size()` elements.
  - `piece` (piece_index_t): The index of the piece to generate data for. This must be a valid piece index.
  - `offset` (int): The offset within the piece where the data should be generated. This should be a non-negative value.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function assumes that the `buffer` is valid and properly allocated.
- **Example**:
```cpp
std::vector<std::uint32_t> buffer(1024);
piece_index_t piece = 0;
int offset = 0;
generate_block(buffer, piece, offset);
```
- **Preconditions**:
  - The `buffer` must be a valid span with enough capacity to hold the data.
  - The `piece` must be a valid piece index.
  - The `offset` must be a non-negative value.
- **Postconditions**:
  - The `buffer` will be filled with data generated based on the piece index and offset.
- **Thread Safety**:
  - This function is thread-safe as it only writes to the provided buffer.
- **Complexity**:
  - Time Complexity: O(n) where n is the size of the buffer.
  - Space Complexity: O(1) additional space.
- **See Also**: `verify_piece`, `write_piece`

## leaf_path

- **Signature**: `std::string leaf_path(std::string f)`
- **Description**: Extracts the leaf path from a given file path string. This function returns the last component of the path, which is the file name or directory name if the path ends with a separator.
- **Parameters**:
  - `f` (std::string): The file path from which to extract the leaf path. This must be a valid string.
- **Return Value**:
  - `std::string`: The leaf path extracted from the input string. If the input is empty, an empty string is returned.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function assumes that the input string is valid.
- **Example**:
```cpp
std::string path = "/home/user/documents/file.txt";
std::string leaf = leaf_path(path);
// leaf will be "file.txt"
```
- **Preconditions**:
  - The input string must be valid and not null.
- **Postconditions**:
  - The returned string will contain the leaf path from the input.
- **Thread Safety**:
  - This function is thread-safe as it only reads from the input string.
- **Complexity**:
  - Time Complexity: O(n) where n is the length of the input string.
  - Space Complexity: O(n) where n is the length of the input string.
- **See Also**: `peer_conn`, `start_conn`

## peer_conn

- **Signature**: `peer_conn(io_context& ios, int piece_count, int blocks_pp, tcp::endpoint const& ep, char const* ih, bool seed_, int churn_, bool corrupt_)`
- **Description**: Constructor for the `peer_conn` class. Initializes a peer connection with the given parameters. This constructor sets up the connection to a peer and initializes various state variables.
- **Parameters**:
  - `ios` (io_context&): The I/O context for the connection. This must be a valid I/O context.
  - `piece_count` (int): The number of pieces in the torrent. This should be a non-negative value.
  - `blocks_pp` (int): The number of blocks per piece. This should be a non-negative value.
  - `ep` (tcp::endpoint const&): The endpoint to connect to. This must be a valid endpoint.
  - `ih` (char const*): The info hash of the torrent. This must be a valid pointer to a string.
  - `seed_` (bool): Whether the peer is a seed. This should be `true` or `false`.
  - `churn_` (int): The churn rate for the connection. This should be a non-negative value.
  - `corrupt_` (bool): Whether to enable corruption for the connection. This should be `true` or `false`.
- **Return Value**:
  - `peer_conn`: An instance of the `peer_conn` class.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function assumes that all parameters are valid.
- **Example**:
```cpp
io_context ios;
tcp::endpoint ep;
char const* ih = "info_hash";
peer_conn conn(ios, 100, 4, ep, ih, true, 0, false);
```
- **Preconditions**:
  - The `ios` must be a valid I/O context.
  - The `ep` must be a valid endpoint.
  - The `ih` must be a valid pointer to a string.
- **Postconditions**:
  - The `peer_conn` instance will be initialized with the provided parameters.
- **Thread Safety**:
  - This function is thread-safe as it only initializes the object.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `start_conn`, `on_connect`

## start_conn

- **Signature**: `void start_conn()`
- **Description**: Starts the connection process by attempting to open and bind the socket. This function is typically called to initiate a connection to a peer.
- **Parameters**:
  - None.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function may throw an error if the socket cannot be opened or bound.
  - The function uses `error_code` to report errors.
- **Example**:
```cpp
peer_conn conn;
conn.start_conn();
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
  - The `local_bind` must be set to `true` if binding is required.
- **Postconditions**:
  - The socket will be opened and bound if successful.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `on_connect`, `close`

## on_connect

- **Signature**: `void on_connect(error_code const& ec)`
- **Description**: Handles the completion of the connect operation. This function is called when the connection attempt has completed, either successfully or with an error.
- **Parameters**:
  - `ec` (error_code const&): The error code indicating the result of the connect operation. This should be a valid error code.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function may close the connection if there is an error.
- **Example**:
```cpp
peer_conn conn;
conn.on_connect(error_code());
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
- **Postconditions**:
  - If there is no error, the handshake process will begin.
  - If there is an error, the connection will be closed.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `on_handshake`, `close`

## on_handshake

- **Signature**: `void on_handshake(char* h, error_code const& ec, size_t)`
- **Description**: Handles the completion of the handshake process. This function is called when the handshake data has been sent and received.
- **Parameters**:
  - `h` (char*): The handshake data. This must be a valid pointer to the handshake data.
  - `ec` (error_code const&): The error code indicating the result of the handshake. This should be a valid error code.
  - `size_t`: The size of the handshake data. This is typically ignored.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function may close the connection if there is an error.
- **Example**:
```cpp
peer_conn conn;
conn.on_handshake(nullptr, error_code(), 0);
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
- **Postconditions**:
  - If there is no error, the next message will be read.
  - If there is an error, the connection will be closed.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `on_handshake2`, `write_have_all`

## on_handshake2

- **Signature**: `void on_handshake2(error_code const& ec, size_t)`
- **Description**: Handles the completion of reading the handshake data. This function is called when the handshake data has been read from the socket.
- **Parameters**:
  - `ec` (error_code const&): The error code indicating the result of the handshake read. This should be a valid error code.
  - `size_t`: The number of bytes read. This is typically ignored.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function may close the connection if there is an error.
- **Example**:
```cpp
peer_conn conn;
conn.on_handshake2(error_code(), 0);
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
- **Postconditions**:
  - If there is no error, the extension bits will be checked.
  - If there is an error, the connection will be closed.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `write_have_all`, `on_sent`

## write_have_all

- **Signature**: `void write_have_all()`
- **Description**: Sends a 'have_all' message to the peer to indicate that the client has all pieces of the torrent. This function is used when the client is a seed.
- **Parameters**:
  - None.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function may throw an error if the write operation fails.
  - The function uses `error_code` to report errors.
- **Example**:
```cpp
peer_conn conn;
conn.write_have_all();
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
  - The `fast_extension` must be `true` for this function to work correctly.
- **Postconditions**:
  - The 'have_all' message will be sent to the peer.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `on_sent`, `write_have`

## on_sent

- **Signature**: `void on_sent(error_code const& ec, size_t, char const* msg)`
- **Description**: Handles the completion of a write operation. This function is called when a message has been sent to the peer.
- **Parameters**:
  - `ec` (error_code const&): The error code indicating the result of the write operation. This should be a valid error code.
  - `size_t`: The number of bytes sent. This is typically ignored.
  - `msg` (char const*): A message describing the write operation. This should be a valid pointer to a string.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function may close the connection if there is an error.
- **Example**:
```cpp
peer_conn conn;
conn.on_sent(error_code(), 0, "ERROR SENT MESSAGE");
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
- **Postconditions**:
  - If there is no error, the next message will be read.
  - If there is an error, the connection will be closed.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `on_message`, `on_msg_length`

## write_request

- **Signature**: `bool write_request()`
- **Description**: Sends a request message to the peer to download a specific block. This function is used to request blocks from the peer.
- **Parameters**:
  - None.
- **Return Value**:
  - `bool`: `true` if the request was sent successfully, `false` otherwise.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function may return `false` if the peer is choked or if there are no pieces left to request.
- **Example**:
```cpp
peer_conn conn;
bool success = conn.write_request();
if (success) {
    // Request was sent successfully
}
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
  - The `current_piece` must be a valid piece index.
- **Postconditions**:
  - If the function returns `true`, a request message will be sent to the peer.
  - If the function returns `false`, no request will be sent.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `on_req_sent`, `write_piece`

## on_req_sent

- **Signature**: `void on_req_sent(char* m, error_code const& ec, size_t)`
- **Description**: Handles the completion of a request message sent to the peer. This function is called when the request message has been sent.
- **Parameters**:
  - `m` (char*): The request message. This must be a valid pointer to the request message.
  - `ec` (error_code const&): The error code indicating the result of the send operation. This should be a valid error code.
  - `size_t`: The number of bytes sent. This is typically ignored.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function may close the connection if there is an error.
- **Example**:
```cpp
peer_conn conn;
conn.on_req_sent(nullptr, error_code(), 0);
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
- **Postconditions**:
  - If there is no error, the download process will continue.
  - If there is an error, the connection will be closed.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `work_download`, `on_sent`

## close

- **Signature**: `void close(char const* msg, error_code const& ec)`
- **Description**: Closes the connection and logs the closure message. This function is called when the connection should be closed, either due to an error or completion.
- **Parameters**:
  - `msg` (char const*): A message describing the reason for closing the connection. This should be a valid pointer to a string.
  - `ec` (error_code const&): The error code indicating the reason for closure. This should be a valid error code.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - The function may log the closure message and close the connection.
- **Example**:
```cpp
peer_conn conn;
conn.close("CONNECTION CLOSED", error_code());
```
- **Preconditions**:
  - The `conn` must be a valid `peer_conn` instance.
- **Postconditions**:
  - The connection will be closed and the closure message will be logged.
- **Thread Safety**:
  - This function is thread-safe as it only modifies the internal state of the `peer_conn` instance.
- **Complexity**:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- **See Also**: `print_usage`, `main`

## work_download

- **Signature**: `void work_download()`
- **Description**: Performs the download work by sending requests and processing received data. This function is called periodically to continue the download process.
- **Parameters**:
  - None.
- **Return Value**:
  - `void`: This function does not