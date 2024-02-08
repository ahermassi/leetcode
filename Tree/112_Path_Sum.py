""" Given a binary tree and a sum, determine if the tree has a root-to-leaf path such that adding up all the values
along the path equals the given sum. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# Video explanation: https://youtu.be/LSKQyOz_P8I
def has_path_sum_v1(root, target_sum):
    """ The most intuitive way is to use recursion. We go through the tree by considering at each step the node itself
         and its children.

            - If the node is not a leaf, we call recursively hasPathSum method for its children with a sum
               decreased by the current node's value.

            - If the node is a leaf, we check if the current sum is zero, i.e. if the initial sum was found.

        Traverse the tree, keeping track of difference of the root-to-node path sum and the target value. As soon as we
        encounter a leaf and the remaining sum is equal to the leaf 's value, we return true. Short circuit evaluation
        of the check ensures that we do not process additional leaves.

    Time complexity: O(N), in the worst case we visit each node exactly once
    Space complexity: in the worst case, the tree is completely unbalanced and the recursion call would occur N times,
    therefore the storage to keep the call stack would be O(N); in the best case (the tree is completely balanced), it
    is O(logN) which is the height of the tree
    """
    if not root:
        return False
    if not root.left and not root.right and root.val == target_sum:
        return True
    target_sum -= root.val
    return has_path_sum_v1(root.left, target_sum) or has_path_sum_v1(root.right, target_sum)
    # Could also be written:
    # def dfs(node, cur_sum):
    #     if not node:
    #         return False
    #     cur_sum += node.val
    #     if not node.left and not node.right:
    #         return cur_sum == targetSum
    #     return dfs(node.left, cur_sum) or dfs(node.right, cur_sum)
    #
    # return dfs(root, 0)


def has_path_sum_v2(root, target_sum):
    """ We could also convert the above recursion into iteration, with the help of stack.

         We start from a stack which contains the root node and the corresponding remaining sum, which is initially
         target_sum. Then we proceed to the iterations: pop the current node out of the stack and return True if
         the node's value is equal to the remaining sum, and we're on a leaf node. If the remaining sum is not zero, or
         if we're not at a leaf node, then we push the children nodes and corresponding remaining sums into the stack.

    Time complexity: O(N)
    Space complexity: in the worst case, the tree is completely unbalanced, and we would keep all N nodes in the stack
    so O(N); in the best case (the tree is completely balanced), it is O(logN) which is the height of the tree
    """
    if not root:
        return False
    stack = [(root, target_sum)]
    while stack:
        node, remaining_sum = stack.pop()
        if not node.left and not node.right and node.val == remaining_sum:
            return True
        remaining_sum -= node.val
        stack.extend([(kid, remaining_sum) for kid in (node.left, node.right) if kid])
    return False


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.right.right.right = TreeNode(1)
    root.left.right = TreeNode(4)

    def test_has_path_sum(self):
        self.assertEqual(True, has_path_sum_v1(self.root, 22))
        self.assertEqual(True, has_path_sum_v2(self.root, 22))


if __name__ == '__main__':
    unittest.main()


