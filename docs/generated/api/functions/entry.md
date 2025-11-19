# libtorrent Python Binding API Documentation

## convert (entry::list_type)
- **Signature**: `auto convert(entry::list_type const& l)`
- **Description**: Converts a libtorrent entry list to a Python list object. This function iterates through the C++ list and appends each entry to a Python list, enabling seamless conversion between libtorrent data structures and Python objects.
- **Parameters**:
  - `l` (entry::list_type const&): The C++ entry list to convert. This must be a valid, non-null list containing libtorrent entry objects.
- **Return Value**:
  - Returns a Python list object containing the converted entries. The returned object is a reference-counted Python object that must be managed properly.
- **Exceptions/Errors**:
  - No exceptions are thrown in normal operation. The function assumes the input is valid and properly constructed.
- **Example**:
```cpp
entry::list_type cpp_list = {entry(123), entry("hello"), entry(45.67)};
object py_list = convert(cpp_list);
// Now py_list is a Python list containing [123, "hello", 45.67]
```
- **Preconditions**: The input list must be a valid, non-null instance of entry::list_type.
- **Postconditions**: Returns a Python list containing the converted entries. The original C++ list remains unchanged.
- **Thread Safety**: Thread-safe for concurrent reads, but concurrent modification is not supported.
- **Complexity**: O(n) time complexity, O(n) space complexity where n is the number of entries.
- **See Also**: `convert(entry::dictionary_type const&)`, `convert0(entry const&)`

## convert (entry::dictionary_type)
- **Signature**: `auto convert(entry::dictionary_type const& d)`
- **Description**: Converts a libtorrent entry dictionary to a Python dictionary object. This function iterates through the C++ dictionary and constructs a Python dictionary with byte-string keys and converted entries as values.
- **Parameters**:
  - `d` (entry::dictionary_type const&): The C++ entry dictionary to convert. This must be a valid, non-null dictionary containing libtorrent entry objects.
- **Return Value**:
  - Returns a Python dictionary object containing the converted entries. The returned object is a reference-counted Python object that must be managed properly.
- **Exceptions/Errors**:
  - No exceptions are thrown in normal operation. The function assumes the input is valid and properly constructed.
- **Example**:
```cpp
entry::dictionary_type cpp_dict = {{"name", entry("test")}, {"port", entry(8080)}};
object py_dict = convert(cpp_dict);
// Now py_dict is a Python dictionary containing {"name": "test", "port": 8080}
```
- **Preconditions**: The input dictionary must be a valid, non-null instance of entry::dictionary_type.
- **Postconditions**: Returns a Python dictionary containing the converted entries. The original C++ dictionary remains unchanged.
- **Thread Safety**: Thread-safe for concurrent reads, but concurrent modification is not supported.
- **Complexity**: O(n) time complexity, O(n) space complexity where n is the number of key-value pairs.
- **See Also**: `convert(entry::list_type const&)`, `convert0(entry const&)`

## convert0 (entry)
- **Signature**: `auto convert0(entry const& e)`
- **Description**: Converts a single libtorrent entry to a corresponding Python object. This function handles different entry types (integer, string, list, dictionary) and converts them appropriately to Python objects.
- **Parameters**:
  - `e` (entry const&): The libtorrent entry to convert. This must be a valid, non-null entry object.
- **Return Value**:
  - Returns a Python object representing the converted entry. The return value is a reference-counted Python object that must be managed properly.
  - Returns an integer object for entry::int_t type
  - Returns a bytes object for entry::string_t type  
  - Returns a list object for entry::list_t type
  - Returns a dictionary object for entry::dictionary_t type
- **Exceptions/Errors**:
  - No exceptions are thrown in normal operation. The function assumes the input is valid and properly constructed.
- **Example**:
```cpp
entry e(entry::int_t);
e.set_integer(42);
object py_obj = convert0(e);
// py_obj is now a Python integer object with value 42
```
- **Preconditions**: The input entry must be a valid, non-null entry object with a properly set type.
- **Postconditions**: Returns a Python object representing the converted entry. The original entry remains unchanged.
- **Thread Safety**: Thread-safe for concurrent reads, but concurrent modification is not supported.
- **Complexity**: O(1) time complexity for basic types, O(n) for container types where n is the number of elements.
- **See Also**: `convert(entry::list_type const&)`, `convert(entry::dictionary_type const&)`

## convert (std::shared_ptr<entry>)
- **Signature**: `auto convert(std::shared_ptr<entry> const& e)`
- **Description**: Converts a shared pointer to a libtorrent entry to a Python object. This function handles null pointers gracefully and converts valid entries using the standard conversion mechanism.
- **Parameters**:
  - `e` (std::shared_ptr<entry> const&): The shared pointer to the libtorrent entry to convert. This can be null.
- **Return Value**:
  - Returns a Python object representing the converted entry, or Py_None if the input pointer is null.
  - The returned object is a reference-counted Python object that must be managed properly.
- **Exceptions/Errors**:
  - No exceptions are thrown in normal operation. The function safely handles null pointers.
- **Example**:
```cpp
std::shared_ptr<entry> ptr = std::make_shared<entry>();
ptr->set_string("hello");
object py_obj = convert(ptr);
// py_obj is now a Python string object with value "hello"
```
- **Preconditions**: The shared pointer can be null or valid.
- **Postconditions**: Returns a Python object representing the converted entry, or Py_None if the input is null. The original entry remains unchanged.
- **Thread Safety**: Thread-safe for concurrent reads, but concurrent modification is not supported.
- **Complexity**: O(1) time complexity.
- **See Also**: `convert(entry const&)`, `convert0(entry const&)`

## convert (entry)
- **Signature**: `auto convert(entry const& e)`
- **Description**: Converts a libtorrent entry to a Python object. This function is the main conversion entry point that calls the appropriate conversion function based on the entry type.
- **Parameters**:
  - `e` (entry const&): The libtorrent entry to convert. This must be a valid, non-null entry object.
- **Return Value**:
  - Returns a Python object representing the converted entry. The returned object is a reference-counted Python object that must be managed properly.
  - The function ensures proper reference counting by using incref on the result.
- **Exceptions/Errors**:
  - No exceptions are thrown in normal operation. The function assumes the input is valid and properly constructed.
- **Example**:
```cpp
entry e(entry::string_t);
e.set_string("test");
PyObject* py_obj = convert(e);
// py_obj is now a Python bytes object with value "test"
```
- **Preconditions**: The input entry must be a valid, non-null entry object.
- **Postconditions**: Returns a Python object representing the converted entry. The original entry remains unchanged.
- **Thread Safety**: Thread-safe for concurrent reads, but concurrent modification is not supported.
- **Complexity**: O(1) time complexity for basic types, O(n) for container types where n is the number of elements.
- **See Also**: `convert0(entry const&)`, `convert(std::shared_ptr<entry> const&)`

## entry_from_python
- **Signature**: `auto entry_from_python()`
- **Description**: Registers a conversion from Python objects to libtorrent entries. This function sets up the necessary converter registry entries to enable automatic conversion of Python objects to libtorrent entries when needed.
- **Parameters**: None
- **Return Value**:
  - Returns void. This function performs registration in a global converter registry.
- **Exceptions/Errors**:
  - No exceptions are thrown in normal operation. The function assumes the underlying converter registry is accessible.
- **Example**:
```cpp
// This function is called during initialization to register the converter
entry_from_python();
// After this call, Python objects can be automatically converted to libtorrent entries
```
- **Preconditions**: The converter registry must be initialized and accessible.
- **Postconditions**: Registers the necessary converter functions in the global converter registry. After this call, Python objects can be converted to libtorrent entries.
- **Thread Safety**: Thread-safe for registration operations, but should only be called during initialization.
- **Complexity**: O(1) time complexity.
- **See Also**: `convertible()`, `construct()`

## convertible
- **Signature**: `auto convertible(PyObject* e)`
- **Description**: Determines if a given Python object can be converted to a libtorrent entry. This function is part of the converter registry and serves as a "check" function to determine if the conversion is possible.
- **Parameters**:
  - `e` (PyObject*): The Python object to check for convertibility. This can be any valid Python object.
- **Return Value**:
  - Returns a pointer to the Python object if conversion is possible, or NULL if conversion is not possible.
  - The function always returns the input object pointer, indicating that all Python objects can be converted (though the conversion might fail at runtime).
- **Exceptions/Errors**:
  - No exceptions are thrown in normal operation. The function assumes the input pointer is valid.
- **Example**:
```cpp
PyObject* py_obj = PyLong_FromLong(42);
void* result = convertible(py_obj);
// result will be the same as py_obj, indicating conversion is possible
```
- **Preconditions**: The input pointer must be a valid Python object or NULL.
- **Postconditions**: Returns the input pointer if conversion is possible, NULL otherwise.
- **Thread Safety**: Thread-safe for concurrent reads, but should be called only during conversion setup.
- **Complexity**: O(1) time complexity.
- **See Also**: `construct()`, `entry_from_python()`

## construct0 (object)
- **Signature**: `auto construct0(object e)`
- **Description**: Constructs a libtorrent entry from a Python object. This function is part of the converter and handles the actual conversion from Python objects to libtorrent entries.
- **Parameters**:
  - `e` (object): The Python object to convert to a libtorrent entry. This can be a dictionary, list, integer, or string.
- **Return Value**:
  - Returns a libtorrent entry object constructed from the Python object. The returned entry is a complete, valid entry object.
- **Exceptions/Errors**:
  - No exceptions are thrown in normal operation. The function assumes the input object is valid.
- **Example**:
```cpp
dict py_dict;
py_dict["name"] = "test";
py_dict["port"] = 8080;
entry result = construct0(object(py_dict));
// result is a libtorrent entry dictionary with the converted values
```
- **Preconditions**: The input object must