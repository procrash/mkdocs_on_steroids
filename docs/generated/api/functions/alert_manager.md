# libtorrent Alert Manager API Documentation

## alert_manager

- **Signature**: `alert_manager(int queue_limit, alert_category_t alert_mask = alert_category::error)`
- **Description**: Constructs an alert manager with the specified queue size limit and alert category mask. This is the primary constructor for the alert manager class, initializing the internal state for alert queuing and filtering.
- **Parameters**:
  - `queue_limit` (int): The maximum number of alerts that can be queued at any time. This limits memory usage and prevents overwhelming the system with too many alerts. Valid values are positive integers.
  - `alert_mask` (alert_category_t): A bitmask specifying which categories of alerts should be enabled. This determines which alerts will be processed and delivered. The default value is `alert_category::error`, which only enables error-level alerts.
- **Return Value**:
  - No return value (constructor)
- **Exceptions/Errors**:
  - None thrown. The constructor is expected to handle all initialization safely.
- **Example**:
```cpp
// Create an alert manager that can queue up to 1000 alerts and enable all categories
auto alert_mgr = alert_manager(1000, alert_category::all);
```
- **Preconditions**:
  - `queue_limit` must be positive
  - The alert manager must not be used after destruction
- **Postconditions**:
  - The alert manager is fully initialized and ready to receive alerts
  - The alert mask is set to the specified value
  - The queue limit is set to the specified value
- **Thread Safety**: Not thread-safe during construction
- **Complexity**: O(1) time and space complexity
- **See Also**: `set_alert_mask()`, `alert_mask()`, `emplace_alert()`

## alert_manager (Copy Constructor)

- **Signature**: `alert_manager(alert_manager const&) = delete`
- **Description**: Deleted copy constructor prevents copying of the alert manager object. This ensures that each alert manager instance maintains its own independent state and prevents potential race conditions or resource conflicts.
- **Parameters**: None (deleted function)
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**: 
```cpp
// This will cause a compile-time error:
// auto copy = alert_mgr; // Error: copy constructor is deleted
```
- **Preconditions**: None
- **Postconditions**: None
- **Thread Safety**: Not applicable (function is deleted)
- **Complexity**: N/A (function not callable)
- **See Also**: `operator=()`, `alert_manager()`

## operator= (Assignment Operator)

- **Signature**: `alert_manager& operator=(alert_manager const&) = delete`
- **Description**: Deleted assignment operator prevents assignment of one alert manager to another. This maintains the integrity of the alert manager's state and prevents unintended side effects from shared state.
- **Parameters**: 
  - `rhs` (alert_manager const&): The right-hand side alert manager to assign from
- **Return Value**: `alert_manager&` - Reference to the current object
- **Exceptions/Errors**: None
- **Example**: 
```cpp
// This will cause a compile-time error:
// alert_mgr = another_mgr; // Error: assignment operator is deleted
```
- **Preconditions**: None
- **Postconditions**: None
- **Thread Safety**: Not applicable (function is deleted)
- **Complexity**: N/A (function not callable)
- **See Also**: `alert_manager()`, `operator=()`

## ~alert_manager

- **Signature**: `~alert_manager()`
- **Description**: Destructor for the alert manager. Cleans up any allocated resources and ensures that all pending alerts are properly handled before the object is destroyed.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
{
    auto alert_mgr = alert_manager(1000);
    // Use alert manager...
} // alert_mgr is automatically destroyed here
```
- **Preconditions**: The alert manager must be in a valid state
- **Postconditions**: All resources are released and the object is completely destroyed
- **Thread Safety**: Not thread-safe
- **Complexity**: O(n) time complexity where n is the number of alerts in the queue
- **See Also**: `alert_manager()`, `emplace_alert()`

## emplace_alert

- **Signature**: `void emplace_alert(Args&&... args) try`
- **Description**: Emplaces an alert into the queue using perfect forwarding. This function creates an alert of the specified type and adds it to the internal queue, with careful handling of thread safety and queue limits.
- **Parameters**:
  - `args` (Args&&...): Arguments forwarded to the constructor of the alert type. These arguments are perfectly forwarded to construct the alert object.
- **Return Value**: None
- **Exceptions/Errors**: 
  - May throw exceptions during construction of the alert object
  - The function may not throw if the alert is filtered out by the alert mask
- **Example**:
```cpp
// Create and add a storage_error alert to the queue
alert_mgr.emplace_alert(storage_error, "failed to write file", 404);
```
- **Preconditions**: The alert manager must be in a valid state
- **Postconditions**: The alert is added to the queue if it passes the filter criteria
- **Thread Safety**: Thread-safe (uses mutex for synchronization)
- **Complexity**: O(1) amortized time complexity
- **See Also**: `should_post()`, `set_alert_mask()`, `alert_mask()`

## should_post

- **Signature**: `bool should_post() const`
- **Description**: Checks whether alerts of the specified type should be posted based on the current alert mask. This function is typically used as a template function to determine if a specific alert type should be processed.
- **Parameters**: 
  - None (template parameter)
- **Return Value**: `bool` - Returns true if the alert category is enabled in the current alert mask
- **Exceptions/Errors**: None
- **Example**:
```cpp
// Check if error alerts should be posted
if (alert_mgr.should_post<alert_type>()) {
    // Process the alert
}
```
- **Preconditions**: The alert manager must be in a valid state
- **Postconditions**: No state changes
- **Thread Safety**: Thread-safe (uses atomic load)
- **Complexity**: O(1) time complexity
- **See Also**: `set_alert_mask()`, `alert_mask()`, `emplace_alert()`

## set_alert_mask

- **Signature**: `void set_alert_mask(alert_category_t const m) noexcept`
- **Description**: Sets the alert mask to filter which categories of alerts are processed. This allows dynamic control over which alerts are delivered to the application.
- **Parameters**:
  - `m` (alert_category_t const): The new alert mask to set. This should be a bitmask of alert categories.
- **Return Value**: None
- **Exceptions/Errors**: None (marked as noexcept)
- **Example**:
```cpp
// Enable all alert categories
alert_mgr.set_alert_mask(alert_category::all);
// Disable error alerts
alert_mgr.set_alert_mask(alert_category::error);
```
- **Preconditions**: The alert manager must be in a valid state
- **Postconditions**: The alert mask is updated to the specified value
- **Thread Safety**: Not thread-safe (but the function is marked as noexcept)
- **Complexity**: O(1) time complexity
- **See Also**: `alert_mask()`, `should_post()`, `emplace_alert()`

## alert_mask

- **Signature**: `alert_category_t alert_mask() const noexcept`
- **Description**: Returns the current alert mask, which determines which categories of alerts are enabled. This allows the application to query the current alert filtering state.
- **Parameters**: None
- **Return Value**: `alert_category_t` - The current alert mask value
- **Exceptions/Errors**: None (marked as noexcept)
- **Example**:
```cpp
auto mask = alert_mgr.alert_mask();
if (mask & alert_category::warning) {
    // Warning alerts are enabled
}
```
- **Preconditions**: The alert manager must be in a valid state
- **Postconditions**: No state changes
- **Thread Safety**: Thread-safe (uses atomic load)
- **Complexity**: O(1) time complexity
- **See Also**: `set_alert_mask()`, `should_post()`, `emplace_alert()`

## alert_queue_size_limit

- **Signature**: `int alert_queue_size_limit() const noexcept`
- **Description**: Returns the maximum number of alerts that can be queued at any time. This provides information about the queue size limit that was specified during construction.
- **Parameters**: None
- **Return Value**: `int` - The queue size limit
- **Exceptions/Errors**: None (marked as noexcept)
- **Example**:
```cpp
int limit = alert_mgr.alert_queue_size_limit();
std::cout << "Alert queue size limit: " << limit << std::endl;
```
- **Preconditions**: The alert manager must be in a valid state
- **Postconditions**: No state changes
- **Thread Safety**: Thread-safe (uses atomic load)
- **Complexity**: O(1) time complexity
- **See Also**: `alert_manager()`, `emplace_alert()`, `alert_mask()`

# Usage Examples

## Basic Usage

```cpp
#include <libtorrent/aux_/alert_manager.hpp>

int main() {
    // Create an alert manager with a queue limit of 500 and only error alerts enabled
    auto alert_mgr = alert_manager(500, alert_category::error);
    
    // Add alerts to the queue
    alert_mgr.emplace_alert(storage_error, "file not found", 404);
    alert_mgr.emplace_alert(connection_error, "connection failed", "192.168.1.1");
    
    // Check the current alert mask
    auto mask = alert_mgr.alert_mask();
    if (mask & alert_category::error) {
        std::cout << "Error alerts are enabled" << std::endl;
    }
    
    return 0;
}
```

## Error Handling

```cpp
#include <libtorrent/aux_/alert_manager.hpp>
#include <iostream>

int main() {
    try {
        // Create alert manager
        auto alert_mgr = alert_manager(1000);
        
        // Add alerts with error handling
        try {
            alert_mgr.emplace_alert(storage_error, "critical error", 500);
        } catch (const std::exception& e) {
            std::cerr << "Failed to add alert: " << e.what() << std::endl;
        }
        
        // Check if alerts are enabled
        if (alert_mgr.alert_mask() & alert_category::warning) {
            std::cout << "Warning alerts are enabled" << std::endl;
        }
    } catch (const std::exception& e) {
        std::cerr << "Initialization failed: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

## Edge Cases

```cpp
#include <libtorrent/aux_/alert_manager.hpp>
#include <vector>

int main() {
    // Edge case 1: Empty queue limit
    try {
        auto alert_mgr = alert_manager(0); // Zero queue limit
        alert_mgr.emplace_alert(storage_error, "test", 1);
        // This might fail or behave unexpectedly
    } catch (const std::exception& e) {
        std::cerr << "Error creating alert manager: " << e.what() << std::endl;
    }
    
    // Edge case 2: Large queue limit
    auto alert_mgr = alert_manager(1000000); // Very large limit
    for (int i = 0; i < 1000; ++i) {
        alert_mgr.emplace_alert(storage_error, "test", i);
    }
    
    // Check queue size limit
    std::cout << "Queue limit: " << alert_mgr.alert_queue_size_limit() << std::endl;
    
    return 0;
}
```

# Best Practices

1. **Use appropriate queue limits**: Choose a queue limit that balances memory usage with the need to capture enough alerts. For most applications, a limit of 100-500 is sufficient.

2. **Set alert mask appropriately**: Only enable the alert categories you actually need to handle to reduce overhead and improve performance.

3. **Use emplace_alert for efficiency**: Use `emplace_alert` instead of creating alert objects manually to avoid unnecessary