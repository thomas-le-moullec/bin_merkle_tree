import merkle_tree

if __name__ == '__main__':
    print("Running the Merkle Tree application")
    posts = ["Hello", "World", "Nice", "To", "Meet", "You", "Friend"]
    mt = merkle_tree.MT(posts)
    mt.print_merkle_tree()
    list_nodes = list(mt.nodes)
    if mt.merkle_proof(list_nodes[0], [list_nodes[12], list_nodes[11], list_nodes[5], list_nodes[1]]) is True:
        print("Hash:"+str(list_nodes[0])+ "is in the tree !")
    else:
        print("Hash:" + str(list_nodes[0]) + " is NOT in the tree !")
