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

# B tree class
class BTreeFile:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            raise Exception("Index file does not exist")
        
        self.file = open(filename, 'r+b')
        self.load_header()

    def load_header(self):
        self.file.seek(0)
        data = self.file.read(BLOCK_SIZE)

        if data[0:8] != MAGIC:
            raise Exception("Invalid index file")
        
        self.root_id = bytes_to_int(data[8:16])
        self.next_block_id = bytes_to_int(data[16:24])

    def write_header(self):
        data = bytearray(BLOCK_SIZE)
        data[0:8] = MAGIC
        data[8:16] = int_to_bytes(self.root_id)
        data[16:24] = int_to_bytes(self.next_block_id)

        self.file.seek(0)
        self.file.write(data)
        self.file.flush()

    def read_node(self, block_id):
        self.file.seek(block_id * BLOCK_SIZE)
        data = self.file.read(BLOCK_SIZE)
        return BTreeNode.deserialize(data)
    
    def write_node(self, node):
        self.file.seek(node.block_id * BLOCK_SIZE)
        self.file.write(node.serialize())
        self.file.flush()

    def allocate_node(self, parent_id=0):
        node = BTreeNode(self.next_block_id, parent_id)
        self.next_block_id += 1
        self.write_header()
        return node

    def close(self):
        self.file.close()


    def search (self, key, block_id=None):
        if self.root_id == 0:
            return None
        
        if block_id is None:
            block_id = self.root_id
        
        node = self.read_node(block_id)
        i = 0

        while i < node.num_keys and key > node.keys[i]:
            i += 1

        if i < node.num_keys and key == node.keys[i]:
            return (node.keys[i], node.values[i])
        if node.is_leaf():
            return None
        
        child_id = node.children[i]
        if child_id == 0:
            return None
        return self.search(key, child_id)
    
    def split_child(self, parent, index, child):
        new_child = self.allocate_node(parent.block_id)
        new_child.num_keys = MIN_DEGREE - 1

        for j in range(MIN_DEGREE - 1):
            new_child.keys[j] = child.keys[j + MIN_DEGREE]
            new_child.values[j] = child.values[j + MIN_DEGREE]

        if not child.is_leaf():
            for j in range(MIN_DEGREE):
                new_child.children[j] = child.children[j + MIN_DEGREE]

        child.num_keys = MIN_DEGREE - 1

        for j in range(parent.num_keys, index, -1):
            parent.children[j + 1] = parent.children[j]

        
        parent.children[index + 1] = new_child.block_id
        
        for j in range(parent.num_keys - 1, index - 1, -1):
            parent.keys[j + 1] = parent.keys[j]
            parent.values[j + 1] = parent.values[j]


        parent.keys[index] = child.keys[MIN_DEGREE - 1]
        parent.values[index] = child.values[MIN_DEGREE - 1]
        
        parent.num_keys += 1

        self.write_node(child)
        self.write_node(new_child)
        self.write_node(parent)

    def insert_non_full(self, node, key, value):
        i = node.num_keys - 1

        if node.is_leaf():
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1

            node.keys[i + 1] = key
            node.values[i + 1] = value
            node.num_keys += 1
            self.write_node(node)

        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1

            i += 1

            child = self.read_node(node.children[i])

            if child.num_keys == MAX_KEYS:
                self.split_child(node, i, child)
                
                if key > node.keys[i]:
                    i += 1

                child = self.read_node(node.children[i])

            self.insert_non_full(child, key, value)

    def insert(self, key, value):
        if self.root_id == 0:
            root = self.allocate_node()
            root.num_keys = 1
            root.keys[0] = key
            root.values[0] = value
            self.root_id = root.block_id
            self.write_header()
            self.write_node(root)
            return 
        
        root = self.read_node(self.root_id)
        
        if root.num_keys == MAX_KEYS:
            new_root = self.allocate_node()
            new_root.children[0] = root.block_id
            root.parent_id = new_root.block_id
            self.write_node(root)
            self.split_child(new_root, 0, root)
            self.root_id = new_root.block_id
            self.write_header()
            self.insert_non_full(new_root, key, value)
        else:
            self.insert_non_full(root, key, value)
        


def create_index(filename):
    if os.path.exists(filename):
        print("File already exists")
        sys.exit(1)

    with open(filename, 'wb') as f:
        data = bytearray(BLOCK_SIZE)
        data[0:8] = MAGIC
        data[8:16] = int_to_bytes(0)  
        data[16:24] = int_to_bytes(1) 
        f.write(data)



