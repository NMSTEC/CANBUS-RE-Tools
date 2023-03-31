import sys

input_bytes = bytearray.fromhex(sys.argv[1])
checksum = bytearray.fromhex(sys.argv[2])
gayness = sum(input_bytes)
gayness += int.from_bytes(checksum, byteorder='big')
result = (gayness >> 8) + (gayness & 0xFF)
print(hex(result))