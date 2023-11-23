""" Given two binary trees, write a function to check if they are the same or not.
Two binary trees are considered the same if they are structurally identical and the nodes have the same value. """

from collections import deque


def is_same_tree_v1(p, q):
    """ The simplest strategy here is to use recursion.

         Check if p and q nodes are not None, and their values are equal. If all checks are OK, do the same for the
         child nodes recursively.

    Time complexity: O(N), where N is a number of nodes in the tree, since we visit each node exactly once
    Space complexity: O(logN) in the best case of completely balanced tree and O(N) in the worst case of skewed tree
    to keep the recursion stack
    """
    if not p and not q:
        return True
    if not p or not q:
        return False
    if p.val != q.val:
        return False
    return is_same_tree_v1(p.left, q.left) and is_same_tree_v1(p.right, q.right)


def is_same_tree_v2(p, q):
    """ Iterative solution using a stack.

    Time complexity: O(N)
    Space complexity: O(1) best case when both trees are skewed where in each iteration we both remove and add exactly
    two nodes to the stack, meaning that there would only ever be two nodes in the stack and the space utilisation
    remains constant throughout execution. O(N) worst case when the tree is balanced
    """
    stack = [(p, q)]
    while stack:
        a, b = stack.pop()
        if not a and not b:
            continue
        if not a or not b or a.val != b.val:
            return False
        stack.extend([(a.left, b.left), (a.right, b.right)])
    return True


def is_same_tree_v3(p, q):
    """ Iterative solution using a queue.

    Time complexity: O(N)
    Space complexity: O(1) best case when both trees are skewed where in each iteration we both remove and add exactly
    two nodes to the stack, meaning that there would only ever be two nodes in the stack and the space utilisation
    remains constant throughout execution. O(N) worst case when the tree is balanced where the last level contains half
    of the nodes, and all of those will be on a queue at the same time. A perfect tree with N nodes will have
    (N + 1) / 2 leaves
    """
    queue = deque([(p, q)])
    while queue:
        a, b = queue.popleft()
        if not a and not b:
            continue
        if not a or not b or a.val != b.val:
            return False
        queue.extend([(a.left, b.left), (a.right, b.right)])
    return True

