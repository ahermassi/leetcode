""" Given a binary tree, determine if it is a complete binary tree.
Definition of a complete binary tree from Wikipedia:
In a complete binary tree every level, except possibly the last, is completely filled, and all nodes in the last level
are as far left as possible. It can have between 1 and 2 ** h nodes inclusive at the last level h. """

from collections import deque
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_complete_tree_v1(root):
    """ Use BFS to do a level order traversal, add children to the BFS queue, until we meet the first empty node.
        For a complete binary tree, there should not be any node after we meet an empty one.
        It's using the key feature of level order traversal - from top to bottom and from left to right, so as soon as
        we see null node (previous level or last level), there should be no more non-null node as we continue the
        traversal.
    Time complexity: O(N), where N is the number of nodes in the tree
    Space complexity: O(N)
    """
    queue, i = [root], 0
    while queue[i]:  # Using an index-based stack to mimic the queue
        queue.extend([kid for kid in (queue[i].left, queue[i].right)])
        i += 1
    return not any(queue[i:])


def is_complete_tree_v2(root):
    """ Similar approach but with a different early termination.
        Perform a standard left-to-right BFS and keep a boolean flag 'end' that is set to True whenever we encounter
        the first null node. If the tree is complete, no non-null node should be met after 'end' is set to True. If
        otherwise, exit early and return False.
        node.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    queue = deque([root])
    end = False
    while queue:
        node = queue.popleft()
        if not node:  # This is the first time we meet a null node
            end = True
        elif end:  # The current node is not null but 'end' is already True: the tree is not complete
            return False
        else:
            queue.extend([kid for kid in (node.left, node.right)])
    return True


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)

    def test_is_complete_tree(self):
        self.assertTrue(is_complete_tree_v1(self.root))
        self.assertTrue(is_complete_tree_v2(self.root))


if __name__ == '__main__':
    unittest.main()