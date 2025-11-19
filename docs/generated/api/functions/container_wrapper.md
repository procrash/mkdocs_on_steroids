# API Documentation for container_wrapper

## container_wrapper

- **Signature**: `container_wrapper()`
- **Description**: Default constructor for the `container_wrapper` class. Initializes the container with default values.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
container_wrapper<int> container;
// container is now initialized with default values
```
- **Preconditions**: None
- **Postconditions**: The container is in a valid, default-constructed state
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `container_wrapper(Base&& b)`, `container_wrapper(IndexType const s)`

## container_wrapper

- **Signature**: `container_wrapper(Base&& b)`
- **Description**: Move constructor for the `container_wrapper` class. Takes ownership of a base container through move semantics.
- **Parameters**:
  - `b` (Base&&): The base container to move into this wrapper
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
std::vector<int> vec = {1, 2, 3};
container_wrapper<int> container(std::move(vec));
// vec is now in a valid but unspecified state
```
- **Preconditions**: The provided `Base` container must be in a valid state
- **Postconditions**: The container wrapper holds the moved container
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `container_wrapper()`, `container_wrapper(IndexType const s)`

## container_wrapper

- **Signature**: `container_wrapper(IndexType const s)`
- **Description**: Constructor that initializes the container with a specified size.
- **Parameters**:
  - `s` (IndexType const): The size of the container to create
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
container_wrapper<int> container(100);
// container is initialized with 100 elements (default-constructed)
```
- **Preconditions**: `s` must be non-negative
- **Postconditions**: The container has size `s`
- **Thread Safety**: Thread-safe
- **Complexity**: O(s)
- **See Also**: `container_wrapper()`, `container_wrapper(Base&& b)`

## operator[]

- **Signature**: `decltype(auto) operator[](IndexType idx) const`
- **Description**: Const overload of the subscript operator for accessing elements in the container.
- **Parameters**:
  - `idx` (IndexType): The index of the element to access
- **Return Value**: Reference to the element at the specified index
- **Exceptions/Errors**: Throws an assertion failure if `idx` is out of bounds
- **Example**:
```cpp
container_wrapper<int> container(10);
container[5] = 42;
int value = container[5]; // value = 42
```
- **Preconditions**: `idx` must be >= 0 and < `end_index()`
- **Postconditions**: Returns a reference to the element at index `idx`
- **Thread Safety**: Thread-safe for concurrent reads
- **Complexity**: O(1)
- **See Also**: `operator[](IndexType idx)`, `end_index()`

## operator[]

- **Signature**: `decltype(auto) operator[](IndexType idx)`
- **Description**: Non-const overload of the subscript operator for accessing and modifying elements in the container.
- **Parameters**:
  - `idx` (IndexType): The index of the element to access
- **Return Value**: Reference to the element at the specified index
- **Exceptions/Errors**: Throws an assertion failure if `idx` is out of bounds
- **Example**:
```cpp
container_wrapper<int> container(10);
container[5] = 42; // Assign value to element at index 5
int value = container[5]; // Read value from element at index 5
```
- **Preconditions**: `idx` must be >= 0 and < `end_index()`
- **Postconditions**: Returns a reference to the element at index `idx`
- **Thread Safety**: Thread-safe for concurrent reads, but not for concurrent writes
- **Complexity**: O(1)
- **See Also**: `operator[](IndexType idx) const`, `end_index()`

## end_index

- **Signature**: `IndexType end_index() const`
- **Description**: Returns the end index of the container, which is the size of the container.
- **Parameters**: None
- **Return Value**: The end index of the container
- **Exceptions/Errors**: None
- **Example**:
```cpp
container_wrapper<int> container(10);
std::cout << "End index: " << container.end_index() << std::endl; // Output: 10
```
- **Preconditions**: None
- **Postconditions**: Returns the size of the container as an `IndexType`
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `range()`, `resize()`

## range

- **Signature**: `index_range<IndexType> range() const noexcept`
- **Description**: Returns a range object representing the valid range of indices in the container.
- **Parameters**: None
- **Return Value**: An `index_range` object containing the start and end indices
- **Exceptions/Errors**: None
- **Example**:
```cpp
container_wrapper<int> container(10);
auto range = container.range();
std::cout << "Range: [" << range.start << ", " << range.end << ")" << std::endl;
```
- **Preconditions**: None
- **Postconditions**: Returns a valid range object
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `end_index()`, `resize()`

## resize

- **Signature**: `void resize(underlying_index s)`
- **Description**: Resizes the container to the specified size using `underlying_index`.
- **Parameters**:
  - `s` (underlying_index): The new size of the container
- **Return Value**: None
- **Exceptions/Errors**: Throws an assertion failure if `s` is negative
- **Example**:
```cpp
container_wrapper<int> container(10);
container.resize(20); // Resize to 20 elements
```
- **Preconditions**: `s` must be >= 0
- **Postconditions**: The container has size `s`, with new elements default-constructed
- **Thread Safety**: Not thread-safe during resize
- **Complexity**: O(s)
- **See Also**: `resize(std::size_t s)`, `resize(underlying_index s, T const& v)`

## resize

- **Signature**: `void resize(underlying_index s, T const& v)`
- **Description**: Resizes the container to the specified size and initializes new elements with a default value.
- **Parameters**:
  - `s` (underlying_index): The new size of the container
  - `v` (T const&): The value to initialize new elements with
- **Return Value**: None
- **Exceptions/Errors**: Throws an assertion failure if `s` is negative
- **Example**:
```cpp
container_wrapper<int> container(10);
container.resize(20, 42); // Resize to 20 elements, initialize with 42
```
- **Preconditions**: `s` must be >= 0
- **Postconditions**: The container has size `s`, with new elements initialized to `v`
- **Thread Safety**: Not thread-safe during resize
- **Complexity**: O(s)
- **See Also**: `resize(underlying_index s)`, `resize(std::size_t s, T const& v)`

## resize

- **Signature**: `void resize(std::size_t s)`
- **Description**: Resizes the container to the specified size.
- **Parameters**:
  - `s` (std::size_t): The new size of the container
- **Return Value**: None
- **Exceptions/Errors**: Throws an assertion failure if `s` exceeds the maximum value of `underlying_index`
- **Example**:
```cpp
container_wrapper<int> container(10);
container.resize(20); // Resize to 20 elements
```
- **Preconditions**: `s` must be <= maximum value of `underlying_index`
- **Postconditions**: The container has size `s`, with new elements default-constructed
- **Thread Safety**: Not thread-safe during resize
- **Complexity**: O(s)
- **See Also**: `resize(underlying_index s)`, `resize(std::size_t s, T const& v)`

## resize

- **Signature**: `void resize(std::size_t s, T const& v)`
- **Description**: Resizes the container to the specified size and initializes new elements with a default value.
- **Parameters**:
  - `s` (std::size_t): The new size of the container
  - `v` (T const&): The value to initialize new elements with
- **Return Value**: None
- **Exceptions/Errors**: Throws an assertion failure if `s` exceeds the maximum value of `underlying_index`
- **Example**:
```cpp
container_wrapper<int> container(10);
container.resize(20, 42); // Resize to 20 elements, initialize with 42
```
- **Preconditions**: `s` must be <= maximum value of `underlying_index`
- **Postconditions**: The container has size `s`, with new elements initialized to `v`
- **Thread Safety**: Not thread-safe during resize
- **Complexity**: O(s)
- **See Also**: `resize(std::size_t s)`, `resize(underlying_index s, T const& v)`

## reserve

- **Signature**: `void reserve(underlying_index s)`
- **Description**: Reserves storage for the container to avoid reallocations.
- **Parameters**:
  - `s` (underlying_index): The number of elements to reserve storage for
- **Return Value**: None
- **Exceptions/Errors**: Throws an assertion failure if `s` is negative
- **Example**:
```cpp
container_wrapper<int> container;
container.reserve(100); // Reserve space for 100 elements
```
- **Preconditions**: `s` must be >= 0
- **Postconditions**: The container's capacity is at least `s`
- **Thread Safety**: Thread-safe
- **Complexity**: O(s)
- **See Also**: `reserve(std::size_t s)`, `resize()`

## reserve

- **Signature**: `void reserve(std::size