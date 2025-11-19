# C++ Python Bindings Converters API Documentation

This documentation provides comprehensive information about the converter functions in the libtorrent Python bindings. These functions enable seamless conversion between C++ and Python types, allowing Python code to interact with C++ objects and vice versa.

## Function Reference

### convert (Endpoint to Python Tuple)

- **Signature**: `static PyObject* convert(T const& ep)`
- **Description**: Converts a C++ endpoint object to a Python tuple containing the IP address and port number. This function is used as a conversion function in the Boost.Python converter registry.
- **Parameters**:
  - `ep` (T const&): The C++ endpoint object to convert. Must be a valid endpoint with a valid address and port.
- **Return Value**:
  - `PyObject*`: A reference to a Python tuple containing the IP address as a string and the port as an integer. The returned object has an increased reference count.
- **Exceptions/Errors**:
  - None directly, but the function relies on the validity of the input endpoint.
- **Example**:
```cpp
// This function is typically called internally by the converter registry
auto py_tuple = convert(ep);
```
- **Preconditions**: The `ep` parameter must be a valid endpoint object.
- **Postconditions**: Returns a new Python tuple with the endpoint information.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `tuple_to_endpoint`, `convertible`, `construct`

### tuple_to_endpoint

- **Signature**: `tuple_to_endpoint()`
- **Description**: Registers a converter for converting Python tuples to C++ endpoint objects. This function pushes the conversion functions into the Boost.Python converter registry.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
// This function is called during initialization to set up the converter
tuple_to_endpoint();
```
- **Preconditions**: The converter registry must be available.
- **Postconditions**: The endpoint conversion functions are registered in the converter registry.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `convert`, `convertible`, `construct`

### convertible (Endpoint Conversion Check)

- **Signature**: `static void* convertible(PyObject* x)`
- **Description**: Checks if a Python object can be converted to a C++ endpoint. This function is used by the Boost.Python converter registry to determine if a conversion should be attempted.
- **Parameters**:
  - `x` (PyObject*): The Python object to check. Must be a Python tuple.
- **Return Value**:
  - `void*`: Returns the input object if it can be converted, or nullptr if it cannot.
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
// This function is called by the converter registry
void* result = convertible(py_tuple);
if (result) {
    // Conversion can proceed
}
```
- **Preconditions**: The input must be a valid Python object.
- **Postconditions**: Returns the input object if it can be converted, or nullptr otherwise.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `convert`, `construct`, `tuple_to_endpoint`

### construct (Endpoint Construction)

- **Signature**: `