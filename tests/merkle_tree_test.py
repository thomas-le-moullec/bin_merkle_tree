import math
import unittest
from src import merkle_tree
from resources import data
from src.encryption import Encode
import random


class MerkleTreeTests(unittest.TestCase):

    def test_empty_data_error(self):
        with self.assertRaises(Exception) as cm:
            tree = merkle_tree.MT(data.ZERO_DATA)

    def test_one_elem_valid(self):
        mt = merkle_tree.MT(data.ONE_DATA)
        expected_digest = Encode.sha256(data.ONE_DATA[0])
        self.assertTrue(mt.merkle_proof(expected_digest, []))
        self.assertEqual(0, mt.max_height)
        self.assertEqual(mt.digest, expected_digest)

    def test_two_element_valid(self):
        mt = merkle_tree.MT(data.TWO_DATA)
        expected_digest = Encode.sha256((Encode.sha256(data.TWO_DATA[0]) +
                                         Encode.sha256(data.TWO_DATA[1])))
        self.assertEqual(expected_digest, mt.digest)
        self.assertEqual(1, mt.max_height)
        self.assertEqual(3, len(mt.nodes.keys()))

    def test_three_element_valid(self):
        mt = merkle_tree.MT(data.THREE_DATA)
        expected_digest = Encode.sha256((Encode.sha256(Encode.sha256(data.THREE_DATA[0]) +
                                                       Encode.sha256(data.THREE_DATA[1]))
                                         + Encode.sha256(data.THREE_DATA[2])))
        self.assertEqual(expected_digest, mt.digest)
        self.assertEqual(2, mt.max_height)
        self.assertEqual(5, len(mt.nodes.keys()))

    def test_six_elements_valid(self):
        mt = merkle_tree.MT(data.SIX_DATA)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[3], [list_nodes[10], list_nodes[9], list_nodes[2], list_nodes[4]]))
        self.assertEqual(3, mt.max_height)
        self.assertEqual(11, len(mt.nodes.keys()))

    def test_seven_elements_valid(self):
        mt = merkle_tree.MT(data.SEVEN_DATA)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[0], [list_nodes[12], list_nodes[11], list_nodes[5], list_nodes[1]]))
        self.assertEqual(3, mt.max_height)
        self.assertEqual(13, len(mt.nodes.keys()))

    def test_three_elements_merkle_proof(self):
        mt = merkle_tree.MT(data.THREE_DATA)
        last_post = Encode.sha256(data.THREE_DATA[-1])
        path = mt.get_branch_by_hash(last_post)
        self.assertTrue(mt.merkle_proof(Encode.sha256(data.THREE_DATA[2]),
                                        [Encode.sha256(Encode.sha256(data.THREE_DATA[0]) +
                                                       Encode.sha256(data.THREE_DATA[1]))]))
        self.assertTrue(mt.merkle_proof(last_post, path))

    def test_six_elements_merkle_proof(self):
        mt = merkle_tree.MT(data.SIX_DATA)
        post_valid_hash = Encode.sha256(data.SIX_DATA[3])
        path = mt.get_branch_by_hash(post_valid_hash)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[3], [list_nodes[10], list_nodes[9], list_nodes[2], list_nodes[4]]))
        # Correct case where the path is corresponding with the hash of the data
        self.assertTrue(mt.merkle_proof(post_valid_hash, path))
        path = mt.get_branch_by_hash(post_valid_hash)

        # Error case where the path is not corresponding with the hash of the data
        post_error_hash = Encode.sha256(data.SIX_DATA[1])
        self.assertFalse(mt.merkle_proof(post_error_hash, path))

    def test_seven_elements_merkle_proof(self):
        mt = merkle_tree.MT(data.SEVEN_DATA)
        list_nodes = list(mt.nodes)
        self.assertTrue(mt.merkle_proof(list_nodes[0], [list_nodes[12], list_nodes[11], list_nodes[5], list_nodes[1]]))

    def test_all_data_merkle_proof_and_valid_tree(self):
        for data_row in data.ALL_DATA:
            mt = merkle_tree.MT(data_row)
            secure_random = random.SystemRandom()
            post = Encode.sha256(secure_random.choice(data_row))
            path = mt.get_branch_by_hash(post)
            self.assertTrue(mt.merkle_proof(post, path))
            path = mt.get_branch_by_hash(post)
            false_post = "Not in the tree data"
            false_post = Encode.sha256(false_post)
            self.assertFalse(mt.merkle_proof(false_post, path))
            number_of_nodes = pow(2, math.log(len(data_row), 2) + 1) - 1
            self.assertEqual(round(number_of_nodes), len(mt.nodes))


if __name__ == "__main__":
    unittest.main()
