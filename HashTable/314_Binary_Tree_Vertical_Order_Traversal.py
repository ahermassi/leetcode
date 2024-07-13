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
    """ We are asked to return the vertical order of a binary tree, which actually implies two sub-orders, where each
         node would have a 2-dimensional index (denoted as <column, row>)

         If we look at a binary tree horizontally, each node can be aligned to a specific column, based on its relative
         offset to the root node of the tree.
         Let us assume that the root node has a column index of 0, then its left child node would have a column index
         of -1 and its right child node would have a column index of +1, and so on.

         Now, if we put the nodes into a vertical dimension, each node would be assigned to a specific row based on its
         level (i.e. the vertical distance to the root node).
         Let us assume that the root node has a row index of 0, then both its child nodes would have the row index of 1.

         Given the above definitions, we can now formulate the problem as a task to order the nodes based on the
         2-dimensional coordinates that we defined above. More specifically, the nodes should be ordered by column
         first, and further the nodes on the same column should be ordered vertically based on their row indices.

         With the BFS traversal, we naturally can guarantee the vertical order of the visits, i.e. the nodes at higher
         levels (large row values) would get visited later than the ones at lower levels. However, we are still missing
         the horizontal order (the column order). To ensure this order, we need to do some additional processing during
         the BFS traversal.

         The idea is that we keep a hashmap where we keep the node values grouped by the column index. The key in the
         hashmap would be the column index, and the corresponding value would be a list which contains the values of
         all the nodes that share the same column index. In addition, the values in the corresponding list should be
         ordered by their row indices, which would be guaranteed by the BFS traversal as mentioned before.

         At each iteration within the BFS, we pop out an element from the queue. The element consists of a node and its
         corresponding column index. We then populate the hashmap with the value of the node. Subsequently, we then put
         its child nodes along with their respective column indices: (column - 1) and (column + 1) into the queue.

         At the end of the BFS traversal, we obtain a hashmap that contains the desired node values grouped by their
         column indices. For each group of values, they are further ordered by their row indices.

         Note that we only need to know the range of the column index (i.e. [min_column, max_column]). Then we can
         simply iterate through this range to generate the outputs without the need for sorting by column.

         Therefore, during the BFS traversal, we could obtain the range of the column indices, i.e. with the variable of
         min_column and max_column. At the end of the BFS traversal, we would then walk through the column range
         [min_column, max_column] and retrieve the results accordingly.

    Time complexity: O(N), we visit each node once and only once
    Space complexity: O(N), for the hashmap. Also, at any given moment, the queue would hold no more two levels of
    nodes. For a binary tree, the maximum number of nodes at a level would be (N+1)/2 which is also the number of leafs
    in a full binary tree. As a result, in the worst case, the queue would consume at most O((N+1)/2) = O(N) space.
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


def vertical_order_v2(root):
    """ Compared to the DFS traversal, the BFS traversal gives us a head start, since the nodes in higher rows would be
         visited later than the ones in the lower lows. As a result, we only need to focus on the column order.

         That being said, we could simply traverse the tree in any DFS order, then we sort the resulting list strictly
         based on two keys <column, row>, which would give us the same results as the BFS traversal.

         An important note is that two nodes might share the same <column, row>, in which case the order between these
         two nodes should be from left to right as we did for BFS traversals. As a result, to ensure such a priority, we
         should make sure to visit the left child node before the right child node during the DFS traversal.

         During the traversal, we build a similar hash map with the column index as the key and the list of (row, val)
         tuples as the value.

         At the end of the DFS traversal, we iterate through the hashmap via the key of column index. Accordingly,
         we have a list of (row, val) tuples associated with each key. We then sort this list based on the row index.

    Time complexity: O(W * HlogH), where W is the width of the binary tree (i.e. the number of columns in the result)
    and H is the height of the tree. In the first part of the algorithm, we traverse the tree in DFS, which results in
    O(N) time complexity. Once we build the hashmap, we then have to sort it column by column. Let us assume the
    time complexity of the sorting algorithm to be O(K logK) where K is the length of the input. The maximal number of
    nodes in a column would be O(H/2) where H is the height of the tree, due to the zigzag nature of the node
    distribution. Since we need to sort W columns, the total time complexity of the sorting operation would then be
    O(W * HlogH). Note that the total number of nodes N in a tree is bounded by W * H, i.e. N < W * H. As a result,
    the time complexity of O(W * HlogH) will dominate the O(N) of the DFS traversal in the first part.
    Space complexity: O(N), where N is the number of nodes in the tree. We keep the hashmap which contains all the
    node values in the binary tree. Since we apply the recursion for the DFS traversal, it would incur additional space
    consumption on the function call stack. In the worst case where the tree is completely imbalanced, we would
    have the size of call stack up to O(N).
    """

    def dfs(node, row, column):
        if not node:
            return
        columns[column].append((row, node.val))
        dfs(node.left, row + 1, column - 1)
        dfs(node.right, row + 1, column + 1)

    if not root:
        return None
    columns = defaultdict(list)
    dfs(root, 0, 0)
    min_col = min(columns.keys())
    max_col = max(columns.keys())
    res = []
    for i in range(min_col, max_col+1):
        column = sorted(columns[i])
        res.append([value for row, value in column])
    return res


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
        self.assertTrue(self.result, vertical_order_v2(self.root))


if __name__ == '__main__':
    unittest.main()
