# C++ API Documentation

## allow_threading_guard

- **Signature**: `allow_threading_guard()`
- **Description**: Constructor for the `allow_threading_guard` class. This function saves the current Python GIL (Global Interpreter Lock) state so it can be restored later.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
allow_threading_guard guard;
```
- **Preconditions**: None
- **Postconditions**: The current GIL state is saved and can be restored
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `~allow_threading_guard()`

## ~allow_threading_guard

- **Signature**: `~allow_threading_guard()`
- **Description**: Destructor for the `allow_threading_guard` class. Restores the saved GIL state to allow other threads to access the Python interpreter.
- **Parameters**: None
- **Return Value**: None (destructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
{
    allow_threading_guard guard;
    // Code that might release the GIL
} // GIL is automatically restored here
```
- **Preconditions**: The `allow_threading_guard` object must have been constructed
- **Postconditions**: The GIL state is restored to what it was when the constructor was called
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `allow_threading_guard()`

## lock_gil

- **Signature**: `lock_gil()`
- **Description**: Constructor for the `lock_gil` class. Acquires the Python GIL to ensure thread safety when accessing Python objects.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
lock_gil gil_lock;
// Code that requires the GIL
```
- **Preconditions**: None
- **Postconditions**: The GIL is acquired and held
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `~lock_gil()`

## ~lock_gil

- **Signature**: `~lock_gil()`
- **Description**: Destructor for the `lock_gil` class. Releases the GIL when the object goes out of scope.
- **Parameters**: None
- **Return Value**: None (destructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
{
    lock_gil gil_lock;
    // Code that requires the GIL
} // GIL is automatically released here
```
- **Preconditions**: The `lock_gil` object must have been constructed
- **Postconditions**: The GIL is released
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `lock_gil()`

## allow_threading

- **Signature**: `allow_threading(F fn)`
- **Description**: Constructor for the `allow_threading` class. Stores a function object that will be executed with the GIL released.
- **Parameters**:
  - `fn` (F): The function to be executed with the GIL released
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
allow_threading my_function(some_function);
```
- **Preconditions**: None
- **Postconditions**: The function object is stored and ready to be called
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `operator()`

## operator()

- **Signature**: `R operator()(Self&& s, Args&&... args)`
- **Description**: Function call operator that executes a function with the GIL released.
- **Parameters**:
  - `s` (Self&&): The object on which the function will be called
  - `args` (Args&&...): The arguments to pass to the function
- **Return Value**: The result of the function call
- **Exceptions/Errors**: Any exceptions thrown by the function `fn` will be propagated
- **Example**:
```cpp
allow_threading my_function(some_function);
auto result = my_function(std::move(s), arg1, arg2);
```
- **Preconditions**: The `allow_threading` object must have been constructed with a valid function
- **Postconditions**: The function is executed with the GIL released
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) plus the complexity of the function being called
- **See Also**: `allow_threading`

## visitor

- **Signature**: `visitor(F fn)`
- **Description**: Constructor for the `visitor` class. Stores a function object that will be used to visit a Python class.
- **Parameters**:
  - `fn` (F): The function to be used for visiting the Python class
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
visitor my_visitor(some_function);
```
- **Preconditions**: None
- **Postconditions**: The function object is stored and ready to be used
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `visit_aux`, `visit`

## visit_aux

- **Signature**: `void visit_aux(Class& cl, char const* name, Options const& options, Signature const& signature)`
- **Description**: Auxiliary function that implements the visitation logic for a Python class. This function registers the function with the class using the boost::python library.
- **Parameters**:
  - `cl` (Class&): The Python class to which the function will be registered
  - `name` (char const*): The name of the function to register
  - `options` (Options const&): Options for the function registration
  - `signature` (Signature const&): The signature of the function
- **Return Value**: None
- **Exceptions/Errors**: Any exceptions thrown by the `cl.def` function will be propagated
- **Example**:
```cpp
visitor my_visitor(some_function);
my_visitor.visit_aux(cl, "function_name", options, signature);
```
- **Preconditions**: The `cl` object must be valid, `name` must not be null
- **Postconditions**: The function is registered with the Python class
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) plus the complexity of the `cl.def` function
- **See Also**: `visit`

## visit

- **Signature**: `void visit(Class& cl, char const* name, Options const& options)`
- **Description**: Function that registers a function with a Python class. This function calls `visit_aux` with the appropriate signature.
- **Parameters**:
  - `cl` (Class&): The Python class to which the function will be registered
  - `name` (char const*): The name of the function to register
  - `options` (Options const&): Options for the function registration
- **Return Value**: None
- **Exceptions/Errors**: Any exceptions thrown by the `visit_aux` function will be propagated
- **Example**:
```cpp
visitor my_visitor(some_function);
my_visitor.visit(cl, "function_name", options);
```
- **Preconditions**: The `cl` object must be valid, `name` must not be null
- **Postconditions**: The function is registered with the Python class
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) plus the complexity of the `visit_aux` function
- **See Also**: `visit_aux`

## allow_threads

- **Signature**: `visitor<F> allow_threads(F fn)`
- **Description**: Function that creates a `visitor` object for a given function. This function is a convenience wrapper to create the visitor.
- **Parameters**:
  - `fn` (F): The function to be visited
- **Return Value**: A `visitor` object that can be used to register the function with a Python class
- **Exceptions/Errors**: None
- **Example**:
```cpp
auto visitor = allow_threads(some_function);
```
- **Preconditions**: None
- **Postconditions**: A `visitor` object is created and ready to be used
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `visitor`

## invoke

- **Signature**: `auto invoke(Fn&& fn, Self&& s) -> decltype(auto)`
- **Description**: Function template that invokes a function with the given arguments. This function is used to handle function calls with the correct return type deduction.
- **Parameters**:
  - `fn` (Fn&&): The function to be invoked
  - `s` (Self&&): The object on which the function will be called
- **Return Value**: The result of the function call
- **Exceptions/Errors**: Any exceptions thrown by the function `fn` will be propagated
- **Example**:
```cpp
auto result = invoke(some_function, std::move(s));
```
- **Preconditions**: The function `fn` must be callable with the given arguments
- **Postconditions**: The function is invoked with the given arguments
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) plus the complexity of the function being called
- **See Also**: `invoke` (overload 2)

## invoke

- **Signature**: `auto invoke(Fn&& fn, Args&&... args) -> decltype(auto)`
- **Description**: Function template