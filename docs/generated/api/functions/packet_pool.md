# libtorrent Packet Pool API Documentation

## operator()

- **Signature**: `void operator()(packet* p) const`
- **Description**: A functor that destructs a packet and frees its memory. This is typically used as a custom deleter for `std::unique_ptr` to properly handle packet cleanup.
- **Parameters**:
  - `p` (`packet*`): Pointer to the packet to be destroyed and freed. Must not be null.
- **Return Value**:
  - None
- **Exceptions/Errors**:
  - Throws no exceptions
- **Example**:
```cpp
auto p = std::make_unique<packet>(packet_ptr::deleter);
p->~packet();
std::free(p.get());
```
- **Preconditions**: `p` must not be null
- **Postconditions**: The packet is destructed and memory is freed
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `create_packet()`, `packet_ptr`

## create_packet()

- **Signature**: `inline packet_ptr create_packet(int size)`
- **Description**: Creates a new packet with the specified size. The function allocates memory for the packet structure plus the required payload space.
- **Parameters**:
  - `size` (`int`): The size of the packet payload to allocate. Must be non-negative and within the range of `std::uint16_t`.
- **Return Value**:
  - `packet_ptr`: A unique pointer to the newly created packet
- **Exceptions/Errors**:
  - Throws `std::bad_alloc` if memory allocation fails
- **Example**:
```cpp
auto packet = create_packet(1500);
if (packet) {
    // Use the packet
}
```
- **Preconditions**: `size >= 0` and `size <= std::numeric_limits<std::uint16_t>::max()`
- **Postconditions**: Returns a valid packet pointer or throws an exception
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `operator()`, `packet_ptr`

## packet_slab

- **Signature**: `struct TORRENT_EXTRA_EXPORT packet_slab`
- **Description**: A slab allocator for packets of a specific size. This class manages a pool of pre-allocated packets of a fixed size, allowing for efficient allocation and deallocation.
- **Parameters**:
  - `alloc_size` (`int`): The size of packets to allocate
  - `limit` (`std::size_t`): Maximum number of packets to keep in the slab (default: 10)
- **Return Value**:
  - None (constructor)
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
packet_slab slab(1500, 5);
auto packet = slab.alloc();
```
- **Preconditions**: None
- **Postconditions**: A packet slab is created with the specified parameters
- **Thread Safety**: Not thread-safe (only used in single-threaded context)
- **Complexity**: O(1)
- **See Also**: `alloc()`, `try_push_back()`

## try_push_back()

- **Signature**: `void try_push_back(packet_ptr &p)`
- **Description**: Attempts to add a packet to the slab's storage if there's room available. This function is used to recycle packets back to the pool.
- **Parameters**:
  - `p` (`packet_ptr &`): The packet to add to the slab. The packet will be moved into the slab.
- **Return Value**:
  - None
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
packet_slab slab(1500);
auto packet = create_packet(1500);
// ... use packet ...
slab.try_push_back(packet);
```
- **Preconditions**: `p` must be a valid packet pointer
- **Postconditions**: If there's space in the slab, the packet is added to the storage
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `alloc()`, `decay()`

## alloc()

- **Signature**: `packet_ptr alloc()`
- **Description**: Allocates a packet from the slab. If the slab has available packets, it returns one from the pool; otherwise, it creates a new packet.
- **Parameters**:
  - None
- **Return Value**:
  - `packet_ptr`: A unique pointer to the allocated packet
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
packet_slab slab(1500);
auto packet = slab.alloc();
if (packet) {
    // Use the packet
}
```
- **Preconditions**: None
- **Postconditions**: Returns a valid packet pointer
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `try_push_back()`, `create_packet()`

## decay()

- **Signature**: `void decay()`
- **Description**: Removes the last packet from the slab's storage. This function is used to reduce the number of packets in the slab.
- **Parameters**:
  - None
- **Return Value**:
  - None
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
packet_slab slab(1500);
auto packet = slab.alloc();
// ... use packet ...
slab.decay();
```
- **Preconditions**: None
- **Postconditions**: The last packet is removed from the slab's storage
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `try_push_back()`, `alloc()`

## packet_pool

- **Signature**: `struct TORRENT_EXTRA_EXPORT packet_pool : private single_threaded`
- **Description**: A packet pool that manages multiple slab allocators for different packet sizes. This class provides a single interface for allocating and releasing packets of various sizes.
- **Parameters**:
  - None
- **Return Value**:
  - None (constructor)
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
packet_pool pool;
auto packet = pool.acquire(1500);
// ... use packet ...
pool.release(packet);
```
- **Preconditions**: None
- **Postconditions**: A packet pool is created with the specified parameters
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `acquire()`, `release()`

## acquire()

- **Signature**: `packet_ptr acquire(int const allocate)`
- **Description**: Acquires a packet of the specified size from the packet pool. This function ensures thread safety and validates the input parameters.
- **Parameters**:
  - `allocate` (`int const`): The size of the packet to acquire. Must be non-negative and within the range of `std::uint16_t`.
- **Return Value**:
  - `packet_ptr`: A unique pointer to the acquired packet
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
packet_pool pool;
auto packet = pool.acquire(1500);
if (packet) {
    // Use the packet
}
```
- **Preconditions**: `allocate >= 0` and `allocate <= std::numeric_limits<std::uint16_t>::max()`
- **Postconditions**: Returns a valid packet pointer
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `release()`, `alloc()`

## release()

- **Signature**: `void release(packet_ptr p)`
- **Description**: Releases a packet back to the appropriate slab in the packet pool. This function ensures the packet is returned to the correct slab based on its allocated size.
- **Parameters**:
  - `p` (`packet_ptr`): The packet to release. Can be null.
- **Return Value**:
  - None
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
packet_pool pool;
auto packet = pool.acquire(1500);
// ... use packet ...
pool.release(packet);
```
- **Preconditions**: `p` must be a valid packet pointer or null
- **Postconditions**: The packet is returned to the appropriate slab
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `acquire()`, `try_push_back()`

## decay()

- **Signature**: `void decay()`
- **Description**: Reduces the number of packets in all slabs by removing the last packet from each. This function is used to clean up the packet pool.
- **Parameters**:
  - None
- **Return Value**:
  - None
- **Exceptions/Errors**:
  - None
- **Example**:
```cpp
packet_pool pool;
// ... acquire and use packets ...
pool.decay();
```
- **Preconditions**: None
- **Postconditions**: The last packet is removed from each slab
- **Thread Safety**: Thread-safe
- **Complexity**: O(1)
- **See Also**: `decay()`, `release()`

