import os
import sys
import csv

# constants
BLOCK_SIZE = 512
MAGIC = b"4348PRJ3"
MIN_DEGREE = 10
MAX_KEYS = 19
MAX_CHILDREN = 20


# integer to bytes and bytes to integer conversion functions
def int_to_bytes(n):
    return int(n).to_bytes(8, byteorder='big', signed=False)

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big', signed=False)

# B tree node class
class BTreeNode:
    def __init__(self, block_id=0, parent_id=0):
        self.block_id = block_id
        self.parent_id = parent_id
        self.num_keys = 0
        self.keys = [0] * MAX_KEYS
        self.values = [0] * MAX_KEYS
        self.children = [0] * MAX_CHILDREN

    def is_leaf(self):
        return all(child == 0 for child in self.children)
    
    # node serialization 
    def serialize(self):
        data = bytearray(BLOCK_SIZE)
        offset = 0
        data[offset:offset+8] = int_to_bytes(self.block_id)
        offset += 8
        data[offset:offset+8] = int_to_bytes(self.parent_id)
        offset += 8
        data[offset:offset+8] = int_to_bytes(self.num_keys)
        offset += 8

        for key in self.keys:
            data[offset:offset+8] = int_to_bytes(key)
            offset += 8

        for value in self.values:
            data[offset:offset+8] = int_to_bytes(value)
            offset += 8

        for child in self.children:
            data[offset:offset+8] = int_to_bytes(child)
            offset += 8
        
        return bytes(data)

    # node deserialization
    @staticmethod
    def deserialize(data):
        offset = 0

        block_id = bytes_to_int(data[offset:offset+8])
        offset += 8
        parent_id = bytes_to_int(data[offset:offset+8])
        offset += 8
        num_keys = bytes_to_int(data[offset:offset+8])
        offset += 8

        node = BTreeNode(block_id, parent_id)
        node.num_keys = num_keys

        for i in range(MAX_KEYS):
            node.keys[i] = bytes_to_int(data[offset:offset+8])
            offset += 8

        for i in range(MAX_KEYS):
            node.values[i] = bytes_to_int(data[offset:offset+8])
            offset += 8

        for i in range(MAX_CHILDREN):
            node.children[i] = bytes_to_int(data[offset:offset+8])
            offset += 8
        
        return node
    