# API Documentation for `aux_/noexcept_movable.hpp`

## Function: `wrap`

- **Signature**: `T&& wrap(T&& v)`
- **Description**: A utility function that wraps a movable value, incrementing a global counter (`g_must_not_fail`) before returning the value. This function is designed to be used in conjunction with `noexcept_movable` and `noexcept_move_only` classes to ensure that move operations do not fail in critical paths.
- **Parameters**:
  - `v` (T&&): The rvalue reference to the value to be wrapped. This parameter must be a movable object.
- **Return Value**:
  - Returns the wrapped value as an rvalue reference (`T&&`). The value is moved, not copied.
- **Exceptions/Errors**:
  - This function does not throw any exceptions.
- **Example**:
```cpp
// Wrapping a temporary object
auto value = wrap(std::string("Hello"));
```
- **Preconditions**: The input must be a valid rvalue reference.
- **Postconditions**: The global counter `g_must_not_fail` is incremented by 1.
- **Thread Safety**: Not thread-safe due to the global counter.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_movable`, `noexcept_move_only`

## Function: `noexcept_movable` (Default Constructor)

- **Signature**: `noexcept_movable() = default;`
- **Description**: Default constructor for the `noexcept_movable` class. This constructor does not perform any operations and does not affect the global counter.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Creating a default instance
noexcept_movable<int> obj;
```
- **Preconditions**: None
- **Postconditions**: The object is constructed and ready for use.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_movable` (Move Constructor), `noexcept_movable` (Move Constructor from T)

## Function: `noexcept_movable` (Move Constructor from `noexcept_movable<T>`)

- **Signature**: `noexcept_movable(noexcept_movable<T>&& rhs) noexcept`
- **Description**: Move constructor for the `noexcept_movable` class that takes an rvalue reference to another `noexcept_movable` object. This constructor moves the value from the source object and decrements the global counter.
- **Parameters**:
  - `rhs` (noexcept_movable<T>&&): The source object to move from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Moving from one instance to another
noexcept_movable<int> obj1;
noexcept_movable<int> obj2 = std::move(obj1);
```
- **Preconditions**: The source object must be valid.
- **Postconditions**: The source object is left in a valid but unspecified state, and the global counter `g_must_not_fail` is decremented by 1.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_movable` (Move Constructor from T), `noexcept_movable` (Default Constructor)

## Function: `noexcept_movable` (Move Constructor from `T`)

- **Signature**: `noexcept_movable(T&& rhs) noexcept`
- **Description**: Move constructor for the `noexcept_movable` class that takes an rvalue reference to a `T` object. This constructor moves the value from the source object and decrements the global counter.
- **Parameters**:
  - `rhs` (T&&): The source object to move from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Moving from a temporary object
noexcept_movable<int> obj = std::move(42);
```
- **Preconditions**: The source object must be valid.
- **Postconditions**: The source object is left in a valid but unspecified state, and the global counter `g_must_not_fail` is decremented by 1.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_movable` (Move Constructor from `noexcept_movable<T>`), `noexcept_movable` (Default Constructor)

## Function: `noexcept_movable` (Move Constructor from `noexcept_movable<T>`)

- **Signature**: `noexcept_movable(noexcept_movable<T>&& rhs) noexcept`
- **Description**: Another move constructor for the `noexcept_movable` class that takes an rvalue reference to another `noexcept_movable` object. This constructor moves the value from the source object without affecting the global counter.
- **Parameters**:
  - `rhs` (noexcept_movable<T>&&): The source object to move from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Moving from one instance to another
noexcept_movable<int> obj1;
noexcept_movable<int> obj2 = std::move(obj1);
```
- **Preconditions**: The source object must be valid.
- **Postconditions**: The source object is left in a valid but unspecified state.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_movable` (Move Constructor from `T`), `noexcept_movable` (Default Constructor)

## Function: `noexcept_movable` (Move Constructor from `T`)

- **Signature**: `noexcept_movable(T&& rhs) noexcept`
- **Description**: Another move constructor for the `noexcept_movable` class that takes an rvalue reference to a `T` object. This constructor moves the value from the source object without affecting the global counter.
- **Parameters**:
  - `rhs` (T&&): The source object to move from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Moving from a temporary object
noexcept_movable<int> obj = std::move(42);
```
- **Preconditions**: The source object must be valid.
- **Postconditions**: The source object is left in a valid but unspecified state.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_movable` (Move Constructor from `noexcept_movable<T>`), `noexcept_movable` (Default Constructor)

## Function: `noexcept_movable` (Copy Constructor)

- **Signature**: `noexcept_movable(noexcept_movable<T> const& rhs) = default;`
- **Description**: Copy constructor for the `noexcept_movable` class that takes a const reference to another `noexcept_movable` object. This constructor performs a copy of the source object.
- **Parameters**:
  - `rhs` (noexcept_movable<T> const&): The source object to copy from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Copying from one instance to another
noexcept_movable<int> obj1;
noexcept_movable<int> obj2 = obj1;
```
- **Preconditions**: The source object must be valid.
- **Postconditions**: A copy of the source object is created.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_movable` (Move Constructor from `noexcept_movable<T>`), `noexcept_movable` (Move Constructor from `T`)

## Function: `noexcept_movable` (Copy Constructor from `T`)

- **Signature**: `noexcept_movable(T const& rhs) : T(rhs) {}`
- **Description**: Copy constructor for the `noexcept_movable` class that takes a const reference to a `T` object. This constructor performs a copy of the source object.
- **Parameters**:
  - `rhs` (T const&): The source object to copy from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Copying from a temporary object
noexcept_movable<int> obj = 42;
```
- **Preconditions**: The source object must be valid.
- **Postconditions**: A copy of the source object is created.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_movable` (Copy Constructor), `noexcept_movable` (Move Constructor from `noexcept_movable<T>`)

## Function: `noexcept_move_only` (Move Constructor from `noexcept_move_only<T>`)

- **Signature**: `noexcept_move_only(noexcept_move_only<T>&& rhs) noexcept`
- **Description**: Move constructor for the `noexcept_move_only` class that takes an rvalue reference to another `noexcept_move_only` object. This constructor moves the value from the source object and decrements the global counter.
- **Parameters**:
  - `rhs` (noexcept_move_only<T>&&): The source object to move from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Moving from one instance to another
noexcept_move_only<int> obj1;
noexcept_move_only<int> obj2 = std::move(obj1);
```
- **Preconditions**: The source object must be valid.
- **Postconditions**: The source object is left in a valid but unspecified state, and the global counter `g_must_not_fail` is decremented by 1.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `noexcept_move_only` (Move Constructor from `T`), `noexcept_move_only` (Default Constructor)

## Function: `noexcept_move_only` (Move Constructor from `T`)

- **Signature**: `noexcept_move_only(T&& rhs) noexcept`
- **Description**: Move constructor for the `noexcept_move_only` class that takes an rvalue reference to a `T` object. This constructor moves the value from the source object and decrements the global counter.
- **Parameters**:
  - `rhs` (T&&): The source object to move from.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: This constructor does not throw any exceptions.
- **Example**:
```cpp
// Moving from a temporary object
noexcept_move_only<int> obj = std::move(42);
```
- **Preconditions**: The source object must be valid.
- **Postconditions**: The source object is left in a valid but unspecified state, and the global counter `g_must_not_fail