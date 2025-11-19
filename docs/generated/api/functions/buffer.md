# libtorrent::aux::buffer API Documentation

## buffer

- **Signature**: `buffer(difference_type size = 0)`
- **Description**: Constructs a buffer of the specified size. The buffer is allocated with `std::malloc` and is 8-byte aligned for better memory access patterns on platforms without `malloc_size()` support.
- **Parameters**:
  - `size` (difference_type): The size of the buffer to allocate. Must be less than `std::numeric_limits<std::int32_t>::max()`. Default is 0, which creates an empty buffer.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: 
  - `std::bad_alloc` may be thrown if memory allocation fails
  - `TORRENT_ASSERT` will trigger if the size exceeds the maximum allowed value
- **Example**:
```cpp
// Create a buffer of 1024 bytes
libtorrent::aux::buffer buf(1024);
```
- **Preconditions**: `size < std::numeric_limits<std::int32_t>::max()`
- **Postconditions**: A buffer of the specified size is created and initialized to zeros
- **Thread Safety**: Thread-safe for concurrent construction
- **Complexity**: O(1) time, O(size) space
- **See Also**: `buffer(buffer const&)`, `buffer(buffer&&)`

## buffer

- **Signature**: `buffer(difference_type const size, span<char const> initialize)`
- **Description**: Constructs a buffer of the specified size and initializes it with the provided data. The initialization copies at most `min(size, initialize.size())` bytes from the source.
- **Parameters**:
  - `size` (difference_type): The size of the buffer to allocate. Must be less than `std::numeric_limits<std::int32_t>::max()`.
  - `initialize` (span<char const>): The span containing data to initialize the buffer with. Must not be larger than the buffer size.
- **Return Value**: None (constructor)
- **Exceptions/Errors**:
  - `std::bad_alloc` may be thrown if memory allocation fails
  - `TORRENT_ASSERT` will trigger if `initialize.size() > size`
- **Example**:
```cpp
// Initialize a buffer with data from an array
char data[] = {'h', 'e', 'l', 'l', 'o'};
libtorrent::aux::buffer buf(10, {data, 5});
```
- **Preconditions**: `size < std::numeric_limits<std::int32_t>::max()` and `initialize.size() <= size`
- **Postconditions**: The buffer is initialized with the first `min(size, initialize.size())` bytes from `initialize`
- **Thread Safety**: Thread-safe for concurrent construction
- **Complexity**: O(min(size, initialize.size())) time, O(size) space
- **See Also**: `buffer(difference_type size)`, `operator[]`

## buffer

- **Signature**: `buffer(buffer const& b) = delete`
- **Description**: Deleted copy constructor to prevent copying of buffer objects. This prevents unintended memory duplication and ensures that only move semantics are used.
- **Parameters**: None (deleted function)
- **Return Value**: None (function is deleted)
- **Exceptions/Errors**: None (function is deleted)
- **Example**: This function cannot be called directly.
- **Preconditions**: None
- **Postconditions**: None
- **Thread Safety**: Not applicable
- **Complexity**: N/A
- **See Also**: `buffer(buffer&&)`

## buffer

- **Signature**: `buffer(buffer&& b)`
- **Description**: Move constructor that transfers ownership of the buffer from the source to the destination. The source buffer is left in a valid but empty state.
- **Parameters**:
  - `b` (buffer&&): The source buffer to move from. This buffer will be left in a valid but empty state.
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::buffer buf1(1024);
libtorrent::aux::buffer buf2(std::move(buf1)); // buf1 is now empty
```
- **Preconditions**: `b` must be a valid buffer object
- **Postconditions**: The destination buffer owns the memory from the source buffer, and the source buffer is left in a valid but empty state
- **Thread Safety**: Thread-safe for concurrent construction
- **Complexity**: O(1) time, O(1) space
- **See Also**: `operator=(buffer&&)`, `swap(buffer&)`

## operator=

- **Signature**: `buffer& operator=(buffer&& b)`
- **Description**: Move assignment operator that transfers ownership of the buffer from the source to the destination. The source buffer is left in a valid but empty state. This function handles self-assignment.
- **Parameters**:
  - `b` (buffer&&): The source buffer to move from. This buffer will be left in a valid but empty state.
- **Return Value**: `buffer&` - a reference to the destination buffer
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::buffer buf1(1024);
libtorrent::aux::buffer buf2;
buf2 = std::move(buf1); // buf1 is now empty
```
- **Preconditions**: `b` must be a valid buffer object
- **Postconditions**: The destination buffer owns the memory from the source buffer, and the source buffer is left in a valid but empty state
- **Thread Safety**: Thread-safe for concurrent assignment
- **Complexity**: O(1) time, O(1) space
- **See Also**: `buffer(buffer&&)`, `swap(buffer&)`

## ~buffer

- **Signature**: `~buffer()`
- **Description**: Destructor that frees the allocated memory using `std::free`. This ensures proper cleanup of the buffer's memory.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
{
    libtorrent::aux::buffer buf(1024);
    // buffer is automatically destroyed here
} // memory is freed when buf goes out of scope
```
- **Preconditions**: None
- **Postconditions**: The allocated memory is freed and the buffer is destroyed
- **Thread Safety**: Thread-safe for concurrent destruction
- **Complexity**: O(1) time, O(1) space
- **See Also**: `buffer()`, `operator=(buffer&&)`

## data

- **Signature**: `char* data()`
- **Description**: Returns a pointer to the beginning of the buffer's memory. This allows direct access to the underlying data.
- **Parameters**: None
- **Return Value**: `char*` - a pointer to the beginning of the buffer's memory
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::buffer buf(1024);
char* ptr = buf.data();
// Use ptr to access the buffer's data
```
- **Preconditions**: The buffer must be valid and not destroyed
- **Postconditions**: A valid pointer to the buffer's memory is returned
- **Thread Safety**: Thread-safe for concurrent access
- **Complexity**: O(1) time, O(1) space
- **See Also**: `data() const`, `begin()`

## data

- **Signature**: `char const* data() const`
- **Description**: Returns a const pointer to the beginning of the buffer's memory. This allows read-only access to the underlying data.
- **Parameters**: None
- **Return Value**: `char const*` - a const pointer to the beginning of the buffer's memory
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::buffer buf(1024);
char const* ptr = buf.data();
// Use ptr to read the buffer's data
```
- **Preconditions**: The buffer must be valid and not destroyed
- **Postconditions**: A valid const pointer to the buffer's memory is returned
- **Thread Safety**: Thread-safe for concurrent access
- **Complexity**: O(1) time, O(1) space
- **See Also**: `data()`, `begin() const`

## size

- **Signature**: `difference_type size() const`
- **Description**: Returns the size of the buffer in bytes.
- **Parameters**: None
- **Return Value**: `difference_type` - the size of the buffer in bytes
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::buffer buf(1024);
difference_type size = buf.size();
// size will be 1024
```
- **Preconditions**: The buffer must be valid and not destroyed
- **Postconditions**: The size of the buffer is returned
- **Thread Safety**: Thread-safe for concurrent access
- **Complexity**: O(1) time, O(1) space
- **See Also**: `empty()`, `begin()`, `end()`

## empty

- **Signature**: `bool empty() const`
- **Description**: Checks if the buffer is empty (size is 0).
- **Parameters**: None
- **Return Value**: `bool` - `true` if the buffer is empty, `false` otherwise
- **Exceptions/Errors**: None
- **Example**:
```cpp
libtorrent::aux::buffer buf(0);
bool is_empty = buf.empty();
// is_empty will be true
```
- **Preconditions**: The buffer must be valid and not destroyed
- **Postconditions**: `true` is returned if the buffer is empty, `false` otherwise
- **Thread Safety**: Thread-safe for concurrent access
- **Complexity**: O(1) time, O(1) space
- **See Also**: `size()`, `data()`

## operator[]

- **Signature**: `char& operator[](index_type const i)`
- **Description**: Returns a reference to the character at the specified index with bounds checking. This allows direct access to individual elements in the buffer.
- **Parameters**:
  - `i` (index_type): The index of the character to access. Must be less than `size()`.
- **Return Value**: `char&` - a reference to the character at the specified index
- **Exceptions/Errors**: `TORRENT_ASSERT` will trigger if `i >= size()`
- **Example**:
```cpp
libtorrent::aux::buffer buf(1024);
buf[0] = 'a'; // Set first character
char c = buf[0]; // Get first character
```
- **