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
    """ By analyzing the definition, we can see that a binary tree is complete if there is no node to the right of the
         first null node and no node at a greater level than the first null node.

         It means that if we traverse the tree level by level from left to right, and we come across a null node, all
         subsequent nodes in this traversal should be null as well. The level-order traversal of a complete binary tree
         will never have a null node in between non-null nodes.

         Use BFS to do a level order traversal, add children to the BFS queue, until we meet the first empty node.
         We use a key feature of level order traversal - from top to bottom and from left to right, so as soon as
         we see a null node (previous level or last level), there should be no more non-null nodes as we continue the
         traversal.

    Time complexity: O(N), where N is the number of nodes in the tree. Each node can only be pushed and popped once
    Space complexity: O(N), the last or second-to-last level would have the most nodes (the last level can have multiple
    null nodes) in a complete binary tree. The BFS queue will be most crowded when all the nodes from the last level
    (or second-to-last level) are in the queue. In a complete binary tree, the last level has (N+1)/2 nodes.
    """
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if not node:
            break
        queue.extend([node.left, node.right])
    while queue:
        if queue.popleft():
            return False
    return True


def is_complete_tree_v2(root):
    """ Similar approach but with early termination.
        Perform a standard left-to-right BFS and keep a boolean flag 'null_found' that is set to true whenever we
        encounter the first null node. If the tree is complete, no non-null node should be met after 'null_found' is
        set to true. Otherwise, exit early and return False.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    queue, null_found = deque([root]), False
    while queue:
        node = queue.popleft()
        if not node:  # This is the first time we meet a null node
            null_found = True
        elif null_found:  # The current node is not null but 'null_found' is true: The tree is not complete
            return False
        else:
            queue.extend([kid for kid in (node.left, node.right)])
    return True


def is_complete_tree_v3(root):
    """ DFS. It uses the node number technique in heap structures like this:
              1
            /  \
           2   3
          / \  /
         4  5 6
         This solution relies on is two properties of a heap. First, a heap is always a complete binary tree. So if a
         tree can be viewed as a heap, it is complete. Second, inside a heap (which is an array), a parent with index
         i has two children with index (i * 2) and (i * 2 + 1), if the parent has two children in the first place.
         With these two properties known, it is easy to understand this solution. Suppose we have an array which
         represents a heap of size 'node_count'. The algorithm tries to verify whether the tree with 'node_count' nodes
         can fit into the array. The tree can fit into the array if and only if all nodes' indices are within the
         boundary of the array, that is, 'node_count'. The dfs() essentially checks whether the index of a node exceeds
         the boundary of a heap with size 'node_count'. If index > node_count, there must be an empty slot in the
         array, which means the tree cannot fit into the array so dfs() returns false. If idx <= total, dfs()
         recursively checks the children of root.
    Time complexity:
    Space complexity:
    """

    def count_nodes(root):
        if not root:
            return 0
        return 1 + count_nodes(root.left) + count_nodes(root.right)

    def dfs(root, index, node_count):
        if not root:
            return True
        if index > node_count:
            return False
        return dfs(root.left, index * 2, node_count) and dfs(root.right, index * 2 + 1, node_count)

    node_count = count_nodes(root)
    return dfs(root, 1, node_count)


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
        self.assertTrue(is_complete_tree_v3(self.root))


if __name__ == '__main__':
    unittest.main()
