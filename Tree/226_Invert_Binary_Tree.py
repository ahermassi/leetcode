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


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def invert_tree_v1(root):
    """ Recursive approach
    Time complexity: O(N). We cannot do better, since at the very least we have to visit each node to invert it.
    Space complexity: O(N). Because of recursion, O(h) function calls will be placed on the stack in
    the worst case, where h is the height of the tree.
    """
    if root:
        root.left, root.right = root.right, root.left
        invert_tree_v1(root.left)
        invert_tree_v1(root.right)
        return root
