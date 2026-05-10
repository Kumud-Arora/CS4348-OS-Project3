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

# May 9th - 8:26 PM

Implemented the create command. The create operation initializes a valid index file containing:
- correct magic number
- empty root pointer
- next block initialized to 1

# May 9th - 8:31 PM

Implemented recursive b-tree search. Basically the search logic compares keys within current node, recursively descends into child blocks, returns matching key/value pairs if any are found s

# May 9th - 8:55 PM

Implemented full b tree insertion and fixed some bugs. Hardest part was correctly handling node splitting while maintaining proper key ordering and the child pointers.

# May 9th - 9:40 PM

Implemented tree traversal functionality. And also implemented all the CLI commands (search, insert, print, load, extract)

# May 9th - 9:50 PM

Added main function

# May 9th - 10:03 PM

Debugged, testing now

# May 9th - 11:49 PM

Debugged insert_non_full because I'd found a bug while testing where the duplicate key check in the internal node branch was referencing the child variable before it was actually defined which was causing a NameError at runtime.


