""" Given a binary tree, return the zigzag level order traversal of its nodes' values. (ie, from left to right, then
right to left for the next level and alternate between).

For example:
Given binary tree [3,9,20,null,null,15,7],
    3
   / \
  9  20
    /  \
   15   7
return its zigzag level order traversal as:
[
  [3],
  [20,9],
  [15,7]
] """

from collections import deque
import unittest2 as unittest


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# Video explanation: https://youtu.be/igbboQbiwqw
def zigzag_level_order_v1(root):
    """ The most intuitive solution would be the BFS approach through which we traverse the tree level-by-level.
         The default ordering of BFS within a single level is from left to right. As a result, we should adjust the BFS
         algorithm a bit to generate the desired zigzag ordering.

         There are several ways to implement the BFS algorithm. One way is to run a two-level nested loop, with the
         outer loop iterating over each level on the tree, and with the inner loop iterating each node within a single
         level.

         We use a 'direction' flag to indicate whether to add the child nodes of the current level to the output list in
         left->right or right->left order.

         direction == 1 means add the nodes of the CURRENT level from left to right.
         direction == -1 means add the nodes of the CURRENT level from right to left.

    Time complexity: O(N), we visit each node twice. In addition, the insertion operation on either end of
    the queue takes a constant time
    Space complexity: O(N), the queue would hold the nodes that are at most across two levels. Therefore, at most, the
    size of the queue would be no more than 2⋅L, where L is the maximum number of nodes that might reside on the
    same level. Since we have a binary tree, the level that contains the most nodes is the one that has all the leave
    nodes in a full binary tree, which is roughly N/2. As a result, we have the space complexity of 2 * N/2 = N
    """
    if not root:
        return None
    res, queue, direction = [], deque([root]), 1
    while queue:
        n, values = len(queue), []
        for _ in range(n):
            node = queue.popleft()
            values.append(node.val)
            queue.extend([kid for kid in (node.left, node.right) if kid])
        if direction == 1:
            res.append(values)
        else:
            res.append(values[::-1])
        direction = -direction
    return res


def zigzag_level_order_v2(root):
    """ The same BFS approach, but we use a queue to hold the values of the popped nodes of the current level which
         makes it easier to append to either end.

         We can also perform a BFS and maintain a dictionary that can contain values in deque for a particular level.
         So, based on the parity of each level, we can append right or append left in the deque. Odd levels mean
         right-to-left ordering, while even levels mean left-to-right ordering.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    res = []
    direction = 1
    queue = deque([root])
    while queue:
        n, values = len(queue), deque()
        for _ in range(n):
            node = queue.popleft()
            if direction == 1:
                values.append(node.val)
            else:
                values.appendleft(node.val)
            queue.extend([kid for kid in (node.left, node.right) if kid])
        res.append(values)
        direction *= -1
    return res


def zigzag_level_order_v3(root):
    """ DFS. Similar to 102- Binary Tree Level Order Traversal.

        We define a recursive function called dfs(root, depth) which only takes care of the current node which is
        located at the specified depth/level. Within the function, there are three steps that we would perform:

        - If this is the first time that we visit any node at the level, i.e. the deque for the level does not exist,
           then we simply create the deque with the current node value as the initial element.

        - If the deque for this level exists, then depending on the ordering, we insert the current node value either to
           the head or to the tail of the queue. Odd levels mean right-to-left ordering, while even levels mean
           left-to-right ordering.

        - At the end, we recursively call the function for each of its child nodes.

    Time complexity: O(N), we visit each node once
    Space complexity: O(N), the size of the call stack for any invocation of dfs(root, depth) will be exactly the number
    of level that the current node resides on. Therefore, the space complexity of the DFS algorithm is O(H), where H is
    the height of the tree. In the worst-case scenario, when the tree is very skewed, the tree height could be N. Thus,
    the space complexity is also O(N).
    """

    def dfs(root, depth):
        if not root:
            return
        if depth == len(levels):
            levels.append(deque())
        if depth % 2 == 0:
            levels[depth].append(root.val)
        else:
            levels[depth].appendleft(root.val)
        dfs(root.left, depth + 1)
        dfs(root.right, depth + 1)

    levels = []
    # levels = defaultdict(deque) could also be used
    dfs(root, 0)
    return levels


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    result = [
        [3],
        [20, 9],
        [15, 7]
    ]

    def test_zigzag_level_order(self):
        self.assertEqual(self.result, zigzag_level_order_v1(self.root))
        self.assertEqual(self.result, zigzag_level_order_v2(self.root))


if __name__ == '__main__':
    unittest.main()
