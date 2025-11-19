# libtorrent Peer Information API Documentation

## Function: get_last_active

- **Signature**: `std::int64_t get_last_active(peer_info const& pi)`
- **Description**: Retrieves the last active time of a peer in seconds since epoch. This function converts the internal time duration to seconds as a signed 64-bit integer.
- **Parameters**:
  - `pi` (peer_info const&): Reference to a peer_info object containing peer information. This parameter must be valid and cannot be null.
- **Return Value**:
  - Returns a `std::int64_t` value representing the number of seconds since epoch when the peer was last active.
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
- **Example**:
```cpp
auto last_active = get_last_active(peer_info_object);
if (last_active > 0) {
    // Use the last active time
}
```
- **Preconditions**: The `peer_info` object must be valid and properly initialized.
- **Postconditions**: The function returns the last active time in seconds.
- **Thread Safety**: This function is thread-safe as it only reads from the `peer_info` object.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_last_request()`, `get_download_queue_time()`

## Function: get_last_request

- **Signature**: `std::int64_t get_last_request(peer_info const& pi)`
- **Description**: Retrieves the last request time of a peer in seconds since epoch. This function converts the internal time duration to seconds as a signed 64-bit integer.
- **Parameters**:
  - `pi` (peer_info const&): Reference to a peer_info object containing peer information. This parameter must be valid and cannot be null.
- **Return Value**:
  - Returns a `std::int64_t` value representing the number of seconds since epoch when the peer made its last request.
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
- **Example**:
```cpp
auto last_request = get_last_request(peer_info_object);
if (last_request > 0) {
    // Use the last request time
}
```
- **Preconditions**: The `peer_info` object must be valid and properly initialized.
- **Postconditions**: The function returns the last request time in seconds.
- **Thread Safety**: This function is thread-safe as it only reads from the `peer_info` object.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_last_active()`, `get_download_queue_time()`

## Function: get_download_queue_time

- **Signature**: `std::int64_t get_download_queue_time(peer_info const& pi)`
- **Description**: Retrieves the download queue time of a peer in seconds since epoch. This function converts the internal time duration to seconds as a signed 64-bit integer.
- **Parameters**:
  - `pi` (peer_info const&): Reference to a peer_info object containing peer information. This parameter must be valid and cannot be null.
- **Return Value**:
  - Returns a `std::int64_t` value representing the number of seconds since epoch when the peer entered the download queue.
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
- **Example**:
```cpp
auto download_queue_time = get_download_queue_time(peer_info_object);
if (download_queue_time > 0) {
    // Use the download queue time
}
```
- **Preconditions**: The `peer_info` object must be valid and properly initialized.
- **Postconditions**: The function returns the download queue time in seconds.
- **Thread Safety**: This function is thread-safe as it only reads from the `peer_info` object.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_last_active()`, `get_last_request()`

## Function: get_local_endpoint

- **Signature**: `tuple get_local_endpoint(peer_info const& pi)`
- **Description**: Retrieves the local endpoint information of a peer as a tuple containing the IP address and port number.
- **Parameters**:
  - `pi` (peer_info const&): Reference to a peer_info object containing peer information. This parameter must be valid and cannot be null.
- **Return Value**:
  - Returns a tuple containing:
    - First element: String representation of the local IP address
    - Second element: Port number as an integer
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
- **Example**:
```cpp
auto [ip, port] = get_local_endpoint(peer_info_object);
std::cout << "Local endpoint: " << ip << ":" << port << std::endl;
```
- **Preconditions**: The `peer_info` object must be valid and properly initialized.
- **Postconditions**: The function returns a tuple with the local endpoint information.
- **Thread Safety**: This function is thread-safe as it only reads from the `peer_info` object.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_ip()`

## Function: get_ip

- **Signature**: `tuple get_ip(peer_info const& pi)`
- **Description**: Retrieves the IP address and port number of a peer as a tuple containing the IP address and port number.
- **Parameters**:
  - `pi` (peer_info const&): Reference to a peer_info object containing peer information. This parameter must be valid and cannot be null.
- **Return Value**:
  - Returns a tuple containing:
    - First element: String representation of the peer's IP address
    - Second element: Port number as an integer
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
- **Example**:
```cpp
auto [ip, port] = get_ip(peer_info_object);
std::cout << "Peer IP: " << ip << ":" << port << std::endl;
```
- **Preconditions**: The `peer_info` object must be valid and properly initialized.
- **Postconditions**: The function returns a tuple with the peer's IP address and port.
- **Thread Safety**: This function is thread-safe as it only reads from the `peer_info` object.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_local_endpoint()`

## Function: get_pieces

- **Signature**: `list get_pieces(peer_info const& pi)`
- **Description**: Retrieves the pieces that a peer has in a torrent, represented as a list of boolean values where true indicates the peer has the piece.
- **Parameters**:
  - `pi` (peer_info const&): Reference to a peer_info object containing peer information. This parameter must be valid and cannot be null.
- **Return Value**:
  - Returns a list of boolean values where each element represents whether the peer has the corresponding piece.
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
- **Example**:
```cpp
auto pieces = get_pieces(peer_info_object);
for (int i = 0; i < pieces.size(); ++i) {
    if (pieces[i]) {
        std::cout << "Peer has piece " << i << std::endl;
    }
}
```
- **Preconditions**: The `peer_info` object must be valid and properly initialized.
- **Postconditions**: The function returns a list of boolean values representing the pieces the peer has.
- **Thread Safety**: This function is thread-safe as it only reads from the `peer_info` object.
- **Complexity**: O(n) time complexity where n is the number of pieces, O(n) space complexity.
- **See Also**: `get_peer_info_client()`

## Function: get_peer_info_client

- **Signature**: `bytes get_peer_info_client(peer_info const& pi)`
- **Description**: Retrieves the client string of a peer, which identifies the torrent client software being used.
- **Parameters**:
  - `pi` (peer_info const&): Reference to a peer_info object containing peer information. This parameter must be valid and cannot be null.
- **Return Value**:
  - Returns a bytes object containing the client string.
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
- **Example**:
```cpp
auto client = get_peer_info_client(peer_info_object);
std::cout << "Client: " << client << std::endl;
```
- **Preconditions**: The `peer_info` object must be valid and properly initialized.
- **Postconditions**: The function returns the client string as a bytes object.
- **Thread Safety**: This function is thread-safe as it only reads from the `peer_info` object.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_pieces()`

## Function: bind_peer_info

- **Signature**: `void bind_peer_info()`
- **Description**: Binds the `peer_info` class to Python using Boost.Python, exposing its properties to Python code. This function is used to make the peer information accessible in Python bindings.
- **Parameters**: None
- **Return Value**:
  - None. This function is a void function used for binding.
- **Exceptions/Errors**:
  - This function may throw exceptions related to Boost.Python initialization or binding errors.
- **Example**:
```cpp
// This function is typically called during library initialization
bind_peer_info();
```
- **Preconditions**: The Boost.Python library must be properly initialized.
- **Postconditions**: The `peer_info` class is bound to Python, allowing access to its properties in Python code.
- **Thread Safety**: This function is not thread-safe and should only be called during library initialization.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_last_active()`, `get_last_request()`

# Usage Examples

## Basic Usage

```cpp
#include <iostream>
#include "peer_info.h"  // Include the header file

// Assuming we have a peer_info object
peer_info peer_data;

// Get various peer information
auto last_active = get_last_active(peer_data);
auto last_request = get_last_request(peer_data);
auto download_queue_time = get_download_queue_time(peer_data);

auto [local_ip, local_port] = get_local_endpoint(peer_data);
auto [peer_ip, peer_port] = get_ip(peer_data);

auto pieces = get_pieces(peer_data);
auto client = get_peer_info_client(peer_data);

// Print the information
std::cout << "Last active: " << last_active << " seconds ago" << std::endl;
std::cout << "Last request: " << last_request << " seconds ago" << std::endl;
std::cout << "Download queue time: " << download_queue_time << " seconds ago" << std::endl;
std::cout << "Local endpoint: " << local_ip << ":" << local_port << std::endl;
std::cout << "Peer IP: " << peer_ip << ":" << peer_port << std::endl;
```

## Error Handling

```cpp
#include <iostream>
#include <stdexcept>

// Function to safely get peer information
std::int64_t safe_get_last_active(peer_info const& pi) {
    try {
        return get_last_active(pi);
    } catch (const std::exception& e) {
        std::cerr << "Error getting last active time: " << e.what() << std::endl;
        return -1;  // Return error value
    }
}

// Function to safely get pieces
std::list<bool> safe_get_pieces(peer_info const& pi) {
    try {
        return get_pieces(pi);
    } catch (const std::exception& e) {
        std::cerr << "Error getting pieces: " << e.what() << std::endl;
        return {};  // Return empty list
    }
}

// Usage
void process_peer(peer_info const& pi) {
    auto last_active = safe_get_last_active(pi);
    if (last_active == -1) {
        std::cerr << "Failed to get last active time" << std::endl;
        return;
    }

    auto pieces = safe_get_pieces(pi);
    for (auto it = pieces.begin(); it != pieces.end(); ++it)