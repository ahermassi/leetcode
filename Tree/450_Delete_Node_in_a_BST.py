""" Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the root node
reference (possibly updated) of the BST.
Basically, the deletion can be divided into two stages:
    Search for a node to remove.
    If the node is found, delete the node.
Note: Time complexity should be O(height of tree). """


def delete_node(root, key):
    """ There are three possible situations here:
            1- Node is a leaf, and one could delete it straightforward : node = null.
            2- Node is not a leaf and has a right child. Then the node could be replaced by its successor which is
               somewhere lower in the right subtree. Then we could proceed down recursively to delete the successor.
            3- Node is not a leaf, has no right child and has a left child. The node could be replaced by its
               predecessor and then we could proceed down recursively to delete the predecessor.
    Time complexity: (logN), during the algorithm execution we go down the tree all the time - on the left or on the
    right, first to search the node to delete (O(H1)) and then to actually delete it. H1 is a tree height from the root
    to the node to delete. Delete process takes O(H2), where H2 is a tree height from the root to delete to the leafs.
    That in total results in O(H1 + H2) = O(H), where H is a tree height, equal to logN in the case of the balanced tree
    Space complexity: O(logN) to keep the recursion stack
    """
    if not root:
        return None
    # We always want to delete the node when it's the root of a subtree, so we handle left or right according to the val
    if root.val < key:
        root.right = delete_node(root.right, key)
    elif root.val > key:
        root.left = delete_node(root.left, key)
    else:  # Now the key is the root of a subtree
        if not root.left and not root.right:  # The node is a leaf
            root = None
        elif root.right:  # The node is not a leaf and has a right child
            root.val = successor(root)
            root.right = delete_node(root.right, root.val)
        else:  # The node is not a leaf, has no right child, and has a left child
            root.val = predecessor(root)
            root.left = delete_node(root.left, root.val)
        return root
    return root

# Utility functions


def successor(root):
    """ Successor = "after node", i.e. the next node, or the smallest node after the current one.
        It's also the next node in the in-order traversal.
        Successor == one step right and then left as you can
    """
    root = root.right
    while root.left:
        root = root.left
    return root


def predecessor(root):
    """ Predecessor = "before node", i.e. the previous node, or the largest node before the current one.
        It's also the previous node in the in-order traversal.
        Predecessor == one step left and then right as you can
    """
    root = root.left
    while root.right:
        root = root.right
    return root
