# API Documentation for datetime.cpp

## Function: convert (Duration)

- **Signature**: `PyObject* convert(Duration const& d)`
- **Description**: Converts a libtorrent Duration object to a Python datetime.timedelta object. The function extracts the total microseconds from the Duration and creates a timedelta object with the corresponding days, seconds, and microseconds.
- **Parameters**:
  - `d` (Duration const&): The libtorrent Duration object to convert. Must be a valid Duration object representing a time interval.
- **Return Value**:
  - Returns a new Python object (PyObject*) representing a datetime.timedelta object. The reference count is incremented, so the caller must decrement it when done.
- **Exceptions/Errors**:
  - No exceptions are thrown, but the function assumes the input Duration is valid.
- **Example**:
```cpp
auto result = convert(lt::duration(1000ms));
// Use result in Python code
```
- **Preconditions**: The input Duration must be valid and represent a non-negative time interval.
- **Postconditions**: The returned PyObject is a valid Python datetime.timedelta object with the correct time interval.
- **Thread Safety**: This function is thread-safe as it only reads the input and creates new Python objects.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `convert(boost::posix_time::time_duration const&)`, `bind_datetime()`

## Function: convert (time_duration)

- **Signature**: `PyObject* convert(boost::posix_time::time_duration const& d)`
- **Description**: Converts a boost::posix_time::time_duration object to a Python datetime.timedelta object. The function extracts the total microseconds from the time_duration and creates a timedelta object with the corresponding seconds and microseconds.
- **Parameters**:
  - `d` (boost::posix_time::time_duration const&): The time_duration object to convert. Must be a valid time_duration object representing a time interval.
- **Return Value**:
  - Returns a new Python object (PyObject*) representing a datetime.timedelta object. The reference count is incremented, so the caller must decrement it when done.
- **Exceptions/Errors**:
  - No exceptions are thrown, but the function assumes the input time_duration is valid.
- **Example**:
```cpp
auto result = convert(boost::posix_time::time_duration(1, 2, 3));
// Use result in Python code
```
- **Preconditions**: The input time_duration must be valid and represent a non-negative time interval.
- **Postconditions**: The returned PyObject is a valid Python datetime.timedelta object with the correct time interval.
- **Thread Safety**: This function is thread-safe as it only reads the input and creates new Python objects.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `convert(Duration const&)`, `bind_datetime()`

## Function: now (time_point)

- **Signature**: `lt::time_point now(::tag<lt::time_point>)`
- **Description**: Returns the current time point from the libtorrent clock. This function is used to get the current time in the libtorrent system clock.
- **Parameters**:
  - `tag` (::tag<lt::time_point>): A tag type used to disambiguate function overloads. The function uses this to determine which overload to call.
- **Return Value**:
  - Returns the current time point as `lt::time_point`. This represents the current time in the libtorrent system clock.
- **Exceptions/Errors**:
  - No exceptions are thrown.
- **Example**:
```cpp
auto current_time = now(::tag<lt::time_point>());
// Use current_time in libtorrent operations
```
- **Preconditions**: None.
- **Postconditions**: The returned `lt::time_point` represents the current time in the libtorrent system clock.
- **Thread Safety**: This function is thread-safe as it only reads the clock.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `now(lt::time_point32)`, `bind_datetime()`

## Function: now (time_point32)

- **Signature**: `lt::time_point32 now(::tag<lt::time_point32>)`
- **Description**: Returns the current time point from the libtorrent clock, but cast to `lt::time_point32` (a 32-bit time point). This function is used to get the current time in a 32-bit format for compatibility with systems that have limited time point precision.
- **Parameters**:
  - `tag` (::tag<lt::time_point32>): A tag type used to disambiguate function overloads. The function uses this to determine which overload to call.
- **Return Value**:
  - Returns the current time point as `lt::time_point32`. This represents the current time in the libtorrent system clock, but truncated to 32 bits.
- **Exceptions/Errors**:
  - No exceptions are thrown.
- **Example**:
```cpp
auto current_time = now(::tag<lt::time_point32>());
// Use current_time in libtorrent operations with 32-bit time points
```
- **Preconditions**: None.
- **Postconditions**: The returned `lt::time_point32` represents the current time in the libtorrent system clock, but truncated to 32 bits.
- **Thread Safety**: This function is thread-safe as it only reads the clock.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `now(lt::time_point)`, `bind_datetime()`

## Function: convert (T)

- **Signature**: `PyObject* convert(T const pt)`
- **Description**: Converts a time point of type T to a Python datetime.datetime object. The function converts the time point to a system time, extracts the date and time components, and creates a datetime object. This function is templated and can handle different time point types.
- **Parameters**:
  - `pt` (T const): The time point to convert. Must be a valid time point representing a specific date and time.
- **Return Value**:
  - Returns a new Python object (PyObject*) representing a datetime.datetime object. The reference count is incremented, so the caller must decrement it when done.
- **Exceptions/Errors**:
  - No exceptions are thrown, but the function assumes the input time point is valid.
- **Example**:
```cpp
auto result = convert(lt::time_point_cast<lt::seconds>(lt::clock_type::now()));
// Use result in Python code
```
- **Preconditions**: The input time point must be valid and represent a specific date and time.
- **Postconditions**: The returned PyObject is a valid Python datetime.datetime object with the correct date and time.
- **Thread Safety**: This function is thread-safe as it only reads the input and creates new Python objects.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `convert(boost::posix_time::ptime const&)`, `bind_datetime()`

## Function: convert (ptime)

- **Signature**: `PyObject* convert(boost::posix_time::ptime const& pt)`
- **Description**: Converts a boost::posix_time::ptime object to a Python datetime.datetime object. The function extracts the date and time components from the ptime object and creates a datetime object with the corresponding year, month, day, hour, minute, and second.
- **Parameters**:
  - `pt` (boost::posix_time::ptime const&): The ptime object to convert. Must be a valid ptime object representing a specific date and time.
- **Return Value**:
  - Returns a new Python object (PyObject*) representing a datetime.datetime object. The reference count is incremented, so the caller must decrement it when done.
- **Exceptions/Errors**:
  - No exceptions are thrown, but the function assumes the input ptime is valid.
- **Example**:
```cpp
auto result = convert(boost::posix_time::ptime(boost::gregorian::date(2023, 1, 1), boost::posix_time::time_duration(12, 0, 0)));
// Use result in Python code
```
- **Preconditions**: The input ptime must be valid and represent a specific date and time.
- **Postconditions**: The returned PyObject is a valid Python datetime.datetime object with the correct date and time.
- **Thread Safety**: This function is thread-safe as it only reads the input and creates new Python objects.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `convert(T const)`, `bind_datetime()`

## Function: bind_datetime

- **Signature**: `void bind_datetime()`
- **Description**: Registers the datetime module's timedelta and datetime classes with the Python C++ binding system. This function sets up the conversion between libtorrent and Python datetime types by binding the appropriate Python classes and converters.
- **Parameters**:
  - None.
- **Return Value**:
  - None.
- **Exceptions/Errors**:
  - No exceptions are thrown, but the function assumes the Python module system is available and properly initialized.
- **Example**:
```cpp
bind_datetime();
// Now datetime conversions are available in Python
```
- **Preconditions**: The Python C++ binding system must be initialized, and the datetime module must be available.
- **Postconditions**: The datetime module's timedelta and datetime classes are bound to the Python C++ binding system, allowing conversion between libtorrent and Python datetime types.
- **Thread Safety**: This function is not thread-safe as it modifies global binding state.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `convert(Duration const&)`, `convert(boost::posix_time::time_duration const&)`

# Usage Examples

## Basic Usage

```cpp
#include "datetime.hpp"
#include <iostream>

int main() {
    // Convert a Duration to Python timedelta
    auto duration = lt::duration(1000ms);
    auto result = convert(duration);
    // Use result in Python code
    
    // Get current time point
    auto current_time = now(::tag<lt::time_point>());
    // Use current_time in libtorrent operations
    
    // Convert a ptime to Python datetime
    auto pt = boost::posix_time::ptime(boost::gregorian::date(2023, 1, 1), boost::posix_time::time_duration(12, 0, 0));
    auto result2 = convert(pt);
    // Use result2 in Python code
    
    // Bind datetime module
    bind_datetime();
    // Now datetime conversions are available
    
    return 0;
}
```

## Error Handling

```cpp
#include "datetime.hpp"
#include <iostream>

int main() {
    try {
        // Convert a Duration to Python timedelta
        auto duration = lt::duration(1000ms);
        auto result = convert(duration);
        if (result == nullptr) {
            std::cerr << "Failed to convert duration to Python object" << std::endl;
            return 1;
        }
        // Use result in Python code
        
        // Get current time point
        auto current_time = now(::tag<lt::time_point>());
        // Use current_time in libtorrent operations
        
        // Convert a ptime to Python datetime
        auto pt = boost::posix_time::ptime(boost::gregorian::date(2023, 1, 1), boost::posix_time::time_duration(12, 0, 0));
        auto result2 = convert(pt);
        if (result2 == nullptr) {
            std::cerr << "Failed to convert ptime to Python object" << std::endl;
            return 1;
        }
        // Use result2 in Python code
        
        // Bind datetime module
        bind_datetime();
        // Now datetime conversions are available
    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

## Edge Cases

```cpp
#include "datetime.hpp"
#include <iostream>

int main() {
    // Handle zero duration
