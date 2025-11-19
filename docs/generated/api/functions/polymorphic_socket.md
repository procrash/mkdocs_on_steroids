# polymorphic_socket API Documentation

## polymorphic_socket

- **Signature**: `polymorphic_socket(S s)`
- **Description**: Constructs a `polymorphic_socket` from a socket object `s`. This is the primary constructor that initializes the variant with a specific socket type.
- **Parameters**:
  - `s` (S): The socket object to construct the polymorphic socket from. This must be a type that is compatible with one of the types in the `Sockets...` template parameter pack.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: 
  - Static assertion failure if the socket type is not nothrow move constructible
  - The static_assert ensures that the socket type can be moved without throwing exceptions
- **Example**:
```cpp
// Create a polymorphic socket from an IPv4 socket
boost::asio::ip::tcp::socket tcp_socket(io_context);
polymorphic_socket socket(std::move(tcp_socket));
```
- **Preconditions**: The socket object `s` must be valid and in a state where it can be moved.
- **Postconditions**: The `polymorphic_socket` is initialized with the provided socket object.
- **Thread Safety**: Thread-safe if the socket object is thread-safe.
- **Complexity**: O(1)
- **See Also**: `polymorphic_socket(polymorphic_socket&&)`

## polymorphic_socket

- **Signature**: `polymorphic_socket(polymorphic_socket&&)`
- **Description**: Move constructor for `polymorphic_socket`. Creates a new `polymorphic_socket` by moving the contents of another `polymorphic_socket` object.
- **Parameters**: 
  - `other` (polymorphic_socket&&): The source `polymorphic_socket` to move from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
polymorphic_socket socket1;
polymorphic_socket socket2(std::move(socket1)); // Move constructor
```
- **Preconditions**: The source `polymorphic_socket` must be in a valid state.
- **Postconditions**: The source `polymorphic_socket` is left in a valid but unspecified state.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `polymorphic_socket(S s)`

## polymorphic_socket

- **Signature**: `~polymorphic_socket()`
- **Description**: Destructor for `polymorphic_socket`. Cleans up the socket resources and destroys the object.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
{
    polymorphic_socket socket;
    // Use socket
} // socket is destroyed here, resources are cleaned up
```
- **Preconditions**: None
- **Postconditions**: The object is destroyed and any associated resources are freed.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `polymorphic_socket(polymorphic_socket&&)`

## is_open

- **Signature**: `bool is_open() const`
- **Description**: Checks if the socket is currently open.
- **Parameters**: None
- **Return Value**: 
  - `true` if the socket is open
  - `false` if the socket is closed
- **Exceptions/Errors**: None
- **Example**:
```cpp
if (socket.is_open()) {
    // Socket is open, can perform operations
}
```
- **Preconditions**: None
- **Postconditions**: The socket state is unchanged.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `open()`, `close()`

## open

- **Signature**: `void open(protocol_type const& p, error_code& ec)`
- **Description**: Opens the socket using the specified protocol. This function forwards to the underlying socket's open function.
- **Parameters**:
  - `p` (protocol_type const&): The protocol to use for opening the socket.
  - `ec` (error_code&): Error code that will be set if an error occurs.
- **Return Value**: None
- **Exceptions/Errors**: 
  - Error code will be set if an error occurs
- **Example**:
```cpp
error_code ec;
socket.open(protocol, ec);
if (ec) {
    // Handle error
}
```
- **Preconditions**: The socket must not be already open.
- **Postconditions**: The socket is open if no error occurs.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `open(protocol_type const& p)`

## close

- **Signature**: `void close(error_code& ec)`
- **Description**: Closes the socket and releases associated resources. This function forwards to the underlying socket's close function.
- **Parameters**:
  - `ec` (error_code&): Error code that will be set if an error occurs.
- **Return Value**: None
- **Exceptions/Errors**: 
  - Error code will be set if an error occurs
- **Example**:
```cpp
error_code ec;
socket.close(ec);
if (ec) {
    // Handle error
}
```
- **Preconditions**: The socket must be open.
- **Postconditions**: The socket is closed and resources are released.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `close()`

## local_endpoint

- **Signature**: `endpoint_type local_endpoint(error_code& ec) const`
- **Description**: Gets the local endpoint of the socket. This function forwards to the underlying socket's local_endpoint function.
- **Parameters**:
  - `ec` (error_code&): Error code that will be set if an error occurs.
- **Return Value**: The local endpoint of the socket.
- **Exceptions/Errors**: 
  - Error code will be set if an error occurs
- **Example**:
```cpp
error_code ec;
endpoint_type ep = socket.local_endpoint(ec);
if (ec) {
    // Handle error
}
```
- **Preconditions**: The socket must be open.
- **Postconditions**: The endpoint is returned if no error occurs.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `local_endpoint()`

## remote_endpoint

- **Signature**: `endpoint_type remote_endpoint(error_code& ec) const`
- **Description**: Gets the remote endpoint of the socket. This function forwards to the underlying socket's remote_endpoint function.
- **Parameters**:
  - `ec` (error_code&): Error code that will be set if an error occurs.
- **Return Value**: The remote endpoint of the socket.
- **Exceptions/Errors**: 
  - Error code will be set if an error occurs
- **Example**:
```cpp
error_code ec;
endpoint_type ep = socket.remote_endpoint(ec);
if (ec) {
    // Handle error
}
```
- **Preconditions**: The socket must be open.
- **Postconditions**: The endpoint is returned if no error occurs.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `remote_endpoint()`

## bind

- **Signature**: `void bind(endpoint_type const& endpoint, error_code& ec)`
- **Description**: Binds the socket to a specific endpoint. This function forwards to the underlying socket's bind function.
- **Parameters**:
  - `endpoint` (endpoint_type const&): The endpoint to bind to.
  - `ec` (error_code&): Error code that will be set if an error occurs.
- **Return Value**: None
- **Exceptions/Errors**: 
  - Error code will be set if an error occurs
- **Example**:
```cpp
error_code ec;
socket.bind(endpoint, ec);
if (ec) {
    // Handle error
}
```
- **Preconditions**: The socket must be open.
-