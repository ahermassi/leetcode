""" Given a binary tree, write a function to get the maximum width of the given tree. The width of a tree is the
maximum width among all levels. The binary tree has the same structure as a full binary tree, but some nodes are null.
The width of one level is defined as the length between the end-nodes (the leftmost and right most non-null nodes in
the level, where the null nodes between the end-nodes are also counted into the length calculation. """

from collections import deque


def width_of_binary_tree_v1(root):
    """ We know that a binary tree can be represented by an array (assume the root begins from the position with index
        0 in the array). If the index of a node is i, the indices of its two children are 2 * i and 2 * i + 1.
        The idea is to record the the indices of each node in each level. This makes it so that when we look at the
        position values L and R of two nodes with the same depth, the width will be (R - L + 1).
        Traverse the tree in breadth-first order, keeping track of each node's position. For each depth, the first node
        reached is the left-most, while the last node reached is the right-most.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return 0
    queue, res = deque([(root, 0)]), 0
    while queue:
        res = max(res, queue[-1][1] - queue[0][1] + 1)  # We directly access the positions of first and last nodes
        n = len(queue)
        for _ in range(n):
            node, position = queue.popleft()
            if node.left:
                queue.append((node.left, 2 * position))
            if node.right:
                queue.append((node.right, 2 * position + 1))
    return res

