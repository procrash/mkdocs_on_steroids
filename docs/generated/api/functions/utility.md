# C++ API Documentation for Utility Functions

## convert

- **Signature**: `PyObject* convert(bytes const& p)`
- **Description**: Converts a `bytes` object to a Python object (PyBytes or PyString depending on Python version). This function is used as a converter in the Boost.Python conversion system to automatically convert C++ `bytes` objects to Python objects.
- **Parameters**:
  - `p` (bytes const&): The bytes object to convert. Must be a valid bytes object containing a sequence of bytes.
- **Return Value**:
  - Returns a Python object (PyBytes or PyString) containing the byte data from the input bytes object.
  - Returns `nullptr` if the conversion fails (though this is unlikely as the function should only be called with valid parameters).
- **Exceptions/Errors**:
  - May throw a `std::bad_alloc` exception if memory allocation fails for the Python object.
- **Example**:
```cpp
bytes data = bytes("hello", "utf-8");
PyObject* py_obj = convert(data);
// Use py_obj in Python code
```
- **Preconditions**: The input `bytes` object must be valid and properly constructed.
- **Postconditions**: The returned PyObject is a valid Python object containing the same byte data as the input.
- **Thread Safety**: Thread-safe, as it only accesses the input parameter and creates a new Python object.
- **Complexity**: O(n) where n is the size of the bytes object.

## convert

- **Signature**: `PyObject* convert(std::array<char, N> const& p)`
- **Description**: Converts a C++ `std::array<char, N>` to a Python object (PyBytes or PyString depending on Python version). This function is used as a converter in the Boost.Python conversion system to automatically convert C++ arrays to Python objects.
- **Parameters**:
  - `p` (std::array<char, N> const&): The array to convert. Must be a valid array of characters with size N.
- **Return Value**:
  - Returns a Python object (PyBytes or PyString) containing the byte data from the input array.
  - Returns `nullptr` if the conversion fails (though this is unlikely as the function should only be called with valid parameters).
- **Exceptions/Errors**:
  - May throw a `std::bad_alloc` exception if memory allocation fails for the Python object.
- **Example**:
```cpp
std::array<char, 10> data = {'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd'};
PyObject* py_obj = convert(data);
// Use py_obj in Python code
```
- **Preconditions**: The input array must be valid and properly constructed.
- **Postconditions**: The returned PyObject is a valid Python object containing the same byte data as the input array.
- **Thread Safety**: Thread-safe, as it only accesses the input parameter and creates a new Python object.
- **Complexity**: O(N) where N is the size of the array.

## bytes_from_python

- **Signature**: `void bytes_from_python()`
- **Description**: Registers the `bytes` type converter with the Boost.Python converter registry. This function enables automatic conversion from Python byte objects to C++ `bytes` objects when passing parameters to C++ functions.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
bytes_from_python();
// Now Python bytes objects can be converted to C++ bytes objects
```
- **Preconditions**: The Boost.Python converter registry must be initialized.
- **Postconditions**: The `bytes` type converter is registered and available for use.
- **Thread Safety**: Thread-safe, as it only modifies the converter registry.
- **Complexity**: O(1) - constant time operation.

## convertible

- **Signature**: `void* convertible(PyObject* x)`
- **Description**: Checks if a Python object can be converted to a `bytes` object. This function is used by Boost.Python as a predicate to determine if a Python object should be converted to a C++ `bytes` object.
- **Parameters**:
  - `x` (PyObject*): The Python object to check. Must be a valid Python object.
- **Return Value**:
  - Returns the input object if it is a PyBytes or PyByteArray (for Python 3) or PyString (for Python 2).
  - Returns `nullptr` if the object cannot be converted to a `bytes` object.
- **Exceptions/Errors**: None
- **Example**:
```cpp
PyObject* py_obj = PyBytes_FromStringAndSize("hello", 5);
void* result = convertible(py_obj);
// If result is not nullptr, the object can be converted to bytes
```
- **Preconditions**: The input Python object must be valid and not null.
- **Postconditions**: Returns a pointer to the original object if convertible, or nullptr if not.
- **Thread Safety**: Thread-safe, as it only reads the object's type information.
- **Complexity**: O(1) - constant time operation.

## construct

- **Signature**: `void construct(PyObject* x, converter::rvalue_from_python_stage1_data* data)`
- **Description**: Constructs a `bytes` object from a Python object. This function is used by Boost.Python as the conversion constructor to create a C++ `bytes` object from a Python object.
- **Parameters**:
  - `x` (PyObject*): The Python object to convert. Must be a valid Python object that has been checked by the `convertible` function.
  - `data` (converter::rvalue_from_python_stage1_data*): The conversion data structure where the constructed object will be stored.
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
PyObject* py_obj = PyBytes_FromStringAndSize("hello", 5);
converter::rvalue_from_python_stage1_data data;
construct(py_obj, &data);
// The bytes object is now constructed and stored in the data structure
```
- **Preconditions**: The input object must be convertible (as checked by `convertible` function), and the data structure must be valid.
- **Postconditions**: The `bytes` object is constructed and stored in the provided data structure.
- **Thread Safety**: Thread-safe, as it only reads the input object and constructs the output.
- **Complexity**: O(n) where n is the size of the Python object's data.

## client_fingerprint_

- **Signature**: `object client_fingerprint_(peer_id const& id)`
- **Description**: Extracts the client fingerprint from a peer ID, returning it as a Python object. This function is deprecated and should not be used in new code.
- **Parameters**:
  - `id` (peer_id const&): The peer ID to extract the fingerprint from. Must be a valid peer ID.
- **Return Value**:
  - Returns a Python object containing the fingerprint if successful.
  - Returns an empty Python object if the fingerprint cannot be extracted or if the peer ID is invalid.
- **Exceptions/Errors**: None
- **Example**:
```cpp
peer_id id = peer_id("ABC123");
object result = client_fingerprint_(id);
if (!result.is_none()) {
    // Use the result
}
```
- **Preconditions**: The input peer ID must be valid and properly constructed.
- **Postconditions**: Returns a Python object containing the extracted fingerprint, or an empty object if extraction fails.
- **Thread Safety**: Thread-safe, as it only reads the input parameter.
- **Complexity**: O(1) - constant time operation.

## bdecode_

- **Signature**: `entry bdecode_(bytes const& data)`
- **Description**: Decodes a bencoded string into an `entry` object. This function is used to parse bencoded data (such as torrent metadata) into a structured format.
- **Parameters**:
  - `data` (bytes const&): The bencoded data to decode. Must be a valid bencoded string.
- **Return Value**:
  - Returns an `entry` object containing the decoded data structure.
  - In case of decoding errors, the function may return an `entry` object in an invalid state (which can be checked with appropriate methods).
- **Exceptions/Errors**: May throw a `libtorrent::invalid_bencode` exception if the input data is not valid bencoded data.
- **Example**:
```cpp
bytes data = bytes("d4:infod6:piece8:82578852e", "utf-8");
entry result = bdecode_(data);
if (result.is_dict()) {
    // Process the dictionary
}
```
- **Preconditions**: The input data must be a valid bencoded string.
- **Postconditions**: Returns an entry object containing the decoded data structure.
- **Thread Safety**: Thread-safe, as it only reads the input parameter and creates new objects.
- **Complexity**: O(n) where n is the size of the input data.

## bencode_

- **Signature**: `bytes bencode_(entry const& e)`
- **Description**: Encodes an `entry` object into a bencoded string. This function is used to serialize structured data into the bencoded format (such as for torrent files).
- **Parameters**:
  - `e` (entry const&): The entry object to encode. Must be a valid entry object.
- **Return Value**:
  - Returns a bytes object containing the bencoded data.
  - Returns an empty bytes object if encoding fails.
- **Exceptions/Errors**: None
- **Example**:
```cpp
entry e;
e["key"] = "value";
bytes result = bencode_(e);
// Use the result in a torrent file or network transmission
```
- **Preconditions**: The input entry object must be valid and properly constructed.
- **Postconditions**: Returns a bytes object containing the bencoded data.
- **Thread Safety**: Thread-safe, as it only reads the input parameter and creates new objects.
- **Complexity**: O(n) where n is the size of the input data structure.

## bind_utility

- **Signature**: `void bind_utility()`
- **Description**: Registers various type converters with the Boost.Python conversion system, enabling automatic conversion between C++ and Python types. This function is typically called during module initialization.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
bind_utility();
// Now various C++ types can be automatically converted to Python types
```
- **Preconditions**: The Boost.Python converter registry must be initialized.
- **Postconditions**: Various type converters are registered and available for use.
- **Thread Safety**: Thread-safe, as it only modifies the converter registry.
- **Complexity**: O(1) - constant time operation.

## Usage Examples

### Basic Usage

```cpp
#include "utility.hpp"  // Assuming the header file exists

// Convert a Python bytes object to C++ bytes
bytes data("hello", "utf-8");
PyObject* py_obj = convert(data);

// Decode bencoded data
bytes bencoded_data("d4:infod6:piece8:82578852e", "utf-8");
entry decoded = bdecode_(bencoded_data);

// Encode data to bencoded format
entry e;
e["name"] = "example";
bytes encoded = bencode_(e);
``