import argparse
from typing import List
import numpy as np

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

def is_sum_checksum_valid(messages: List[List[int]], correlation_threshold: float) -> bool:
    for idx in [0, -1]:
        sums = [sum(message[:idx] + message[idx+1:]) % 256 for message in messages]
        checksums = [message[idx] for message in messages]
        stddev_sums = np.std(sums)
        stddev_checksums = np.std(checksums)
        if stddev_sums == 0 or stddev_checksums == 0:
            continue
        correlation = np.corrcoef(sums, checksums)[0, 1]
        if correlation > correlation_threshold:
            return True
    return False

def detect_checksum_type(messages: List[List[int]], threshold: float = 0.5, correlation_threshold: float = 0.9):
    total_messages = len(messages)
    crc_matches = 0
    if is_sum_checksum_valid(messages, correlation_threshold):
        return "Sum"
    for message in messages:
        data_len = len(message) - 1
        for poly in range(0x01, 0xFF):
            for start in range(0x00, 0x100):
                if crc(message[:data_len], data_len, start, poly) == message[-1]:
                    crc_matches += 1
    if crc_matches / total_messages > threshold:
        return "CRC"
    return "Unknown"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Checksum type detector for CAN bus messages")
    parser.add_argument("messages", nargs="+", help="CAN bus messages (AABBCCDDEEFF0011)")
    args = parser.parse_args()
    messages = [list(bytes.fromhex(msg)) for msg in args.messages]
    checksum_type = detect_checksum_type(messages)
    print(f"The detected checksum type is: {checksum_type}")
