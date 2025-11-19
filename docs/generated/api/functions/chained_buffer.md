# chnaged_buffer API Documentation

## chained_buffer

- **Signature**: `chained_buffer()`
- **Description**: Default constructor for the chained_buffer class. Initializes the buffer with zero bytes and zero capacity, and marks the object as not destructed. This constructor is thread-safe and should be called before any other operations on the buffer.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
chained_buffer buffer;
// The buffer is now initialized and ready for use
```
- **Preconditions**: None
- **Postconditions**: The buffer is initialized with m_bytes = 0, m_capacity = 0, and m_destructed = false
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: append_buffer, prepend_buffer

## buffer_t

- **Signature**: `buffer_t()`
- **Description**: Default constructor for the buffer_t class. Initializes a new buffer_t object with default values.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
buffer_t buffer;
// The buffer is now initialized and ready for use
```
- **Preconditions**: None
- **Postconditions**: The buffer is initialized with default values
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: buffer_t(buffer_t&&), buffer_t(buffer_t const&)

## buffer_t

- **Signature**: `buffer_t(buffer_t&& rhs)`
- **Description**: Move constructor for the buffer_t class. Moves the contents of the source buffer to the destination buffer, leaving the source in a valid but unspecified state. This is a no-op move constructor that transfers ownership of the buffer's data and metadata.
- **Parameters**:
  - `rhs` (buffer_t&&): The source buffer to move from
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
buffer_t buffer1;
// ... populate buffer1 ...
buffer_t buffer2 = std::move(buffer1);
// buffer1 is now in a valid but unspecified state
```
- **Preconditions**: The source buffer must be in a valid state
- **Postconditions**: The destination buffer contains the moved data, and the source buffer is in a valid but unspecified state
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: operator=(buffer_t&&), buffer_t(buffer_t const&)

## destruct_holder

- **Signature**: `buffer_t& operator=(buffer_t&& rhs) & noexcept`
- **Description**: Move assignment operator for the buffer_t class. Moves the contents of the source buffer to the destination buffer, freeing the destination's previous resources. This operation transfers ownership of the buffer's data and metadata.
- **Parameters**:
  - `rhs` (buffer_t&&): The source buffer to move from
- **Return Value**: Reference to the current buffer
- **Exceptions/Errors**: None
- **Example**:
```cpp
buffer_t buffer1;
buffer_t buffer2;
// ... populate buffer1 ...
buffer2 = std::move(buffer1);
// buffer1 is now in a valid but unspecified state
```
- **Preconditions**: The source buffer must be in a valid state
- **Postconditions**: The destination buffer contains the moved data, and the source buffer is in a valid but unspecified state
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: buffer_t(buffer_t&&), operator=(buffer_t const&)

## buffer_t

- **Signature**: `buffer_t(buffer_t const& rhs)`
- **Description**: Copy constructor for the buffer_t class. Creates a copy of the source buffer, duplicating all data and metadata. This constructor is used when you need to create a separate copy of a buffer.
- **Parameters**:
  - `rhs` (buffer_t const&): The source buffer to copy from
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
buffer_t buffer1;
// ... populate buffer1 ...
buffer_t buffer2(buffer1); // Creates a copy
```
- **Preconditions**: The source buffer must be in a valid state
- **Postconditions**: The destination buffer contains a copy of the source buffer's data and metadata
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: operator=(buffer_t const&), buffer_t(buffer_t&&)

## move

- **Signature**: `buffer_t& operator=(buffer_t const& rhs) & noexcept`
- **Description**: Copy assignment operator for the buffer_t class. Copies the contents of the source buffer to the destination buffer, freeing the destination's previous resources. This operator is implemented by calling the move constructor on a temporary moved version of the source.
- **Parameters**:
  - `rhs` (buffer_t const&): The source buffer to copy from
- **Return Value**: Reference to the current buffer
- **Exceptions/Errors**: None
- **Example**:
```cpp
buffer_t buffer1;
buffer_t buffer2;
// ... populate buffer1 ...
buffer2 = buffer1; // Creates a copy
```
- **Preconditions**: The source buffer must be in a valid state
- **Postconditions**: The destination buffer contains a copy of the source buffer's data and metadata
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: buffer_t(buffer_t const&), operator=(buffer_t&&)

## buffer_t

- **Signature**: `buffer_t(buffer_t&&) = delete`
- **Description**: Deleted move constructor for the buffer_t class. This constructor is deleted to prevent accidental move operations on buffer_t objects, as the class is designed to be copied rather than moved.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: Compilation error if attempted
- **Example**: This function cannot be called directly as it's deleted.
- **Preconditions**: None
- **Postconditions**: None
- **Thread Safety**: N/A (function is deleted)
- **Complexity**: N/A (function is deleted)
- **See Also**: buffer_t(buffer_t&&), operator=(buffer_t&&)

## buffer_t

- **Signature**: `buffer_t(buffer_t const&) = delete`
- **Description**: Deleted copy constructor for the buffer_t class. This constructor is deleted to prevent accidental copy operations on buffer_t objects, as the class is designed to be moved rather than copied.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: Compilation error if attempted
- **Example**: This function cannot be called directly as it's deleted.
- **Preconditions**: None
- **Postconditions**: None
- **Thread Safety**: N/A (function is deleted)
- **Complexity**: N/A (function is deleted)
- **See Also**: buffer_t(buffer_t const&), operator=(buffer_t const&)

## size

- **Signature**: `int size() const`
- **Description**: Returns the number of bytes currently stored in the chained buffer.
- **Parameters**: None
- **Return Value**: The number of bytes currently stored in the buffer
- **Exceptions/Errors**: None
- **Example**:
```cpp
chained_buffer buffer;
// ... add data to buffer ...
int bytes = buffer.size();
// bytes contains the number of bytes currently stored in the buffer
```
- **Preconditions**: The buffer must be initialized
- **Postconditions**: The function returns the current number of bytes in the buffer
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: capacity, append_buffer, prepend_buffer

## capacity

- **Signature**: `int capacity() const`
- **Description**: Returns the total capacity of the chained buffer in bytes.
- **Parameters**: None
- **Return Value**: The total capacity of the buffer in bytes
- **Exceptions/Errors**: None
- **Example**:
```cpp
chained_buffer buffer;
// ... add data to buffer ...
int capacity = buffer.capacity();
// capacity contains the total capacity of the buffer
```
- **Preconditions**: The buffer must be initialized
- **Postconditions**: The function returns the current capacity of the buffer
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: size, append_buffer, prepend_buffer

## append_buffer

- **Signature**: `void append_buffer(Holder buffer, int used_size)`
- **Description**: Appends a buffer to the end of the chained buffer. The function adds the provided buffer to the back of the buffer chain and updates the buffer's used size.
- **Parameters**:
  - `buffer` (Holder): The buffer to append
  - `used_size` (int): The number of bytes used in the buffer
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
chained_buffer buffer;
Holder data = createBuffer();
buffer.append_buffer(data, 100);
```
- **Preconditions**: The buffer must be initialized, and the buffer size must be greater than or equal to used_size
- **Postconditions**: The buffer is appended to the end of the chain, and the buffer's used size is updated
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: prepend_buffer, size, capacity

## prepend_buffer

- **Signature**: `void prepend_buffer(Holder buffer, int used_size)`
- **Description**: Prepends a buffer to the beginning of the chained buffer. The function adds the provided buffer to the front of the buffer chain and updates the buffer's used size.
- **Parameters**:
  - `buffer` (Holder): The buffer to prepend
  - `used_size` (int): The number of bytes used in the buffer
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
chained_buffer buffer;
Holder data = createBuffer();
buffer.prepend_buffer(data, 100);
```
- **Preconditions**: The buffer must be initialized, and the buffer size must be greater than or equal to used_size
- **Postconditions**: The buffer is prepended to the beginning of the chain,