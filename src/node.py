class Node:
    def __init__(self, parent_a, parent_b, hash_value):
        self.parent_a = parent_a
        self.parent_b = parent_b
        self.hash_value = hash_value
        if parent_b is None or parent_a is None:
            self._height = 0
        else:
            if parent_b.height != parent_a.height:
                raise ValueError("Parents do not have the same height !")
            self._height = parent_a.height + 1
        self.child = None

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        if height < 0:
            raise Exception("Attempt to set height < 0.")
        self._height = height


