class HashTableEntry:
    """Represents a single entry within a hash table, to be used when handling collisions."""
    def __init__(self, key, value): # Constructor
        self.key = key
        self.value = value
        self.next = None  # Points to the next entry in case of a collision

class HashTable:
    """Creates a hash table to house hash table entries."""
    def __init__(self): # Constructor
        self.size = 40  # Fixed size for the table
        self.table = [None] * self.size  # Initialize table with empty buckets

    def hash_function(self, key):
        """Computes the index for a key using the modulo operation."""
        return hash(key) % self.size # Compute hash value. 

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table."""
        index = self.hash_function(key) # Use 'hash_function' with 'key' to compute index
        entry = self.table[index] # Retrieve entry from hash table
        if entry is None:  # If bucket is empty
            self.table[index] = HashTableEntry(key, value) # Create new 'HashTableEntry'
            return
        # Traverse the chain to find the right place to insert
        while entry.next is not None:  # When bucket is not empty, iterate through chain
            if entry.key == key: # If enry with same key is found
                entry.value = value  # Update existing entry
                return
            entry = entry.next # Move to next entry in chain
        entry.next = HashTableEntry(key, value) # Add new 'HashTableEntry' at end of chain

    def lookup(self, key):
        """Looks up the value associated with a key in the hash table."""
        index = self.hash_function(key) # Use 'hash_function' with 'key' to compute index
        entry = self.table[index] # Retrieve entry from hash table
        while entry is not None: # Iterate through chain as long as 'entry' is not 'None' in case of collision
            if entry.key == key: # Check if entry's key matches lookup key
                return entry.value # If match is found, return value
            entry = entry.next # Move to next entry in chain
        return None  # Key not found

    def delete(self, key):
        """Removes a key-value pair from the hash table."""
        index = self.hash_function(key) # Use 'hash_function' with 'key' to compute index
        entry = self.table[index] # Retrieve enry from hash table
        prev = None # Initialize previous node to 'None'
        while entry is not None: # Iterate through chain as long as 'entry' is not 'None'
            if entry.key == key: # Check if entry's key matches lookup key
                if prev is None: # If first in chain
                    self.table[index] = entry.next # Point to next node
                else: # If not the first in chain
                    prev.next = entry.next # Skips over current 'entry'
                return # Exits method
            prev = entry # Set up for next iteration
            entry = entry.next