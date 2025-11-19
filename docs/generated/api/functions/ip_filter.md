# C++ API Documentation: IP Filter Bindings

## add_rule

- **Signature**: `void add_rule(ip_filter& filter, std::string start, std::string end, int flags)`
- **Description**: Adds a rule to the IP filter that specifies a range of IP addresses that should be allowed or denied access. The rule is defined by a start and end IP address, along with flags that determine the behavior (e.g., allow or deny).
- **Parameters**:
  - `filter` (ip_filter&): The IP filter instance to which the rule will be added. This must be a valid, initialized ip_filter object.
  - `start` (std::string): The starting IP address of the range in string format (e.g., "192.168.1.1"). This must be a valid IP address string.
  - `end` (std::string): The ending IP address of the range in string format (e.g., "192.168.1.255"). This must be a valid IP address string and should be greater than or equal to the start address.
  - `flags` (int): Flags that determine the behavior of the rule. Common flags include `ip_filter::allow` (allow traffic) or `ip_filter::deny` (deny traffic).
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - `std::invalid_argument`: Thrown if the IP address strings are invalid (e.g., malformed IP addresses).
  - `std::out_of_range`: Thrown if the start IP address is greater than the end IP address.
  - `std::runtime_error`: Thrown if there is an internal error during rule addition.
- **Example**:
```cpp
try {
    ip_filter filter;
    add_rule(filter, "192.168.1.1", "192.168.1.255", ip_filter::allow);
} catch (const std::exception& e) {
    std::cerr << "Error adding rule: " << e.what() << std::endl;
}
```
- **Preconditions**:
  - The `filter` parameter must be a valid, initialized ip_filter object.
  - The `start` and `end` IP address strings must be valid and in the correct format (IPv4 or IPv6).
  - The `start` IP address must be less than or equal to the `end` IP address.
- **Postconditions**:
  - The IP filter will contain the new rule with the specified range and flags.
- **Thread Safety**:
  - This function is not thread-safe. Multiple threads accessing the same ip_filter object concurrently may lead to undefined behavior.
- **Complexity**:
  - Time: O(1) - Adding a rule is a constant-time operation.
  - Space: O(1) - No additional memory is allocated beyond the existing data structure.
- **See Also**: `access0`, `export_filter`

## access0

- **Signature**: `int access0(ip_filter& filter, std::string addr)`
- **Description**: Checks whether a given IP address is allowed or denied by the IP filter. This function returns a value indicating the access status of the IP address.
- **Parameters**:
  - `filter` (ip_filter&): The IP filter instance to check against. This must be a valid, initialized ip_filter object.
  - `addr` (std::string): The IP address to check in string format (e.g., "192.168.1.1"). This must be a valid IP address string.
- **Return Value**:
  - `int`: Returns `ip_filter::allow` (typically 1) if the IP address is allowed, `ip_filter::deny` (typically 0) if it is denied, or a negative value if an error occurs.
- **Exceptions/Errors**:
  - `std::invalid_argument`: Thrown if the IP address string is invalid.
  - `std::runtime_error`: Thrown if there is an internal error during the access check.
- **Example**:
```cpp
try {
    ip_filter filter;
    add_rule(filter, "192.168.1.1", "192.168.1.255", ip_filter::allow);
    int result = access0(filter, "192.168.1.100");
    if (result == ip_filter::allow) {
        std::cout << "Access granted" << std::endl;
    } else if (result == ip_filter::deny) {
        std::cout << "Access denied" << std::endl;
    }
} catch (const std::exception& e) {
    std::cerr << "Error checking access: " << e.what() << std::endl;
}
```
- **Preconditions**:
  - The `filter` parameter must be a valid, initialized ip_filter object.
  - The `addr` IP address string must be valid and in the correct format (IPv4 or IPv6).
- **Postconditions**:
  - The function returns the access status of the IP address without modifying the filter.
- **Thread Safety**:
  - This function is thread-safe as long as the `filter` object is not being modified by another thread simultaneously.
- **Complexity**:
  - Time: O(log n) - The search in the filter's data structure is typically logarithmic.
  - Space: O(1) - No additional memory is allocated.
- **See Also**: `add_rule`, `export_filter`

## convert_range_list

- **Signature**: `list convert_range_list(std::vector<ip_range<T>> const& l)`
- **Description**: Converts a vector of IP range objects into a list of tuples, where each tuple contains the start and end IP addresses as strings. This function is typically used for exporting IP filter ranges to a format suitable for Python.
- **Parameters**:
  - `l` (std::vector<ip_range<T>> const&): A constant reference to a vector of ip_range objects. This must be a valid, non-empty vector.
- **Return Value**:
  - `list`: A Python list containing tuples, where each tuple has two string elements representing the start and end IP addresses of each range.
- **Exceptions/Errors**:
  - `std::bad_alloc`: Thrown if there is insufficient memory to create the list.
  - `std::runtime_error`: Thrown if there is an internal error during conversion.
- **Example**:
```cpp
std::vector<ip_range<ip_address>> ranges = {
    {ip_address("192.168.1.1"), ip_address("192.168.1.255")},
    {ip_address("10.0.0.1"), ip_address("10.0.0.255")}
};
list result = convert_range_list(ranges);
// result now contains [(192.168.1.1, 192.168.1.255), (10.0.0.1, 10.0.0.255)]
```
- **Preconditions**:
  - The `l` parameter must be a valid, non-empty vector of ip_range objects.
- **Postconditions**:
  - The returned list contains the IP ranges as tuples of string representations.
- **Thread Safety**:
  - This function is thread-safe as it does not modify any shared state.
- **Complexity**:
  - Time: O(n) - Each range is processed once.
  - Space: O(n) - Additional memory is allocated for the list and tuples.
- **See Also**: `export_filter`, `add_rule`

## export_filter

- **Signature**: `tuple export_filter(ip_filter const& f)`
- **Description**: Exports the current IP filter configuration as a tuple containing two lists: one for IPv4 ranges and one for IPv6 ranges. This function is used to serialize the filter's state for external use, typically in a Python environment.
- **Parameters**:
  - `f` (ip_filter const&): A constant reference to the ip_filter object to export. This must be a valid, initialized ip_filter object.
- **Return Value**:
  - `tuple`: A Python tuple containing two elements: a list of IPv4 ranges and a list of IPv6 ranges. Each list is a list of tuples representing the start and end IP addresses.
- **Exceptions/Errors**:
  - `std::runtime_error`: Thrown if there is an internal error during the export process.
- **Example**:
```cpp
ip_filter filter;
add_rule(filter, "192.168.1.1", "192.168.1.255", ip_filter::allow);
add_rule(filter, "2001:db8::1", "2001:db8::ffff", ip_filter::allow);
tuple result = export_filter(filter);
// result now contains ([("192.168.1.1", "192.168.1.255")], [("2001:db8::1", "2001:db8::ffff")])
```
- **Preconditions**:
  - The `f` parameter must be a valid, initialized ip_filter object.
- **Postconditions**:
  - The returned tuple contains the exported filter state with all IP ranges separated by version.
- **Thread Safety**:
  - This function is thread-safe as it only reads the filter state.
- **Complexity**:
  - Time: O(n) - Each range in the filter is processed once.
  - Space: O(n) - Additional memory is allocated for the tuple and lists.
- **See Also**: `add_rule`, `access0`, `convert_range_list`

## bind_ip_filter

- **Signature**: `void bind_ip_filter()`
- **Description**: Binds the ip_filter class to Python using Boost.Python, making the class and its methods accessible from Python code. This function sets up the necessary bindings for the ip_filter class.
- **Parameters**:
  - None
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - `std::runtime_error`: Thrown if there is an error during the binding process, such as a missing dependency or invalid configuration.
- **Example**:
```cpp
// This function is typically called once during initialization
bind_ip_filter();
// After this call, the ip_filter class is available in Python
```
- **Preconditions**:
  - The Boost.Python library must be properly installed and linked.
  - The ip_filter class and its methods must be defined and compiled.
- **Postconditions**:
  - The ip_filter class and its methods are bound to Python, allowing Python code to create ip_filter instances and call its methods.
- **Thread Safety**:
  - This function is not thread-safe. It should only be called once during program initialization.
- **Complexity**:
  - Time: O(1) - The binding process is a one-time setup.
  - Space: O(1) - No additional memory is allocated beyond the binding data.
- **See Also**: `add_rule`, `access0`, `export_filter`

## Usage Examples

### Basic Usage

```cpp
#include "ip_filter.hpp"
#include <iostream>

int main() {
    ip_filter filter;
    
    // Add a rule to allow traffic from 192.168.1.0/24
    add_rule(filter, "192.168.1.1", "192.168.1.255", ip_filter::allow);
    
    // Check access for a specific IP
    int result = access0(filter, "192.168.1.100");
    if (result == ip_filter::allow) {
        std::cout << "Access granted" << std::endl;
    } else {
        std::cout << "Access denied" << std::endl;
    }
    
    // Export the filter configuration
    tuple export_result = export_filter(filter);
    // Use the exported result in Python code
    return 0;
}
```

### Error Handling

```cpp
#include "ip_filter.hpp"
#include <iostream>
#include <exception>

int main() {
    ip_filter filter;
    
    try {
        // Attempt to add an invalid rule
        add_rule(filter, "invalid", "192.168.1.255", ip_filter::allow);
    } catch (const std::invalid_argument& e) {
        std::cerr << "Invalid IP address: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
