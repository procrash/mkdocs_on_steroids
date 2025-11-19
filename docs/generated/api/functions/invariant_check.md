# libtorrent Invariant Check API Documentation

## check_invariant (Static Version)

- **Signature**: `static void check_invariant(T const& self)`
- **Description**: Static helper function that calls the `check_invariant()` method on the given object. This function is designed to be used as a template parameter for `invariant_checker_impl` to perform invariant checking on objects of type T. It is typically used in conjunction with the `invariant_checker_impl` class to ensure object invariants are maintained.
- **Parameters**:
  - `self` (T const&): The object whose invariants should be checked. The object must have a `check_invariant()` member function.
- **Return Value**: None. This function does not return a value.
- **Exceptions/Errors**: 
  - May throw exceptions if the `check_invariant()` method of the object throws.
  - No explicit error handling in this function itself.
- **Example**:
```cpp
// Example usage in a class template
class MyClass {
public:
    void check_invariant() const {
        // Validate that my invariant holds
        assert(some_condition);
    }
};

// Using check_invariant in a template context
check_invariant<MyClass>(my_object);
```
- **Preconditions**: 
  - The type T must have a `check_invariant()` member function.
  - The object must be in a valid state.
- **Postconditions**: 
  - The object's invariants are checked.
  - No state changes are made to the object.
- **Thread Safety**: 
  - Not thread-safe unless the `check_invariant()` method itself is thread-safe.
- **Complexity**: O(1) - assumes the `check_invariant()` method is O(1).
- **See Also**: `make_invariant_checker()`, `invariant_checker_impl`

## check_invariant (Runtime Version)

- **Signature**: `void check_invariant(T const& x)`
- **Description**: Runtime function that checks the invariants of the given object while handling exceptions. This function attempts to call the `invariant_access::check_invariant(x)` function, but catches and reports any exceptions that occur during the invariant check. This provides a safety net for invariant checking in production code where exceptions should not crash the application.
- **Parameters**:
  - `x` (T const&): The object whose invariants should be checked. The object must be compatible with the `invariant_access::check_invariant` function.
- **Return Value**: None. This function does not return a value.
- **Exceptions/Errors**:
  - Catches `std::exception` and prints an error message to stderr.
  - Catches any other exceptions and prints an error message to stderr.
  - This function may not handle all possible error conditions due to incomplete error handling code.
- **Example**:
```cpp
// Example usage
try {
    check_invariant(some_object);
} catch (const std::exception& e) {
    // Handle the exception
    std::cerr << "Exception in invariant check: " << e.what() << std::endl;
}
```
- **Preconditions**: 
  - The object must be in a valid state.
  - The `invariant_access::check_invariant` function must be properly implemented for the type T.
- **Postconditions**: 
  - The object's invariants are checked.
  - Any exceptions during invariant checking are caught and reported.
- **Thread Safety**: 
  - Not thread-safe unless the `invariant_access::check_invariant` function itself is thread-safe.
- **Complexity**: O(1) - assumes the `invariant_access::check_invariant` function is O(1).
- **See Also**: `invariant_checker_impl`, `make_invariant_checker`

## invariant_checker_impl (Constructor)

- **Signature**: `explicit invariant_checker_impl(T const& self_)`
- **Description**: Constructor for the `invariant_checker_impl` class that initializes the checker with a reference to the object to be checked. The constructor immediately calls `check_invariant(self)` to validate the object's invariants upon construction.
- **Parameters**:
  - `self_` (T const&): The object whose invariants should be checked. This reference must remain valid for the lifetime of the `invariant_checker_impl` instance.
- **Return Value**: None. This is a constructor, not a function that returns a value.
- **Exceptions/Errors**:
  - May throw exceptions if `check_invariant(self)` throws.
  - This function does not handle exceptions itself - they will propagate to the caller.
- **Example**:
```cpp
// Example usage in a class
class SomeClass {
public:
    void check_invariant() const {
        // Implementation of invariant checking
    }
};

void someFunction(SomeClass& obj) {
    invariant_checker_impl<SomeClass> checker(obj);
    // Object invariants are checked immediately
}
```
- **Preconditions**: 
  - The object must be in a valid state.
  - The object must have a `check_invariant()` method.
- **Postconditions**: 
  - The object's invariants are checked.
  - The `invariant_checker_impl` instance is initialized and ready for use.
- **Thread Safety**: 
  - Not thread-safe unless the `check_invariant()` method itself is thread-safe.
- **Complexity**: O(1) - assumes the `check_invariant()` method is O(1).
- **See Also**: `invariant_checker_impl`, `make_invariant_checker`

## invariant_checker_impl (Move Constructor)

- **Signature**: `invariant_checker_impl(invariant_checker_impl&& rhs)`
- **Description**: Move constructor for the `invariant_checker_impl` class that transfers ownership from a temporary instance to a new instance. This allows efficient transfer of the checker instance without copying the potentially expensive object reference.
- **Parameters**:
  - `rhs` (invariant_checker_impl&&): The source instance to move from. After the move, the source instance is in a valid but unspecified state.
- **Return Value**: None. This is a constructor, not a function that returns a value.
- **Exceptions/Errors**: 
  - Should not throw exceptions (noexcept).
- **Example**:
```cpp
// Example of moving an invariant checker
invariant_checker_impl<SomeClass> createChecker() {
    SomeClass obj;
    return invariant_checker_impl<SomeClass>(obj);
}

void useChecker() {
    auto checker = createChecker(); // Move constructor called
    // Use checker
}
```
- **Preconditions**: 
  - The source instance must be in a valid state before the move.
- **Postconditions**: 
  - The new instance owns the object reference.
  - The source instance is in a valid but unspecified state.
- **Thread Safety**: 
  - Not thread-safe unless the underlying object is thread-safe.
- **Complexity**: O(1) - constant time operation.
- **See Also**: `invariant_checker_impl`, `make_invariant_checker`

## invariant_checker_impl (Copy Constructor)

- **Signature**: `invariant_checker_impl(invariant_checker_impl const& rhs) = delete`
- **Description**: Deleted copy constructor for the `invariant_checker_impl` class. This prevents copying of invariant checker instances, which could lead to double invariant checking or other issues since the checker is designed to be moved rather than copied.
- **Parameters**:
  - `rhs` (invariant_checker_impl const&): The source instance to copy from (this parameter is not used since the function is deleted).
- **Return Value**: None. This is a constructor, not a function that returns a value.
- **Exceptions/Errors**: 
  - Attempting to copy an `invariant_checker_impl` instance will result in a compile-time error.
- **Example**: 
```cpp
// This will cause a compile error:
invariant_checker_impl<SomeClass> checker1;
invariant_checker_impl<SomeClass> checker2 = checker1; // Compile error
```
- **Preconditions**: 
  - None - this function is not callable.
- **Postconditions**: 
  - None - this function is not callable.
- **Thread Safety**: 
  - Not applicable - this function is not callable.
- **Complexity**: Not applicable.
- **See Also**: `invariant_checker_impl`, `make_invariant_checker`

## invariant_checker_impl (Destructor)

- **Signature**: `~invariant_checker_impl()`
- **Description**: Destructor for the `invariant_checker_impl` class that checks the object's invariants when the checker is destroyed. This provides a final invariant check to ensure the object's state hasn't been corrupted during its lifetime.
- **Parameters**: None.
- **Return Value**: None. This is a destructor, not a function that returns a value.
- **Exceptions/Errors**: 
  - May throw exceptions if `check_invariant(self)` throws.
  - This function does not handle exceptions - they will propagate to the caller.
- **Example**:
```cpp
// Example of destructor usage
{
    SomeClass obj;
    invariant_checker_impl<SomeClass> checker(obj);
    // Object is checked at construction
    // Object is checked again at destruction
} // Destructor called here
```
- **Preconditions**: 
  - The object must be in a valid state.
- **Postconditions**: 
  - The object's invariants are checked upon destruction.
  - The destructor releases any resources held by the checker.
- **Thread Safety**: 
  - Not thread-safe unless the `check_invariant()` method itself is thread-safe.
- **Complexity**: O(1) - assumes the `check_invariant()` method is O(1).
- **See Also**: `invariant_checker_impl`, `make_invariant_checker`

## make_invariant_checker

- **Signature**: `invariant_checker_impl<T> make_invariant_checker(T const& x)`
- **Description**: Factory function that creates an `invariant_checker_impl` instance for the given object. This function provides a convenient way to create invariant checkers without explicitly specifying the template parameter, as the template parameter can be deduced from the argument type.
- **Parameters**:
  - `x` (T const&): The object whose invariants should be checked. The object must be compatible with the `invariant_checker_impl` template.
- **Return Value**: 
  - Returns an `invariant_checker_impl<T>` instance that can be used to check the object's invariants.
  - The returned instance owns the object reference and will check invariants on construction and destruction.
- **Exceptions/Errors**: 
  - May throw exceptions if `check_invariant(x)` throws during construction of the `invariant_checker_impl` instance.
  - This function does not handle exceptions - they will propagate to the caller.
- **Example**:
```cpp
// Example usage
SomeClass obj;
auto checker = make_invariant_checker(obj);
// The checker will check invariants on construction and destruction
```
- **Preconditions**: 
  - The object must be in a valid state.
  - The object must be compatible with the `invariant_checker_impl` template.
- **Postconditions**: 
  - An `invariant_checker_impl<T>` instance is created and ready to check invariants.
  - The object's invariants are checked immediately.
- **Thread Safety**: 
  - Not thread-safe unless the `check_invariant()` method itself is thread-safe.
- **Complexity**: O(1) - assumes the `check_invariant()` method is O(1).
- **See Also**: `invariant_checker_impl`, `check_invariant`

# Usage Examples

## Basic Usage

```cpp
#include "libtorrent/aux_/invariant_check.hpp"
#include <iostream>

// Example class with invariants
class ExampleClass {
public:
    void check_invariant() const {
        // Check that the state is valid
        assert(m_value >= 0 && "Value cannot be negative");
    }

    int getValue() const { return m_value; }
    void setValue(int value) { m_value = value; }

private:
    int m_value = 0;
};

int main() {
    ExampleClass obj;
    obj.setValue(42);

    // Create an invariant checker
    auto checker = make_invariant_checker(obj);
    
    // The invariant is checked on construction
    std::cout << "Value: " << obj.getValue() << std::endl;
    
    // The invariant is checked again on destruction
    return 0;
}
```

## Error Handling

```cpp
#include "libtorrent/aux_/invariant_check.hpp"
#include <iostream>
#include <stdexcept>

class ErrorProneClass {
public:
    void check_invariant() const {
        if (m_state == ERROR_STATE) {
            throw std::runtime_error("Invalid state in ErrorProneClass");
        }
    }

    void setState(int state) { m_state = state; }

private:
    int m_state = 0;
    static constexpr int