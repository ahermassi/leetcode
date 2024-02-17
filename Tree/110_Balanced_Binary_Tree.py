""" Given a binary tree, determine if it is height-balanced.
For this problem, a height-balanced binary tree is defined as:
    a binary tree in which the depth of the two subtrees of every node never differ by more than 1.
"""

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_balanced_v1(root):
    """ "Top-Down" or Preorder DFS.

         The balanced subtree definition hints at the fact that we should treat each subtree as a sub-problem.

         Check whether the tree is height-balanced strictly according to the definition: A tree is height-balanced if
         and only if the height of its two children subtrees are within 1 of each other and the subtrees at each child
         are also height-balanced. Therefore, we can compare the two child subtrees' heights then recurse on each one.

    Time complexity: O(N^2), for the current root node, calling height() for its left and right children actually has
    to access all of its children, thus the complexity is O(N). We do this for each node in the tree, so the overall
    complexity is O(N logN) because there are logN levels, but in the worst case of skewed tree the complexity is
    O(N^2). However, it is important to note that we stop recursion as soon as the height of a node's children are not
    within 1. In fact, in the skewed-tree case the algorithm is bounded by O(N), as it only checks the height of the
    first two subtrees.
    Space complexity: O(N), in the worst case
    """

    def height(root):
        if not root:
            return 0
        return 1 + max(height(root.left), height(root.right))

    if not root:
        return True
    left_height, right_height = height(root.left), height(root.right)
    # Check if subtrees have height within 1. If they do, check if the subtrees are balanced.
    if abs(left_height - right_height) > 1:
        return False
    return is_balanced_v1(root.left) and is_balanced_v1(root.right)


# Video explanation: https://www.youtube.com/watch?v=LU4fGD-fgJQ
# Video explanation: https://www.youtube.com/watch?v=QfJsau0ItOY
def is_balanced_v2(root):
    """ "Bottom-Up" or Postorder DFS.

         In the previous approach, we perform redundant calculations when computing height. In each call to height(), we
         require that the subtrees heights also be computed. Therefore, when working top-down we will compute the height
         of a subtree once for every parent.

         We can remove the redundancy by first recursing on the children of the current node and then using their
         computed heights to determine whether the current subtree rooted at the current node is height-balanced.
         This bottom-up approach is different from the logic of the top-down approach since we first check if the
         children  subtrees are height-balanced before comparing their heights.

         Check if the child subtrees are height-balanced. If they are, use their heights to determine if the current
         subtree is height-balanced as well as to calculate the current subtree's height.

         The key difference between the two approaches is that this second optimized approach refuses to do any
         processing/work until the left child recursion and right child recursion are done. The key here is that this
         allows us to reuse old results and do everything only once. This is called bottom-up strictly because we need
         to get answers from nodes at height n-1 beforehand, in order to get answers at height n. The first approach will
         make nodes do the processing/work FIRST, and then make its left and right children go through the same exact
         burden. Nothing is reused, a lot of work is repeated. This is a problematic ordering given the nature of this
         problem, where results at the lower levels of the tree will definitely prove to be useful to get results at
         higher levels of the tree.

         "Bottom" in recursion simply means the end of some recursive depth. Top-down implies we are doing work to find
         the solution as we reach this recursive depth. Bottom-up implies that we are doing work to find the solution
         only once we hit the recursive depth, and we propagate the results upwards to previous recursive calls.

        Instead of saying top-down and bottom-up, it would be better to just call it one-pass or multiple-pass.

    Time complexity: O(N) in the worst case of a skewed tree, each node in the tree only need to be accessed once
    Space complexity: O(N), in the worst case
    """

    def check_balanced(root):
        # First member of the return value is the height of the subtree rooted at 'root', and the second member of
        # the return value indicates if the tree is balanced
        if not root:
            return 0, True
        left_height, left_balanced = check_balanced(root.left)
        right_height, right_balanced = check_balanced(root.right)
        height_balanced = abs(left_height - right_height) <= 1
        return 1 + max(left_height, right_height), height_balanced and left_balanced and right_balanced

    return check_balanced(root)[1]


def is_balanced_v3(root):
    """ Notice that the height of a tree is always >= 0, and we do not care about the height when the subtree is already
         confirmed imbalanced. So we can use -1 to represent imbalanced.

         When the subtree of the current node (inclusive) is balanced, the function height() returns a non-negative
         value as the height. According to the left height and right height of the two children, the parent node could
         check if the subtree is balanced, and decides its return value.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    def height(root):
        if not root:
            return 0
        left_height = height(root.left)
        if left_height == -1:
            return -1
        right_height = height(root.right)
        if right_height == -1:
            return -1
        if abs(left_height - right_height) > 1:
            return -1
        return max(left_height, right_height) + 1

    return height(root) != -1


class Test(unittest.TestCase):
    root1 = TreeNode(3)
    root1.left = TreeNode(9)
    root1.right = TreeNode(20)
    root1.right.left = TreeNode(15)
    root1.right.right = TreeNode(7)
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(2)
    root2.left.left = TreeNode(3)
    root2.left.right = TreeNode(3)
    root2.left.left.left = TreeNode(4)
    root2.left.left.right = TreeNode(4)

    def test_is_balanced(self):
        self.assertTrue(is_balanced_v1(self.root1))
        self.assertFalse(is_balanced_v2(self.root2))
        self.assertFalse(is_balanced_v3(self.root2))


if __name__ == '__main__':
    unittest.main()

