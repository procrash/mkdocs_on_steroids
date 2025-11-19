# libtorrent Auxiliary I/O Functions API Documentation

## `read_impl` (template)

- **Signature**: `template<typename T> auto read_impl(span<Byte>& view, type<T>)`
- **Description**: Reads a value of type T from a byte span, extracting the bytes and advancing the view. This is a low-level implementation function used by higher-level read functions. The function assumes that the byte span has at least sizeof(T) bytes available and that the endianness matches the target architecture.
- **Parameters**:
  - `view` (span<Byte>&): A mutable reference to a span of bytes from which to read the value. The span must have at least sizeof(T) bytes available. After the function call, the view will be advanced by sizeof(T) bytes.
  - `type<T>`: A type tag indicating the type of data to read. This is used for template specialization.
- **Return Value**: Returns a value of type T containing the data read from the byte span.
- **Exceptions/Errors**:
  - `std::assert`: The function includes an assertion that fails if the source data cannot be safely cast to the target type T.
  - **Buffer overflow**: If the view has fewer than sizeof(T) bytes remaining, the behavior is undefined (typically results in a crash or incorrect data).
- **Example**:
```cpp
#include <libtorrent/aux_/io.hpp>
#include <span>

std::uint32_t value;
span<Byte> buffer = /* some buffer */;
value = read_impl(buffer, type<std::uint32_t>());
```
- **Preconditions**: 
  - The view must have at least sizeof(T) bytes available.
  - The Byte type must be exactly 1 byte in size (verified by static_assert).
  - The type T must be a fundamental integral type.
- **Postconditions**: 
  - The returned value contains the data read from the view.
  - The view has been advanced by sizeof(T) bytes.
  - The view is no longer valid if it had exactly sizeof(T) bytes before the call.
- **Thread Safety**: The function is thread-safe as long as the underlying data is not modified concurrently.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `read_uint32`, `read_int64`, `read_uint8`

## `write_impl` (template)

- **Signature**: `template<typename T> auto write_impl(In data, span<Byte>& view)`
- **Description**: Writes a value of type T to a byte span, storing the bytes in network byte order (big-endian). This is a low-level implementation function used by higher-level write functions. The function assumes that the byte span has at least sizeof(T) bytes available and that the endianness matches the target architecture.
- **Parameters**:
  - `data` (In): The value to write to the byte span. This must be convertible to T without loss of information.
  - `view` (span<Byte>&): A mutable reference to a span of bytes to which to write the value. The span must have at least sizeof(T) bytes available. After the function call, the view will be advanced by sizeof(T) bytes.
- **Return Value**: None (void function).
- **Exceptions/Errors**:
  - `std::assert`: The function includes an assertion that fails if the data cannot be safely cast to the target type T.
  - **Buffer overflow**: If the view has fewer than sizeof(T) bytes remaining, the behavior is undefined (typically results in a crash or incorrect data).
- **Example**:
```cpp
#include <libtorrent/aux_/io.hpp>
#include <span>

std::uint32_t value = 12345;
span<Byte> buffer = /* some buffer */;
write_impl<std::uint32_t>(value, buffer);
```
- **Preconditions**: 
  - The view must have at least sizeof(T) bytes available.
  - The Byte type must be exactly 1 byte in size (verified by static_assert).
  - The type T must be a fundamental integral type.
  - The type In must be either an integral type or an enumeration type.
- **Postconditions**: 
  - The value has been written to the view.
  - The view has been advanced by sizeof(T) bytes.
  - The view is no longer valid if it had exactly sizeof(T) bytes before the call.
- **Thread Safety**: The function is thread-safe as long as the underlying data is not modified concurrently.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `write_uint32`, `write_int64`, `write_uint8`

## `read_uint64`

- **Signature**: `std::uint64_t read_uint64(span<Byte>& view)`
- **Description**: Reads an unsigned 64-bit integer from a byte span in network byte order (big-endian). This function is a wrapper around the generic read_impl template with T=std::uint64_t.
- **Parameters**:
  - `view` (span<Byte>&): A mutable reference to a span of bytes from which to read the value. The span must have at least 8 bytes available. After the function call, the view will be advanced by 8 bytes.
- **Return Value**: Returns the unsigned 64-bit integer value read from the byte span.
- **Exceptions/Errors**:
  - **Buffer overflow**: If the view has fewer than 8 bytes remaining, the behavior is undefined (typically results in a crash or incorrect data).
- **Example**:
```cpp
#include <libtorrent/aux_/io.hpp>
#include <span>

std::uint64_t value;
span<Byte> buffer = /* some buffer */;
value = read_uint64(buffer);
```
- **Preconditions**: 
  - The view must have at least 8 bytes available.
- **Postconditions**: 
  - The returned value contains the data read from the view.
  - The view has been advanced by 8 bytes.
- **Thread Safety**: The function is thread-safe as long as the underlying data is not modified concurrently.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `read_impl`, `write_uint64`, `read_uint32`

## `read_int64`

- **Signature**: `std::int64_t read_int64(span<Byte>& view)`
- **Description**: Reads a signed 64-bit integer from a byte span in network byte order (big-endian). This function is a wrapper around the generic read_impl template with T=std::int64_t.
- **Parameters**:
  - `view` (span<Byte>&): A mutable reference to a span of bytes from which to read the value. The span must have at least 8 bytes available. After the function call, the view will be advanced by 8 bytes.
- **Return Value**: Returns the signed 64-bit integer value read from the byte span.
- **Exceptions/Errors**:
  - **Buffer overflow**: If the view has fewer than 8 bytes remaining, the behavior is undefined (typically results in a crash or incorrect data).
- **Example**:
```cpp
#include <libtorrent/aux_/io.hpp>
#include <span>

std::int64_t value;
span<Byte> buffer = /* some buffer */;
value = read_int64(buffer);
```
- **Preconditions**: 
  - The view must have at least 8 bytes available.
- **Postconditions**: 
  - The returned value contains the data read from the view.
  - The view has been advanced by 8 bytes.
- **Thread Safety**: The function is thread-safe as long as the underlying data is not modified concurrently.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `read_impl`, `write_int64`, `read_int32`

## `read_uint32`

- **Signature**: `std::uint32_t read_uint32(span<Byte>& view)`
- **Description**: Reads an unsigned 32-bit integer from a byte span in network byte order (big