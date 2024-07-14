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


# Video explanation: https://www.youtube.com/watch?v=olbiZ-EOSig
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
    """ Same idea, but we use a boolean flag, null_found, to keep track of whether we have seen a null node.

         While the BFS queue is not empty, we fetch the front node in the queue. If the node is null, we mark
         null_found = true. Otherwise, if the node is not null, we check if we have already visited a null node.
         If we've previously visited a null node and the current node is not null, the given tree isn't a complete
         binary tree as we are encountering a node after visiting a null node.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    queue, null_found = deque([root]), False
    while queue:
        node = queue.popleft()
        if not node:
            # This is the first time we meet a null node
            null_found = True
        elif null_found:
            # The current node is not null but 'null_found' is true: the tree is not complete
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

         A complete binary tree has an interesting property that we can use to find the children and parents of any
         node.

         A complete binary tree can be represented with an array. If the index of a node in the array is i, the element
         at index 2i + 1 will be its left child and the element at index 2i + 2 will be its right child. If there are a
         total of n nodes in a complete binary tree, it can be represented with an array where the nodes are ordered
         level by level, left to right. As we saw in the previous approach, there will be no null node between two
         non-null nodes.

         Suppose we have an array which represents a heap of size n. The algorithm tries to verify whether the tree with
         n nodes can fit into the array.

         Starting with the root node and assigning it an index of 0, we can use the above property to assign indices to
         all the other nodes in the tree. The assigned index of every node must be smaller than or equal to n for the
         given tree to form a complete binary tree. The tree can fit into the array if and only if all nodes' indices
         are within the boundary of the array, that is, n.

         If the index of a node is greater than or equal to n, it means a node is missing from the first n indices.
         Therefore, the tree is not a complete binary tree. The array representation of such a binary tree will have at
         least one null node in between non-null nodes. (check the attached diagram)

         The DFS essentially checks whether the index of a node exceeds the boundary of a heap of size n. If index > n,
         there must be an empty slot in the array, which means the tree cannot fit into the array. Otherwise, it
         recursively checks the children of the root.

    Time complexity: O(N), where N is the number of nodes in the tree. Each node is visited once.
    Space complexity: O(h), for call stack
    """

    def count_nodes(root):
        if not root:
            return 0
        return 1 + count_nodes(root.left) + count_nodes(root.right)

    def dfs(root, index, node_count):
        if not root:
            return True
        if index >= node_count:
            return False
        return dfs(root.left, 2 * index + 1, node_count) and dfs(root.right, 2 * index + 2, node_count)

    node_count = count_nodes(root)
    return dfs(root, 0, node_count)


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
