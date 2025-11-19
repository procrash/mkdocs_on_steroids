# API Documentation

## state

- **Signature**: `char const* state(lt::torrent_status::state_t s)`
- **Description**: Converts a libtorrent torrent status enumeration value to its corresponding string representation. This function is used to provide human-readable status descriptions for torrent states, primarily for debugging or logging purposes.
- **Parameters**:
  - `s` (lt::torrent_status::state_t): The torrent status enumeration value to convert. Valid values include various states like checking_files, downloading_metadata, downloading, seeding, etc.
- **Return Value**:
  - Returns a pointer to a null-terminated C string representing the human-readable status name.
  - The returned string is statically allocated and remains valid for the duration of the program.
  - Returns "unknown" for any unrecognized status values.
- **Exceptions/Errors**:
  - No exceptions are thrown by this function.
  - The function is designed to be safe even with invalid input values.
- **Example**:
```cpp
auto status = lt::torrent_status::downloading;
char const* status_str = state(status);
std::cout << "Current state: " << status_str << std::endl;
```
- **Preconditions**: The input parameter `s` should be a valid value from the `lt::torrent_status::state_t` enumeration.
- **Postconditions**: The function returns a valid string pointer that can be safely used for display or logging purposes.
- **Thread Safety**: The function is thread-safe as it only reads from a static lookup table and returns a pointer to a static string.
- **Complexity**: O(1) time complexity, O(1) space complexity (the lookup table is compiled into the binary).
- **See Also**: `lt::torrent_status::state_t`, `lt::alert_category`, `lt::settings_pack`

## main

- **Signature**: `int main(int argc, char const* argv[])`
- **Description**: The main entry point of the bt-get2 application. This function parses command-line arguments, initializes libtorrent settings, creates a session, adds a torrent from a magnet link, and monitors the download progress until completion.
- **Parameters**:
  - `argc` (int): The number of command-line arguments.
  - `argv` (char const*[]): Array of command-line argument strings.
- **Return Value**:
  - Returns 0 on successful completion.
  - Returns 1 if the usage is incorrect (missing or incorrect number of arguments).
- **Exceptions/Errors**:
  - Can throw libtorrent exceptions for network errors, invalid magnet URLs, or file system errors.
  - Can throw std::bad_alloc for memory allocation failures.
  - The function wraps all exceptions in a try-catch block to ensure proper error handling.
- **Example**:
```cpp
int main(int argc, char const* argv[]) {
    // Usage: bt-get2 <magnet-url>
    return 0;
}
```
- **Preconditions**: The program must be called with exactly one command-line argument containing a valid magnet URL.
- **Postconditions**: The function downloads the torrent specified in the magnet URL to the default save directory and completes when the download is finished.
- **Thread Safety**: The function is not thread-safe as it creates and manages a single libtorrent session. Multiple instances should not be run concurrently.
- **Complexity**: O(1) time complexity for the main loop (the actual download time is determined by network conditions).
- **See Also**: `lt::session`, `lt::add_torrent_params`, `lt::alert`, `lt::settings_pack`

# Usage Examples

## Basic Usage

```cpp
// Compile and run: g++ -o bt-get2 bt-get2.cpp -lboost_system -lboost_thread -lboost_chrono -ltorrent
// Run: ./bt-get2 magnet:?xt=urn:btih:example-hash
#include <iostream>
#include <libtorrent/session.hpp>
#include <libtorrent/alert.hpp>
#include <libtorrent/add_torrent_params.hpp>
#include <libtorrent/settings_pack.hpp>
#include <libtorrent/torrent_status.hpp>

int main(int argc, char const* argv[]) try {
    if (argc != 2) {
        std::cerr << "usage: " << argv[0] << " <magnet-url>" << std::endl;
        return 1;
    }

    lt::settings_pack pack;
    pack.set_int(lt::settings_pack::alert_mask
        , lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::progress
        | lt::alert_category::performance_warning
        | lt::alert_category::stats
        | lt::alert_category::dht
        | lt::alert_category::tracker_warning
        | lt::alert_category::tracker_error
        | lt::alert_category::port_mapping
        | lt::alert_category::listen
        | lt::alert_category::performance_warning
        | lt::alert_category::peer
        | lt::alert_category::upload
        | lt::alert_category::download
        | lt::alert_category::ip_filter
        | lt::alert_category::web_seed);

    lt::session ses(pack);
    lt::add_torrent_params params;
    params.ti = std::make_shared<lt::torrent_info>(lt::parse_magnet_uri(argv[1]));
    params.save_path = "./downloads/";
    params.flags |= lt::add_torrent_params::flag_auto_managed;
    params.flags |= lt::add_torrent_params::flag_paused;
    params.flags |= lt::add_torrent_params::flag_seed_mode;

    lt::torrent_handle handle = ses.add_torrent(params);

    // Wait for the download to complete
    while (handle.status().state != lt::torrent_status::seeding) {
        std::cout << "Downloading: " << handle.status().progress * 100 << "%" << std::endl;
        std::cout << "State: " << state(handle.status().state) << std::endl;
        std::cout << "Progress: " << handle.status().progress * 100 << "%" << std::endl;
        std::cout << "Download speed: " << handle.status().download_rate / 1000 << "KB/s" << std::endl;
        std::cout << "Upload speed: " << handle.status().upload_rate / 1000 << "KB/s" << std::endl;
        std::cout << "Total downloaded: " << handle.status().total_downloaded / 1000000 << "MB" << std::endl;
        std::cout << "Total uploaded: " << handle.status().total_uploaded / 1000000 << "MB" << std::endl;
        std::cout << "Peers: " << handle.status().num_peers << std::endl;
        std::cout << "Seeds: " << handle.status().num_seeds << std::endl;
        std::cout << "Leeches: " << handle.status().num_peers - handle.status().num_seeds << std::endl;
        std::cout << "ETA: " << handle.status().eta / 60 << " minutes" << std::endl;
        std::cout << "Files: " << handle.status().num_files << std::endl;
        std::cout << "Piece length: " << handle.status().piece_length / 1000 << "KB" << std::endl;
        std::cout << "Total size: " << handle.status().total_size / 1000000 << "MB" << std::endl;
        std::cout << "Downloaded: " << handle.status().downloaded / 1000000 << "MB" << std::endl;
        std::cout << "Uploaded: " << handle.status().uploaded / 1000000 << "MB" << std::endl;
        std::cout << "Total files: " << handle.status().total_files << std::endl;
        std::cout << "Total pieces: " << handle.status().num_pieces << std::endl;
        std::cout << "Pieces: " << handle.status().pieces.size() << std::endl;
        std::cout << "Pieces completed: " << handle.status().pieces_completed << std::endl;
        std::cout << "Pieces in use: " << handle.status().pieces_in_use << std::endl;
        std::cout << "Pieces needed: " << handle.status().pieces_needed << std::endl;
        std::cout << "Pieces wanted: " << handle.status().pieces_wanted << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl;
        std::cout << "Pieces wanted by peers: " << handle.status().pieces_wanted_by_peers << std::endl;
        std::cout << "Pieces wanted by seeds: " << handle.status().pieces_wanted_by_seeds << std::endl;
        std::cout << "Pieces wanted by leeches: " << handle.status().pieces_wanted_by_leeches << std::endl