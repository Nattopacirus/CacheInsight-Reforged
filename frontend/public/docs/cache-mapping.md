# Cache Mapping Methods

A cache mapping policy dictates how main memory addresses are mapped to cache locations. 
There are three main types of cache mapping techniques:

## 1. Direct-Mapped Cache
Every block in main memory has exactly one possible location in the cache. 
- **Advantage**: Simple and fast to check.
- **Disadvantage**: High conflict miss rate if two variables map to the same block.

## 2. Fully Associative Cache
A block in main memory can be placed in *any* location in the cache.
- **Advantage**: Lowest conflict miss rate.
- **Disadvantage**: Slow and expensive, as all tags must be compared simultaneously.

## 3. Set-Associative Cache
A compromise between Direct and Fully Associative. The cache is divided into *sets*, and each set contains *N* blocks (N-way). A memory block maps to a specific set, but can be placed in any of the *N* blocks within that set.
- **Advantage**: Good balance of speed and miss rate.
- **Disadvantage**: More complex replacement policy (e.g., LRU) needed within each set.
