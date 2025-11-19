# Network Link (Netlink) Utilities API Documentation

This documentation provides a comprehensive overview of the network link (Netlink) utility functions in the libtorrent library. These functions serve as inline wrappers around the Netlink API macros, providing a C++-friendly interface for working with Netlink messages and attributes.

## Function Reference

### nlmsg_ok

- **Signature**: `bool nlmsg_ok(nlmsghdr const* hdr, int const len)`
- **Description**: Checks if a Netlink message header is valid and properly aligned within the given buffer length. This function validates that the message header is within the bounds of the provided buffer and that it's properly aligned for the architecture.
- **Parameters**:
  - `hdr` (nlmsghdr const*): Pointer to the Netlink message header to validate. Must not be null.
  - `len` (int const): The length of the buffer containing the message. Must be non-negative.
- **Return Value**:
  - `true`: The message header is valid and properly aligned.
  - `false`: The message header is invalid or misaligned.
- **Exceptions/Errors**:
  - None thrown.
  - This function has undefined behavior if `hdr` is null.
- **Example**:
```cpp
// Check if a Netlink message header is valid
bool isValid = nlmsg_ok(msg_hdr, buffer_size);
if (isValid) {
    // Process the message
}
```
- **Preconditions**: 
  - `hdr` must be a valid pointer to a `nlmsghdr` structure.
  - `len` must be greater than or equal to 0.
- **Postconditions**: 
  - Returns true if the message header is valid and within bounds.
  - Returns false if the message header is invalid or out of bounds.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `nlmsg_next`, `nlmsg_data`

### nlmsg_next

- **Signature**: `nlmsghdr const* nlmsg_next(nlmsghdr const* hdr, int& len)`
- **Description**: Advances to the next Netlink message in a sequence of messages. This function updates the length parameter to reflect the remaining length of the buffer after the current message.
- **Parameters**:
  - `hdr` (nlmsghdr const*): Pointer to the current Netlink message header. Must not be null.
  - `len` (int&): Reference to the current length of the buffer. This will be updated to reflect the remaining length after processing the current message.
- **Return Value**:
  - Pointer to the next Netlink message header, or null if there are no more messages.
- **Exceptions/Errors**:
  - None thrown.
  - This function has undefined behavior if `hdr` is null or if `len` is negative.
- **Example**:
```cpp
// Process a sequence of Netlink messages
nlmsghdr const* msg = initial_msg;
int remaining_len = buffer_size;

while (msg != nullptr) {
    // Process current message
    process_message(msg);
    
    // Get next message
    msg = nlmsg_next(msg, remaining_len);
}
```
- **Preconditions**: 
  - `hdr` must be a valid pointer to a `nlmsghdr` structure.
  - `len` must be non-negative.
- **Postconditions**: 
  - Returns a pointer to the next message header, or null if no more messages exist.
  - Updates `len` to the remaining length of the buffer.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `nlmsg_ok`, `nlmsg_data`

### nlmsg_data

- **Signature**: `void const* nlmsg_data(nlmsghdr const* hdr)`
- **Description**: Returns a pointer to the data portion of a Netlink message. This function extracts the actual payload data from a Netlink message header, which can be used to access the message contents.
- **Parameters**:
  - `hdr` (nlmsghdr const*): Pointer to the Netlink message header. Must not be null.
- **Return Value**:
  - Pointer to the data portion of the message, or null if the header is invalid.
- **Exceptions/Errors**:
  - None thrown.
  - This function has undefined behavior if `hdr` is null.
- **Example**:
```cpp
// Extract data from a Netlink message
void const* data = nlmsg_data(msg_hdr);
if (data != nullptr) {
    // Process the message data
    process_data(data, nlmsg_len(msg_hdr));
}
```
- **Preconditions**: 
  - `hdr` must be a valid pointer to a `nlmsghdr` structure.
- **Postconditions**: 
  - Returns a pointer to the data portion of the message.
  - The returned pointer is valid for the duration of the message header's lifetime.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `nlmsg_ok`, `nlmsg_next`

### rtm_rta

- **Signature**: `rtattr const* rtm_rta(rtmsg const* hdr)`
- **Description**: Returns a pointer to the first attribute in a routing message. This function extracts the pointer to the first attribute in a routing message header, which can be used to iterate through the message's attributes.
- **Parameters**:
  - `hdr` (rtmsg const*): Pointer to the routing message header. Must not be null.
- **Return Value**:
  - Pointer to the first attribute in the routing message, or null if the header is invalid.
- **Exceptions/Errors**:
  - None thrown.
  - This function has undefined behavior if `hdr` is null.
- **Example**:
```cpp
// Access routing message attributes
rtattr const* attr = rtm_rta(routing_msg);
while (attr != nullptr) {
    // Process each attribute
    process_attribute(attr);
    attr = rta_next(attr, attr_len);
}
```
- **Preconditions**: 
  - `hdr` must be a valid pointer to a `rtmsg` structure.
- **Postconditions**: 
  - Returns a pointer to the first attribute in the routing message.
  - The returned pointer is valid for the duration of the message header's lifetime.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `rtm_payload`, `rta_ok`, `rta_next`

### rtm_payload

- **Signature**: `std::size_t rtm_payload(nlmsghdr const* hdr)`
- **Description**: Returns the payload length of a routing message. This function calculates the length of the payload data in a routing message, which is the size of the message data excluding the header.
- **Parameters**:
  - `hdr` (nlmsghdr const*): Pointer to the Netlink message header. Must not be null.
- **Return Value**:
  - The length of the payload data in the message.
- **Exceptions/Errors**:
  - None thrown.
  - This function has undefined behavior if `hdr` is null.
- **Example**:
```cpp
// Get the payload length of a routing message
std::size_t payload_len = rtm_payload(msg_hdr);
if (payload_len > 0) {
    // Process the payload data
    void const* data = nlmsg_data(msg_hdr);
    process_data(data, payload_len);
}
```
- **Preconditions**: 
  - `hdr` must be a valid pointer to a `nlmsghdr` structure.
- **Postconditions**: 
  - Returns the length of the payload data.
  - The returned value is always non-negative.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `nlmsg_data`, `nlmsg_ok`

### rta_ok

- **Signature**: `bool rta_ok(rtattr const* rt, std::size_t const len)`
- **Description**: Checks if a route attribute is valid and properly aligned within the given buffer length. This function validates that the attribute is within bounds and properly aligned.
- **Parameters**:
  - `rt` (rtattr const*): Pointer to the route attribute to validate. Must not be null.
  - `len` (std::size_t const): The length of the buffer containing the attribute. Must be non-negative.
- **Return Value**:
  - `true`: The route attribute is valid and properly aligned.
  - `false`: The route attribute is invalid or misaligned.
- **Exceptions/Errors**:
  - None thrown.
  - This function has undefined behavior if `rt` is null.
- **Example**:
```cpp
// Check if a route attribute is valid
bool isValid = rta_ok(attr, buffer_size);
if (isValid) {
    // Process the attribute data
    void const* data = rta_data(attr);
    process_attribute_data(data, RTA_PAYLOAD(attr));
}
```
- **Preconditions**: 
  - `rt` must be a valid pointer to an `rtattr` structure.
  - `len` must be non-negative.
- **Postconditions**: 
  - Returns true if the attribute is valid and within bounds.
  - Returns false if the attribute is invalid or out of bounds.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `rta_data`, `rta_next`

### rta_data

- **Signature**: `void const* rta_data(rtattr const* rt)`
- **Description**: Returns a pointer to the data portion of a route attribute. This function extracts the actual payload data from a route attribute, which can be used to access the attribute contents.
- **Parameters**:
  - `rt` (rtattr const*): Pointer to the route attribute. Must not be null.
- **Return Value**:
  - Pointer to the data portion of the attribute, or null if the attribute is invalid.
- **Exceptions/Errors**:
  - None thrown.
  - This function has undefined behavior if `rt` is null.
- **Example**:
```cpp
// Extract data from a route attribute
void const* data = rta_data(attr);
if (data != nullptr) {
    // Process the attribute data
    process_attribute_data(data, RTA_PAYLOAD(attr));
}
```
- **Preconditions**: 
  - `rt` must be a valid pointer to an `rtattr` structure.
- **Postconditions**: 
  - Returns a pointer to the data portion of the attribute.
  - The returned pointer is valid for the duration of the attribute's lifetime.
- **Thread Safety**: Thread-safe.
- **Complexity**: O(1)
- **See Also**: `rta_ok`, `rta_next`

### rta_next

- **Signature**: `rtattr const* rta_next(rtattr const* rt, std::size_t& len)`
- **Description**: Advances to the next route attribute in a sequence of attributes. This function updates the length parameter to reflect the remaining length of the buffer after the current attribute.
- **Parameters**:
  - `rt` (rtattr const*): Pointer to the current route attribute. Must not be null.
  - `len` (std::size_t&): Reference to the current length of the buffer. This will be updated to reflect the remaining length after processing the current attribute.
- **Return Value**:
  - Pointer to the next route attribute, or null if there are no more attributes.
- **Exceptions/Errors**:
  - None thrown.
  - This function has undefined behavior