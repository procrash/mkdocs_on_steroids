# Magnet URI API Documentation

## _add_magnet_uri

- **Signature**: `torrent_handle _add_magnet_uri(lt::session& s, std::string uri, dict params)`
- **Description**: Adds a torrent to the session using a magnet URI. This function is deprecated and should not be used in new code. It converts the magnet URI and parameters into an add_torrent_params structure and adds the torrent to the session. The function is marked as deprecated with a warning message.
- **Parameters**:
  - `s` (lt::session&): Reference to the libtorrent session object. Must be valid and not destroyed during the function call.
  - `uri` (std::string): The magnet URI string to be parsed and added. Must be a valid magnet URI format.
  - `params` (dict): Dictionary containing additional parameters for the torrent addition. These parameters are converted to an add_torrent_params structure.
- **Return Value**:
  - `torrent_handle`: A handle to the added torrent. This handle can be used to control the torrent and access its information. If the function fails, the behavior is undefined due to the incomplete code.
- **Exceptions/Errors**:
  - `system_error`: Thrown if the magnet URI parsing fails or if there's an error during the torrent addition process. The error code is obtained from the parse_magnet_uri function.
  - `std::runtime_error`: Potentially thrown if the parameters dictionary is invalid or contains unsupported keys.
- **Example**:
```cpp
try {
    lt::session ses;
    std::string magnet_uri = "magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678";
    dict params;
    params["save_path"] = "/tmp/torrents";
    
    torrent_handle handle = _add_magnet_uri(ses, magnet_uri, params);
    if (handle.is_valid()) {
        std::cout << "Torrent added successfully with handle: " << handle.info_hash().to_string() << std::endl;
    }
} catch (const std::exception& e) {
    std::cerr << "Error adding magnet URI: " << e.what() << std::endl;
}
```
- **Preconditions**:
  - The session object must be valid and running.
  - The magnet URI must be syntactically correct.
  - The parameters dictionary must be properly formatted and contain valid keys.
- **Postconditions**:
  - A torrent is added to the session if successful.
  - The returned torrent handle is valid and can be used to control the torrent.
  - If the function fails, the session state is unchanged.
- **Thread Safety**: The function is thread-safe as it acquires a threading guard.
- **Complexity**:
  - Time Complexity: O(n) where n is the length of the magnet URI.
  - Space Complexity: O(1) additional space, excluding the input parameters.
- **See Also**: `parse_magnet_uri`, `add_torrent_params`, `lt::session`

## parse_magnet_uri_dict

- **Signature**: `dict parse_magnet_uri_dict(std::string const& uri)`
- **Description**: Parses a magnet URI and returns a dictionary containing the extracted information. This function converts the magnet URI into an add_torrent_params structure and then extracts relevant fields into a Python dictionary format. It's useful for examining the components of a magnet URI without actually adding a torrent.
- **Parameters**:
  - `uri` (std::string const&): The magnet URI to parse. Must be a valid magnet URI format.
- **Return Value**:
  - `dict`: A dictionary containing the parsed components of the magnet URI. The dictionary may include keys like "ti" for the torrent info, "trackers" for tracker URLs, and other relevant fields.
- **Exceptions/Errors**:
  - `system_error`: Thrown if the magnet URI cannot be parsed due to invalid format or other parsing errors.
- **Example**:
```cpp
try {
    std::string magnet_uri = "magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&tr=http://tracker1.com&tr=http://tracker2.com";
    dict result = parse_magnet_uri_dict(magnet_uri);
    
    if (result.has_key("ti")) {
        // Process the torrent info
        torrent_info ti = result["ti"];
        std::cout << "Torrent info hash: " << ti.info_hash().to_string() << std::endl;
    }
    
    if (result.has_key("trackers")) {
        list trackers = result["trackers"];
        for (int i = 0; i < trackers.size(); ++i) {
            std::cout << "Tracker: " << trackers[i].as<std::string>() << std::endl;
        }
    }
} catch (const std::exception& e) {
    std::cerr << "Error parsing magnet URI: " << e.what() << std::endl;
}
```
- **Preconditions**:
  - The magnet URI must be valid and properly formatted.
  - The function should not be called with null or empty strings.
- **Postconditions**:
  - The returned dictionary contains the parsed components of the magnet URI.
  - The dictionary is valid and can be safely used to access the parsed information.
- **Thread Safety**: The function is thread-safe as it operates on local variables and does not modify global state.
- **Complexity**:
  - Time Complexity: O(n) where n is the length of the magnet URI.
  - Space Complexity: O(m) where m is the number of trackers and other components in the magnet URI.
- **See Also**: `parse_magnet_uri_wrap`, `add_torrent_params`, `lt::session`

## parse_magnet_uri_wrap

- **Signature**: `add_torrent_params parse_magnet_uri_wrap(std::string const& uri)`
- **Description**: A wrapper function that parses a magnet URI and returns an add_torrent_params structure. This function provides a simpler interface for accessing the parsed components of a magnet URI without the need to handle the dictionary conversion directly.
- **Parameters**:
  - `uri` (std::string const&): The magnet URI to parse. Must be a valid magnet URI format.
- **Return Value**:
  - `add_torrent_params`: An add_torrent_params structure containing the parsed components of the magnet URI. This structure can be used directly with the add_torrent function.
- **Exceptions/Errors**:
  - `system_error`: Thrown if the magnet URI cannot be parsed due to invalid format or other parsing errors.
- **Example**:
```cpp
try {
    std::string magnet_uri = "magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&tr=http://tracker1.com&tr=http://tracker2.com";
    add_torrent_params params = parse_magnet_uri_wrap(magnet_uri);
    
    // Use the parameters to add a torrent
    lt::session ses;
    torrent_handle handle = ses.add_torrent(params);
    if (handle.is_valid()) {
        std::cout << "Torrent added successfully with handle: " << handle.info_hash().to_string() << std::endl;
    }
} catch (const std::exception& e) {
    std::cerr << "Error parsing magnet URI: " << e.what() << std::endl;
}
```
- **Preconditions**:
  - The magnet URI must be valid and properly formatted.
  - The function should not be called with null or empty strings.
- **Postconditions**:
  - The returned add_torrent_params structure contains the parsed components of the magnet URI.
  - The structure is valid and can be used to add a torrent to a session.
- **Thread Safety**: The function is thread-safe as it operates on local variables and does not modify global state.
- **Complexity**:
  - Time Complexity: O(n) where n is the length of the magnet URI.
  - Space Complexity: O(m) where m is the number of trackers and other components in the magnet URI.
- **See Also**: `parse_magnet_uri_dict`, `add_torrent_params`, `lt::session`

## bind_magnet_uri

- **Signature**: `void bind_magnet_uri()`
- **Description**: Binds magnet URI functions to the Python module. This function registers the magnet URI functions with the Python module, making them available for use in Python scripts. It conditionally registers functions based on the TORRENT_ABI_VERSION.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**: None
- **Example**:
```cpp
// This function is typically called during module initialization
// No direct usage in application code
bind_magnet_uri();
```
- **Preconditions**:
  - The Python module must be initialized.
  - The functions being bound must be properly defined and available.
- **Postconditions**:
  - The magnet URI functions are registered in the Python module.
  - The functions are available for use in Python scripts.
- **Thread Safety**: The function is not thread-safe and should only be called during module initialization.
- **Complexity**:
  - Time Complexity: O(1) as it's a simple registration process.
  - Space Complexity: O(1) additional space.
- **See Also**: `def`, `add_magnet_uri`, `make_magnet_uri`, `parse_magnet_uri`

# Usage Examples

## Basic Usage

```cpp
#include <libtorrent/session.hpp>
#include <libtorrent/add_torrent_params.hpp>
#include <libtorrent/magnet_uri.hpp>
#include <libtorrent/dict.hpp>
#include <libtorrent/torrent_handle.hpp>
#include <iostream>
#include <string>

int main() {
    // Initialize libtorrent session
    lt::session ses;
    
    // Parse a magnet URI and add it to the session
    std::string magnet_uri = "magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678";
    
    try {
        // Parse magnet URI into parameters
        add_torrent_params params = parse_magnet_uri_wrap(magnet_uri);
        
        // Add the torrent to the session
        torrent_handle handle = ses.add_torrent(params);
        
        if (handle.is_valid()) {
            std::cout << "Successfully added torrent: " << handle.info_hash().to_string() << std::endl;
        } else {
            std::cout << "Failed to add torrent" << std::endl;
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    
    return 0;
}
```

## Error Handling

```cpp
#include <libtorrent/session.hpp>
#include <libtorrent/add_torrent_params.hpp>
#include <libtorrent/magnet_uri.hpp>
#include <libtorrent/dict.hpp>
#include <libtorrent/torrent_handle.hpp>
#include <iostream>
#include <string>

int main() {
    lt::session ses;
    
    // Test with invalid magnet URI
    std::string invalid_magnet = "invalid_magnet_uri";
    
    try {
        // Try to parse invalid magnet URI
        add_torrent_params params = parse_magnet_uri_wrap(invalid_magnet);
        
        // This should not be reached if the URI is invalid
        torrent_handle handle = ses.add_torrent(params);
        std::cout << "Successfully added torrent: " << handle.info_hash().to_string() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Caught exception while parsing magnet URI: " << e.what() << std::endl;
        
        // Check specific error types
        if (typeid(e) == typeid(lt::system_error)) {
            std::cerr << "Error was a system_error, check the error code" << std::endl;
        }
    }
    
    return 0;
}
```

## Edge Cases

```cpp
#include <libtorrent/session.hpp>
#include <libtorrent/add_torrent_params.hpp>
#include <libtorrent/magnet_uri.hpp>
#include <libtorrent/dict.hpp>
#include <libtorrent/torrent_handle.hpp>
#include <iostream>
#include <string>

int main() {
    lt::session ses;
    
    // Test with empty magnet URI
    std::string empty_magnet = "";
    
    try {
        add_torrent_params params = parse_m