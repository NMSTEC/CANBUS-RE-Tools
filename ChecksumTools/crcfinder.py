import sys
import argparse
from typing import List, Tuple


def crc(data: List[int], len_: int, start_val: int, poly: int) -> int:
    crc_val = start_val
    for i in range(len_):
        crc_val ^= data[i]
        for _ in range(8):
            if (crc_val & 0x80) != 0:
                crc_val = ((crc_val << 1) ^ poly) & 0xFF
            else:
                crc_val <<= 1
                crc_val &= 0xFF
    return crc_val ^ 0xFF

def main(data: List[List[int]]):
    for poly in range(0x01, 0xFF):
        for start in range(0x00, 0x100):
            found = 0
            for pkt in data:
                if crc(pkt[:7], 7, start, poly) == pkt[7]:
                    found += 1
            if found >= 4:
                print(f"found = {found}! poly = {poly:02X} start = {start:02X}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CRC finder")
    parser.add_argument("data", nargs="+", help="Data packets (8-byte hex strings)")

    args = parser.parse_args()

    data = [list(bytes.fromhex(pkt)) for pkt in args.data]

    main(data)
#thank you Alexey Esaulenko for original program design in CAN decoders