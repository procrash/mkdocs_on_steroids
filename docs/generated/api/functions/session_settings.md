# libtorrent Session Settings API Documentation

## Function: set_str (session_settings_single_thread)

- **Signature**: `void set_str(int name, std::string value)`
- **Description**: Sets a string configuration value in the session settings. This function is part of the internal implementation of the session settings system and is used to store string values in a container based on a unique identifier.
- **Parameters**:
  - `name` (int): The unique identifier for the setting. Must have the correct type mask set (settings_pack::string_type_base) to ensure type safety.
  - `value` (std::string): The string value to store. The function takes ownership of the string via move semantics.
- **Return Value**: None. The function does not return a value.
- **Exceptions/Errors**: The function asserts that the type mask matches the expected type. If it doesn't, the function returns without modifying the container.
- **Example**:
```cpp
session_settings_single_thread settings;
settings.set_str(settings_pack::alert_mask, "all");
```
- **Preconditions**: The `name` parameter must have the correct type mask set.
- **Postconditions**: The string value is stored in the appropriate container if the type mask matches.
- **Thread Safety**: Not thread-safe. This function is intended for internal use and should not be called concurrently.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_str`, `set_int`, `set_bool`

## Function: set_int (session_settings_single_thread)

- **Signature**: `void set_int(int name, int value)`
- **Description**: Sets an integer configuration value in the session settings. This function is part of the internal implementation of the session settings system and is used to store integer values in a container based on a unique identifier.
- **Parameters**:
  - `name` (int): The unique identifier for the setting. Must have the correct type mask set (settings_pack::int_type_base) to ensure type safety.
  - `value` (int): The integer value to store.
- **Return Value**: None. The function does not return a value.
- **Exceptions/Errors**: The function asserts that the type mask matches the expected type. If it doesn't, the function returns without modifying the container.
- **Example**:
```cpp
session_settings_single_thread settings;
settings.set_int(settings_pack::max_connections, 100);
```
- **Preconditions**: The `name` parameter must have the correct type mask set.
- **Postconditions**: The integer value is stored in the appropriate container if the type mask matches.
- **Thread Safety**: Not thread-safe. This function is intended for internal use and should not be called concurrently.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_int`, `set_str`, `set_bool`

## Function: set_bool (session_settings_single_thread)

- **Signature**: `void set_bool(int name, bool value)`
- **Description**: Sets a boolean configuration value in the session settings. This function is part of the internal implementation of the session settings system and is used to store boolean values in a container based on a unique identifier.
- **Parameters**:
  - `name` (int): The unique identifier for the setting. Must have the correct type mask set (settings_pack::bool_type_base) to ensure type safety.
  - `value` (bool): The boolean value to store.
- **Return Value**: None. The function does not return a value.
- **Exceptions/Errors**: The function asserts that the type mask matches the expected type. If it doesn't, the function returns without modifying the container.
- **Example**:
```cpp
session_settings_single_thread settings;
settings.set_bool(settings_pack::enable_dht, true);
```
- **Preconditions**: The `name` parameter must have the correct type mask set.
- **Postconditions**: The boolean value is stored in the appropriate container if the type mask matches.
- **Thread Safety**: Not thread-safe. This function is intended for internal use and should not be called concurrently.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `get_bool`, `set_str`, `set_int`

## Function: get_str (session_settings_single_thread)

- **Signature**: `std::string const& get_str(int name) const`
- **Description**: Retrieves a string configuration value from the session settings. This function is part of the internal implementation of the session settings system and is used to access string values stored in a container based on a unique identifier.
- **Parameters**:
  - `name` (int): The unique identifier for the setting. Must have the correct type mask set (settings_pack::string_type_base) to ensure type safety.
- **Return Value**: A reference to the stored string value. The function returns a default empty string if the type mask doesn't match.
- **Exceptions/Errors**: The function asserts that the type mask matches the expected type. If it doesn't, the function returns a default empty string.
- **Example**:
```cpp
session_settings_single_thread settings;
std::string alert_mask = settings.get_str(settings_pack::alert_mask);
```
- **Preconditions**: The `name` parameter must have the correct type mask set.
- **Postconditions**: The function returns a reference to the stored string value if the type mask matches.
- **Thread Safety**: Not thread-safe. This function is intended for internal use and should not be called concurrently.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `set_str`, `get_int`, `get_bool`

## Function: get_int (session_settings_single_thread)

- **Signature**: `int get_int(int name) const`
- **Description**: Retrieves an integer configuration value from the session settings. This function is part of the internal implementation of the session settings system and is used to access integer values stored in a container based on a unique identifier.
- **Parameters**:
  - `name` (int): The unique identifier for the setting. Must have the correct type mask set (settings_pack::int_type_base) to ensure type safety.
- **Return Value**: The stored integer value. The function returns a default value (likely 0) if the type mask doesn't match.
- **Exceptions/Errors**: The function asserts that the type mask matches the expected type. If it doesn't, the function returns a default value.
- **Example**:
```cpp
session_settings_single_thread settings;
int max_connections = settings.get_int(settings_pack::max_connections);
```
- **Preconditions**: The `name` parameter must have the correct type mask set.
- **Postconditions**: The function returns the stored integer value if the type mask matches.
- **Thread Safety**: Not thread-safe. This function is intended for internal use and should not be called concurrently.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `set_int`, `get_str`, `get_bool`

## Function: get_bool (session_settings_single_thread)

- **Signature**: `bool get_bool(int name) const`
- **Description**: Retrieves a boolean configuration value from the session settings. This function is part of the internal implementation of the session settings system and is used to access boolean values stored in a container based on a unique identifier.
- **Parameters**:
  - `name` (int): The unique identifier for the setting. Must have the correct type mask set (settings_pack::bool_type_base) to ensure type safety.
- **Return Value**: The stored boolean value. The function returns a default value (likely false) if the type mask doesn't match.
- **Exceptions/Errors**: The function asserts that the type mask matches the expected type. If it doesn't, the function returns a default value.
- **Example**:
```cpp
session_settings_single_thread settings;
bool enable_dht = settings.get_bool(settings_pack::enable_dht);
```
- **Preconditions**: The `name` parameter