# C++ API Documentation

## torrent_state

- **Signature**: `std::string torrent_state(lt::torrent_status const& s)`
- **Description**: Converts a torrent status into a human-readable string representation, including error messages if the torrent has an error condition.
- **Parameters**:
  - `s` (lt::torrent_status const&): The torrent status object to convert to string. Must be a valid torrent status object.
- **Return Value**:
  - `std::string`: A string representing the torrent's state. Returns error message if the torrent has an error, otherwise returns a state string from the state_str array.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
auto status = get_torrent_status();
auto state_str = torrent_state(status);
std::cout << "Torrent state: " << state_str << std::endl;
```
- **Preconditions**: The `s` parameter must be a valid torrent status object.
- **Postconditions**: The returned string contains a human-readable representation of the torrent status.
- **Thread Safety**: Thread-safe if the `s` parameter is not modified concurrently.
- **Complexity**: O(1)
- **See Also**: `lt::torrent_status`

## cmp_torrent_position

- **Signature**: `bool cmp_torrent_position(lt::torrent_status const* lhs, lt::torrent_status const* rhs)`
- **Description**: Comparator function for sorting torrents by queue position when both are downloading.
- **Parameters**:
  - `lhs` (lt::torrent_status const*): Pointer to the first torrent status to compare.
  - `rhs` (lt::torrent_status const*): Pointer to the second torrent status to compare.
- **Return Value**:
  - `bool`: Returns true if `lhs` should come before `rhs` in sorting order (lower queue position comes first).
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::vector<lt::torrent_status const*> torrents = get_torrent_list();
std::sort(torrents.begin(), torrents.end(), &cmp_torrent_position);
```
- **Preconditions**: Both pointers must be valid and point to valid torrent status objects.
- **Postconditions**: The relative order of torrents in the vector is updated based on queue position.
- **Thread Safety**: Thread-safe if the torrent status objects are not modified concurrently.
- **Complexity**: O(1)
- **See Also**: `std::sort`, `torrent_view::update_sort_order`

## cmp_torrent_name

- **Signature**: `bool cmp_torrent_name(lt::torrent_status const* lhs, lt::torrent_status const* rhs)`
- **Description**: Comparator function for sorting torrents by name in lexicographic order.
- **Parameters**:
  - `lhs` (lt::torrent_status const*): Pointer to the first torrent status to compare.
  - `rhs` (lt::torrent_status const*): Pointer to the second torrent status to compare.
- **Return Value**:
  - `bool`: Returns true if `lhs` should come before `rhs` in sorting order (lexicographically smaller name comes first).
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::vector<lt::torrent_status const*> torrents = get_torrent_list();
std::sort(torrents.begin(), torrents.end(), &cmp_torrent_name);
```
- **Preconditions**: Both pointers must be valid and point to valid torrent status objects.
- **Postconditions**: The relative order of torrents in the vector is updated based on name.
- **Thread Safety**: Thread-safe if the torrent status objects are not modified concurrently.
- **Complexity**: O(n) where n is the length of the shorter name string.
- **See Also**: `std::sort`, `torrent_view::update_sort_order`

## cmp_torrent_size

- **Signature**: `bool cmp_torrent_size(lt::torrent_status const* lhs, lt::torrent_status const* rhs)`
- **Description**: Comparator function for sorting torrents by total download size in descending order.
- **Parameters**:
  - `lhs` (lt::torrent_status const*): Pointer to the first torrent status to compare.
  - `rhs` (lt::torrent_status const*): Pointer to the second torrent status to compare.
- **Return Value**:
  - `bool`: Returns true if `lhs` should come before `rhs` in sorting order (larger total_done comes first).
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::vector<lt::torrent_status const*> torrents = get_torrent_list();
std::sort(torrents.begin(), torrents.end(), &cmp_torrent_size);
```
- **Preconditions**: Both pointers must be valid and point to valid torrent status objects.
- **Postconditions**: The relative order of torrents in the vector is updated based on total download size.
- **Thread Safety**: Thread-safe if the torrent status objects are not modified concurrently.
- **Complexity**: O(1)
- **See Also**: `std::sort`, `torrent_view::update_sort_order`

## torrent_view

- **Signature**: `torrent_view::torrent_view()`
- **Description**: Default constructor for the torrent_view class. Initializes a new torrent view object with default settings.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
torrent_view view;
view.set_size(80, 24);
```
- **Preconditions**: None
- **Postconditions**: The torrent_view object is initialized with default values.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: None

## set_size

- **Signature**: `void torrent_view::set_size(int width, int height)`
- **Description**: Sets the size of the torrent view window and triggers a re-render if dimensions changed.
- **Parameters**:
  - `width` (int): The new width of the view window.
  - `height` (int): The new height of the view window.
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.set_size(100, 40);
```
- **Preconditions**: The view must be in a valid state.
- **Postconditions**: The view dimensions are updated, and the view is rendered if dimensions changed.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(1)
- **See Also**: `render`, `height`

## filter

- **Signature**: `int torrent_view::filter() const`
- **Description**: Gets the current filter setting for the torrent view.
- **Parameters**: None
- **Return Value**:
  - `int`: The current filter mode (one of the torrent filter constants).
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
int current_filter = view.filter();
if (current_filter == torrents_downloading) {
    std::cout << "Viewing downloading torrents" << std::endl;
}
```
- **Preconditions**: The view must be in a valid state.
- **Postconditions**: Returns the current filter setting.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `set_filter`

## set_filter

- **Signature**: `void torrent_view::set_filter(int filter)`
- **Description**: Sets the filter mode for the torrent view and updates the filtered torrents list.
- **Parameters**:
  - `filter` (int): The new filter mode to apply.
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.set_filter(torrents_seeding);
```
- **Preconditions**: The filter value must be one of the valid torrent filter constants.
- **Postconditions**: The filter is updated, and the filtered torrents list is regenerated.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(n) where n is the number of torrents
- **See Also**: `filter`, `update_filtered_torrents`

## sort_order

- **Signature**: `int torrent_view::sort_order() const`
- **Description**: Gets the current sort order for the torrent view.
- **Parameters**: None
- **Return Value**:
  - `int`: The current sort order (one of the order constants).
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
int current_sort = view.sort_order();
if (current_sort == order::name) {
    std::cout << "Sorting by name" << std::endl;
}
```
- **Preconditions**: The view must be in a valid state.
- **Postconditions**: Returns the current sort order.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `set_sort_order`

## set_sort_order

- **Signature**: `void torrent_view::set_sort_order(int const o)`
- **Description**: Sets the sort order for the torrent view and updates the sorting.
- **Parameters**:
  - `o` (int const): The new sort order to apply.
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.set_sort_order(order::queue);
```
- **Preconditions**: The sort order value must be one of the valid order constants.
- **Postconditions**: The sort order is updated, and the torrents are sorted accordingly.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(n log n) where n is the number of torrents
- **See Also**: `sort_order`, `update_sort_order`

## get_active_torrent

- **Signature**: `lt::torrent_status const& torrent_view::get_active_torrent() const`
- **Description**: Returns a reference to the currently active torrent status.
- **Parameters**: None
- **Return Value**:
  - `lt::torrent_status const&`: A reference to the active torrent status. Returns a valid torrent status object.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
auto& active_torrent = view.get_active_torrent();
std::cout << "Active torrent: " << active_torrent.name << std::endl;
```
- **Preconditions**: The view must be in a valid state and have at least one torrent.
- **Postconditions**: Returns a reference to the active torrent status.
- **Thread Safety**: Thread-safe if the torrent status object is not modified concurrently.
- **Complexity**: O(1)
- **See Also**: `get_active_handle`, `m_filtered_handles`

## get_active_handle

- **Signature**: `lt::torrent_handle torrent_view::get_active_handle() const`
- **Description**: Returns the handle of the currently active torrent.
- **Parameters**: None
- **Return Value**:
  - `lt::torrent_handle`: The handle of the active torrent.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
auto active_handle = view.get_active_handle();
if (active_handle.is_valid()) {
    std::cout << "Active torrent handle is valid" << std::endl;
}
```
- **Preconditions**: The view must be in a valid state and have at least one torrent.
- **Postconditions**: Returns a valid torrent handle if available.
- **Thread Safety**: Thread-safe if the torrent handle is not modified concurrently.
- **Complexity**: O(1)
- **See Also**: `get_active_torrent`, `m_filtered_handles`

## remove_torrent

- **Signature**: `void torrent_view::remove_torrent(lt::torrent_handle h)`
- **Description**: Removes a torrent from the view based on its handle.
- **Parameters**:
  - `h` (lt::torrent_handle): The handle of the torrent to remove.
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.remove_torrent(torrent_handle);
```
- **Preconditions**: The handle must be valid and associated with a torrent in the view.
- **Postconditions**: The torrent is removed from the view, and the filtered list may be updated.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(n) where n is the number of torrents
- **See Also**: `m_all_handles`, `m_filtered_handles`

## update_torrents

- **Signature**: `void torrent_view::update_torrents(std::vector<lt::torrent_status> st)`
- **Description**: Updates the torrent status information in the view with new data from the libtorrent library.
- **Parameters**:
  - `st` (std::vector<lt::torrent_status>): The updated torrent status information to process.
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
std::vector<lt::torrent_status> new_status = get_updated_torrents();
view.update_torrents(new_status);
```
- **Preconditions**: The view must be in a valid state.
- **Postconditions**: The torrent status information in the view is updated with the new data.
- **Thread Safety**: Thread-safe if the torrent status objects are not modified concurrently.
- **Complexity**: O(n) where n is the number of torrents
- **See Also**: `m_all_handles`, `m_filtered_handles`

## height

- **Signature**: `int torrent_view::height() const`
- **Description**: Gets the current height of the torrent view.
- **Parameters**: None
- **Return Value**:
  - `int`: The current height of the view.
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
int view_height = view.height();
std::cout << "View height: " << view_height << std::endl;
```
- **Preconditions**: The view must be in a valid state.
- **Postconditions**: Returns the current height of the view.
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `set_size`

## arrow_up

- **Signature**: `void torrent_view::arrow_up()`
- **Description**: Moves the active torrent selection up by one position in the view.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.arrow_up();
```
- **Preconditions**: The view must be in a valid state with at least one torrent.
- **Postconditions**: The active torrent selection is moved up by one position, or remains at the top if already at the top.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(1)
- **See Also**: `arrow_down`, `m_active_torrent`, `m_scroll_position`

## arrow_down

- **Signature**: `void torrent_view::arrow_down()`
- **Description**: Moves the active torrent selection down by one position in the view.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.arrow_down();
```
- **Preconditions**: The view must be in a valid state with at least one torrent.
- **Postconditions**: The active torrent selection is moved down by one position, or remains at the bottom if already at the bottom.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(1)
- **See Also**: `arrow_up`, `m_active_torrent`, `m_scroll_position`

## render

- **Signature**: `void torrent_view::render()`
- **Description**: Renders the entire torrent view to the screen, including tabs, headers, and torrent list.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.render();
```
- **Preconditions**: The view must be in a valid state with valid dimensions and torrent data.
- **Postconditions**: The view is displayed on the screen with all current information.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(n) where n is the number of torrents
- **See Also**: `print_tabs`, `print_headers`, `print_torrent`

## print_tabs

- **Signature**: `void torrent_view::print_tabs()`
- **Description**: Prints the filter tabs at the top of the torrent view.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.print_tabs();
```
- **Preconditions**: The view must be in a valid state with valid dimensions.
- **Postconditions**: The filter tabs are printed at the top of the view.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(1)
- **See Also**: `render`, `m_torrent_filter`

## print_headers

- **Signature**: `void torrent_view::print_headers()`
- **Description**: Prints the column headers for the torrent list.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
view.print_headers();
```
- **Preconditions**: The view must be in a valid state with valid dimensions.
- **Postconditions**: The column headers are printed below the tabs.
- **Thread Safety**: Thread-safe if called from a single thread or with proper synchronization.
- **Complexity**: O(1)
- **See Also**: `render`, `torrent_columns`

## print_torrent

- **Signature**: `void torrent_view::print_torrent(lt::torrent_status const& s, bool selected)`
- **Description**: Prints a single torrent's information to the view.
- **Parameters**:
  - `s` (lt::torrent_status const&): The torrent status to print.
  - `selected` (bool): Whether this torrent is currently selected.
- **Return Value**: None
- **Exceptions/Errors**:
  - No exceptions thrown.
- **Example**:
```cpp
auto torrent = get_torrent_status();
view.print_torrent(torrent, true);
```
- **Preconditions**: The view