from app.simulator.core import direct_map, fully_associative, set_associative
from app.simulator.utils import log2_int, hex_to_dec

def test_utils():
    assert log2_int(4) == 2
    assert log2_int(1024) == 10
    assert hex_to_dec("1F") == 31
    assert hex_to_dec("000a") == 10

def test_direct_map():
    addresses = ["0000", "0010", "0000", "0010", "001F"]
    res = direct_map(1, 16, addresses)
    # Block size 16 = 4 offset bits.
    # 0000 -> dec 0 -> index 0, tag 0. (Miss)
    # 0010 -> dec 16 -> index 1, tag 0. (Miss)
    # 0000 -> dec 0 -> index 0, tag 0. (Hit)
    # 0010 -> dec 16 -> index 1, tag 0. (Hit)
    # 001F -> dec 31 -> index 1, tag 0. (Hit) - offset 15
    assert res["hits"] == 3
    assert res["misses"] == 2

def test_fully_associative():
    addresses = ["0000", "0200", "0400", "0000"]
    res = fully_associative(1, 512, addresses)
    # Cache 1KB, Block 512B -> 2 blocks.
    # 0000 -> dec 0 -> tag 0 (Miss)
    # 0200 -> dec 512 -> tag 1 (Miss)
    # 0400 -> dec 1024 -> tag 2 (Miss, LRU kicks out tag 0)
    # 0000 -> dec 0 -> tag 0 (Miss, kicks out tag 1)
    assert res["hits"] == 0
    assert res["misses"] == 4
    
    addresses_hit = ["0000", "0200", "0000"]
    res_hit = fully_associative(1, 512, addresses_hit)
    assert res_hit["hits"] == 1
    assert res_hit["misses"] == 2

def test_set_associative():
    addresses = ["0000", "0200", "0400", "0000"]
    res = set_associative(1, 256, 2, addresses)
    # Cache 1KB, Block 256B, 2 Sets -> 4 blocks -> 2 blocks per set.
    # offset_bits = 8, index_bits = 1
    # 0000 -> dec 0, index 0, tag 0 (Miss)
    # 0200 -> dec 512, index 0, tag 1 (Miss)
    # 0400 -> dec 1024, index 0, tag 2 (Miss, LRU kicks out tag 0 in set 0)
    # 0000 -> dec 0, index 0, tag 0 (Miss)
    assert res["hits"] == 0
    assert res["misses"] == 4
