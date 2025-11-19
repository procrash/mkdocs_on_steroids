# `libtorrent::aux_` API Documentation

## numeric_cast

- **Signature**: `template <typename T, typename In> T numeric_cast(In v)`
- **Description**: Performs a safe numeric conversion from type `In` to type `T`. The function ensures the conversion is valid by asserting that the original value can be precisely represented in the target type. This is useful when converting between different numeric types while maintaining data integrity.
- **Parameters**:
  - `v` (In): The value to convert. Must be convertible to `T` without loss of precision. The value must also satisfy the constraints defined by the assertions in the function.
- **Return Value**:
  - Returns the converted value of type `T`. The return value is guaranteed to be equal to the original value when converted back to `In` type.
- **Exceptions/Errors**:
  - No exceptions are thrown. However, the function relies on `TORRENT_ASSERT` which will trigger a runtime assertion failure if the conditions are not met. This indicates a programming error rather than a recoverable error.
- **Example**:
```cpp
#include <libtorrent/aux_/numeric_cast.hpp>
#include <iostream>

int main() {
    long long value = 123456789;
    int result = numeric_cast<int>(value);
    std::cout << "Converted value: " << result << std::endl;
    return 0;
}
```
- **Preconditions**:
  - The value `v` must be representable in type `T` without loss of precision.
  - The types `T` and `In` must be numeric types.
  - The conditions asserted in the function must be satisfied (i.e., the conversion must not result in overflow or sign issues).
- **Postconditions**:
  - The returned value is equal to the original value when converted back to the input type.
  - The conversion is safe and does not result in data loss.
- **Thread Safety**:
  - The function is thread-safe as it only performs simple arithmetic operations and assertions.
- **Complexity**:
  - Time Complexity: O(1)
  - Space Complexity: O(1)
- **See Also**: `clamp()`, `static_cast()`

## clamp

- **Signature**: `template <typename T> T clamp(T v, T lo, T hi)`
- **Description**: Clamps a value `v` to be within the range `[lo, hi]`. If `v` is less than `lo`, the function returns `lo`. If `v` is greater than `hi`, the function returns `hi`. Otherwise, it returns `v`. This function is commonly used to ensure a value stays within a specified range.
- **Parameters**:
  - `v` (T): The value to clamp. This is the value that may be adjusted to fit within the specified range.
  - `lo` (T): The lower bound of the range. Must be less than or equal to `hi`.
  - `hi` (T): The upper bound of the range. Must be greater than or equal to `lo`.
- **Return Value**:
  - Returns the clamped value, which is either `lo`, `hi`, or `v` depending on the input. The return value will always be within the range `[lo, hi]`.
- **Exceptions/Errors**:
  - No exceptions are thrown. However, the function relies on `TORRENT_ASSERT` which will trigger a runtime assertion failure if `lo > hi`.
- **Example**:
```cpp
#include <libtorrent/aux_/numeric_cast.hpp>
#include <iostream>

int main() {
    int value = 150;
    int min_value = 100;
    int max_value = 200;
    int result = clamp(value, min_value, max_value);
    std::cout << "Clamped value: " << result << std::endl;
    return 0;
}
```
- **Preconditions**:
  - `lo` must be less than or equal to `hi`.
  - The types `T` must support comparison operations (`<`, `>`, `<=`, `>=`).
- **Postconditions**:
  - The returned value is within the range `[lo, hi]`.
  - The function preserves the original value if it is already within the range.
- **Thread Safety**:
  - The function is thread-safe as it only performs simple comparisons and arithmetic operations.
- **Complexity**:
  - Time Complexity: O(1)
  - Space Complexity: O(1)
- **See Also**: `numeric_cast()`, `std::clamp()`

---

## Usage Examples

### Basic Usage

```cpp
#include <libtorrent/aux_/numeric_cast.hpp>
#include <libtorrent/aux_/numeric_cast.hpp>
#include <iostream>

int main() {
    // Using numeric_cast to safely convert between types
    long long large_value = 2147483647;
    int safe_value = numeric_cast<int>(large_value);
    std::cout << "Numeric cast result: " << safe_value << std::endl;

    // Using clamp to restrict a value to a specific range
    int temperature = 35;
    int min_temp = 0;
    int max_temp = 30;
    int clamped_temp = clamp(temperature, min_temp, max_temp);
    std::cout << "Clamped temperature: " << clamped_temp << std::endl;

    return 0;
}
```

### Error Handling

```cpp
#include <libtorrent/aux_/numeric_cast.hpp>
#include <libtorrent/aux_/numeric_cast.hpp>
#include <iostream>

int main() {
    // Error handling for numeric_cast
    try {
        long long out_of_range = 2147483648;
        int result = numeric_cast<int>(out_of_range);
        std::cout << "Result: " << result << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    // Error handling for clamp
    try {
        int value = 100;
        int low = 200;
        int high = 150;
        int clamped = clamp(value, low, high);
        std::cout << "Clamped value: " << clamped << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
```

### Edge Cases

```cpp
#include <libtorrent/aux_/numeric_cast.hpp>
#include <libtorrent/aux_/numeric_cast.hpp>
#include <iostream>

int main() {
    // Edge case: numeric_cast with maximum value
    int max_int = std::numeric_limits<int>::max();
    long long very_large = static_cast<long long>(max_int) + 1;
    int result = numeric_cast<int>(very_large);
    std::cout << "Numeric cast of max int + 1: " << result << std::endl;

    // Edge case: clamp with equal bounds
    int value = 10;
    int min = 10;
    int max = 10;
    int clamped = clamp(value, min, max);
    std::cout << "Clamp with equal bounds: " << clamped << std::endl;

    // Edge case: negative values with clamp
    int negative_value = -5;
    int min_negative = -10;
    int max_negative = 0;
    int clamped_negative = clamp(negative_value, min_negative, max_negative);
    std::cout << "Clamped negative value: " << clamped_negative << std::endl;

    return 0;
}
```

---

## Best Practices

### How to Use These Functions Effectively

1. **Use `numeric_cast` for Type Safety**: When converting between numeric types, use `numeric_cast` to ensure the conversion is safe and does not result in data loss or overflow.

2. **Use `clamp` for Range Validation**: When you need to ensure a value stays within a specific range, use `clamp` to avoid manual conditional checks.

3. **Combine with Assertions**: Use `TORRENT_ASSERT` in debug builds to catch potential issues early during development.

### Common Mistakes to Avoid

1. **Ignoring Assertions**: Do not ignore the assertions in `numeric_cast`. They are critical for catching programming errors.

2. **Incorrect Range Specifications**: Ensure that the lower bound is always less than or equal to the upper bound in `clamp`.

3. **Using Wrong Data Types**: Make sure the data types used in `numeric_cast` are appropriate for the conversion. For example, converting a floating-point number to an integer may result in truncation.

### Performance Tips

1. **Avoid Unnecessary Conversions**: Only use `numeric_cast` when necessary. Direct assignments are often faster and sufficient.

2. **Minimize Function Calls**: If you need to clamp values frequently, consider caching the results or using a more efficient data structure.

3. **Use Inline Functions**: Since both functions are simple, they should be defined inline to reduce function call overhead.

---

## Code Review & Improvement Suggestions

### Potential Issues

**Function**: `numeric_cast`
**Issue**: The function uses `TORRENT_ASSERT` which can cause program termination in debug builds. This might not be suitable for production code where runtime assertions are disabled.
**Severity**: Medium
**Impact**: Could lead to unexpected program termination in debug builds if assertions fail.
**Fix**: Consider using a more graceful error handling mechanism, such as returning a `std::optional<T>` or throwing an exception.

```cpp
// Before
template <typename T, typename In> T numeric_cast(In v) {
    T r = static_cast<T>(v);
    TORRENT_ASSERT(v == static_cast<In>(r));
    TORRENT_ASSERT(std::is_unsigned<In>::value || std::is_signed<T>::value || std::int64_t(v) >= 0);
    TORRENT_ASSERT(std::is_signed<In>::value || std::is_unsigned<T>::value || std::size_t(v) <= std::si);
    return r;
}

// After (using optional)
#include <optional>

template <typename T, typename In> std::optional<T> numeric_cast(In v) {
    T r = static_cast<T>(v);
    if (v == static_cast<In>(r) && 
        (std::is_unsigned<In>::value || std::is_signed<T>::value || std::int64_t(v) >= 0) && 
        (std::is_signed<In>::value || std::is_unsigned<T>::value || std::size_t(v) <= std::si)) {
        return r;
    }
    return std::nullopt;
}
```

**Function**: `clamp`
**Issue**: The function uses `TORRENT_ASSERT` which can cause program termination in debug builds. This might not be suitable for production code where runtime assertions are disabled.
**Severity**: Medium
**Impact**: Could lead to unexpected program termination in debug builds if assertions fail.
**Fix**: Consider using a more graceful error handling mechanism, such as returning a default value or throwing an exception.

```cpp
// Before
template <typename T> T clamp(T v, T lo, T hi) {
    TORRENT_ASSERT(lo <= hi);
    if (v < lo) return lo;
    if (hi < v) return hi;
    return v;
}

// After (using optional)
#include <optional>

template <typename T> std::optional<T> clamp(T v, T lo, T hi) {
    if (lo > hi) {
        return std::nullopt;
    }
    if (v < lo) return lo;
    if (hi < v) return hi;
    return v;
}
```

### Modernization Opportunities

**Function**: `numeric_cast`
**Opportunity**: Use `[[nodiscard]]` to indicate that the function return value should not be ignored.
**Modern C++ Improvement**: Add `[[nodiscard]]` to the function signature.

```cpp
template <typename T, typename In> [[nodiscard]] T numeric_cast(In v) {
    T r = static_cast<T>(v);
    TORRENT_ASSERT(v == static_cast<In>(r));
    TORRENT_ASSERT(std::is_unsigned<In>::value || std::is_signed<T>::value || std::int64_t(v) >= 0);
    TORRENT_ASSERT(std::is_signed<In>::value || std::is_unsigned<T>::value || std::size_t(v) <= std::si);
    return r;
}
```

**Function**: `clamp`
**Opportunity**: Use `[[nodiscard]]` to indicate that the function return value should not be ignored.
**Modern C++ Improvement**: Add `[[nodiscard]]` to the function signature.

```cpp
template <typename T> [[nodiscard]] T clamp(T v, T lo, T hi) {
    TORRENT_ASSERT(lo <= hi);
    if (v < lo) return lo;
    if (hi < v) return hi;
    return v;
}
```

### Refactoring Suggestions

**Function**: `numeric_cast`
**Suggestion**: The function could be split into two separate functions: one for safe conversion and one for unsafe conversion. This would make the intent clearer and allow users to choose the appropriate function based on their needs.

**Function**: `clamp`
**Suggestion**: The function is well-structured and could be made more generic by using `std::span` or `std::array` for handling collections of values.

### Performance Optimizations

**Function**: `numeric_cast`
**Opportunity**: The function could be optimized by using `constexpr` if the input