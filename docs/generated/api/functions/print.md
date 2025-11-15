```markdown
# API Documentation

## esc

- **Signature**: `char const* esc(char const* code)`
- **Description**: Converts a string code to a human-readable string representation using a static buffer. This function uses a round-robin buffer to avoid string copying overhead. It's designed for performance-critical code where frequent string formatting occurs.
- **Parameters**:
  - `code` (char const*): The input code string to convert. This string is interpreted as a format specifier or identifier.
- **Return Value**:
  - `char const*`: A pointer to a static buffer containing the formatted string. The returned pointer is valid until the next call to `esc()`, so the caller must not store it beyond that point.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
auto result = esc("OK");
if (result != nullptr) {
    std::cout << result << std::endl;
}
```
- **Preconditions**: `code` must not be null.
- **Postconditions**: Returns a pointer to a static buffer containing the formatted string.
- **Thread Safety**: Not thread-safe due to the use of a static buffer and mutable state.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `to_string()`, `color()`

## to_string

- **Signature**: `std::string to_string(int v, int width)`
- **Description**: Converts an integer to a string with a specified minimum width, padding with spaces if necessary.
- **Parameters**:
  - `v` (int): The integer value to convert.
  - `width` (int): The minimum width of the resulting string. If the number has fewer digits than `width`, it will be padded with spaces on the left.
- **Return Value**:
  - `std::string`: The formatted string representation of the integer.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
auto result = to_string(42, 5);
std::cout << result << std::endl; // Output: "   42"
```
- **Preconditions**: `width` must be non-negative.
- **Postconditions**: Returns a string representation of `v` with at least `width` characters.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `esc()`, `add_suffix_float()`

## add_suffix_float

- **Signature**: `std::string add_suffix_float(double val, char const* suffix)`
- **Description**: Formats a floating-point number with an appropriate SI prefix (kB, MB, GB, etc.) and optional suffix. The function scales the value down to a more readable format and appends the appropriate suffix.
- **Parameters**:
  - `val` (double): The floating-point value to format.
  - `suffix` (char const*): Optional suffix to append to the result. Can be null.
- **Return Value**:
  - `std::string`: The formatted string with the appropriate prefix and suffix.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
auto result = add_suffix_float(1234567.89, "B");
std::cout << result << std::endl; // Output: "1.23MB"
```
- **Preconditions**: `suffix` must be null or a valid C-string.
- **Postconditions**: Returns a formatted string representing the value in human-readable units.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `to_string()`, `color()`

## color

- **Signature**: `std::string color(std::string const& s, color_code c)`
- **Description**: Applies ANSI color codes to a string for terminal display. The function wraps the input string with ANSI escape sequences to color it in the terminal.
- **Parameters**:
  - `s` (std::string const&): The string to colorize.
  - `c` (color_code): The color code to apply. If `col_none`, no color is applied.
- **Return Value**:
  - `std::string`: The colorized string with ANSI escape sequences.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
auto result = color("Hello World", col_red);
std::cout << result << std::endl;
```
- **Preconditions**: `s` must be a valid string.
- **Postconditions**: Returns a string with ANSI color codes applied.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time and space complexity, where n is the length of the input string.
- **See Also**: `progress_bar()`, `set_cursor_pos()`

## progress_bar

- **Signature**: `std::string const& progress_bar(int progress, int width, color_code c, char fill, char bg, std::string caption, int flags)`
- **Description**: Generates a progress bar string with specified parameters. The function calculates the progress as a percentage and creates a visual representation of it.
- **Parameters**:
  - `progress` (int): The current progress as a percentage (0-100).
  - `width` (int): The width of the progress bar in characters.
  - `c` (color_code): The color code for the progress bar.
  - `fill` (char): The character used to fill the progress portion of the bar.
  - `bg` (char): The background character for the non-progress portion of the bar.
  - `caption` (std::string): An optional caption to display with the progress bar.
  - `flags` (int): Additional flags to modify the behavior of the progress bar.
- **Return Value**:
  - `std::string const&`: A reference to a static string containing the progress bar. This reference is valid until the next call to `progress_bar()`.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
auto result = progress_bar(75, 50, col_green, '#', ' ', "Download Progress", 0);
std::cout << result << std::endl;
```
- **Preconditions**: `progress` must be between 0 and 100, `width` must be positive.
- **Postconditions**: Returns a reference to a static string containing the progress bar.
- **Thread Safety**: Not thread-safe due to the use of a static buffer.
- **Complexity**: O(n) time and space complexity, where n is the width of the progress bar.
- **See Also**: `piece_bar()`, `avail_bar()`

## piece_bar

- **Signature**: `std::string const& piece_bar(lt::bitfield const& p, int width)`
- **Description**: Generates a visual representation of a bitfield as a piece bar. The function converts each bit in the bitfield to a character, creating a visual bar that shows which pieces are available.
- **Parameters**:
  - `p` (lt::bitfield const&): The bitfield to visualize.
  - `width` (int): The width of the piece bar in characters.
- **Return Value**:
  - `std::string const&`: A reference to a static string containing the piece bar. This reference is valid until the next call to `piece_bar()`.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
lt::bitfield bf(100);
// Set some bits
auto result = piece_bar(bf, 50);
std::cout << result << std::endl;
```
- **Preconditions**: `width` must be positive.
- **Postconditions**: Returns a reference to a static string containing the piece bar.
- **Thread Safety**: Not thread-safe due to the use of a static buffer.
- **Complexity**: O(n) time and space complexity, where n is the width of the piece bar.
- **See Also**: `progress_bar()`, `avail_bar()`

## avail_bar

- **Signature**: `std::string avail_bar(lt::span<int> avail, int const width, int& pos)`
- **Description**: Generates a visual representation of the availability of pieces, displaying them as a bar with different characters for different availability levels. The function returns a string and updates the position pointer.
- **Parameters**:
  - `avail` (lt::span<int>): A span of integers representing the availability of each piece.
  - `width` (int): The width of the availability bar in characters.
  - `pos` (int&): A reference to an integer that will be updated to the current position in the availability data.
- **Return Value**:
  - `std::string`: The availability bar string.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
std::vector<int> availability(100, 0);
// Populate availability data
int pos = 0;
auto result = avail_bar(avail, 50, pos);
std::cout << result << std::endl;
```
- **Preconditions**: `width` must be positive, `avail` must be valid.
- **Postconditions**: Returns a string representing the availability bar and updates `pos` to the current position.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time and space complexity, where n is the width of the bar.
- **See Also**: `piece_bar()`, `piece_matrix()`

## get_piece

- **Signature**: `int get_piece(lt::bitfield const& p, int index)`
- **Description**: Retrieves the availability status of a specific piece from a bitfield.
- **Parameters**:
  - `p` (lt::bitfield const&): The bitfield containing piece availability data.
  - `index` (int): The index of the piece to check.
- **Return Value**:
  - `int`: Returns 1 if the piece is available, 0 otherwise.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
lt::bitfield bf(100);
// Set some bits
int result = get_piece(bf, 42);
if (result == 1) {
    std::cout << "Piece 42 is available" << std::endl;
}
```
- **Preconditions**: `index` must be within the bounds of the bitfield.
- **Postconditions**: Returns 1 if the piece is available, 0 otherwise.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `piece_matrix()`, `avail_bar()`

## piece_matrix

- **Signature**: `std::string piece_matrix(lt::bitfield const& p, int width, int* height)`
- **Description**: Generates a matrix representation of a bitfield, displaying pieces in a grid format. The function returns a string and updates the height pointer.
- **Parameters**:
  - `p` (lt::bitfield const&): The bitfield to visualize.
  - `width` (int): The width of the matrix in characters.
  - `height` (int*): A pointer to an integer that will be updated to the height of the matrix.
- **Return Value**:
  - `std::string`: The matrix representation of the bitfield.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
lt::bitfield bf(100);
// Set some bits
int height = 0;
auto result = piece_matrix(bf, 50, &height);
std::cout << result << std::endl;
```
- **Preconditions**: `width` must be positive, `height` must be a valid pointer.
- **Postconditions**: Returns a string representing the piece matrix and updates `height` to the height of the matrix.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(n) time and space complexity, where n is the number of pieces.
- **See Also**: `avail_bar()`, `get_piece()`

## set_cursor_pos

- **Signature**: `void set_cursor_pos(int x, int y)`
- **Description**: Sets the cursor position in the terminal. This function works on both Windows and Unix-like systems.
- **Parameters**:
  - `x` (int): The horizontal position of the cursor.
  - `y` (int): The vertical position of the cursor.
- **Return Value**:
  - `void`: No return value.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
set_cursor_pos(10, 5);
std::cout << "Hello" << std::endl;
```
- **Preconditions**: `x` and `y` must be within the terminal's dimensions.
- **Postconditions**: The cursor is moved to the specified position.
- **Thread Safety**: Not thread-safe due to direct console access.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `clear_screen()`, `clear_rows()`

## clear_screen

- **Signature**: `void clear_screen()`
- **Description**: Clears the entire terminal screen. This function works on both Windows and Unix-like systems.
- **Parameters**:
  - None.
- **Return Value**:
  - `void`: No return value.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
clear_screen();
std::cout << "Screen cleared" << std::endl;
```
- **Preconditions**: None.
- **Postconditions**: The entire terminal screen is cleared.
- **Thread Safety**: Not thread-safe due to direct console access.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `set_cursor_pos()`, `clear_rows()`

## clear_rows

- **Signature**: `void clear_rows(int y1, int y2)`
- **Description**: Clears a range of rows in the terminal screen. This function works on both Windows and Unix-like systems.
- **Parameters**:
  - `y1` (int): The starting row to clear.
  - `y2` (int): The ending row to clear.
- **Return Value**:
  - `void`: No return value.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
clear_rows(5, 10);
std::cout << "Rows 5-10 cleared" << std::endl;
```
- **Preconditions**: `y1` must be less than or equal to `y2`.
- **Postconditions**: The specified range of rows is cleared.
- **Thread Safety**: Not thread-safe due to direct console access.
- **Complexity**: O(n) time and space complexity, where n is the number of rows to clear.
- **See Also**: `clear_screen()`, `set_cursor_pos()`

## apply_ansi_code

- **Signature**: `void apply_ansi_code(WORD* attributes, bool* reverse, bool* support_chaining, int code)`
- **Description**: Applies ANSI color codes to console attributes. This function is used internally by `print()` to handle color formatting.
- **Parameters**:
  - `attributes` (WORD*): Pointer to the console attributes to modify.
  - `reverse` (bool*): Pointer to a boolean indicating whether reverse video is enabled.
  - `support_chaining` (bool*): Pointer to a boolean indicating whether chaining is supported.
  - `code` (int): The ANSI code to apply.
- **Return Value**:
  - `void`: No return value.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
WORD attributes = 7;
bool reverse = false;
bool support_chaining = true;
apply_ansi_code(&attributes, &reverse, &support_chaining, 31); // Red text
```
- **Preconditions**: `attributes` must be a valid pointer to console attributes.
- **Postconditions**: The console attributes are modified according to the ANSI code.
- **Thread Safety**: Not thread-safe due to direct console access.
- **Complexity**: O(1) time and space complexity.
- **See Also**: `print()`, `color()`

## print

- **Signature**: `void print(char const* buf)`
- **Description**: Prints a string to the console, handling ANSI escape sequences for color and formatting. This function is used to display formatted text in the terminal.
- **Parameters**:
  - `buf` (char const*): The string to print.
- **Return Value**:
  - `void`: No return value.
- **Exceptions/Errors**:
  - None thrown.
- **Example**:
```cpp
print("Hello \033[31mWorld\033[0m");
```
- **Preconditions**: `buf` must not be null.
- **Postconditions**: The string is printed to the console with any ANSI escape sequences processed.
- **Thread Safety**: Not thread-safe due to direct console access.
- **Complexity**: O(n) time and space complexity, where n is the length of the input string.
- **See Also**: `apply_ansi_code()`, `color()`

# Usage Examples

## Basic Usage

```cpp
#include <iostream>
#include <string>

int main() {
    // Basic string formatting
    std::string result = to_string(42, 5);
    std::cout << result << std::endl; // Output: "   42"

    // Colorized text
    std::string colored = color("Hello World", col_red);
    std::cout << colored << std::endl;

    // Progress bar
    auto progress = progress_bar(75, 50, col_green, '#', ' ', "Download Progress", 0);
    std::cout << progress << std::endl;

    // Set cursor position
    set_cursor_pos(10, 5);
    std::cout << "Hello" << std::endl;

    return 0;
}
```

## Error Handling

```cpp
#include <iostream>
#include <string>
#include <stdexcept>

int main() {
    try {
        // Validate inputs
        if (width < 0) {
            throw std::invalid_argument("Width must be non-negative");
        }

        // Use functions with proper error handling
        std::string result = to_string(42, 5);
        if (result.empty()) {
            std::cerr << "Error: Failed to format string" << std::endl;
            return 1;
        }

        // Handle potential console errors
