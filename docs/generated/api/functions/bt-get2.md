# API Documentation for bt-get2.cpp

## state

- **Signature**: `char const* state(lt::torrent_status::state_t s)`
- **Description**: Converts a libtorrent torrent status enumeration value to its corresponding string representation. This function is used to display human-readable status messages for a torrent's current state.
- **Parameters**:
  - `s` (lt::torrent_status::state_t): The torrent status enum value to convert. Valid values include all members of the lt::torrent_status::state_t enumeration such as checking_files, downloading_metadata, downloading, etc.
- **Return Value**:
  - Returns a null-terminated C-style string representing the status.
  - Returns "checking" for lt::torrent_status::checking_files
  - Returns "dl" for lt::torrent_status::downloading_metadata
  - Returns "error" for lt::torrent_status::error
  - Returns "finished" for lt::torrent_status::finished
  - Returns "seeding" for lt::torrent_status::seeding
  - Returns "allocating" for lt::torrent_status::allocating
  - Returns "downloading" for lt::torrent_status::downloading
  - Returns "paused" for lt::torrent_status::paused
  - Returns "queued" for lt::torrent_status::queued
  - Returns "stalled" for lt::torrent_status::stalled
  - Returns "checking resume data" for lt::torrent_status::checking_resume_data
  - Returns "checking" for lt::torrent_status::checking
  - Returns "unknown" for any other unknown status
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
  - The function is designed to handle all valid values in the enumeration.
- **Example**:
```cpp
// Convert a torrent status to a string
lt::torrent_status::state_t status = lt::torrent_status::downloading;
char const* status_str = state(status);
std::cout << "Current status: " << status_str << std::endl;
```
- **Preconditions**: The input parameter `s` must be a valid lt::torrent_status::state_t enum value.
- **Postconditions**: The function returns a valid null-terminated string that can be safely used for display purposes.
- **Thread Safety**: The function is thread-safe as it only reads from the input parameter and returns a constant string literal.
- **Complexity**: O(1) time complexity, O(1) space complexity.
- **See Also**: `lt::torrent_status`, `lt::alert_category`

## main

- **Signature**: `int main(int argc, char const* argv[])`
- **Description**: The entry point of the bt-get2 application. This function parses command-line arguments, initializes the libtorrent session, and starts downloading a torrent from a magnet link. It handles the core functionality of downloading a torrent file and providing status updates.
- **Parameters**:
  - `argc` (int): The number of command-line arguments passed to the program.
  - `argv` (char const*[]): An array of C-style strings containing the command-line arguments.
- **Return Value**:
  - Returns 0 if the program executes successfully.
  - Returns 1 if there's an error (such as incorrect number of arguments).
- **Exceptions/Errors**:
  - Throws exceptions from libtorrent library functions.
  - Throws std::invalid_argument if the magnet URL is invalid.
  - Throws std::runtime_error if the libtorrent session cannot be created.
- **Example**:
```cpp
// Run the bt-get2 application
int result = main(2, (char const*[]){"bt-get2", "magnet:?xt=urn:btih:..."}); 
if (result != 0) {
    std::cerr << "Program failed with error code: " << result << std::endl;
}
```
- **Preconditions**: The program must be called with exactly one argument (the magnet URL).
- **Postconditions**: If successful, the torrent will be downloaded and the program will exit after completion.
- **Thread Safety**: The function itself is not thread-safe due to its global state manipulation, but it's designed to be called from the main thread only.
- **Complexity**: O(1) time complexity for the main function itself, though the actual torrent download process has variable time complexity depending on network conditions and torrent size.
- **See Also**: `lt::settings_pack`, `lt::alert_category`, `lt::session`

## Usage Examples

### Basic Usage
```cpp
// Compile and run with a magnet URL
g++ -o bt-get2 bt-get2.cpp -lboost_system -lboost_thread -ltorrent
./bt-get2 "magnet:?xt=urn:btih:example_magnet_hash"
```

### Error Handling
```cpp
int main(int argc, char const* argv[]) try {
    if (argc != 2) {
        std::cerr << "usage: " << argv[0] << " <magnet-url>" << std::endl;
        return 1;
    }

    lt::settings_pack pack;
    pack.set_int(lt::settings_pack::alert_mask
        , lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::status
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::ip_filter
        | lt::alert_category::performance_warning
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::announce
        | lt::alert_category::performance_warning
        | lt::alert_category::tracker
        | lt::alert_category::announce
        | lt::alert_category::peer
        | lt::alert_category::magnet_uri
        | lt::alert_category::external_ip
        | lt::alert_category::port
        | lt::alert_category::announce
        | lt::alert_category::status
        | lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
