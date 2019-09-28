""" Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the root node
reference (possibly updated) of the BST.
Basically, the deletion can be divided into two stages:
    Search for a node to remove.
    If the node is found, delete the node.
Note: Time complexity should be O(height of tree). """


def delete_node(root, key):
    """ Read the comments.
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
        if not root.left:  # If the subtree does not have a left child, we just return its right child to its father,
            # and they will be connected on the higher level recursion
            return root.right
        else:  # If it has a left child, we want to find the max val on the left subtree to replace the node we want
            # to delete
            temp = root.left
            while temp.right:
                temp = temp.right
            root.val = temp.val
            # Since we have replaced the node we want to delete with temp, now we don't want to keep temp on this
            # tree, so we just use our function to delete it. Pass the val of temp to the left subtree and repeat the
            # whole approach
            root.left = delete_node(root.left, temp.val)
    return root

