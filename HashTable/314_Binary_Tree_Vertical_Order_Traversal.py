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


def vertical_order_v1(root):
    """ If we look at a binary tree horizontally, each node can be aligned to a specific column, based on its relative
        offset to the root node of the tree.
        Let us assume that the root node has a column index of 0, then its left child node would have a column index
        of -1 and its right child node would have a column index of +1, and so on.
        Now if we put the nodes into a vertical dimension, each node would be assigned to a specific row based on its
        level (i.e. the vertical distance to the root node).
        Let us assume that the root node has a row index of 0, then both its child nodes would have the row index of 1.
        Given the above definitions, we can now formulate the problem as a task to order the nodes based on the
        2-dimensional coordinates that we defined above. More specifically, the nodes should be ordered by column
        first, and further the nodes on the same column should be ordered vertically based on their row indices.
        With the BFS traversal, we naturally can guarantee the vertical order of the visits, i.e. the nodes at higher
        levels (large row values) would get visited later than the ones at lower levels. However, we are still missing
        the horizontal order (the column order). To ensure this order, we need to do some additional processing during
        the BFS traversal.
        The idea is that we keep a hash table where we keep the node values grouped by the column index. The key in the
        hash table would be the column index, and the corresponding value would be a list which contains the values of
        all the nodes that share the same column index. In addition, the values in the corresponding list should be
        ordered by their row indices, which would be guaranteed by the BFS traversal as we mentioned before.
        At each iteration within the BFS, we pop out an element from the queue. The element consists of a node and its
        corresponding column index. If the node is not empty, we then populate the hash table with the value of the
        node. Subsequently, we then put its child nodes along with their respective column indices: (column - 1) and
        (column + 1) into the queue.
        During the BFS traversal, we could obtain the range of the column indices, i.e. with the variable of
        min_column and max_column. At the end of the BFS traversal, we would then walk through the column range
        [min_column, max_column] and retrieve the results accordingly.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    columns, queue = defaultdict(list), deque([(root, 0)])
    min_col, max_col = float('inf'), float('-inf')
    while queue:
        node, column = queue.popleft()
        min_col = min(min_col, column)
        max_col = max(max_col, column)
        columns[column].append(node.val)
        if node.left:
            queue.append((node.left, column - 1))
        if node.right:
            queue.append((node.right, column + 1))
    return [columns[i] for i in range(min_col, max_col + 1)]


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
        self.assertTrue(self.result, vertical_order_v1(self.root))


if __name__ == '__main__':
    unittest.main()
