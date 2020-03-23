""" Given a binary tree, return the vertical order traversal of its nodes' values. (ie, from top to bottom, column by
column).
If two nodes are in the same row and column, the order should be from left to right. """

from collections import defaultdict, deque
import unittest2 as unittest


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def vertical_order(root):
    """ Give the root a column index of 0. For the left node, set its index to (col - 1), and for the right node set
        its index to (col + 1). We use a queue to loop through all the nodes in the tree in a BFS manner.
        Set the column as a key of the hash map and append the node value to the list of values for that column.
        We also keep track of min and max indices. Finally, we retrieve the results from the hash map by looping
        through the indices in sorted order from min index to max index.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    min_col = max_col = 0
    cols, queue = defaultdict(list), deque([(root, 0)])
    while queue:
        node, col = queue.popleft()
        cols[col].append(node.val)
        if node.left:
            queue.append((node.left, col - 1))
            min_col = min(min_col, col - 1)
        if node.right:
            queue.append((node.right, col + 1))
            max_col = max(max_col, col + 1)
    return [cols[i] for i in range(min_col, max_col + 1)]


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(8)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(0)
    root.right.left = TreeNode(1)
    root.right.right = TreeNode(7)
    result = [[4], [9], [3, 0, 1], [8], [7]]

    def test_vertical_order(self):
        self.assertTrue(self.result, vertical_order(self.root))


if __name__ == '__main__':
    unittest.main()
