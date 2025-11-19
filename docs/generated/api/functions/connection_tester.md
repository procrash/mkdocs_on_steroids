# Connection Tester API Documentation

## generate_block

- **Signature**: `void generate_block(span<std::uint32_t> buffer, piece_index_t const piece, int const offset)`
- **Description**: Fills a buffer with a pattern based on a piece index and offset. This function generates a block of data that can be used for testing or verification purposes. The pattern is created by combining the piece index and offset into a 32-bit value.
- **Parameters**:
  - `buffer` (span<std::uint32_t>): The buffer to fill with the generated pattern. This must be a valid span of 32-bit unsigned integers.
  - `piece` (piece_index_t const): The piece index to use in generating the pattern. This should be a valid piece index within the torrent's piece range.
  - `offset` (int const): The offset within the piece to use in generating the pattern. This should be a valid offset within the piece size.
- **Return Value**:
  - `void`: This function does not return a value.
- **Exceptions/Errors**:
  - This function does not throw exceptions.
  - It assumes that the input parameters are valid and that the buffer has sufficient capacity.
- **Example**:
```cpp
std::vector<std::uint32_t> buffer(1024);
piece_index_t piece = 5;
int offset = 0;
generate_block(buffer, piece, offset);
```
- **Preconditions**:
  - `buffer` must be a valid span of 32-bit