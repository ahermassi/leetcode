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
         branch.

         So, the algorithm to solve this problem will find the node where the sum of its longest left and right branches
         is maximized. This would hint at us to apply depth-first search (DFS) to count each node's branch lengths,
         because it would allow us to dive deep into the leaves first, and then start counting the edges upwards.

         Let's try to be more specific about how to apply DFS to this question. To count the lengths of each node's left
         and right branches, we can implement a recursive function height(root) which takes a TreeNode as input and
         returns the height of that node.

         So, we can solve this problem with two different cases:

             1- If the longest path will include the current root node, then the longest path must be:
                        left height + right height

             2- If the longest path does not include the current root node, this problem is divided into 2 sub-problems:
                  Set left child and right child as the new root separately, and repeat previous step.

        We initialize a global variable 'diameter' to keep track of the longest path and updating it at each node with
        the sum of the node's left and right branches.

        We implement a recursive function height which takes a TreeNode as input. It should recursively explore the
        entire tree rooted at the given node. Once it's finished, it should return the longest path out of its left and
        right branches:

            - If node is None, we have reached the end of the tree, hence we should return 0.

            - Otherwise, we want to recursively explore the node's children, so we call height again with the node's
               left and right children. In return, we get the heights of its left and right children, left_height and
               right_height.

            - if left_height plus right_height is longer than the current longest diameter found, then we need to update
              'diameter'.

            - Finally, we return the longer one of left_height and right_height. Remember to add 1 as the edge
               connecting it with its parent.

        Conclusion:

        Diameter of a tree in regard to root can be defined as:

                Maximum(Diameter of left subtree, Diameter of right subtree, Longest path between two nodes which passes
                through the root)

        The diameter of left and right subtrees can be solved recursively. Longest path between two nodes which passes
        through the root can be calculated as: height of left subtree + height of right subtree. Therefore:

                Diameter = max(Diameter of left subtree, Diameter of right subtree, left height + right height)

    Time complexity: O(N)
    Space complexity: O(h), in the worst case the tree is skewed so the height of the tree is O(N). If the tree is
    balanced, it'd be O(logN)
    """

    def height(root):
        if not root:
            return 0
        left_height, right_height = height(root.left), height(root.right)
        diameter[0] = max(diameter[0], left_height + right_height)
        return 1 + max(left_height, right_height)

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

