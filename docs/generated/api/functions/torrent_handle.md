# libtorrent Python Bindings API Documentation

## url_seeds

- **Signature**: `list url_seeds(torrent_handle& handle)`
- **Description**: Returns a list of magnet URL seeds associated with the torrent. This function queries the torrent handle for its list of URL seeds and returns them as a Python list.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object. The handle must be valid and associated with an active torrent.
- **Return Value**:
  - `list`: A Python list containing all URL seeds as strings. Returns an empty list if no URL seeds are available.
- **Exceptions/Errors**:
  - `std::runtime_error`: Thrown if the torrent handle is invalid or the underlying library call fails.
- **Example**:
```cpp
auto seeds = url_seeds(torrent_handle);
for (auto& seed : seeds) {
    std::cout << seed << std::endl;
}
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent.
- **Postconditions**: The returned list contains all URL seeds currently known to the torrent handle.
- **Thread Safety**: Thread-safe when accessed through the `allow_threading_guard`.
- **Complexity**: O(n) where n is the number of URL seeds.
- **See Also**: `http_seeds()`, `trackers()`

## http_seeds

- **Signature**: `list http_seeds(torrent_handle& handle)`
- **Description**: Returns a list of HTTP seeds associated with the torrent. This function queries the torrent handle for its list of HTTP seeds and returns them as a Python list.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object. The handle must be valid and associated with an active torrent.
- **Return Value**:
  - `list`: A Python list containing all HTTP seeds as strings. Returns an empty list if no HTTP seeds are available.
- **Exceptions/Errors**:
  - `std::runtime_error`: Thrown if the torrent handle is invalid or the underlying library call fails.
- **Example**:
```cpp
auto http_seeds_list = http_seeds(torrent_handle);
for (auto& seed : http_seeds_list) {
    std::cout << seed << std::endl;
}
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent.
- **Postconditions**: The returned list contains all HTTP seeds currently known to the torrent handle.
- **Thread Safety**: Thread-safe when accessed through the `allow_threading_guard`.
- **Complexity**: O(n) where n is the number of HTTP seeds.
- **See Also**: `url_seeds()`, `trackers()`

## piece_availability

- **Signature**: `list piece_availability(torrent_handle& handle)`
- **Description**: Returns a list indicating the availability of each piece in the torrent. Each element represents the number of peers that have that piece.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object. The handle must be valid and associated with an active torrent.
- **Return Value**:
  - `list`: A Python list where each element represents the availability of a piece (number of peers that have that piece). Returns an empty list if the torrent has no pieces.
- **Exceptions/Errors**:
  - `std::runtime_error`: Thrown if the torrent handle is invalid or the underlying library call fails.
- **Example**:
```cpp
auto availability = piece_availability(torrent_handle);
for (size_t i = 0; i < availability.size(); ++i) {
    std::cout << "Piece " << i << " availability: " << availability[i] << std::endl;
}
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent.
- **Postconditions**: The returned list has the same length as the number of pieces in the torrent, with each element indicating piece availability.
- **Thread Safety**: Thread-safe when accessed through the `allow_threading_guard`.
- **Complexity**: O(n) where n is the number of pieces in the torrent.
- **See Also**: `piece_priorities()`, `file_progress()`

## piece_priorities

- **Signature**: `list piece_priorities(torrent_handle& handle)`
- **Description**: Returns a list of piece priorities for the torrent. Each element represents the download priority of a piece (0-7).
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object. The handle must be valid and associated with an active torrent.
- **Return Value**:
  - `list`: A Python list where each element represents the download priority of a piece (0-7). Returns an empty list if the torrent has no pieces.
- **Exceptions/Errors**:
  - `std::runtime_error`: Thrown if the torrent handle is invalid or the underlying library call fails.
- **Example**:
```cpp
auto priorities = piece_priorities(torrent_handle);
for (size_t i = 0; i < priorities.size(); ++i) {
    std::cout << "Piece " << i << " priority: " << priorities[i] << std::endl;
}
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent.
- **Postconditions**: The returned list has the same length as the number of pieces in the torrent, with each element indicating piece priority.
- **Thread Safety**: Thread-safe when accessed through the `allow_threading_guard`.
- **Complexity**: O(n) where n is the number of pieces in the torrent.
- **See Also**: `piece_availability()`, `prioritize_pieces()`

## file_progress

- **Signature**: `list file_progress(torrent_handle& handle, file_progress_flags_t const flags)`
- **Description**: Returns progress information for each file in the torrent.