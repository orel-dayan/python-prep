# a & b        # AND  - masking: which bits are set in both
# a | b        # OR   - setting bits
# a ^ b        # XOR  - toggling, and simple checksums
# ~a           # NOT
# a << 2       # shift left  = multiply by 4
# a >> 2       # shift right = divide by 4

# # Common patterns
# value & 0xFF              # keep only the low byte
# value & (1 << 3)          # is bit 3 set?
# value | (1 << 3)          # set bit 3
# value & ~(1 << 3)         # clear bit 3
# value ^ (1 << 3)          # toggle bit 3
# (value >> 4) & 0x0F       # extract bits 4-7

# bin(0b1010 & 0b0110)      # '0b10'
# format(value, "08b")      # '00001010' - padded binary string

def xor_checksum(data: bytes) -> int:
    """Compute a simple XOR checksum of the input data."""
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

# def verify_checksum(data: bytes, checksum: int) -> bool:
#     """Verify that the XOR checksum of the data matches the provided checksum."""
#     return xor_checksum(data) == checksum

def verify(frame: bytes) -> bool:
    """Verify that the last byte of the frame is a valid XOR checksum of the preceding bytes."""
    return xor_checksum(frame[:-1]) == frame[-1] #xor checksum of all but last byte should equal last byte

import struct


# pack value into a single byte
def pack_byte(value: int) -> bytes:
    """Pack an integer value into a single byte."""
    return struct.pack('B', value)

# pack: values -> bytes
data = struct.pack(">HBI", 1024, 5, 999999)     # 2+1+4 = 7 bytes
print(data)  # b'\x04\x00\x05\x00\x0fB@'

# unpack: bytes -> tuple of values
msg_id, status, timestamp = struct.unpack(">HBI", data)
print(msg_id, status, timestamp)  # 1024 5 999999

MESSAGE_FORMAT = ">HBI"
struct.calcsize(MESSAGE_FORMAT)  # 7 - how many bytes this format needs
print(struct.calcsize(MESSAGE_FORMAT))  # 7