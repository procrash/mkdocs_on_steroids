# libtorrent receive_buffer API Documentation

## Overview
The `receive_buffer` class in libtorrent provides a mechanism for managing incoming packet data, particularly for handling encrypted connections. It tracks the state of received data, supports packet size validation, and provides utilities for cryptographic operations. The class is designed to be used with the `crypto_receive_buffer` decorator to handle encrypted traffic.

## Function Reference

### packet_size

- **Signature**: `int packet_size() const`
- **Description**: Returns the total size of the current packet being received. This value is set when a new packet is received and remains constant until the packet is fully processed.
- **Parameters**: None
- **Return Value**: 
  - The total packet size in bytes
  - Always returns a positive value when valid
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
int packet_size = buffer.packet_size();
if (packet_size > 0) {
    // Process packet of known size
    std::cout << "Packet size: " << packet_size << " bytes" << std::endl;
}
```
- **Preconditions**: The buffer must have a valid packet size set
- **Postconditions**: Returns the current packet size without modifying the buffer state
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `packet_bytes_remaining()`, `packet_finished()`

### packet_bytes_remaining

- **Signature**: `int packet_bytes_remaining() const`
- **Description**: Calculates how many bytes are still needed to complete the current packet. This is the difference between the total packet size and the number of bytes already received.
- **Parameters**: None
- **Return Value**:
  - Number of bytes remaining to complete the packet
  - Returns 0 when the packet is complete
  - Returns a positive value when more data is needed
- **Exceptions/Errors**:
  - `TORRENT_ASSERT` failures if internal state is inconsistent
- **Example**:
```cpp
int bytes_remaining = buffer.packet_bytes_remaining();
if (bytes_remaining > 0) {
    std::cout << bytes_remaining << " bytes remaining" << std::endl;
}
```
- **Preconditions**: 
  - `m_packet_size` must be positive
  - `m_recv_start` must be 0
- **Postconditions**: Returns the number of bytes needed to complete the packet
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `packet_size()`, `packet_finished()`

### packet_finished

- **Signature**: `bool packet_finished() const`
- **Description**: Determines whether the current packet has been fully received by comparing the received position with the packet size.
- **Parameters**: None
- **Return Value**:
  - `true` if the packet is complete (all bytes received)
  - `false` if more data is needed
- **Exceptions/Errors**:
  - `TORRENT_ASSERT` failures if internal state is inconsistent
- **Example**:
```cpp
if (buffer.packet_finished()) {
    std::cout << "Packet received completely" << std::endl;
    // Process the complete packet
} else {
    std::cout << "Still receiving data" << std::endl;
}
```
- **Preconditions**: The buffer must have a valid packet size set
- **Postconditions**: Returns true if the packet is complete, false otherwise
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `packet_bytes_remaining()`, `packet_size()`

### pos

- **Signature**: `int pos() const`
- **Description**: Returns the current position in the receive buffer, indicating how many bytes have been received so far.
- **Parameters**: None
- **Return Value**:
  - The number of bytes received in the current packet
  - Returns 0 when no bytes have been received
  - Returns a positive value representing the current position
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
int current_pos = buffer.pos();
std::cout << "Received " << current_pos << " bytes so far" << std::endl;
```
- **Preconditions**: None
- **Postconditions**: Returns the current receive position without modifying the buffer state
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `received()`, `packet_bytes_remaining()`

### capacity

- **Signature**: `int capacity() const`
- **Description**: Returns the total capacity of the receive buffer in bytes.
- **Parameters**: None
- **Return Value**:
  - The capacity of the receive buffer
  - The value is converted from `std::size_t` to `int` using `aux::numeric_cast`
- **Exceptions/Errors**:
  - `TORRENT_ASSERT` failures if the buffer size exceeds the maximum int value
- **Example**:
```cpp
int buffer_capacity = buffer.capacity();
std::cout << "Buffer capacity: " << buffer_capacity << " bytes" << std::endl;
```
- **Preconditions**: The buffer must be properly initialized
- **Postconditions**: Returns the buffer capacity without modifying the buffer state
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `received()`, `pos()`

### watermark

- **Signature**: `int watermark() const`
- **Description**: Returns the current watermark value, which represents the average watermark for the connection.
- **Parameters**: None
- **Return Value**:
  - The watermark value as an integer
  - The value is converted from `std::size_t` to `int` using `aux::numeric_cast`
- **Exceptions/Errors**:
  - `TORRENT_ASSERT` failures if the watermark exceeds the maximum int value
- **Example**:
```cpp
int current_watermark = buffer.watermark();
std::cout << "Current watermark: " << current_watermark << std::endl;
```
- **Preconditions**: The buffer must be properly initialized
- **Postconditions**: Returns the watermark value without modifying the buffer state
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `capacity()`, `received()`

### received

- **Signature**: `void received(int bytes_transferred)`
- **Description**: Updates the receive position by adding the number of bytes transferred to the current position. This function is called when data is received from the network.
- **Parameters**:
  - `bytes_transferred` (int): The number of bytes that were successfully received
  - Must be non-negative
  - Should not exceed the remaining capacity
- **Return Value**: None
- **Exceptions/Errors**:
  - `TORRENT_ASSERT` failures if `m_packet_size` is not positive or if the position exceeds the buffer size
- **Example**:
```cpp
buffer.received(1024); // Mark that 1024 bytes were received
if (buffer.packet_finished()) {
    // Process the complete packet
}
```
- **Preconditions**: 
  - `m_packet_size` must be positive
  - `bytes_transferred` must be non-negative
- **Postconditions**: Updates the receive position and end position
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `pos()`, `packet_finished()`, `packet_bytes_remaining()`

### pos_at_end

- **Signature**: `bool pos_at_end()`
- **Description**: Checks if the current receive position is at the end of the received data for this packet.
- **Parameters**: None
- **Return Value**:
  - `true` if the receive position equals the end position
  - `false` otherwise
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
if (buffer.pos_at_end()) {
    std::cout << "All data for this packet has been received" << std::endl;
} else {
    std::cout << "Still receiving data" << std::endl;
}
```
- **Preconditions**: The buffer must have valid receive positions
- **Postconditions**: Returns true if pos equals end, false otherwise
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `pos()`, `received()`

### normalized

- **Signature**: `bool normalized() const`
- **Description**: Checks if the receive buffer is in a normalized state, where `m_recv_start` is 0.
- **Parameters**: None
- **Return Value**:
  - `true` if the buffer is normalized (m_recv_start == 0)
  - `false` otherwise
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
if (buffer.normalized()) {
    std::cout << "Buffer is in normalized state" << std::endl;
} else {
    std::cout << "Buffer needs normalization" << std::endl;
}
```
- **Preconditions**: The buffer must be properly initialized
- **Postconditions**: Returns the normalized state without modifying the buffer
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `check_invariant()`, `received()`

### check_invariant

- **Signature**: `void check_invariant() const`
- **Description**: Verifies the internal consistency of the receive buffer. This function should be called during debugging to ensure the buffer is in a valid state.
- **Parameters**: None
- **Return Value**: None
- **Exceptions/Errors**:
  - `TORRENT_ASSERT` failures if any invariant is violated
- **Example**:
```cpp
buffer.check_invariant(); // Verify buffer consistency
```
- **Preconditions**: The buffer must be in a consistent state
- **Postconditions**: No state changes; only performs assertions
- **Thread Safety**: Thread-safe
- **Complexity**: O(1) with assertions
- **See Also**: `pos()`, `pos_at_end()`, `normalized()`

### crypto_receive_buffer

- **Signature**: `crypto_receive_buffer(receive_buffer& next)`
- **Description**: Constructor for the `crypto_receive_buffer` decorator. Creates a wrapper around a `receive_buffer` to handle cryptographic operations.
- **Parameters**:
  - `next` (receive_buffer&): Reference to the underlying receive buffer to be decorated
  - Must be a valid, non-null reference to a receive_buffer
- **Return Value**: None (constructor)
- **Exceptions/Errors**:
  - None
-