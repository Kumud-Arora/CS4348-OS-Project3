# CS4348 OS Project 3

# May 9th - 7:45 PM

Reading project description rn...

# May 9th - 7:50 PM

So basically the project is implementing a disk based b-tree stored in fixed-size blocks. These are some of the requirements:
- 512 byte blocks
- 8 byte big endian ints
- b-tree min degree 10
- file header with a magic number
- node serialization/ deserialization
- command line interface

# May 9th - 8:11 PM

Implemted BTreeNode structure and serialization logic. Node format follows project specification. Implemented serialization and deserialization to conver nodes b/w memory and raw 512-byte blocks. Also added helper functions for converting integers to/ from 8-byte big endian format. 

# May 9th - 8:21 PM

Implemeneted the BTreeFile manager class. Added the following:
- header loading
- header writing
- node allocation
- disk block reading
- disk block writing
