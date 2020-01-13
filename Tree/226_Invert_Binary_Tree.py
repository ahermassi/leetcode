""" Invert a binary tree.
 Example:

Input:

     4
   /   \
  2     7
 / \   / \
1   3 6   9

Output:

     4
   /   \
  7     2
 / \   / \
9   6 3   1
 """

# Definition for a binary tree node.
from collections import deque


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def invert_tree_v1(root):
    """ Recursive approach
    Time complexity: O(N), we cannot do better since at the very least we have to visit each node to invert it
    Space complexity: O(N), because of recursion, O(h) function calls will be placed on the stack in the worst case,
    where h is the height of the tree
    """
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invert_tree_v1(root.left)
    invert_tree_v1(root.right)
    return root


def invert_tree_v2(root):
    """ Iterative approach, in a manner similar to DFS.
        As long as the stack is not empty, remove the next node from the stack, swap its children, and add the children
        to the stack. Eventually, the stack will be empty and all the children swapped.
    Time complexity: O(N)
    Space complexity: O(N), since in the worst case the stack will contain all nodes in one level of the binary tree
    """
    if not root:
        return None
    stack = [root]
    while stack:
        node = stack.pop()
        node.left, node.right = node.right, node.left
        stack.extend([child for child in (node.left, node.right) if child])
    return root


def invert_tree_v3(root):
    """ Iterative approach, in a manner similar to BFS, using a deque.
        As long as the queue is not empty, remove the next node from the queue, swap its children, and add the children
        to the left of the queue. Eventually, the queue will be empty and all the children swapped.
    Time complexity: O(N)
    Space complexity: O(N), since in the worst case the queue will contain all nodes in one level of the binary tree.
    For a full binary tree, the leaf level has ⌈N/2⌉= O(N) leaves.
    """
    if not root:
        return None
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            node.left, node.right = node.right, node.left
            queue.extend([node.left, node.right])
    return root
