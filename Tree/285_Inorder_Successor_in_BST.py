""" Given a binary search tree and a node in it, find the in-order successor of that node in the BST.
The successor of a node p is the node with the smallest key greater than p.val. """


def inorder_successor_v1(root, p):
    """ Successor is the smallest node in the in-order traversal after the current one.
        There could be two situations :
            1- If the node has a right child, the successor is somewhere lower in the tree
            2- Otherwise, the successor is somewhere upper in the tree. There is no access to the parent nodes here,
               and hence we have to traverse the tree starting from the root and not from the node.
        If the node has a right child, go one step right and then left till you can. Return the successor.
        Otherwise, implement iterative in-order traversal. While there are still nodes in the tree or in the stack:
            - Go left till you can, adding nodes in stack.
            - Pop out the last node. If its predecessor is equal to p, return that last node. Otherwise, save that node
              to be the predecessor in the next turn of the loop.
            - Go one step right.
        The idea is to keep just one previous node during the in-order traversal. If that previous node is equal to p,
        then the current node is a successor of p.
    Time complexity: O(height(p)) in the best case when node p has a right child, O(logN) in the worst case of no right
    child (or O(N) if the tree is skewed)
    Space complexity: O(1) in the best case when node p has a right child, and up to O(logN) to keep the stack
    """
    if p.right:  # The successor is somewhere lower in the right subtree
        p = p.right
        while p.left:
            p = p.left
        return p
    stack, pre = [], None  # The successor is somewhere upper in the tree
    while stack or root:
        while root:
            stack.append(root)
            root = root.left
        node = stack.pop()
        if pre == p:
            return node
        pre = node
        root = node.right


