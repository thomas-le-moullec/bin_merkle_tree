from src.encryption import Encode
from src import merkle_tree

if __name__ == '__main__':
    print("Running the Merkle Tree application")
    posts = ["Hello", "World", "Nice", "To", "Meet", "You", "Friend"]
    mt = merkle_tree.MT(posts)
    mt.print_merkle_tree()
    last_post = Encode.sha256(posts[-1])
    path = mt.get_branch_by_hash(last_post)
    print("Path:"+str(path))
    if mt.merkle_proof(last_post, path) is True:
        print("Hash:"+str(last_post)+ "is in the tree !")
    else:
        print("Hash:" + str(last_post) + " is NOT in the tree !")
