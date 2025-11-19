# API Documentation for TCP Keepalive Configuration Functions

## tcp_keepalive_idle

- **Signature**: `explicit tcp_keepalive_idle(int seconds)`
- **Description**: Constructor for a TCP keepalive idle configuration object that sets the time interval in seconds after which the first keepalive probe is sent.
- **Parameters**:
  - `seconds` (int): The number of seconds to wait before sending the first keepalive probe. Valid values are positive integers. A value of 0 means no keepalive is sent.
- **Return Value**:
  - None (constructor)
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
auto keepalive = tcp_keepalive_idle(60); // Send first keepalive after 60 seconds
```
- **Preconditions**: None
- **Postconditions**: The keepalive configuration object is initialized with the specified idle time.
- **Thread Safety**: Thread-safe (constructor is called once)
- **Complexity**: O(1)
- **See Also**: `tcp_keepalive_interval`, `tcp_keepalive_count`

## level

- **Signature**: `int level(Protocol const&) const`
- **Description**: Returns the protocol level for the TCP keepalive option, which is IPPROTO_TCP.
- **Parameters**:
  - `Protocol` (const&): The protocol type (not used in the function body).
- **Return Value**:
  - Returns IPPROTO_TCP (an integer constant representing the TCP protocol level).
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
int protocol_level = level(Protocol{}); // Returns IPPROTO_TCP
```
- **Preconditions**: None
- **Postconditions**: The function returns the correct protocol level for TCP keepalive.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `name`, `data`, `size`

## name

- **Signature**: `int name(Protocol const&) const`
- **Description**: Returns the socket option name for the TCP keepalive idle setting.
- **Parameters**:
  - `Protocol` (const&): The protocol type (not used in the function body).
- **Return Value**:
  - Returns TCP_KEEPIDLE (an integer constant representing the socket option name).
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
int option_name = name(Protocol{}); // Returns TCP_KEEPIDLE
```
- **Preconditions**: None
- **Postconditions**: The function returns the correct socket option name.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `level`, `data`, `size`

## data

- **Signature**: `char const* data(Protocol const&) const`
- **Description**: Returns a pointer to the data buffer containing the keepalive idle value.
- **Parameters**:
  - `Protocol` (const&): The protocol type (not used in the function body).
- **Return Value**:
  - Returns a pointer to the internal data buffer containing the keepalive idle value.
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
char const* buffer = data(Protocol{}); // Returns pointer to internal data
```
- **Preconditions**: None
- **Postconditions**: The function returns a valid pointer to the data buffer.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `level`, `name`, `size`

## size

- **Signature**: `size_t size(Protocol const&) const`
- **Description**: Returns the size of the data buffer for the keepalive idle setting.
- **Parameters**:
  - `Protocol` (const&): The protocol type (not used in the function body).
- **Return Value**:
  - Returns the size of the integer value storing the keepalive idle time in bytes.
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
size_t buffer_size = size(Protocol{}); // Returns sizeof(int)
```
- **Preconditions**: None
- **Postconditions**: The function returns the correct size of the data buffer.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `level`, `name`, `data`

## tcp_keepalive_interval

- **Signature**: `explicit tcp_keepalive_interval(int seconds)`
- **Description**: Constructor for a TCP keepalive interval configuration object that sets the time interval in seconds between successive keepalive probes.
- **Parameters**:
  - `seconds` (int): The number of seconds to wait between keepalive probes. Valid values are positive integers. A value of 0 means no keepalive is sent.
- **Return Value**:
  - None (constructor)
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
auto keepalive = tcp_keepalive_interval(30); // Send keepalive every 30 seconds
```
- **Preconditions**: None
- **Postconditions**: The keepalive configuration object is initialized with the specified interval time.
- **Thread Safety**: Thread-safe (constructor is called once)
- **Complexity**: O(1)
- **See Also**: `tcp_keepalive_idle`, `tcp_keepalive_count`

## level

- **Signature**: `int level(Protocol const&) const`
- **Description**: Returns the protocol level for the TCP keepalive option, which is IPPROTO_TCP.
- **Parameters**:
  - `Protocol` (const&): The protocol type (not used in the function body).
- **Return Value**:
  - Returns IPPROTO_TCP (an integer constant representing the TCP protocol level).
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
int protocol_level = level(Protocol{}); // Returns IPPROTO_TCP
```
- **Preconditions**: None
- **Postconditions**: The function returns the correct protocol level for TCP keepalive.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `name`, `data`, `size`

## name

- **Signature**: `int name(Protocol const&) const`
- **Description**: Returns the socket option name for the TCP keepalive interval setting.
- **Parameters**:
  - `Protocol` (const&): The protocol type (not used in the function body).
- **Return Value**:
  - Returns TCP_KEEPINTVL (an integer constant representing the socket option name).
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
int option_name = name(Protocol{}); // Returns TCP_KEEPINTVL
```
- **Preconditions**: None
- **Postconditions**: The function returns the correct socket option name.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `level`, `data`, `size`

## data

- **Signature**: `char const* data(Protocol const&) const`
- **Description**: Returns a pointer to the data buffer containing the keepalive interval value.
- **Parameters**:
  - `Protocol` (const&): The protocol type (not used in the function body).
- **Return Value**:
  - Returns a pointer to the internal data buffer containing the keepalive interval value.
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
char const* buffer = data(Protocol{}); // Returns pointer to internal data
```
- **Preconditions**: None
- **Postconditions**: The function returns a valid pointer to the data buffer.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `level`, `name`, `size`

## size

- **Signature**: `size_t size(Protocol const&) const`
- **Description**: Returns the size of the data buffer for the keepalive interval setting.
- **Parameters**:
  - `Protocol` (const&): The protocol type (not used in the function body).
- **Return Value**:
  - Returns the size of the integer value storing the keepalive interval time in bytes.
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
size_t buffer_size = size(Protocol{}); // Returns sizeof(int)
```
- **Preconditions**: None
- **Postconditions**: The function returns the correct size of the data buffer.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `level`, `name`, `data`

# Usage Examples

## Basic Usage

```cpp
#include "libtorrent/aux_/keepalive.hpp"

int main() {
    // Configure TCP keepalive settings
    auto idle_config = tcp_keepalive_idle(60);   // Send first probe after 60 seconds
    auto interval_config = tcp_keepalive_interval(30); // Send probes every 30 seconds
    
    // Use the configuration with socket options
    // (Note: In a real implementation, these would be passed to setsockopt)
    
    return 0;
}
```

## Error Handling

```cpp
#include "libtorrent/aux_/keepalive.hpp"
#include <iostream>

int main() {
    try {
        // Create keepalive configurations
        auto idle_config = tcp_keepalive_idle(60);
        auto interval_config = tcp_keepalive_interval(30);
        
        // Validate the configurations (in a real system, you'd check socket operations)
        if (idle_config.size(Protocol{}) == 0 || interval_config.size(Protocol{}) == 0) {
            std::cerr << "Failed to create keepalive configurations" << std::endl;
            return 1;
        }
        
        // Use the configurations
        std::cout << "Keepalive idle: " << idle_config.data(Protocol{}) << std::endl;
        std::cout << "Keepalive interval: " << interval_config.data(Protocol{}) << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

## Edge Cases

```cpp
#include "libtorrent/aux_/keepalive.hpp"
#include <iostream>

int main() {
    // Edge case: zero value
    auto zero_idle = tcp_keepalive_idle(0);
    auto zero_interval = tcp_keepalive_interval(0);
    
    std::cout << "Zero idle config size: " << zero_idle.size(Protocol{}) << std::endl;
    std::cout << "Zero interval config size: " << zero_interval.size(Protocol{}) << std::endl;
    
    // Edge case: negative value (though the constructor doesn't validate)
    // Note: In practice, you should validate input parameters
    auto negative_idle = tcp_keepalive_idle(-1);
    auto negative_interval = tcp_keepalive_interval(-1);
    
    std::cout << "Negative idle config size: " << negative_idle.size(Protocol{}) << std::endl;
    std::cout << "Negative interval config size: " << negative_interval.size(Protocol{}) << std::endl;
    
    return 0;
}
```

# Best Practices

## How to Use These Functions Effectively

1. **Set appropriate values**: Choose keepalive intervals that balance network efficiency and connection reliability.
2. **Use consistent configuration**: Apply the same keepalive settings across similar connections for predictable behavior.
3. **Consider network conditions**: Adjust keepalive settings based on network latency and reliability.
4. **Monitor connection health**: Use keepalive settings to detect and handle disconnected connections.

## Common Mistakes to Avoid

1. **Using overly aggressive keepalive intervals**: This can cause unnecessary network traffic and performance degradation.
2. **Using overly long intervals**: This can result in delayed detection of disconnected connections.
3. **Not validating input parameters**: The constructor doesn't validate the input, so ensure the values are appropriate.
4. **Ignoring return values**: These functions are constructors and don't return values to check, but the configuration objects should be used correctly.

## Performance Tips

1. **Reuse configuration objects**: Create configuration objects