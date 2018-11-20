import hashlib
import math
from encryption import Encode

from node import Node


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
            print("Number of leaves to insert in the Tree:" + str(len(self.leaves)))
            self.build_tree()

    def __add_leaves(self, items):
        for item in items:
            self.leaves.append(Node(None, None, Encode.sha256(item)))

    def build_tree(self):
        # TODO: Split in submethods
        # TODO: Allow the three updates without building everything
        stack = []
        # Condition for solo node, otherwise the loop below will run forever because we need a pair
        if len(self.leaves) == 1:
            solo_node = self.leaves.pop()
            self.digest = solo_node.hash_value
            self.nodes[solo_node.hash_value] = solo_node
        while self.digest is None:
            if len(stack) >= 2 and stack[-1].height == stack[-2].height:
                # Get the two parents : Two last nodes on the same level / same height
                parent_a = stack.pop()
                parent_b = stack.pop()
                # Calculate the Hash value of the child with the parents hashes

                child_hash = Encode.sha256(parent_a.hash_value + parent_b.hash_value)
                print("Child Hash :"+child_hash+ " parent_a: "+str(parent_a.hash_value)+
                      "parent_b: "+str(parent_b.hash_value))
                # Inserting of the new Node as a child of the two parents
                child = Node(parent_a, parent_b, child_hash)
                self.nodes[child_hash] = child
                parent_a.child = child
                parent_b.child = child
                if child.height == self.max_height:
                    self.digest = child.hash_value
                stack.append(child)
            # Push a future parent in the stack
            elif len(self.leaves) > 0:
                leaf = self.leaves.pop()
                self.nodes[leaf.hash_value] = leaf
                stack.append(leaf)
            # Promote a node to find a pair and balance the three
            else:
                stack[-1].height += 1
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

    def merkle_proof(self, hash_to_check, proof_hashes):

        # TODO: Order the proof_hashes by height ?

        # The following steps can be skipped in the recursive calls
        # Tree not Built
        if not self.digest:
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
        if pair.child.parent_a.hash_value == hash_to_check:
            hash_next_height = Encode.sha256(hash_to_check + pair_hash)
        elif pair.child.parent_b.hash_value == hash_to_check:
            hash_next_height = Encode.sha256(pair_hash + hash_to_check)
        else:
            return False
        if pair.child.hash_value != self.nodes[hash_to_check].child.hash_value \
                or pair.child.hash_value != hash_next_height:
            return False
        if hash_next_height == self.digest:
            return True
        return self.merkle_proof(hash_next_height, proof_hashes)
