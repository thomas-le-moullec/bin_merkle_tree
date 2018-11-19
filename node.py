class Node:
    def __init__(self, parent_a, parent_b, hash_value):
        self.parent_a = parent_a
        self.parent_b = parent_b
        self.hash_value = hash_value
        if parent_b is None or parent_a is None:
            self.height = 0
        else:
            if parent_b.height != parent_a.height:
                raise ValueError("Parents do not have the same height !")
            self.height = parent_a.height + 1
        self.child = None

