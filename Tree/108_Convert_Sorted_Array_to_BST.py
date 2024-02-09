""" Given an array where elements are sorted in ascending order, convert it to a height balanced BST.
For this problem, a height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees of
every node never differ by more than 1. """

import unittest2 as unittest


# Definition for a  binary tree node


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# Video explanation: https://youtu.be/0K0uCMYq5ng
def sorted_array_to_bst(nums):
    """ It's known that the inorder traversal of BST is an array sorted in the ascending order. Having the sorted array
         as an input, we could rewrite the problem as "Construct Binary Search Tree from Inorder Traversal."

         Does this problem have a unique solution, i.e. could inorder traversal be used as a unique identifier to
         encode/decode BST? The answer is no.

         Inorder traversal is not a unique identifier of BST. At the same time, both preorder and postorder traversals
         are unique identifiers of BST. From these traversals we could restore the inorder one:

                    inorder = sorted(postorder) = sorted(preorder)
                    inorder + postorder or inorder + preorder are both unique identifiers of every binary tree

        So, the problem "sorted array -> BST" has multiple solutions.

        The height-balanced restriction means that at each step we have to pick the number in the middle as a root.
        That works fine with arrays containing an odd number of elements but there is no predefined choice for arrays
        with an even number of elements.

        Intuitively, to make a minimum height BST, we want the subtrees to be as balanced as possible. There's no point
        in one subtree being shorter than the other since the height is determined by the taller one. More formally,
        balance can be achieved by keeping the number of nodes in both subtrees as close as possible.

        Let N be the length of the array. To achieve optimum balance, we can make the element in the middle of the
        array, i.e., the (N/2)th entry, the root, and recursively compute minimum height BSTs for the sub-arrays on
        either side of this entry.

    Time complexity: O(N), we make exactly N calls to the recursive function and spend O(1) within each call. Don't be
    fooled by the binary search nature of the solution and think the time complexity is O(logN).
    Example: nums = [2, 3, 5, 7, 11, 13, 77, 79, 23]. Split nums into 2 halves in first call, then RECURSIVELY split
    left and right halves in the subsequent calls, resulting in N calls to the recursive function, not logN calls.
    Space complexity: O(logN), there is no case of skewed binary tree because we're creating a balanced BST from the
    start by picking the middle element every time. It's not possible to have a skewed input or output, so the recursion
    stack requires O(logN) space because the tree is height-balanced.
    """

    def build_tree(left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = build_tree(left, mid - 1)
        root.right = build_tree(mid + 1, right)
        return root

    return build_tree(0, len(nums) - 1)


class Test(unittest.TestCase):
    data = [-10, -3, 0, 5, 9]

    def test_sorted_array_to_bst(self):
        root = sorted_array_to_bst(self.data)
        self.assertEqual(0, root.val)
        self.assertEqual(-3, root.left.val)
        self.assertEqual(9, root.right.val)
        self.assertEqual(-10, root.left.left.val)
        self.assertEqual(5, root.right.left.val)


if __name__ == '__main__':
    unittest.main()
