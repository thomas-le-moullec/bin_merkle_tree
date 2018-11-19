import hashlib
import math

from node import Node


class MT:
    def __init__(self, items):
        nbr_items = len(items)
        if nbr_items <= 0:
            raise ValueError("Need at least 1 item in the list to build a valid Merkle Tree. "
                             "Only 1 item merkle tree is handle in the build tree method")
        self.root_hash = None
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
            self.leaves.append(Node(None, None, hashlib.sha256(item.encode()).hexdigest()))

    def build_tree(self):
        stack = []
        # Condition for solo node, otherwise the loop below will run forever because we need a pair
        if len(self.leaves) == 1:
            solo_node = self.leaves.pop()
            self.root_hash = solo_node.hash_value
            self.nodes[solo_node.hash_value] = solo_node
        while self.root_hash is None:
            if len(stack) >= 2 and stack[-1].height == stack[-2].height:
                # Get the two parents : Two last nodes on the same level / same height
                parent_a = stack.pop()
                parent_b = stack.pop()
                # Calculate the Hash value of the child with the parents hashes

                child_hash = hashlib.sha256(parent_a.hash_value.encode() + parent_b.hash_value.encode()).hexdigest()
                # Inserting of the new Node as a child of the two parents
                child = Node(parent_a, parent_b, child_hash)
                self.nodes[child_hash] = child
                parent_a.child = child
                parent_b.child = child
                if child.height == self.max_height:
                    self.root_hash = child.hash_value
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

    def merkle_proof(self):
        pass
