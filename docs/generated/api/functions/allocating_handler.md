# API Documentation for `aux_/allocating_handler.hpp`

## handler_storage

- **Signature**: `handler_storage()`
- **Description**: Default constructor for the `handler_storage` class. This creates an empty storage object that can be used to manage memory for handlers.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
handler_storage storage;
```
- **Preconditions**: None
- **Postconditions**: The storage object is in a valid state and ready to be used.
- **Thread Safety**: Thread-safe for construction
- **Complexity**: O(1)
- **See Also**: `handler_storage(handler_storage const&)`

## handler_storage

- **Signature**: `handler_storage(handler_storage const&)`
- **Description**: Deleted copy constructor for the `handler_storage` class. This prevents copying of storage objects, ensuring that each storage object is unique and properly managed.
- **Parameters**: `other` (handler_storage const&): The other storage object to copy from (not used)
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
// This will cause a compilation error
handler_storage storage1;
handler_storage storage2 = storage1; // Error: copy constructor deleted
```
- **Preconditions**: None
- **Postconditions**: None (constructor is deleted)
- **Thread Safety**: N/A (function is deleted)
- **Complexity**: N/A (function is deleted)
- **See Also**: `handler_storage()`

## on_exception

- **Signature**: `virtual void on_exception(std::exception const&) = 0;`
- **Description**: Pure virtual function that must be implemented by derived classes to handle exceptions. This function is called when an exception occurs during handler execution.
- **Parameters**:
  - `e` (std::exception const&): The exception that was thrown
- **Return Value**: None
- **Exceptions/Errors**: None (function is virtual)
- **Example**:
```cpp
class MyErrorHandler : public error_handler_interface {
public:
    void on_exception(std::exception const& e) override {
        std::cerr << "Exception caught: " << e.what() << std::endl;
    }
    void on_error(error_code const& e) override {
        std::cerr << "Error caught: " << e.message() << std::endl;
    }
};
```
- **Preconditions**: The object must be properly constructed and derived from `error_handler_interface`
- **Postconditions**: The exception is handled according to the implementation
- **Thread Safety**: Implementation-dependent
- **Complexity**: Implementation-dependent
- **See Also**: `on_error`

## handler_allocator

- **Signature**: `explicit handler_allocator(handler_storage<Size, Name>* s)`
- **Description**: Constructor that initializes the handler allocator with a specific storage object. This allocator will use the provided storage to allocate memory for handlers.
- **Parameters**:
  - `s` (handler_storage<Size, Name>*): Pointer to the storage object to use for allocation
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
handler_storage<sizeof(MyHandler), "MyHandler"> storage;
handler_allocator<MyHandler> allocator(&storage);
```
- **Preconditions**: The storage pointer must be valid and not null
- **Postconditions**: The allocator is initialized with the specified storage
- **Thread Safety**: Thread-safe for construction
- **Complexity**: O(1)
- **See Also**: `handler_allocator(handler_allocator<U, Size, Name> const&)`

## handler_allocator

- **Signature**: `handler_allocator(handler_allocator<U, Size, Name> const& other)`
- **Description**: Copy constructor that initializes the handler allocator with another allocator of the same type. This allows the allocator to be copied and share the same storage.
- **Parameters**:
  - `other` (handler_allocator<U, Size, Name> const&): The other allocator to copy from
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
handler_allocator<MyHandler> allocator1(&storage);
handler_allocator<MyHandler> allocator2 = allocator1; // Copy constructor called
```
- **Preconditions**: The other allocator must be valid
- **Postconditions**: The allocator is initialized with the same storage as the other allocator
- **Thread Safety**: Thread-safe for construction
- **Complexity**: O(1)
- **See Also**: `handler_allocator(handler_storage<Size, Name>* s)`

## allocate

- **Signature**: `T* allocate(std::size_t size)`
- **Description**: Allocates memory for a handler of type `T` from the storage. This function ensures that the allocated memory is properly managed and checked for validity.
- **Parameters**:
  - `size` (std::size_t): The number of elements to allocate (must be 1)
- **Return Value**: Pointer to the allocated memory (T*)
- **Exceptions/Errors**: Throws an assertion error if the size is not 1 or if the size exceeds the storage capacity
- **Example**:
```cpp
T* ptr = allocator.allocate(1);
if (ptr != nullptr) {
    // Use the allocated memory
}
```
- **Preconditions**: The storage must be valid and not used, and the size must be 1
- **Postconditions**: The memory is allocated and marked as used in the storage
- **Thread Safety**: Not thread-safe (modifies shared state)
- **Complexity**: O(1)
- **See Also**: `deallocate`

## deallocate

- **Signature**: `void deallocate(T* ptr, std::size_t size)`
- **Description**: Deallocates memory for a handler of type `T` from the storage. This function ensures that the deallocated memory is properly validated and the storage state is updated.
- **Parameters**:
  - `ptr` (T*): Pointer to the memory to deallocate
  - `size` (std::size_t): The number of elements to deallocate (must be 1)
- **Return Value**: None
- **Exceptions/Errors**: Throws an assertion error if the size is not 1, if the memory size exceeds the storage capacity, if the pointer is not in the correct location, or if the storage is not marked as used
- **Example**:
```cpp
T* ptr = allocator.allocate(1);
allocator.deallocate(ptr, 1);
```
- **Preconditions**: The memory must be valid and allocated by this allocator, and the size must be 1
- **Postconditions**: The memory is deallocated and the storage state is updated
- **Thread Safety**: Not thread-safe (modifies shared state)
- **Complexity**: O(1)
- **See Also**: `allocate`

## allocating_handler

- **Signature**: `allocating_handler(Handler h, handler_storage<Size, Name>* s, error_handler_interface* eh)`
- **Description**: Constructor that initializes an allocating handler with a specific handler, storage, and error handler. This handler will use the provided storage to manage memory and the error handler to handle exceptions.
- **Parameters**:
  - `h` (Handler): The handler to execute
  - `s` (handler_storage<Size, Name>*): Pointer to the storage object to use for allocation
  - `eh` (error_handler_interface*): Pointer to the error handler to use for exception handling
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
allocating_handler<MyHandler, sizeof(MyHandler), "MyHandler"> handler(
    myHandler, &storage, &errorHandler);
```
- **Preconditions**: The handler, storage, and error handler pointers must be valid
- **Postconditions**: The allocating handler is initialized with the specified components
- **Thread Safety**: Thread-safe for construction
- **Complexity**: O(1)
- **See Also**: `operator()`

## operator()

- **Signature**: `void operator()(A&&... a)`
- **Description**: Executes the handler with the provided arguments. This operator handles exceptions and forwards them to the error handler if necessary.
- **Parameters**:
  - `a` (A&&...): Arguments to pass to the handler
- **Return Value**: None
- **Exceptions/Errors**: Catches `system_error` and `std::exception` and forwards them to the error handler
- **Example**:
```cpp
allocating_handler<MyHandler, sizeof(MyHandler), "MyHandler"> handler(
    myHandler, &storage, &errorHandler);
handler(arg1, arg2); // Executes the handler
```
- **Preconditions**: The handler must be properly initialized
- **Postconditions**: The handler is executed with the provided arguments
- **Thread Safety**: Not thread-safe (modifies shared state)
- **Complexity**: O(1)
- **See Also**: `allocating_handler`

## get_allocator

- **Signature**: `allocator_type get_allocator() const noexcept`
- **Description**: Returns the allocator type associated with this handler. This allocator can be used to allocate memory for handlers.
- **Parameters**: None
- **Return Value**: Allocator type (allocator_type)
- **Exceptions/Errors**: None
- **Example**:
```cpp
allocating_handler<MyHandler, sizeof(MyHandler), "MyHandler"> handler(
    myHandler, &storage, &errorHandler);
auto allocator = handler.get_allocator();
```
- **Preconditions**: The handler must be properly initialized
- **Postconditions**: The allocator is returned
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `allocating_handler`

## make_handler

- **Signature**: `aux::allocating_handler<Handler, Size, Name> make_handler(Handler handler, handler_storage<Size, Name>& storage, error_handler_interface& err_handler)`
- **Description**: Creates an allocating handler with the specified handler, storage, and error handler. This function provides a convenient way to create an allocating handler without