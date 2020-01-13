""" Given two binary trees, write a function to check if they are the same or not.
Two binary trees are considered the same if they are structurally identical and the nodes have the same value. """


def is_same_tree_v1(p, q):
    """ The simplest strategy here is to use recursion. Check if p and q nodes are not None, and their values are equal.
        If all checks are OK, do the same for the child nodes recursively.
    Time complexity: O(N), where N is a number of nodes in the tree, since we visit each node exactly once
    Space complexity: O(logN), in the best case of completely balanced tree and O(N) in the worst case of completely
    unbalanced tree, to keep a recursion stack
    """
    if not p and not q:
        return True
    if not p or not q:
        return False
    if p.val == q.val:
        return is_same_tree_v1(p.left, q.left) and is_same_tree_v1(p.right, q.right)
    return False

