# libtorrent Byte Order Conversion API Documentation

## host_to_network (std::uint32_t version)

- **Signature**: `std::uint32_t host_to_network(std::uint32_t x)`
- **Description**: Converts a 32-bit unsigned integer from host byte order to network byte order. This function is essential for ensuring proper data serialization when transmitting data over networks, as network protocols use big-endian byte order while most modern CPUs use little-endian byte order.
- **Parameters**:
  - `x` (std::uint32_t): The 32-bit unsigned integer to convert from host to network byte order. This parameter must be a valid 32-bit unsigned integer value.
- **Return Value**:
  - Returns the input value converted to network byte order (big-endian). The return value is guaranteed to be in the correct byte order for network transmission.
- **Exceptions/Errors**:
  - This function does not throw exceptions. It performs a simple byte order conversion that cannot fail.
- **Example**:
```cpp
auto result = host_to_network(0x12345678);
// result will be 0x78563412 on little-endian systems
```
- **Preconditions**: The input parameter must be a valid 32-bit unsigned integer.
- **Postconditions**: The return value is guaranteed to be in network byte order (big-endian).
- **Thread Safety**: This function is thread-safe as it performs a simple bitwise operation without modifying shared state.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `network_to_host`, `swap_byteorder`

## network_to_host (std::uint32_t version)

- **Signature**: `std::uint32_t network_to_host(std::uint32_t x)`
- **Description**: Converts a 32-bit unsigned integer from network byte order to host byte order. This function reverses the byte order conversion performed by `host_to_network`, making network data readable on the local system.
- **Parameters**:
  - `x` (std::uint32_t): The 32-bit unsigned integer to convert from network to host byte order. This parameter must be a valid 32-bit unsigned integer value.
- **Return Value**:
  - Returns the input value converted to host byte order. The return value is guaranteed to be in the correct byte order for local processing.
- **Exceptions/Errors**:
  - This function does not throw exceptions. It performs a simple byte order conversion that cannot fail.
- **Example**:
```cpp
auto result = network_to_host(0x78563412);
// result will be 0x12345678 on little-endian systems
```
- **Preconditions**: The input parameter must be a valid 32-bit unsigned integer.
- **Postconditions**: The return value is guaranteed to be in host byte order.
- **Thread Safety**: This function is thread-safe as it performs a simple bitwise operation without modifying shared state.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `host_to_network`, `swap_byteorder`

## host_to_network (std::uint16_t version)

- **Signature**: `std::uint16_t host_to_network(std::uint16_t x)`
- **Description**: Converts a 16-bit unsigned integer from host byte order to network byte order. This function is essential for ensuring proper data serialization when transmitting 16-bit values over networks, as network protocols use big-endian byte order while most modern CPUs use little-endian byte order.
- **Parameters**:
  - `x` (std::uint16_t): The 16-bit unsigned integer to convert from host to network byte order. This parameter must be a valid 16-bit unsigned integer value.
- **Return Value**:
  - Returns the input value converted to network byte order (big-endian). The return value is guaranteed to be in the correct byte order for network transmission.
- **Exceptions/Errors**:
  - This function does not throw exceptions. It performs a simple byte order conversion that cannot fail.
- **Example**:
```cpp
auto result = host_to_network(0x1234);
// result will be 0x3412 on little-endian systems
```
- **Preconditions**: The input parameter must be a valid 16-bit unsigned integer.
- **Postconditions**: The return value is guaranteed to be in network byte order.
- **Thread Safety**: This function is thread-safe as it performs a simple bitwise operation without modifying shared state.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `network_to_host`, `swap_byteorder`

## network_to_host (std::uint16_t version)

- **Signature**: `std::uint16_t network_to_host(std::uint16_t x)`
- **Description**: Converts a 16-bit unsigned integer from network byte order to host byte order. This function reverses the byte order conversion performed by `host_to_network`, making network data readable on the local system.
- **Parameters**:
  - `x` (std::uint16_t): The 16-bit unsigned integer to convert from network to host byte order. This parameter must be a valid 16-bit unsigned integer value.
- **Return Value**:
  - Returns the input value converted to host byte order. The return value is guaranteed to be in the correct byte order for local processing.
- **Exceptions/Errors**:
  - This function does not throw exceptions. It performs a simple byte order conversion that cannot fail.
- **Example**:
```cpp
auto result = network_to_host(0x3412);
// result will be 0x1234 on little-endian systems
```
- **Preconditions**: The input parameter must be a valid 16-bit unsigned integer.
- **Postconditions**: The return value is guaranteed to be in host byte order.
- **Thread Safety**: This function is thread-safe as it performs a simple bitwise operation without modifying shared state.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `host_to_network`, `swap_byteorder`

## swap_byteorder

- **Signature**: `std::uint32_t swap_byteorder(std::uint32_t const x)`
- **Description**: Swaps the byte order of a 32-bit unsigned integer. This function converts between little-endian and big-endian byte orders regardless of the host system's endianness. It's particularly useful for cross-platform applications where byte order consistency is required.
- **Parameters**:
  - `x` (std::uint32_t const): The 32-bit unsigned integer whose byte order should be swapped. This parameter must be a valid 32-bit unsigned integer value.
- **Return Value**:
  - Returns the input value with its byte order reversed. The return value is the original value with all bytes swapped.
- **Exceptions/Errors**:
  - This function does not throw exceptions. It performs a simple bitwise operation that cannot fail.
- **Example**:
```cpp
auto result = swap_byteorder(0x12345678);
// result will be 0x78563412 regardless of system endianness
```
- **Preconditions**: The input parameter must be a valid 32-bit unsigned integer.
- **Postconditions**: The return value is guaranteed to have the byte order swapped from the input.
- **Thread Safety**: This function is thread-safe as it performs a simple bitwise operation without modifying shared state.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `little_endian_to_host`, `host_to_network`, `network_to_host`
- **Modernization Opportunities**: Consider adding `[[nodiscard]]` attribute to indicate that the return value should not be ignored.

## little_endian_to_host

- **Signature**: `std::uint32_t little_endian_to_host(std::uint32_t x)`
- **Description**: Converts a 32-bit unsigned integer from little-endian byte order to host byte order. This function is specifically designed to handle the common case where data is stored in little-endian format (common on x86/x64 architectures) and needs to be converted to the host system's native byte order.
- **Parameters**:
  - `x` (std::uint32_t): The 32-bit unsigned integer in little-endian format to convert to host byte order. This parameter must be a valid 32-bit unsigned integer value.
- **Return Value**:
  - Returns the input value converted to host byte order. If the host system is little-endian, the value is returned unchanged. If the host system is big-endian, the value is converted from little-endian to big-endian.
- **Exceptions/Errors**:
  - This function does not throw exceptions. However, it relies on the `BOOST_ENDIAN_*` macros being properly defined by the build system. If these macros are not defined, the compilation will fail with an error.
- **Example**:
```cpp
auto result = little_endian_to_host(0x78563412);
// result will be 0x12345678 on little-endian systems
// result will be 0x78563412 on big-endian systems
```
- **Preconditions**: The input parameter must be a valid 32-bit unsigned integer. The build system must properly define the `BOOST_ENDIAN_*` macros.
- **Postconditions**: The return value is guaranteed to be in host byte order.
- **Thread Safety**: This function is thread-safe as it performs a simple conditional operation without modifying shared state.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `swap_byteorder`, `host_to_network`, `network_to_host`
- **Modernization Opportunities**: Consider adding `[[nodiscard]]` attribute to indicate that the return value should not be ignored.

# Usage Examples

## Basic Usage

```cpp
#include <libtorrent/aux_/byteswap.hpp>
#include <iostream>

int main() {
    // Convert a 32-bit integer from host to network byte order
    std::uint32_t host_value = 0x12345678;
    std::uint32_t network_value = host_to_network(host_value);
    
    // Convert back from network to host byte order
    std::uint32_t restored_value = network_to_host(network_value);
    
    std::cout << "Original: 0x" << std::hex << host_value << std::endl;
    std::cout << "Network: 0x" << std::hex << network_value << std::endl;
    std::cout << "Restored: 0x" << std::hex << restored_value << std::endl;
    
    return 0;
}
```

## Error Handling

```cpp
#include <libtorrent/aux_/byteswap.hpp>
#include <iostream>
#include <stdexcept>

int main() {
    // Since these functions don't throw exceptions, error handling is minimal
    // but we can check for valid input ranges
    std::uint32_t valid_input = 0x12345678;
    std::uint32_t invalid_input = 0xFFFFFFFF; // This is valid, but we'll use it to demonstrate
    
    try {
        // These functions don't throw, but we can verify the results
        std::uint32_t converted = host_to_network(valid_input);
        std::uint32_t restored = network_to_host(converted);
        
        if (restored != valid_input) {
            throw std::runtime_error("Byte order conversion failed");
        }
        
        std::cout << "Conversion successful: " << std::hex << restored << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    
    return 0;
}
```

## Edge Cases

```cpp
#include <libtorrent/aux_/byteswap.hpp>
#include <iostream>

int main() {
    // Test with edge cases
    std::uint32_t zero = 0;
    std::uint32_t max_value = 0xFFFFFFFF;
    std::uint32_t middle_value = 0x80000000;
    
    std::cout << "Testing edge cases:" << std::endl;
    
    // Zero value
    std::uint32_t zero_network = host_to_network(zero);
    std::uint32_t