from dataclasses import dataclass
from typing import List, Dict, Any, Callable, Optional
from .utils import log2_int, hex_to_dec

@dataclass
class CacheBlock:
    tag: int = 0
    valid: bool = False
    last_used: int = 0

def direct_map(cache_size_kb: int, block_size: int, addresses: List[str], progress_callback: Optional[Callable[[int, int], None]] = None) -> Dict[str, Any]:
    cache_size_bytes = cache_size_kb * 1024
    num_blocks = cache_size_bytes // block_size
    offset_bits = log2_int(block_size)
    index_bits = log2_int(num_blocks)

    cache = [CacheBlock(0, False, 0) for _ in range(num_blocks)]
    hits = 0
    misses = 0
    total_addresses = len(addresses)

    for i, addr_str in enumerate(addresses):
        address = hex_to_dec(addr_str)
        index = (address >> offset_bits) & (num_blocks - 1)
        tag = address >> (offset_bits + index_bits)

        hit = cache[index].valid and cache[index].tag == tag
        if hit:
            hits += 1
        else:
            misses += 1
            cache[index] = CacheBlock(tag=tag, valid=True, last_used=0)
            
        if progress_callback and (i + 1) % 10000 == 0:
            progress_callback(i + 1, total_addresses)

    total_accesses = hits + misses
    hit_rate = (hits / total_accesses * 100) if total_accesses > 0 else 0.0
    miss_rate = (misses / total_accesses * 100) if total_accesses > 0 else 0.0

    return {
        "hits": hits,
        "misses": misses,
        "hit_rate": hit_rate,
        "miss_rate": miss_rate
    }

def fully_associative(cache_size_kb: int, block_size: int, addresses: List[str], progress_callback: Optional[Callable[[int, int], None]] = None) -> Dict[str, Any]:
    cache_size_bytes = cache_size_kb * 1024
    num_blocks = cache_size_bytes // block_size
    offset_bits = log2_int(block_size)

    cache = [CacheBlock(0, False, 0) for _ in range(num_blocks)]
    hits = 0
    misses = 0
    global_time = 0
    total_addresses = len(addresses)

    for i, addr_str in enumerate(addresses):
        global_time += 1
        address = hex_to_dec(addr_str)
        tag = address >> offset_bits

        hit = False
        last_accessed = -1

        for j in range(num_blocks):
            if cache[j].valid and cache[j].tag == tag:
                hit = True
                last_accessed = j
                break

        if hit:
            hits += 1
            cache[last_accessed].last_used = global_time
        else:
            misses += 1
            lru_idx = 0
            min_time = cache[0].last_used

            for j in range(num_blocks):
                if not cache[j].valid:
                    lru_idx = j
                    break
                if cache[j].last_used < min_time:
                    min_time = cache[j].last_used
                    lru_idx = j

            last_accessed = lru_idx
            cache[last_accessed] = CacheBlock(tag=tag, valid=True, last_used=global_time)
            
        if progress_callback and (i + 1) % 10000 == 0:
            progress_callback(i + 1, total_addresses)

    total_accesses = hits + misses
    hit_rate = (hits / total_accesses * 100) if total_accesses > 0 else 0.0
    miss_rate = (misses / total_accesses * 100) if total_accesses > 0 else 0.0

    return {
        "hits": hits,
        "misses": misses,
        "hit_rate": hit_rate,
        "miss_rate": miss_rate
    }

def set_associative(cache_size_kb: int, block_size: int, sets: int, addresses: List[str], progress_callback: Optional[Callable[[int, int], None]] = None) -> Dict[str, Any]:
    cache_size_bytes = cache_size_kb * 1024
    blocks_per_set = cache_size_bytes // block_size // sets
    offset_bits = log2_int(block_size)
    index_bits = log2_int(sets)

    cache = [[CacheBlock(0, False, 0) for _ in range(blocks_per_set)] for _ in range(sets)]
    hits = 0
    misses = 0
    global_time = 0
    total_addresses = len(addresses)

    for i, addr_str in enumerate(addresses):
        global_time += 1
        address = hex_to_dec(addr_str)
        index = (address >> offset_bits) & (sets - 1)
        tag = address >> (offset_bits + index_bits)

        hit = False
        hit_block_idx = -1

        for j in range(blocks_per_set):
            if cache[index][j].valid and cache[index][j].tag == tag:
                hit = True
                hit_block_idx = j
                break

        if hit:
            hits += 1
            cache[index][hit_block_idx].last_used = global_time
        else:
            misses += 1
            lru_idx = 0
            min_time = cache[index][0].last_used

            for j in range(blocks_per_set):
                if not cache[index][j].valid:
                    lru_idx = j
                    break
                if cache[index][j].last_used < min_time:
                    min_time = cache[index][j].last_used
                    lru_idx = j

            cache[index][lru_idx] = CacheBlock(tag=tag, valid=True, last_used=global_time)
            
        if progress_callback and (i + 1) % 10000 == 0:
            progress_callback(i + 1, total_addresses)

    total_accesses = hits + misses
    hit_rate = (hits / total_accesses * 100) if total_accesses > 0 else 0.0
    miss_rate = (misses / total_accesses * 100) if total_accesses > 0 else 0.0

    return {
        "hits": hits,
        "misses": misses,
        "hit_rate": hit_rate,
        "miss_rate": miss_rate
    }
