""" Given a binary tree, find its maximum depth.
The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
    3
   / \
  9  20
    /  \
   15   7
return its depth = 3.
"""

from collections import deque
import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# Video explanation: https://www.youtube.com/watch?v=hTM3phVI6YQ


def max_depth_v1(root):
    """ Recursive DFS.

        By definition, the maximum depth of a binary tree is the maximum number of steps to reach a leaf node from the
        root node. From the definition, an intuitive idea would be to traverse the tree and record the maximum depth
        during the traversal.

        Let's have faith in recursion and assume that we are already given the maximum depth of root's left and right
        subtrees by recursion. So, to fnd the maximum depth of the binary tree, we will have to take out the maximum out
        of the left and right subtrees' depths and add 1 to that to account for the root's level.

    Time complexity: O(N), where N is the number of nodes
    Space complexity: in the worst case, the tree is completely unbalanced, e.g. each node has only left child node,
    the recursive call would occur N times (the height of the tree), therefore the storage to keep the call stack
    would be O(N). But in the best case (the tree is completely balanced), the height of the tree would be logN.
    Therefore, the space complexity in this case would be O(logN).
    """
    if not root:
        return 0
    left_max_depth = max_depth_v1(root.left)
    right_max_depth = max_depth_v1(root.right)
    return 1 + max(left_max_depth, right_max_depth)  # Add 1 to account for the root level


def max_depth_v2(root):
    """ Iterative DFS using a stack.

        We could also convert the above recursion into iteration, with the help of the stack data structure. Similar to
        the behavior of the function call stack, the stack data structure follows the pattern of LIFO
        (Last-In-First-Out), i.e. the last element that is added to a stack would come out first.

        The idea is to keep the next nodes to visit in a stack. Due to the LIFO behavior of the stack, we would get the
        order of visit same as the one in recursion.

        We start from a stack which contains the root node and the corresponding depth which is 1. Then we proceed to
        the iterations: pop the current node out of the stack and push the child nodes. The depth is incremented at each
        step.

    Time complexity: O(N)
    Space complexity: O(logN) best case, O(N) worst case
    """
    if not root:
        return 0
    res, stack = 0, [(root, 1)]
    while stack:
        node, depth = stack.pop()
        res = max(res, depth)
        stack.extend([(child, depth + 1) for child in (node.left, node.right) if child])
    return res


def max_depth_v3(root):
    """ BFS. We could also convert the recursion into iteration using a queue and perform a level-order traversal.

    Time complexity: O(N)
    Space complexity: O(N), since in the worst case the queue will contain all nodes in one level of the binary tree.
    For a full binary tree, the leaf level has ⌈N/2⌉= O(N) leaves.
    """
    if not root:
        return 0
    level, queue = 0, deque([root])
    while queue:  # At every iteration, queue holds the nodes of one level of the tree: there is no need to track depth
        n = len(queue)
        for _ in range(n):
            node = queue.popleft()
            queue.extend([child for child in (node.left, node.right) if child])
        level += 1
    return level


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    def test_max_depth(self):
        self.assertEqual(3, max_depth_v1(self.root))
        self.assertEqual(3, max_depth_v2(self.root))
        self.assertEqual(3, max_depth_v3(self.root))


if __name__ == '__main__':
    unittest.main()

