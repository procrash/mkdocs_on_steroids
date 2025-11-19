```markdown
# Session View API Documentation

## Overview
The `session_view` class provides a mechanism to track and display session statistics from a libtorrent session. It captures metrics over time and provides methods to render and analyze performance data, particularly focusing on download rates and other session statistics.

---

## session_view

- **Signature**: `session_view::session_view()`
- **Description**: Constructs a new `session_view` object, initializing the internal counter arrays and timestamp vectors. This constructor queries the available libtorrent session statistics metrics and pre-allocates space for storing current and previous metric values.
- **Parameters**: None
- **Return Value**: None (constructor)
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
// view is now ready to track session metrics
```
- **Preconditions**: None
- **Postconditions**: The `session_view` object is initialized with empty metric counters and timestamp vectors. The number of metrics is determined by `lt::session_stats_metrics()`.
- **Thread Safety**: Not thread-safe. Must not be accessed concurrently by multiple threads.
- **Complexity**: O(n) where n is the number of statistics metrics.
- **See Also**: `set_pos()`, `set_width()`, `update_counters()`

---

## set_pos

- **Signature**: `void session_view::set_pos(int pos)`
- **Description**: Sets the vertical position (y-coordinate) where the session view will be rendered on a display.
- **Parameters**:
  - `pos` (int): The vertical position (y-coordinate) for rendering. Valid values are typically >= 0.
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
view.set_pos(10); // Position the view at y=10
```
- **Preconditions**: None
- **Postconditions**: The internal `m_position` member is set to the provided `pos` value.
- **Thread Safety**: Not thread-safe. Concurrent calls may result in race conditions.
- **Complexity**: O(1)
- **See Also**: `pos()`, `set_width()`

---

## set_width

- **Signature**: `void session_view::set_width(int width)`
- **Description**: Sets the width of the session view, which determines how many columns of data can be displayed horizontally.
- **Parameters**:
  - `width` (int): The width in characters/columns. Must be >= 0.
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
view.set_width(50); // Set view width to 50 characters
```
- **Preconditions**: None
- **Postconditions**: The internal `m_width` member is set to the provided `width` value.
- **Thread Safety**: Not thread-safe. Concurrent calls may result in race conditions.
- **Complexity**: O(1)
- **See Also**: `pos()`, `render()`

---

## pos

- **Signature**: `int session_view::pos() const`
- **Description**: Returns the current vertical position (y-coordinate) where the session view is rendered.
- **Parameters**: None
- **Return Value**: 
  - `int`: The current vertical position (y-coordinate) of the view.
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
view.set_pos(15);
int current_pos = view.pos(); // Returns 15
```
- **Preconditions**: The `session_view` object must be properly constructed.
- **Postconditions**: Returns the last set position value.
- **Thread Safety**: Thread-safe for read operations.
- **Complexity**: O(1)
- **See Also**: `set_pos()`, `height()`

---

## height

- **Signature**: `int session_view::height() const`
- **Description**: Returns the height of the session view in lines. The height is fixed at 3 lines, as it displays a header and two data rows (current and previous values).
- **Parameters**: None
- **Return Value**: 
  - `int`: Always returns 3.
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
int h = view.height(); // Returns 3
```
- **Preconditions**: The `session_view` object must be properly constructed.
- **Postconditions**: Always returns 3.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `pos()`, `render()`

---

## value

- **Signature**: `std::int64_t session_view::value(int idx) const`
- **Description**: Returns the current value of a specific statistic metric at the given index.
- **Parameters**:
  - `idx` (int): The index of the metric to retrieve. Negative values are treated as 0.
- **Return Value**:
  - `std::int64_t`: The current value of the metric at index `idx`. Returns 0 if `idx` is negative or out of bounds.
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
std::int64_t current_download = view.value(5); // Get value at index 5
```
- **Preconditions**: The `session_view` object must be properly constructed. The index must be less than the number of metrics available.
- **Postconditions**: Returns the current counter value for the specified metric index.
- **Thread Safety**: Thread-safe for read operations.
- **Complexity**: O(1)
- **See Also**: `prev_value()`, `update_counters()`

---

## prev_value

- **Signature**: `std::int64_t session_view::prev_value(int idx) const`
- **Description**: Returns the previous value of a specific statistic metric at the given index. This value is from the last update cycle.
- **Parameters**:
  - `idx` (int): The index of the metric to retrieve. Negative values are treated as 0.
- **Return Value**:
  - `std::int64_t`: The previous value of the metric at index `idx`. Returns 0 if `idx` is negative or out of bounds.
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
std::int64_t previous_download = view.prev_value(5); // Get previous value at index 5
```
- **Preconditions**: The `session_view` object must be properly constructed. The index must be less than the number of metrics available.
- **Postconditions**: Returns the previous counter value for the specified metric index.
- **Thread Safety**: Thread-safe for read operations.
- **Complexity**: O(1)
- **See Also**: `value()`, `update_counters()`

---

## render

- **Signature**: `void session_view::render()`
- **Description**: Renders the session view to the display, calculating and displaying metrics such as download rate. The function computes the rate of change over time and formats the output as a string.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
view.render(); // Render the current session view
```
- **Preconditions**: The `session_view` object must be properly constructed. `update_counters()` must have been called previously to populate the metric data.
- **Postconditions**: The session view is rendered to the display using the current metric values and timestamps.
- **Thread Safety**: Not thread-safe. Concurrent calls may result in race conditions.
- **Complexity**: O(n) where n is the number of metrics.
- **See Also**: `update_counters()`, `value()`, `prev_value()`

---

## update_counters

- **Signature**: `void session_view::update_counters(span<std::int64_t const> stats_counters, lt::clock_type::time_point const t)`
- **Description**: Updates the session view counters with new statistics from the libtorrent session. The function compares the current timestamp with the last update time to determine if the previous counter values should be updated. It then stores the new counters and updates the timestamp.
- **Parameters**:
  - `stats_counters` (span<std::int64_t const>): A span containing the current session statistics counters from libtorrent.
  - `t` (lt::clock_type::time_point): The current timestamp for the update.
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
session_view view;
std::vector<std::int64_t> current_stats = get_current_stats();
lt::clock_type::time_point now = std::chrono::steady_clock::now();
view.update_counters(current_stats, now);
```
- **Preconditions**: The `session_view` object must be properly constructed. The `stats_counters` span must contain the same number of elements as the metrics retrieved in the constructor.
- **Postconditions**: The current counter values are updated with the new statistics. The previous counter values are swapped to the current ones if enough time has passed since the last update.
- **Thread Safety**: Not thread-safe. Concurrent calls may result in race conditions.
- **Complexity**: O(n) where n is the number of metrics.
- **See Also**: `session_view()`, `render()`, `value()`, `prev_value()`

---

## Usage Examples

### Basic Usage
```cpp
#include <iostream>
#include "session_view.h" // Assume header exists

int main() {
    session_view view;
    
    // Set up the view position and width
    view.set_pos(5);
    view.set_width(60);
    
    // Simulate receiving new stats from libtorrent
    std::vector<std::int64_t> stats = {1000, 2000, 3000, 4000}; // Example stats
    lt::clock_type::time_point now = std::chrono::steady_clock::now();
    
    // Update the counters with new data
    view.update_counters(stats, now);
    
    // Render the view
    view.render();
    
    return 0;
}
```

### Error Handling
```cpp
#include <iostream>
#include <stdexcept>

int main() {
    try {
        session_view view;
        view.set_pos(5);
        view.set_width(60);
        
        // Simulate receiving stats
        std::vector<std::int64_t> stats = {1000, 2000, 3000, 4000};
        
        // Validate stats size matches expected count
        auto metrics = lt::session_stats_metrics();
        if (stats.size() != metrics.size()) {
            throw std::runtime_error("Stats count mismatch");
        }
        
        lt::clock_type::time_point now = std::chrono::steady_clock::now();
        view.update_counters(stats, now);
        view.render();
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

### Edge Cases
```cpp
#include <iostream>
#include "session_view.h"

int main() {
    session_view view;
    
    // Edge case: negative index
    std::int64_t val = view.value(-1);
    std::cout << "Value at -1: " << val << std::endl; // Should output 0
    
    // Edge case: out of bounds index
    std::int64_t val2 = view.value(1000); // Should output 0 if 1000 > metrics.size()
    std::cout << "Value at 1000: " << val2 << std::endl;
    
    // Edge case: update with empty stats
    std::vector<std::int64_t> empty_stats;
    lt::clock_type::time_point now = std::chrono::steady_clock::now();
    view.update_counters(empty