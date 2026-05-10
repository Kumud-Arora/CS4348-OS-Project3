# CS4348-OS-Project3

## Overview:
This project implements a disk-based B-tree index file manager. The program allows users to create, insert, search, and traverse index files stored in a binary format. The biggest challenge was implementing the B-tree insertion and node splitting logic while keeping at most 3 nodes in memory at a time.

## Data Structure:
The index file is divided into 512-byte blocks. The first block is the header and each subsequent block stores a B-tree node. The B-tree has a minimal degree of 10, giving each node up to 19 keys and 20 child pointers.

## File Format:
### Header Block
- Magic number "4348PRJ3"
- Root block ID
- Next free block ID

### Node Block
- Block ID and parent ID
- Number of keys
- 19 keys and 19 values (8 bytes each, big-endian)
- 20 child pointers

## Commands:
- create -> Creates a new index file
- insert -> Inserts a key/value pair into the B-tree
- search -> Searches for a key and prints the key/value pair if found
- print -> Prints all key/value pairs in sorted order
- load -> Loads key/value pairs from a CSV file
- extract -> Saves all key/value pairs to a CSV file

## Files:
- project3.py -> Full implementation of the B-tree index manager

## Challenges Encountered:
The hardest part was correctly implementing node splitting during insertion while maintaining proper key ordering and child pointers. Another challenge was implementing iterative traversal using parent IDs to walk back up the tree instead of recursion, in order to satisfy the 3-node memory requirement.

## Conclusion:
This program successfully implements a disk-based B-tree that supports insertion, search, and traversal while keeping memory usage minimal.

## How to run:
```bash
python3 project3.py create <file>
python3 project3.py insert <file> <key> <value>
python3 project3.py search <file> <key>
python3 project3.py print <file>
python3 project3.py load <file> <csvfile>
python3 project3.py extract <file> <csvfile>
```

Also read devlog.md for a better understanding of the project
