# API Documentation for bind_to_device Functions

## bind_to_device (string constructor)

- **Signature**: `explicit bind_to_device(char const* device)`
- **Description**: Constructs a bind_to_device option that binds a socket to a specific network interface using its name (e.g., "eth0", "wlan0"). This is used to set the SO_BINDTODEVICE socket option on Unix-like systems.
- **Parameters**:
  - `device` (char const*): The name of the network interface to bind to. This must be a null-terminated string containing the interface name. Valid values include interface names like "eth0", "wlan0", "lo", etc.
- **Return Value**:
  - This is a constructor, so it doesn't return a value in the traditional sense. It initializes a bind_to_device object.
- **Exceptions/Errors**:
  - No exceptions are thrown from this constructor.
- **Example**:
```cpp
// Create a bind_to_device option for the "eth0" interface
bind_to_device binding("eth0");
```
- **Preconditions**: The `device` parameter must be a valid, null-terminated string. The interface name must exist on the system.
- **Postconditions**: The bind_to_device object is initialized with the specified device name.
- **Thread Safety**: This function is thread-safe as it's a constructor.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `bind_device`, `bind_to_device(unsigned int)`

## level

- **Signature**: `int level(Protocol const&) const`
- **Description**: Returns the socket level at which the bind_to_device option should be set. This function is part of the socket option interface and returns SOL_SOCKET for string-based interface binding.
- **Parameters**:
  - `Protocol` (Protocol const&): The protocol parameter is ignored as this is a standard socket option.
- **Return Value**:
  - Returns `SOL_SOCKET`, which is the socket level for standard socket options.
- **Exceptions/Errors**:
  - None.
- **Example**:
```cpp
bind_to_device binding("eth0");
int socket_level = binding.level(Protocol());
// socket_level will be SOL_SOCKET
```
- **Preconditions**: None.
- **Postconditions**: The function returns the appropriate socket level.
- **Thread Safety**: This function is thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `name`, `data`, `size`

## name

- **Signature**: `int name(Protocol const&) const`
- **Description**: Returns the socket option name for the bind_to_device option. This function is part of the socket option interface and returns SO_BINDTODEVICE for string-based interface binding.
- **Parameters**:
  - `Protocol` (Protocol const&): The protocol parameter is ignored as this is a standard socket option.
- **Return Value**:
  - Returns `SO_BINDTODEVICE`, which is the option name for binding a socket to a specific network interface.
- **Exceptions/Errors**:
  - None.
- **Example**:
```cpp
bind_to_device binding("eth0");
int option_name = binding.name(Protocol());
// option_name will be SO_BINDTODEVICE
```
- **Preconditions**: None.
- **Postconditions**: The function returns the appropriate socket option name.
- **Thread Safety**: This function is thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `level`, `data`, `size`

## data

- **Signature**: `char const* data(Protocol const&) const`
- **Description**: Returns a pointer to the data that should be passed to the socket option. For string-based interface binding, this returns a pointer to the device name string.
- **Parameters**:
  - `Protocol` (Protocol const&): The protocol parameter is ignored as this is a standard socket option.
- **Return Value**:
  - Returns a pointer to the null-terminated string containing the interface name.
- **Exceptions/Errors**:
  - None.
- **Example**:
```cpp
bind_to_device binding("eth0");
char const* device_data = binding.data(Protocol());
// device_data points to "eth0\0"
```
- **Preconditions**: None.
- **Postconditions**: The function returns a valid pointer to the device name string.
- **Thread Safety**: This function is thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `level`, `name`, `size`

## size

- **Signature**: `size_t size(Protocol const&) const`
- **Description**: Returns the size of the data that should be passed to the socket option. For string-based interface binding, this returns the length of the device name plus one for the null terminator.
- **Parameters**:
  - `Protocol` (Protocol const&): The protocol parameter is ignored as this is a standard socket option.
- **Return Value**:
  - Returns the size in bytes of the device name string, including the null terminator.
- **Exceptions/Errors**:
  - None.
- **Example**:
```cpp
bind_to_device binding("eth0");
size_t data_size = binding.size(Protocol());
// data_size will be 5 (for "eth0\0")
```
- **Preconditions**: None.
- **Postconditions**: The function returns the correct size of the data.
- **Thread Safety**: This function is thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `level`, `name`, `data`

## bind_device

- **Signature**: `void bind_device(T& sock, char const* device, error_code& ec)`
- **Description**: Binds a socket to a specific network interface using its name. This function uses the bind_to_device option to set the SO_BINDTODEVICE socket option on the socket.
- **Parameters**:
  - `sock` (T&): The socket object to bind to the interface. This must be a socket object that supports the set_option method.
  - `device` (char const*): The name of the network interface to bind to (e.g., "eth0", "wlan0").
  - `ec` (error_code&): The error code to set if an error occurs during binding.
- **Return Value**:
  - This function returns void.
- **Exceptions/Errors**:
  - The error code `ec` will be set if an error occurs, such as when the interface name is invalid or the system cannot bind to the specified interface.
- **Example**:
```cpp
boost::asio::ip::tcp::socket socket(io_context);
error_code ec;
bind_device(socket, "eth0", ec);
if (ec) {
    std::cerr << "Failed to bind to interface: " << ec.message() << std::endl;
}
```
- **Preconditions**: The `sock` parameter must be a valid socket object. The `device` parameter must be a valid, null-terminated string.
- **Postconditions**: The socket is bound to the specified interface if no error occurs.
- **Thread Safety**: This function is thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `bind_to_device`, `bind_device(unsigned int)`

## bind_to_device (unsigned int constructor)

- **Signature**: `explicit bind_to_device(unsigned int idx)`
- **Description**: Constructs a bind_to_device option that binds a socket to a specific network interface using its interface index. This is used to set the IP_BOUND_IF socket option on Unix-like systems.
- **Parameters**:
  - `idx` (unsigned int): The interface index to bind to. This must be a valid interface index on the system.
- **Return Value**:
  - This is a constructor, so it doesn't return a value in the traditional sense. It initializes a bind_to_device object.
- **Exceptions/Errors**:
  - No exceptions are thrown from this constructor.
- **Example**:
```cpp
// Create a bind_to_device option for interface index 2
bind_to_device binding(2);
```
- **Preconditions**: The `idx` parameter must be a valid interface index on the system.
- **Postconditions**: The bind_to_device object is initialized with the specified interface index.
- **Thread Safety**: This function is thread-safe as it's a constructor.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `bind_device`, `bind_to_device(char const*)`

## level

- **Signature**: `int level(Protocol const&) const`
- **Description**: Returns the socket level at which the bind_to_device option should be set. This function is part of the socket option interface and returns IPPROTO_IP for interface index binding.
- **Parameters**:
  - `Protocol` (Protocol const&): The protocol parameter is ignored as this is a standard socket option.
- **Return Value**:
  - Returns `IPPROTO_IP`, which is the socket level for IP-level socket options.
- **Exceptions/Errors**:
  - None.
- **Example**:
```cpp
bind_to_device binding(2);
int socket_level = binding.level(Protocol());
// socket_level will be IPPROTO_IP
```
- **Preconditions**: None.
- **Postconditions**: The function returns the appropriate socket level.
- **Thread Safety**: This function is thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `name`, `data`, `size`

## name

- **Signature**: `int name(Protocol const&) const`
- **Description**: Returns the socket option name for the bind_to_device option. This function is part of the socket option interface and returns IP_BOUND_IF for interface index binding.
- **Parameters**:
  - `Protocol` (Protocol const&): The protocol parameter is ignored as this is a standard socket option.
- **Return Value**:
  - Returns `IP_BOUND_IF`, which is the option name for binding a socket to a specific network interface by index.
- **Exceptions/Errors**:
  - None.
- **Example**:
```cpp
bind_to_device binding(2);
int option_name = binding.name(Protocol());
// option_name will be IP_BOUND_IF
```
- **Preconditions**: None.
- **Postconditions**: The function returns the appropriate socket option name.
- **Thread Safety**: This function is thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `level`, `data`, `size`

## data

- **Signature**: `char const* data(Protocol const&) const`
- **Description**: Returns a pointer to the data that should be passed to the socket option. For interface index binding, this returns a pointer to the interface index value.
- **Parameters**:
  - `Protocol` (Protocol const&): The protocol parameter is ignored as this is a standard socket option.
- **Return Value**:
  - Returns a pointer to the interface index value.
- **Exceptions/Errors**:
  - None.
- **Example**:
```cpp
bind_to_device binding(2);
char const* index_data = binding.data