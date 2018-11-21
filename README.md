# bin_merkle_tree
Simple merkle tree implementation to bootstrap Authenticated Data Structure in Infnote  project


### Project structure:
* app.py offer a simple example of the implementation of the merkle tree.
* merkle_tree.py contains the entire logic of the merkle tree implementation
* node.py is the class defining each node of the merkle tree: Hash, parents, child
* encryption.py is a simple encapsulation of cryptography functions used for hash.

### Run the tests
In project root folder:
python -m unittest tests/merkle_tree_test.py
Currently 10 tests

### TO DO:
* Need to update the three

#### Rights and License:
GNU GENERAL PUBLIC LICENSE - Check LICENSE file