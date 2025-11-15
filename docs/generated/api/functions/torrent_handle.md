# libtorrent Python Bindings - Torrent Handle API Documentation

## url_seeds

- **Signature**: `list url_seeds(torrent_handle& handle)`
- **Description**: Returns a list of URL seeds associated with the torrent. URL seeds are alternative sources for torrent data that use HTTP/HTTPS protocols.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
- **Return Value**:
  - Returns a Python list containing strings representing the URL seeds
  - Returns an empty list if no URL seeds are available
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid
- **Example**:
```python
seeds = url_seeds(torrent_handle)
for seed in seeds:
    print(f"URL Seed: {seed}")
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The returned list contains all URL seeds currently known to the torrent
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of URL seeds
- **See Also**: `http_seeds()`, `trackers()`

## http_seeds

- **Signature**: `list http_seeds(torrent_handle& handle)`
- **Description**: Returns a list of HTTP seeds associated with the torrent. HTTP seeds are similar to URL seeds but specifically use HTTP/HTTPS protocols for downloading.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
- **Return Value**:
  - Returns a Python list containing strings representing the HTTP seeds
  - Returns an empty list if no HTTP seeds are available
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid
- **Example**:
```python
http_seeds_list = http_seeds(torrent_handle)
for seed in http_seeds_list:
    print(f"HTTP Seed: {seed}")
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The returned list contains all HTTP seeds currently known to the torrent
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of HTTP seeds
- **See Also**: `url_seeds()`, `trackers()`

## piece_availability

- **Signature**: `list piece_availability(torrent_handle& handle)`
- **Description**: Returns a list representing the availability of each piece in the torrent. Each entry corresponds to a piece and indicates how many peers have that piece.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
- **Return Value**:
  - Returns a Python list where each element represents the number of peers that have a specific piece
  - The list is ordered by piece index (0, 1, 2, ...)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid
- **Example**:
```python
availability = piece_availability(torrent_handle)
for i, count in enumerate(availability):
    print(f"Piece {i} available with {count} peers")
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The returned list contains availability counts for all pieces in the torrent
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of pieces in the torrent
- **See Also**: `piece_priorities()`, `file_progress()`

## piece_priorities

- **Signature**: `list piece_priorities(torrent_handle& handle)`
- **Description**: Returns a list of piece priorities for the torrent. This indicates the priority level for each piece in the download queue.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
- **Return Value**:
  - Returns a Python list where each element represents the download priority for a specific piece
  - The list is ordered by piece index (0, 1, 2, ...)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid
- **Example**:
```python
priorities = piece_priorities(torrent_handle)
for i, prio in enumerate(priorities):
    print(f"Piece {i} priority: {prio}")
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The returned list contains priority values for all pieces in the torrent
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of pieces in the torrent
- **See Also**: `prioritize_pieces()`, `file_priorities()`

## file_progress

- **Signature**: `list file_progress(torrent_handle& handle, file_progress_flags_t const flags)`
- **Description**: Returns a list representing the download progress for each file in the torrent. The progress is measured in bytes completed for each file.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
  - `flags` (file_progress_flags_t const): Optional flags to control the behavior of the function
- **Return Value**:
  - Returns a Python list where each element represents the number of bytes downloaded for a specific file
  - The list is ordered by file index (0, 1, 2, ...)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid
- **Example**:
```python
progress = file_progress(torrent_handle, file_progress_flags_t.DEFAULT)
for i, bytes_downloaded in enumerate(progress):
    print(f"File {i}: {bytes_downloaded} bytes downloaded")
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The returned list contains download progress for all files in the torrent
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of files in the torrent
- **See Also**: `file_priorities()`, `get_download_queue()`

## get_peer_info

- **Signature**: `list get_peer_info(torrent_handle const& handle)`
- **Description**: Returns a list of peer information for the torrent. This includes details about each peer that is connected to the torrent.
- **Parameters**:
  - `handle` (torrent_handle const&): Reference to the torrent handle object that contains the torrent information
- **Return Value**:
  - Returns a Python list containing `peer_info` objects for each connected peer
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid
- **Example**:
```python
peers = get_peer_info(torrent_handle)
for peer in peers:
    print(f"Peer IP: {peer.ip}, Download Speed: {peer.download_rate} KB/s")
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The returned list contains information about all connected peers
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of connected peers
- **See Also**: `get_download_queue()`, `trackers()`

## extract_fn

- **Signature**: `T extract_fn(object o)`
- **Description**: Extracts a value of type T from a Python object using boost::python's extraction mechanism. This is a template function that can extract various types.
- **Parameters**:
  - `o` (object): Python object to extract the value from
- **Return Value**:
  - Returns the extracted value of type T
- **Exceptions/Errors**:
  - May throw `boost::python::error_already_set` if the extraction fails
- **Example**:
```python
# Assuming this is used internally in the bindings
int value = extract_fn<int>(python_object)
```
- **Preconditions**: The Python object must be convertible to the target type T
- **Postconditions**: Returns the extracted value if successful
- **Thread Safety**: Depends on the underlying boost::python implementation
- **Complexity**: O(1) for simple types, O(n) for complex types
- **See Also**: None (internal utility function)

## prioritize_pieces

- **Signature**: `void prioritize_pieces(torrent_handle& info, object o)`
- **Description**: Sets the priorities for pieces in the torrent based on the provided object. The function determines whether the input is a list of priorities or a list of piece->priority mappings.
- **Parameters**:
  - `info` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
  - `o` (object): Python object containing the priority data
- **Return Value**:
  - None (void function)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid or the input is malformed
- **Example**:
```python
# Setting priorities for all pieces
prioritize_pieces(torrent_handle, [1, 2, 3, 4, 5])
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The piece priorities are updated according to the input
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of pieces
- **See Also**: `prioritize_files()`, `piece_priorities()`

## prioritize_files

- **Signature**: `void prioritize_files(torrent_handle& info, object o)`
- **Description**: Sets the priorities for files in the torrent based on the provided object. The function converts the Python object to a vector of download_priority_t values.
- **Parameters**:
  - `info` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
  - `o` (object): Python object containing the priority data
- **Return Value**:
  - None (void function)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid or the input is malformed
- **Example**:
```python
# Setting priorities for all files
prioritize_files(torrent_handle, [1, 2, 3, 4, 5])
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The file priorities are updated according to the input
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of files
- **See Also**: `prioritize_pieces()`, `file_priorities()`

## file_priorities

- **Signature**: `list file_priorities(torrent_handle& handle)`
- **Description**: Returns a list of file priorities for the torrent. This indicates the priority level for each file in the download queue.
- **Parameters**:
  - `handle` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
- **Return Value**:
  - Returns a Python list where each element represents the download priority for a specific file
  - The list is ordered by file index (0, 1, 2, ...)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid
- **Example**:
```python
priorities = file_priorities(torrent_handle)
for i, prio in enumerate(priorities):
    print(f"File {i} priority: {prio}")
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The returned list contains priority values for all files in the torrent
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of files in the torrent
- **See Also**: `prioritize_files()`, `file_priority0()`

## file_priority0

- **Signature**: `download_priority_t file_priority0(torrent_handle& h, file_index_t index)`
- **Description**: Returns the current priority of a specific file in the torrent.
- **Parameters**:
  - `h` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
  - `index` (file_index_t): Index of the file whose priority to retrieve
- **Return Value**:
  - Returns the download priority of the specified file
  - Returns a default priority if the file index is invalid
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid
- **Example**:
```python
priority = file_priority0(torrent_handle, 0)
print(f"File 0 priority: {priority}")
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: Returns the current priority of the specified file
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(1)
- **See Also**: `file_priority1()`, `file_priorities()`

## file_priority1

- **Signature**: `void file_priority1(torrent_handle& h, file_index_t index, download_priority_t prio)`
- **Description**: Sets the priority of a specific file in the torrent.
- **Parameters**:
  - `h` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
  - `index` (file_index_t): Index of the file whose priority to set
  - `prio` (download_priority_t): The new priority value for the file
- **Return Value**:
  - None (void function)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid or the index is out of bounds
- **Example**:
```python
file_priority1(torrent_handle, 0, download_priority_t.HIGH)
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The specified file's priority is updated to the new value
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(1)
- **See Also**: `file_priority0()`, `file_priorities()`

## dict_to_announce_entry

- **Signature**: `void dict_to_announce_entry(dict d, announce_entry& ae)`
- **Description**: Converts a Python dictionary to an announce_entry structure. This function extracts values from the dictionary and populates the announce_entry.
- **Parameters**:
  - `d` (dict): Python dictionary containing tracker information
  - `ae` (announce_entry&): Reference to the announce_entry structure to populate
- **Return Value**:
  - None (void function)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the dictionary doesn't contain required keys
- **Example**:
```python
# This function is used internally in the bindings
ae = announce_entry()
dict_to_announce_entry({"url": "http://example.com"}, ae)
```
- **Preconditions**: The dictionary must contain a "url" key
- **Postconditions**: The announce_entry structure is populated with values from the dictionary
- **Thread Safety**: Depends on the context in which it's called
- **Complexity**: O(1)
- **See Also**: `add_tracker()`, `replace_trackers()`

## replace_trackers

- **Signature**: `void replace_trackers(torrent_handle& h, object trackers)`
- **Description**: Replaces all existing trackers for a torrent with the provided list of trackers.
- **Parameters**:
  - `h` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
  - `trackers` (object): Python object containing the list of trackers
- **Return Value**:
  - None (void function)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid or the input is malformed
- **Example**:
```python
# Replace all trackers with a new list
replace_trackers(torrent_handle, [{"url": "http://newtracker.com"}, {"url": "http://anothertracker.com"}])
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: All existing trackers are replaced with the new ones
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(n) where n is the number of trackers
- **See Also**: `add_tracker()`, `trackers()`

## add_tracker

- **Signature**: `void add_tracker(torrent_handle& h, dict d)`
- **Description**: Adds a single tracker to the torrent using the provided dictionary.
- **Parameters**:
  - `h` (torrent_handle&): Reference to the torrent handle object that contains the torrent information
  - `d` (dict): Python dictionary containing tracker information
- **Return Value**:
  - None (void function)
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the handle is invalid or the dictionary doesn't contain required keys
- **Example**:
```python
# Add a new tracker
add_tracker(torrent_handle, {"url": "http://newtracker.com", "tier": 1})
```
- **Preconditions**: The torrent handle must be valid and associated with a running torrent
- **Postconditions**: The specified tracker is added to the torrent
- **Thread Safety**: Thread-safe due to the `allow_threading_guard`
- **Complexity**: O(1)
- **See Also**: `replace_trackers()`, `trackers()`

## to_ptime

- **Signature**: `object to_ptime(time_point tpt)`
- **Description**: Converts a time_point to a Python object representing a timestamp. This function handles the conversion of libtorrent's time_point to a Python timestamp.
- **Parameters**:
  - `tpt` (time_point): The time point to convert
- **Return Value**:
  - Returns a Python object representing the timestamp
  - Returns None if the time point is invalid
- **Exceptions/Errors**:
  - None explicitly thrown, but may fail if the time point is invalid
- **Example**:
```python
# This function is used internally in the