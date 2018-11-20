import unittest
import hashlib
import merkle_tree
from encryption import Encode

ZERO_DATA = []
ONE_DATA = ["Hello"]
TWO_DATA = ["Hello", "World"]
THREE_DATA = ["Hello", "World", "Nice"]
SIX_DATA = ["Hello", "World", "Nice", "To", "Meet", "You"]
SEVEN_DATA = ["Hello", "World", "Nice", "To", "Meet", "You", "Friend"]


class MerkleTreeTests(unittest.TestCase):

    def test_empty_data_error(self):
        with self.assertRaises(Exception) as cm:
            tree = merkle_tree.MT(ZERO_DATA)

    def test_one_elem_valid(self):
        mt = merkle_tree.MT(ONE_DATA)
        expected_digest = Encode.sha256(ONE_DATA[0])
        self.assertTrue(mt.merkle_proof(expected_digest, []))
        self.assertEqual(0, mt.max_height)
        self.assertEqual(mt.digest, expected_digest)

    def test_two_element_valid(self):
        mt = merkle_tree.MT(TWO_DATA)
        expected_digest = Encode.sha256((Encode.sha256(TWO_DATA[0]) +
                                         Encode.sha256(TWO_DATA[1])))
        self.assertEqual(expected_digest, mt.digest)
        self.assertEqual(1, mt.max_height)
        self.assertEqual(3, len(mt.nodes.keys()))

    def test_three_element_valid(self):
        mt = merkle_tree.MT(THREE_DATA)
        expected_digest = Encode.sha256((Encode.sha256(THREE_DATA[0]) +
                                         Encode.sha256(Encode.sha256(THREE_DATA[1]) +
                                                       Encode.sha256(THREE_DATA[2]))))
        self.assertEqual(expected_digest, mt.digest)
        self.assertEqual(2, mt.max_height)
        self.assertEqual(5, len(mt.nodes.keys()))

    def test_six_elements_valid(self):
        mt = merkle_tree.MT(SIX_DATA)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[3], [list_nodes[10], list_nodes[9], list_nodes[2], list_nodes[4]]))
        self.assertEqual(3, mt.max_height)
        self.assertEqual(11, len(mt.nodes.keys()))

    def test_seven_elements_valid(self):
        mt = merkle_tree.MT(SEVEN_DATA)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[0], [list_nodes[12], list_nodes[11], list_nodes[5], list_nodes[1]]))
        self.assertEqual(3, mt.max_height)
        self.assertEqual(13, len(mt.nodes.keys()))

    def test_three_elements_merkle_proof(self):
        mt = merkle_tree.MT(THREE_DATA)
        self.assertTrue(mt.merkle_proof(Encode.sha256(THREE_DATA[2]), [Encode.sha256(THREE_DATA[0]),
                                                                       Encode.sha256(THREE_DATA[1])]))

    def test_six_elements_merkle_proof(self):
        mt = merkle_tree.MT(SIX_DATA)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[3], [list_nodes[10], list_nodes[9], list_nodes[2], list_nodes[4]]))

    def test_seven_elements_merkle_proof(self):
        mt = merkle_tree.MT(SEVEN_DATA)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[0], [list_nodes[12], list_nodes[11], list_nodes[5], list_nodes[1]]))


if __name__ == "__main__":
    unittest.main()
