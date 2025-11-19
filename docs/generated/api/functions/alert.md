```markdown
# libtorrent Alert API Documentation

## alert

- **Signature**: `alert(alert&& rhs) noexcept = default;`
- **Description**: Move constructor for the `alert` class. This function enables efficient transfer of ownership of an `alert` object from one instance to another. The move constructor is explicitly defaulted, which means the compiler will generate a move constructor that efficiently transfers the resources from the rvalue parameter to the new object. This is essential for performance in scenarios where alerts are frequently moved between containers or temporary objects.
- **Parameters**:
  - `rhs` (`alert&&`): The rvalue reference to the alert object being moved. This parameter is guaranteed to be in a valid but unspecified state after the move operation.
- **Return Value**:
  - None. This is a constructor, so it does not return a value.
- **Exceptions/Errors**:
  - No exceptions are thrown. The function is marked `noexcept`, indicating it will not throw any exceptions.
- **Example**:
```cpp
// The move constructor is automatically used when moving alert objects
std::unique_ptr<alert> create_alert() {
    auto alert_ptr = std::make_unique<alert>();
    return alert_ptr; // Move constructor called here
}
```
- **Preconditions**: The `rhs` parameter must be a valid `alert` object (not in a destroyed state).
- **Postconditions**: The moved-from object (`rhs`) is left in a valid but unspecified state. The new object contains the resources from the moved object.
- **Thread Safety**: This function is thread-safe as it does not access shared data and does not perform any synchronization.
- **Complexity**: O(1) - Constant time complexity, as it only involves transferring pointers or other lightweight resources.
- **See Also**: `alert(alert const&)`, `operator=(alert const&)`

## alert_cast

- **Signature**: `T* alert_cast(alert* a)`
- **Description**: Attempts to cast a generic `alert` pointer to a specific alert type `T`. This function performs a type-safe cast by checking if the alert's actual type matches the expected type `T`. It leverages the `alert_type` static member of the target type to perform the comparison. The function is designed to be used with alert types derived from `alert` and provides a safer alternative to `static_cast` when dealing with polymorphic alert objects.
- **Parameters**:
  - `a` (`alert*`): A pointer to the alert object to be cast. If `nullptr`, the function returns `nullptr` immediately.
- **Return Value**:
  - Returns a pointer of type `T*` if the alert's type matches `T::alert_type`.
  - Returns `nullptr` if the alert type does not match or if the input pointer is `nullptr`.
- **Exceptions/Errors**:
  - No exceptions are thrown. The function is implemented with a simple conditional check and does not involve dynamic allocation or complex operations.
- **Example**:
```cpp
// Example usage of alert_cast to safely downcast an alert
alert* raw_alert = get_next_alert(); // Assume this returns an alert pointer
peer_disconnected_alert* peer_alert = alert_cast<peer_disconnected_alert>(raw_alert);
if (peer_alert != nullptr) {
    // Successfully cast to peer_disconnected_alert
    std::cout << "Peer disconnected: " << peer_alert->peer_id << std::endl;
}
```
- **Preconditions**: The function template parameter `T` must be a type derived from `alert`. The `alert` pointer `a` must be valid (not a dangling pointer).
- **Postconditions**: The function returns a valid `T*` pointer if the type matches, or `nullptr` otherwise.
- **Thread Safety**: This function is thread-safe as it only performs a simple type check and pointer conversion.
- **Complexity**: O(1) - Constant time complexity, as it involves a single comparison and pointer cast.
- **See Also**: `alert_cast<T const*>(alert const*)`, `alert::type()`

## alert_cast

- **Signature**: `T const* alert_cast(alert const* a)`
- **Description**: Const version of `alert_cast` that safely casts a const `alert` pointer to a specific const alert type `T`. This function is identical to the non-const version but is designed for use with const alert objects, ensuring that the original object cannot be modified through the cast pointer. It provides the same type-safe downcasting behavior as the non-const version.
- **Parameters**:
  - `a` (`alert const*`): A const pointer to the alert object to be cast. If `nullptr`, the function returns `nullptr` immediately.
- **Return Value**:
  - Returns a pointer of type `T const*` if the alert's type matches `T::alert_type`.
  - Returns `nullptr` if the alert type does not match or if the input pointer is `nullptr`.
- **Exceptions/Errors**:
  - No exceptions are thrown. The function is implemented with a simple conditional check and does not involve dynamic allocation or complex operations.
- **Example**:
```cpp
// Example usage with const alerts
alert const* const_alert = get_next_alert_const(); // Assume this returns const alert
torrent_alert* torrent_alert_ptr = alert_cast<torrent_alert const*>(const_alert);
if (torrent_alert_ptr != nullptr) {
    // Successfully cast to torrent_alert
    std::cout << "Torrent name: " << torrent_alert_ptr->name << std::endl;
}
```
- **Preconditions**: The function template parameter `T` must be a type derived from `alert`. The `alert` pointer `a` must be valid (not a dangling pointer) and must not be modified.
- **Postconditions**: The function returns a valid `T const*` pointer if the type matches, or `nullptr` otherwise.
- **Thread Safety**: This function is thread-safe as it only performs a simple type check and pointer conversion.
- **Complexity**: O(1) - Constant time complexity, as it involves a single comparison and pointer cast.
- **See Also**: `alert_cast<T*>(alert*)`, `alert::type()`

## alert

- **Signature**: `auto alert()`
- **Description**: The `alert` class is the base class for all alert types in libtorrent. This is a polymorphic base class that represents a notification or event from the libtorrent library. It provides a common interface for all alerts, allowing them to be stored in a container and processed polymorphically. The class is marked with `TORRENT_EXPORT`, indicating it's part of the public API and exported from the library. The class is designed to be lightweight and efficiently handled by the library's alert system.
- **Parameters**: N/A - This is a class definition, not a function.
- **Return Value**: N/A - This is a class definition, not a function.
- **Exceptions/Errors**: N/A - This is a class definition, not a function.
- **Example**:
```cpp
// Example of defining a custom alert type
class my_custom_alert : public alert {
public:
    static const int alert_type = 1234; // Unique alert type identifier
    // ... other members and methods
};

// Usage of the alert base class
alert* alert_ptr = new my_custom_alert();
// Process the alert through the base class interface
```
- **Preconditions**: N/A - This is a class definition, not a function.
- **Postconditions**: N/A - This is a class definition, not a function.
- **Thread Safety**: This class is designed to be thread-safe for use in the libtorrent library, but specific thread safety depends on the implementation details of derived classes.
- **Complexity**: N/A - This is a class definition, not a function.
- **See Also**: `alert_cast<T>()`, `alert::type()`

# Usage Examples

## Basic Usage

```cpp
#include "libtorrent/alert.hpp"
#include "libtorrent/peer_disconnected_alert.hpp"
#include "libtorrent/torrent_alert.hpp"

// Get an alert from the alert queue
alert* alert_ptr = get_next_alert(); // Assume this returns a valid alert pointer

// Use alert_cast to safely downcast to the expected type
peer_disconnected_alert* peer_alert = alert_cast<peer_disconnected_alert>(alert_ptr);
if (peer_alert != nullptr) {
    // Handle peer disconnected alert
    std::cout << "Peer disconnected: " << peer_alert->peer_id << std::endl;
}

// Use const version for read-only access
alert const* const_alert = get_next_alert_const();
torrent_alert* torrent_alert_ptr = alert_cast<torrent_alert const*>(const_alert);
if (torrent_alert_ptr != nullptr) {
    // Handle torrent alert
    std::cout << "Torrent name: " << torrent_alert_ptr->name << std::endl;
}
```

## Error Handling

```cpp
// Safe handling of potential null returns from alert_cast
alert* raw_alert = get_next_alert();
if (raw_alert == nullptr) {
    // Handle case where no alert is available
    std::cerr << "No alert available" << std::endl;
    return;
}

// Check the type before casting
if (raw_alert->type() == peer_disconnected_alert::alert_type) {
    peer_disconnected_alert* peer_alert = static_cast<peer_disconnected_alert*>(raw_alert);
    if (peer_alert != nullptr) {
        // Process the alert
        std::cout << "Peer disconnected: " << peer_alert->peer_id << std::endl;
    }
} else if (raw_alert->type() == torrent_alert::alert_type) {
    torrent_alert* torrent_alert = static_cast<torrent_alert*>(raw_alert);
    if (torrent_alert != nullptr) {
        // Process the torrent alert
        std::cout << "Torrent name: " << torrent_alert->name << std::endl;
    }
} else {
    // Handle unknown alert type
    std::cerr << "Unknown alert type: " << raw_alert->type() << std::endl;
}
```

## Edge Cases

```cpp
// Handling null pointers and invalid alerts
alert* raw_alert = nullptr;
peer_disconnected_alert* peer_alert = alert_cast<peer_disconnected_alert>(raw_alert);
if (peer_alert == nullptr) {
    // This will always be true for null input
    std::cout << "No alert to cast" << std::endl;
}

// Invalid alert types
alert* invalid_alert = create_invalid_alert(); // This creates an alert of unknown type
if (invalid_alert->type() != peer_disconnected_alert::alert_type) {
    peer_disconnected_alert* peer_alert = alert_cast<peer_disconnected_alert>(invalid_alert);
    if (peer_alert == nullptr) {
        // This will be true since the types don't match
        std::cout << "Type mismatch" << std::endl;
    }
}

// Multiple alert types in a queue
std::vector<alert*> alerts = get_all_alerts();
for (alert* alert_ptr : alerts) {
    if (alert_ptr == nullptr) continue; // Skip null alerts
    
    // Use alert_cast for safe downcasting
    if (auto* piece_finished = alert_cast<piece_finished_alert>(alert_ptr)) {
        std::cout << "Piece finished: " << piece_finished->piece_index << std::endl;
    } else if (auto* peer_disconnected = alert_cast<peer_disconnected_alert>(alert_ptr)) {
        std::cout << "Peer disconnected: " << peer_disconnected->peer_id << std::endl;
    }
}
```

# Best Practices

## Effective Usage

1. **Always use alert_cast for downcasting**: Instead of using `static_cast` directly, use `alert_cast` to safely check the type before casting.
2. **Check return values**: Always check if `alert_cast` returns `nullptr` before using the casted pointer.
3. **Use const versions for read-only access**: When you don't need to modify the alert data, use the const version of `alert_cast`.
4. **Handle all possible alert types**: In alert processing loops, consider all possible alert types that might be generated by libtorrent.

## Common Mistakes to Avoid

1. **Using static_cast without type checking**: This can lead to undefined behavior if the alert type doesn't match.
   ```cpp
   // ❌ BAD: No type checking
   peer_disconnected_alert* peer_alert = static_cast<peer_disconnected_alert*>(raw_alert);
   
   // ✅ GOOD: Safe type checking
   peer_disconnected_alert* peer_alert = alert_cast<peer_disconnected_alert>(raw_alert);
   ```

2. **Assuming all alerts are valid**: Always check for `nullptr` inputs and ensure alert objects are valid before processing.
3. **Ignoring the return value**: Never assume that `alert_cast` will always succeed; always check the return value.

## Performance Tips

1. **Use move semantics**: When moving alert objects between containers or temporary objects, rely on the move constructor for efficient transfers.
2. **Avoid unnecessary casts**: Only cast when you need the specific alert type's members; otherwise, process through the base `alert` interface.
3. **Batch processing**: When processing multiple alerts, consider processing them in batches to minimize