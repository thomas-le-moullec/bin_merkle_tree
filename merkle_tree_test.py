import unittest
import hashlib
import merkle_tree

ZERO_DATA = []
ONE_DATA = ["Hello"]
TWO_DATA = ["Hello", "World"]
THREE_DATA = ["Hello", "World", "Nice"]
SIX_DATA = ["Hello", "World", "Nice", "To", "Meet", "You"]
SEVEN_DATA = ["Hello", "World", "Nice", "To", "Meet", "You", "Friend"]


class MerkleTreeTests(unittest.TestCase):

    def test_three_element_valid(self):
        pass

    def test_seven_elements_valid(self):
        mt = merkle_tree.MT(SEVEN_DATA)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[0], [list_nodes[12], list_nodes[11], list_nodes[5], list_nodes[1]]))


if __name__ == "__main__":
    unittest.main()
