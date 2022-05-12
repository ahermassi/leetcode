""" Given a binary tree, you need to compute the length of the diameter of the tree. The diameter of a binary tree is
the length of the longest path between any two nodes in a tree. This path may or may not pass through the root. """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# Video explanation: https://www.youtube.com/watch?v=bkxqA8Rfv04

def diameter_of_binary_tree(root):
    """ The key observation to make is:

                    The longest path has to be between two leaf nodes

         We can prove this with contradiction. Imagine that we have found the longest path, and it is not between two
         leaf nodes. We can extend that path by 1, by adding the child node of one of the end nodes (as at least one
         must have a child, given that they aren't both leaves). This contradicts the fact that our path is the longest
         path. Therefore, the longest path must be between two leaf nodes.

        Moreover, we know that in a tree, nodes are only connected with their parent node and 2 children. Therefore, we
        know that the longest path in the tree would consist of a node, its longest left branch, and its longest right
        branch. So, our algorithm to solve this problem will find the node where the sum of its longest left and right
        branches is maximized. This would hint at us to apply Depth-first search (DFS) to count each node's branch
        lengths, because it would allow us to dive deep into the leaves first, and then start counting the edges
        upwards.

        Let's try to be more specific about how to apply DFS to this question. To count the lengths of each node's left
        and right branches, we can implement a recursive function height(root) which takes a TreeNode as input and
        returns the height of that node.

        So, we can solve this problem with two different cases:

            1- If the longest path will include the current root node, then the longest path must be:
                        left height + right height + 2
                 The +2 accounts for 1 edge leading to each tree on the left and right

            2- If the longest path does not include the current root node, this problem is divided into 2 sub-problems:
                 Set left child and right child as the new root separately, and repeat previous step.

        Conclusion:

        Diameter of a tree in regard to root can be defined as:

                Maximum(Diameter of left subtree, Diameter of right subtree, Longest path between two nodes which passes
                through the root)

        Now, the diameter of left and right subtrees can be solved recursively. Longest path between two nodes which
        passes through the root can be calculated as: height of left subtree + height of right subtree + 2. Therefore:

                Diameter = max(Diameter of left subtree, Diameter of right subtree, left height + right height + 2)

    Time complexity: O(N)
    Space complexity: O(N)
    """

    def height(root):
        if not root:
            return -1
        left_height = height(root.left)
        right_height = height(root.right)
        diameter[0] = max(diameter[0], left_height + right_height + 2)  # The "+2" accounts for the edge on the left
        # plus the edge on the right
        return max(left_height, right_height) + 1

    diameter = [0]
    height(root)
    return diameter[0]


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    def test_diameter_of_binary_tree(self):
        self.assertEqual(3, diameter_of_binary_tree(self.root))


if __name__ == '__main__':
    unittest.main()

