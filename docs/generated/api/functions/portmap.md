```markdown
# API Documentation: libtorrent Port Mapping Functions

## portmap_callback

- **Signature**: `virtual void operator()(int port_mapping_index, address const& external_address, int external_port, int protocol, error_code const& ec, int transport) = 0;`

- **Description**: This is an abstract base class for port mapping callback functions in libtorrent. It defines the interface for receiving notifications about port mapping operations. The callback is invoked when port mapping operations (add, delete) are completed or fail. This class is intended to be inherited by user-defined classes that need to handle port mapping events.

- **Parameters**:
  - `port_mapping_index` (int): The index of the port mapping being operated on. This can be used to identify which specific mapping request the callback corresponds to.
  - `external_address` (address const&): The external IP address as reported by the router. This is the address that should be used to reach the mapped port from the internet.
  - `external_port` (int): The external port number that was mapped. This is the port number that should be used for incoming connections from the internet.
  - `protocol` (int): The protocol used for the port mapping, where 0 represents UDP and 1 represents TCP.
  - `ec` (error_code const&): An error code indicating the success or failure of the port mapping operation. An empty error code indicates success.
  - `transport` (int): The transport protocol used for the port mapping, where 0 indicates NAT-PMP and 1 indicates UPnP.

- **Return Value**: This function is a virtual function and does not return a value. It is called to process the port mapping event.

- **Exceptions/Errors**: 
  - This function is part of a virtual interface and does not throw exceptions directly. However, the derived class implementation should handle exceptions appropriately.
  - The error_code parameter can indicate various errors such as network connectivity issues, router authentication failures, or unsupported port mapping protocols.

- **Example**:
```cpp
class MyPortmapCallback : public portmap_callback
{
public:
    void operator()(int port_mapping_index, address const& external_address, int external_port, int protocol, error_code const& ec, int transport) override
    {
        if (ec)
        {
            std::cerr << "Port mapping failed: " << ec.message() << std::endl;
            return;
        }

        std::string protocol_str = (protocol == 0) ? "UDP" : "TCP";
        std::string transport_str = (transport == 0) ? "NAT-PMP" : "UPnP";

        std::cout << "Port mapping succeeded:" << std::endl;
        std::cout << "  Index: " << port_mapping_index << std::endl;
        std::cout << "  External Address: " << external_address << std::endl;
        std::cout << "  External Port: " << external_port << std::endl;
        std::cout << "  Protocol: " << protocol_str << std::endl;
        std::cout << "  Transport: " << transport_str << std::endl;
    }
};

// Usage in libtorrent:
// portmap_manager pm;
// pm.set_callback(std::make_shared<MyPortmapCallback>());
```

- **Preconditions**: 
  - The callback object must be properly constructed and initialized.
  - The callback must be set on a portmap manager before any port mapping operations are initiated.

- **Postconditions**: 
  - The callback will be invoked once per port mapping operation (add or delete) with the appropriate parameters.
  - The callback may be called multiple times for different port mappings.

- **Thread Safety**: 
  - This function is not inherently thread-safe. The implementation must handle concurrent calls if the portmap manager may call it from multiple threads.

- **Complexity**: 
  - Time Complexity: O(1) - The function performs a fixed amount of work.
  - Space Complexity: O(1) - The function uses a constant amount of additional memory.

- **See Also**: `portmap_manager`, `portmap_protocol`, `portmap_action`

## to_string (portmap_protocol)

- **Signature**: `inline char const* to_string(portmap_protocol const p)`

- **Description**: Converts a portmap_protocol enumeration value to its string representation. This function is used to generate human-readable strings for logging, debugging, or display purposes.

- **Parameters**:
  - `p` (portmap_protocol const): The portmap_protocol enumeration value to convert to a string.

- **Return Value**:
  - Returns a pointer to a null-terminated C-style string representing the protocol.
  - Returns "UDP" if the input is `portmap_protocol::udp`.
  - Returns "TCP" if the input is `portmap_protocol::tcp`.

- **Exceptions/Errors**: 
  - This function does not throw exceptions.
  - No error conditions are possible as the function only handles valid enumeration values.

- **Example**:
```cpp
#include <iostream>
#include <libtorrent/aux_/portmap.hpp>

int main()
{
    portmap_protocol protocol = portmap_protocol::udp;
    std::cout << "Protocol: " << to_string(protocol) << std::endl;
    // Output: Protocol: UDP

    protocol = portmap_protocol::tcp;
    std::cout << "Protocol: " << to_string(protocol) << std::endl;
    // Output: Protocol: TCP

    return 0;
}
```

- **Preconditions**: 
  - The `portmap_protocol` enumeration value must be valid.

- **Postconditions**: 
  - Returns a valid null-terminated string for the given protocol.

- **Thread Safety**: 
  - This function is thread-safe as it only reads from a constant string and returns a pointer.

- **Complexity**: 
  - Time Complexity: O(1) - The function performs a simple conditional check.
  - Space Complexity: O(1) - The function uses a constant amount of additional memory.

- **See Also**: `portmap_protocol`, `to_string(portmap_action)`

## to_string (portmap_action)

- **Signature**: `inline char const* to_string(portmap_action const act)`

- **Description**: Converts a portmap_action enumeration value to its string representation. This function is used to generate human-readable strings for logging, debugging, or display purposes.

- **Parameters**:
  - `act` (portmap_action const): The portmap_action enumeration value to convert to a string.

- **Return Value**:
  - Returns a pointer to a null-terminated C-style string representing the action.
  - Returns "none" if the input is `portmap_action::none`.
  - Returns "add" if the input is `portmap_action::add`.
  - Returns "delete" if the input is `portmap_action::del`.
  - Returns an empty string for any other value (though this should not occur with valid enumeration values).

- **Exceptions/Errors**: 
  - This function does not throw exceptions.
  - No error conditions are possible as the function handles all defined enumeration values.

- **Example**:
```cpp
#include <iostream>
#include <libtorrent/aux_/portmap.hpp>

int main()
{
    portmap_action action = portmap_action::add;
    std::cout << "Action: " << to_string(action) << std::endl;
    // Output: Action: add

    action = portmap_action::del;
    std::cout << "Action: " << to_string(action) << std::endl;
    // Output: Action: delete

    action = portmap_action::none;
    std::cout << "Action: " << to_string(action) << std::endl;
    // Output: Action: none

    return 0;
}
```

- **Preconditions**: 
  - The `portmap_action` enumeration value must be valid.

- **Postconditions**: 
  - Returns a valid null-terminated string for the given action.

- **Thread Safety**: 
  - This function is thread-safe as it only reads from a constant string and returns a pointer.

- **Complexity**: 
  - Time Complexity: O(1) - The function performs a simple switch statement.
  - Space Complexity: O(1) - The function uses a constant amount of additional memory.

- **See Also**: `portmap_action`, `to_string(portmap_protocol)`

# Usage Examples

## Basic Usage

```cpp
#include <iostream>
#include <libtorrent/aux_/portmap.hpp>

int main()
{
    // Convert protocol enum to string
    std::cout << "UDP Protocol: " << to_string(portmap_protocol::udp) << std::endl;
    std::cout << "TCP Protocol: " << to_string(portmap_protocol::tcp) << std::endl;

    // Convert action enum to string
    std::cout << "Add Action: " << to_string(portmap_action::add) << std::endl;
    std::cout << "Delete Action: " << to_string(portmap_action::del) << std::endl;
    std::cout << "None Action: " << to_string(portmap_action::none) << std::endl;

    return 0;
}
```

## Error Handling

```cpp
#include <iostream>
#include <libtorrent/aux_/portmap.hpp>

class ErrorHandlingCallback : public portmap_callback
{
public:
    void operator()(int port_mapping_index, address const& external_address, int external_port, int protocol, error_code const& ec, int transport) override
    {
        if (ec)
        {
            std::cerr << "Port mapping failed for index " << port_mapping_index << ": " 
                      << ec.message() << std::endl;
            return;
        }

        std::string protocol_str = to_string(static_cast<portmap_protocol>(protocol));
        std::string transport_str = (transport == 0) ? "NAT-PMP" : "UPnP";
        
        std::cout << "Port mapping succeeded for index " << port_mapping_index << std::endl;
        std::cout << "  External Address: " << external_address << std::endl;
        std::cout << "  External Port: " << external_port << std::endl;
        std::cout << "  Protocol: " << protocol_str << std::endl;
        std::cout << "  Transport: " << transport_str << std::endl;
    }
};

int main()
{
    // In a real application, you would set this callback on a portmap_manager
    // Error handling is done through the error_code parameter in the callback
    return 0;
}
```

## Edge Cases

```cpp
#include <iostream>
#include <libtorrent/aux_/portmap.hpp>

int main()
{
    // Test all possible protocol values
    for (int i = 0; i <= 1; ++i)
    {
        portmap_protocol proto = static_cast<portmap_protocol>(i);
        std::cout << "Protocol " << i << ": " << to_string(proto) << std::endl;
    }

    // Test all possible action values
    for (int i = 0; i <= 2; ++i)
    {
        portmap_action act = static_cast<portmap_action>(i);
        std::cout << "Action " << i << ": " << to_string(act) << std::endl;
    }

    // Test the case where the function returns an empty string
    // This should not happen with valid enumeration values but demonstrates the boundary
    portmap_action invalid_action = static_cast<portmap_action>(3);
    std::cout << "Invalid action: " << to_string(invalid_action) << std::endl;

    return 0;
}
```

# Best Practices

## Usage Tips

1. **Use to_string functions for debugging**: These functions are invaluable for logging and debugging port mapping operations.
2. **Use meaningful callback names**: When implementing custom portmap_callback classes, use descriptive names that reflect the purpose of the callback.
3. **Handle errors gracefully**: Always check the error_code parameter in your callback implementation.
4. **Use const references where appropriate**: For large objects, use const references to avoid unnecessary copying.

## Common Mistakes to Avoid

1. **Assuming to_string functions can return invalid values**: While the functions are designed to handle all valid enumeration values, be aware that passing invalid values to the functions could result in undefined behavior.
2. **Not handling callback concurrency**: If the portmap manager might call the callback from multiple threads, ensure your implementation is thread-safe.
3. **Ignoring error codes**: Always check the error_code parameter in the callback to determine if the port mapping operation was successful.

## Performance Tips

1. **Use the inline keyword**: These functions are properly marked as inline, which helps the compiler optimize them.
2. **Avoid string creation overhead**: These functions return pointers to static strings, avoiding the cost of string allocation.
3. **Minimize logging in callbacks**: In high-frequency scenarios, avoid expensive operations like extensive logging in the callback function.

# Code Review & Improvement Suggestions

## Modernization Opportunities

1. **Add [[nodiscard]] attribute**: The to_string functions return important values that should not be ignored.
```cpp
[[nodiscard]] inline char const* to_string(portmap_protocol const p)
{
    return p == portmap_protocol::udp ? "UDP" : "TCP";
}

[[nodiscard]] inline char const* to_string(portmap_action const act)
{
    switch (act)
    {
        case portmap_action::none: return "none";
        case portmap_action::add: return "add