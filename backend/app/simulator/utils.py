import math

def log2_int(n: int) -> int:
    if n <= 0 or (n & (n - 1)) != 0:
        raise ValueError("Error: Block size must be a power of 2!")
    return int(math.log2(n))

def hex_to_dec(hex_str: str) -> int:
    return int(hex_str.strip(), 16)
