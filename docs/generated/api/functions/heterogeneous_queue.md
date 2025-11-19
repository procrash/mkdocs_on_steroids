# API Documentation for `heterogeneous_queue.hpp`

## operator

- **Signature**: `void operator()(char* ptr)`
- **Description**: This function is an instance of a function object (functor) that invokes `std::free()` on the provided pointer. It's designed to be used as a custom deleter for `std::unique_ptr` to properly deallocate memory allocated with `std::malloc()`.
- **Parameters**:
  - `ptr` (char*): A pointer to memory that was allocated with `std::malloc()`. The pointer must be valid and must point to memory that was allocated with `std::malloc()` or `std::realloc()`. Passing a null pointer or a pointer to memory not allocated with `std::malloc()` results in undefined behavior.
- **Return Value**: None. This function does not return a value.
- **Exceptions/Errors**: This function does not throw exceptions. However, if `ptr` is invalid (e.g., null or points to unallocated memory), the behavior is undefined.
- **Example**:
```cpp
auto deleter = operator()();
char* memory = static_cast<char*>(std::malloc(1024));
// Use memory...
deleter(memory); // Properly deallocate memory
```
- **Preconditions**: The pointer must be a valid pointer returned by `std::malloc()`.
- **Postconditions**: The memory pointed to by `ptr` is deallocated and is no longer accessible.
- **Thread Safety**: This function is thread-safe as it only calls a standard library function (`std::free`) which is thread-safe.
- **Complexity**: O(1) - constant time.
- **See Also**: `std::malloc`, `std::free`, `std::unique_ptr`, `aux::free_deleter`

## calculate_pad_bytes

- **Signature**: `inline std::size_t calculate_pad_bytes(char const* inptr, std::size_t alignment)`
- **Description**: This function calculates the number of padding bytes required to align a given memory address to a specified alignment boundary. It's used internally by the `heterogeneous_queue` to ensure proper memory alignment for objects stored in the queue.
- **Parameters**:
  - `inptr` (char const*): A pointer to the memory location whose alignment we want to check. The pointer must be valid and must point to a memory location that is properly aligned for the given alignment.
  - `alignment` (std::size_t): The alignment boundary in bytes. This value must be a power of two (e.g., 1, 2, 4, 8, 16, etc.) and must be greater than zero. The function will return the number of bytes needed to pad the current address to reach the next multiple of this alignment.
- **Return Value**: The number of bytes needed to pad the memory address to the specified alignment boundary. This value will be in the range [0, alignment - 1].
- **Exceptions/Errors**: This function does not throw exceptions. However, if the `alignment` parameter is not a power of two or is zero, the behavior is undefined.
- **Example**:
```cpp
char* ptr = reinterpret_cast<char*>(0x1001);
std::size_t padding = calculate_pad_bytes(ptr, 8);
// padding will be 7, because 0x1001 + 7 = 0x1008, which is aligned to 8 bytes
```
- **Preconditions**: The `inptr` must be a valid pointer to a memory location, and the `alignment` must be a power of two and greater than zero.
- **Postconditions**: The return value is the number of bytes needed to align the address to the specified boundary.
- **Thread Safety**: This function is thread-safe as it only performs arithmetic operations on the input parameters.
- **Complexity**: O(1) - constant time.
- **See Also**: `heterogeneous_queue`, `alignof`, `std::uintptr_t`

## heterogeneous_queue

- **Signature**: `heterogeneous_queue()`
- **Description**: Default constructor for the `heterogeneous_queue` class. Initializes an empty queue with no items. The queue is backed by a dynamically allocated memory block that is managed by a `std::unique_ptr` with a custom deleter to ensure proper memory cleanup.
- **Parameters**: None.
- **Return Value**: None. This function does not return a value.
- **Exceptions/Errors**: This function does not throw exceptions. However, if there is insufficient memory to allocate the initial storage, it may throw a `std::bad_alloc` exception.
- **Example**:
```cpp
heterogeneous_queue<int> queue;
// queue is now an empty queue ready for use
```
- **Preconditions**: None.
- **Postconditions**: The queue is initialized to an empty state with no items.
- **Thread Safety**: This function is thread-safe.
- **Complexity**: O(1) - constant time.
- **See Also**: `~heterogeneous_queue`, `clear`, `empty`, `size`

## heterogeneous_queue

- **Signature**: `heterogeneous_queue(heterogeneous_queue const&) = delete;`
- **Description**: Deleted copy constructor for the `heterogeneous_queue` class. This prevents the copying of `heterogeneous_queue` objects. The queue is designed to be moved rather than copied due to its internal memory management.
- **Parameters**: None.
- **Return Value**: None. This function is deleted and cannot be called.
- **Exceptions/Errors**: Attempting to copy a `heterogeneous_queue` object will result in a compile-time error.
- **Example**: This function cannot be called directly, but the following code will result in a compile error:
```cpp
heterogeneous_queue<int> queue1;
heterogeneous_queue<int> queue2 = queue1; // Compile error: copy constructor is deleted
```
- **Preconditions**: None.
- **Postconditions**: None.
- **Thread Safety**: This function is not applicable as it is deleted.
- **Complexity**: Not applicable.
- **See Also**: `swap`, `operator=`, `move`, `heterogeneous_queue`

## emplace_back

- **Signature**: `typename std::enable_if<std::is_base_of<T, U>::value, U&>::type emplace_back(Args&&... args)`
- **Description**: This function template adds a new object of type `U` to the end of the queue. The object is constructed in-place using the provided arguments `args`. The function uses SFINAE (Substitution Failure Is Not An Error) to ensure that `U` is a derived class of `T`, making the queue heterogeneous. If the queue does not have enough capacity, it grows its capacity to accommodate the new object.
- **Parameters**:
  - `args` (Args&&...): Arguments to forward to the constructor of `U`. These arguments are used to construct the new object in-place within the queue's storage.
- **Return Value**: A reference to the newly constructed object of type `U`.
- **Exceptions/Errors**: This function may throw exceptions if the constructor of `U` throws an exception. If the allocation of additional memory fails, it may throw a `std::bad_alloc` exception.
- **Example**:
```cpp
heterogeneous_queue<Base> queue;
// Assuming Derived is a derived class of Base
Derived& obj = queue.emplace_back(1, 2, 3); // Construct Derived with arguments 1, 2, 3
```
- **Preconditions**: The queue must be in a valid state, and `U` must be a derived class of `T`.
- **Postconditions**: The queue contains the newly constructed object, and the size of the queue is increased by one.
- **Thread Safety**: This function is not thread-safe. Multiple threads should not call this function simultaneously without external synchronization.
- **Complexity**: O(1) average case, O(n) worst case (when the queue needs to grow its capacity).
- **See Also**: `heterogeneous_queue`, `emplace_front`, `clear`, `size`

## get_pointers

- **Signature**: `void get_pointers(std::vector<T*>& out)`
- **Description**: This function retrieves pointers to all objects of type `T` currently stored in the queue and adds them to the provided vector. The function traverses the internal storage of the queue, extracting the pointers to the objects of type `T`.
- **Parameters**:
  - `out` (std::vector<T*>&): A reference to a vector where the pointers to the objects of type `T` will be stored. The vector will be cleared before adding the pointers.
- **Return Value**: None. This function does not return a value.
- **Exceptions/Errors**: This function does not throw exceptions. However, if the internal state of the queue is corrupted, it may cause undefined behavior.
- **Example**:
```cpp
heterogeneous_queue<Base> queue;
// Add some Base objects to the queue
std::vector<Base*> pointers;
queue.get_pointers(pointers);
// pointers now contains pointers to all Base objects in the queue
```
- **Preconditions**: The queue must be in a valid state, and `T` must be the base type of the objects stored in the queue.
- **Postconditions**: The `out` vector contains pointers to all objects of type `T` in the queue, in the order they were added.
- **Thread Safety**: This function is not thread-safe. Multiple threads should not call this function simultaneously without external synchronization.
- **Complexity**: O(n) - linear time, where n is the number of items in the queue.
- **See Also**: `heterogeneous_queue`, `size`, `front`, `back`

## swap

- **Signature**: `void swap(heterogeneous_queue&