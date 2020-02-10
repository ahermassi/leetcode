""" Given a node in a binary search tree, find the in-order successor of that node in the BST.
You will have direct access to the node but not to the root of the tree. Each node will have a reference to its parent
node. Could you solve it without looking up any of the node's values?
"""


def inorder_successor(node):
    """ Looking carefully at the structure of the tree, observe that if the given node has a nonempty right subtree,
        its successor must lie in that subtree, and the rest of the nodes are immaterial. Furthermore, when a node has
        a nonempty right subtree, its successor is the first node visited when performing an in-order traversal on that
        subtree. This node is the leftmost node in that subtree, and can be computed by following left children
        exclusively, stopping when there is no left child to continue from.
        The challenge comes when the given node does not have a right subtree. We can determine the next visited node
        by iteratively following parents, stopping when we move up from a left child.
        Note that we may reach the root without ever moving up from a left child. This happens when the given node is
        the last node visited in an in-order traversal, and hence has no successor.
            1- If the node has a right child, and hence its successor is somewhere lower in the tree. Go to the right
               once and then as many times to the left as you could. Return the node you end up with.
            2- If the node has no right child, and hence its successor is somewhere upper in the tree. Go up till the
               node is left child of its parent. The answer is the parent.
    Time complexity: O(LogN) average case, O(N) worst case, since the number of edges followed cannot be more than the
    tree height
    Space complexity: O(1)
    """
    if node.right:
        node = node.right
        while node.left:
            node = node.left
        return node
    while node.parent and node == node.parent.right:  # Find the closest ancestor whose left subtree contains node
        node = node.parent
    # If we were allowed to use nodes' values:
    # while node.parent and node.parent.val < node.val:
    #   node = node.parent
    return node.parent
