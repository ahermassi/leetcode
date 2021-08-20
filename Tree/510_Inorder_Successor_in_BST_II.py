""" Given a node in a binary search tree, find the in-order successor of that node in the BST.
You will have direct access to the node but not to the root of the tree. Each node will have a reference to its parent
node. Could you solve it without looking up any of the node's values?
"""


def inorder_successor_v1(node):
    """ Looking carefully at the structure of the tree, observe that if the given node has a nonempty right subtree,
        its successor must lie in that subtree, and the rest of the nodes are immaterial. Furthermore, the successor is
        the first node visited when performing an in-order traversal on that subtree. This node is the leftmost node in
        that subtree, and can be computed by following left children exclusively, stopping when there is no left child
        to continue from.
        The challenge arises when the given node does not have a right subtree. When the node has no right child, it
        means the node is the rightmost one in the subtree. We can determine its successor by iteratively following
        parents, stopping when we move up from a left child.
        Note that we may reach the root without ever moving up from a left child. This happens when the given node is
        the last node visited in an in-order traversal, and hence has no successor.
            1- If the node has a right child, its successor is somewhere lower in the tree. Go to the right once and
               then as many times to the left as you could. Return the node you end up with.
            2- If the node has no right child, its successor is somewhere upper in the tree. Go up till the node is
               left child of its parent. The answer is the parent.
        The logic behind following parent pointers has two pieces to it:
            - The right child of the parent is always greater than parent
            - A node in the left subtree of a parent is smaller than the parent
        If the node of interest (X) is the right child of parent (Y) we know that X.val > Y.val
        If node Z is the left child of node W we know that Z.val < W.val also W.val > X.val is X is in the left subtree
        of W.
    Time complexity: O(LogN) average case, O(N) worst case, since the number of edges followed cannot be more than the
    tree height
    Space complexity: O(1)
    """
    if node.right:
        node = node.right
        while node.left:
            node = node.left
        return node
    while node.parent and node == node.parent.right:  # Find the closest ancestor such as the node is its left child
        node = node.parent
    # If we were allowed to use nodes' values:
    # while node.parent and node.parent.val < node.val:
    #   node = node.parent
    return node.parent


def inorder_successor_v2(node):
    """ A slightly different way of writing the same algorithm.
    Time complexity: O(logN) average case, O(N) worst case
    Space complexity: O(1)
    """
    if node.right:
        node = node.right
        while node.left:
            node = node.left
        return node
    while node.parent:
        if node == node.parent.left:
            return node.parent
        node = node.parent
    return None
