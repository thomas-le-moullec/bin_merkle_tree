import math
from src.encryption import Encode

from src.node import Node


class MT:
    def __init__(self, items):
        nbr_items = len(items)
        if nbr_items <= 0:
            raise ValueError("Need at least 1 item in the list to build a valid Merkle Tree. "
                             "Only 1 item merkle tree is handle in the build tree method")
        self.digest = None
        self.nodes = {}
        self.leaves = []
        self.__add_leaves(items)
        self.max_height = int(math.log(len(items), 2) + 0.5)
        self.is_built = False
        if self.leaves:
            # print("Number of leaves to insert in the Tree:" + str(len(self.leaves)))
            self.build_tree()

    def __add_leaves(self, items):
        for item in items:
            self.leaves.append(Node(None, None, Encode.sha256(item)))

    def add_data(self, data):
        self.__add_leaves(data)
        self.__update_tree()

    def __update_tree(self):
        # This method is used to update the merkle tree with a new list of values
        # If we want to balance the tree
        # 2 possibilities: current number of leaves = 2n + 1 or 2n
        # First case, we need to decrease the height of the unpair leaf to 0 and recalculate the branch to the root
        # Second case, we can just add the new leaves using the 'pair stack' and recalculate the branch
        pass

    def __create_child(self, parent_a, parent_b):
        child_hash = Encode.sha256(parent_a.hash_value + parent_b.hash_value)
        # print("Child Hash :" + child_hash + " parent_a: " + str(parent_a.hash_value) +
        #     "parent_b: " + str(parent_b.hash_value))
        # Inserting of the new Node as a child of the two parents
        child = Node(parent_a, parent_b, child_hash)
        self.nodes[child_hash] = child
        parent_a.child = child
        parent_b.child = child
        return child

    def __get_pair_hash_by_hash(self, hash_val):
        child = self.nodes[hash_val].child
        if hash_val == child.parent_a.hash_value:
            pair_hash = child.parent_b.hash_value
        elif hash_val == child.parent_b.hash_value:
            pair_hash = child.parent_a.hash_value
        else:
            raise ValueError("Hash value error in the Tree, check hash input.")
        return pair_hash

    def get_branch_by_hash(self, hash_val):
        if not self.is_built:
            raise Exception("Not Existing Merkle tree built")
        if hash_val not in self.nodes:
            raise ValueError("No such data found in the Merkle Tree")
        branch = []
        # Go to the next height until digest/root is reached
        while hash_val != self.digest:
            pair_hash = self.__get_pair_hash_by_hash(hash_val)
            branch.insert(0, pair_hash)
            hash_val = self.nodes[hash_val].child.hash_value
        branch.insert(0, hash_val)
        return branch

    def __create_one_leaf_tree(self):
        if len(self.leaves) == 1:
            solo_node = self.leaves.pop(0)
            self.digest = solo_node.hash_value
            self.nodes[solo_node.hash_value] = solo_node

    def __insert_pair_in_tree(self, stack):
        # Get the two parents : Two last nodes on the same level / same height
        parent_b = stack.pop(0)
        parent_a = stack.pop(0)
        # Calculate the Hash value of the child with the parents hashes
        child = self.__create_child(parent_a, parent_b)
        if child.height == self.max_height:
            self.digest = child.hash_value
        stack.insert(0, child)

    def __move_leaf_to_tree(self, stack):
        leaf = self.leaves.pop(0)
        self.nodes[leaf.hash_value] = leaf
        stack.insert(0, leaf)

    def build_tree(self):
        # TODO: Think about balancing the three with updates without building everything
        stack = []
        # Condition for solo node, otherwise the loop below will run forever because we need a pair
        self.__create_one_leaf_tree()
        while self.digest is None:
            if len(stack) >= 2 and stack[0].height == stack[1].height:
                self.__insert_pair_in_tree(stack)
            # Push a future parent in the stack
            elif len(self.leaves) > 0:
                self.__move_leaf_to_tree(stack)
            # Promote a node to find a pair and balance the three
            else:
                stack[0].height += 1  # To change
        self.is_built = True

    def print_merkle_tree(self):
        print("Number of nodes in the Tree:"+str(len(self.nodes)))
        print("Max height of the Tree:"+str(self.max_height)+" Number of nodes ")
        cnt = 0
        for key, node in self.nodes.items():
            print("Node number:" + str(cnt) + " | Height:" + str(node.height) + " Hash:" + key, end='', flush=True)
            if node.child:
                print(" Child:" + str(node.child.hash_value), end='', flush=True)
            if node.parent_a:
                print(" parent_a:" + str(node.parent_a.hash_value), end='', flush=True)
            if node.parent_b:
                print(" parent_b" + str(node.parent_b.hash_value), end='', flush=True)
            print("\n", end='', flush=True)
            cnt += 1

    def __generate_next_hash_by_hash(self, pair, given_hash):
        if pair.child.parent_a.hash_value == given_hash:
            hash_next_height = Encode.sha256(given_hash + pair.hash_value)
        elif pair.child.parent_b.hash_value == given_hash:
            hash_next_height = Encode.sha256(pair.hash_value + given_hash)
        else:
            return None
        return hash_next_height

    def merkle_proof(self, hash_to_check, proof_hashes):
        # print("Proof Hashes: "+str(proof_hashes))
        # print("Hash_to_check: "+str(hash_to_check))
        # TODO: Order the proof_hashes by height ?
        # The following steps can be skipped in the recursive calls
        # Tree not Built
        if not self.digest or not self.is_built:
            return False
        # Handle Single element Tree
        if self.max_height == 0 and hash_to_check == self.digest:
            return True
        if self.max_height == 0 and hash_to_check != self.digest:
            return False
        # Until here can be skipped in the recursive calls
        # Simplest error, not in the nodes list
        if hash_to_check not in self.nodes:
            return False
        # Get the closest / sibling hash to compute the next level
        pair_hash = proof_hashes.pop()
        pair = self.nodes[pair_hash]
        hash_next_height = self.__generate_next_hash_by_hash(pair, hash_to_check)
        if not hash_next_height:
            return False
        if pair.child.hash_value != self.nodes[hash_to_check].child.hash_value \
                or pair.child.hash_value != hash_next_height:
            return False
        if hash_next_height == self.digest:
            return True
        return self.merkle_proof(hash_next_height, proof_hashes)
