import merkle_tree

if __name__ == '__main__':
    print("Running the Merkle Tree application")
    posts = ["Hello", "World", "Nice", "To", "Meet", "You"]
    mt = merkle_tree.MT(posts)
    mt.print_merkle_tree()
