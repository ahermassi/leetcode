""" Given an integer n, generate all structurally unique BST's (binary search trees) that store values 1 ... n. """


# Definition of a binary tree node.
class TreeNode:
    def __init__(self, x, left=None, right=None):
        self.val = x
        self.left = None
        self.right = None


# Video explanation: https://youtu.be/m907FlQa2Yc
def generate_trees(n):
    """ Top-Down Dynamic Programming.

         Note that 1...n is the inorder traversal for any BST with nodes 1 to n. We know that in a BST all nodes in the
         left subtree are smaller than the root and in the right subtree are larger than the root. So if we pick the ith
         node as root, the left subtree contains elements 1 to i-1, and the right subtree contains elements i+1 to n.

         To find all the possible permutations of BSTs with n nodes, we can lock one node as the root node and split
         n-1 nodes between the left and right subtrees in all the possible ways. Let's say we place a node with value
         i as the root node and place i-1 nodes having values from 1 to i-1 in the left subtree. Similarly, we place the
         remaining n-i nodes having values from i+1 to n in the right subtree.

         Now, we create a list of nodes called left_subtrees for all the possible BSTs that could be the left subtree.
         Similarly, we create a list of nodes called right_subtrees for all the BSTs that could be the right subtree.
         In a BST, every subtree is also a BST.

         We iterate over both the lists and for each node pair left in left_subtrees and right in right_subtrees, we
         create a new root node with value i and set the left and right child of root to left and right respectively to
         form all the BSTs with the root node as i (cartesian product).

         Notice that the sub-problem of finding the arrays left_subtrees and right_subtrees are similar to the original
         problem. We can implement this approach using recursion as we are breaking down a problem with n nodes to
         smaller, repetitive sub-problems with i-1 and n-i nodes (for i = 1 till n) to compute the answer for n nodes.
         We only need the range of node values as the parameters to create the BSTs with nodes having values in that
         range.

         If we draw the entire recursion tree, we can see that there are many sub-problems that are solved repeatedly.
         To avoid this issue, we store the solution of the sub-problem in a hashmap that stores the mapping from a range
         of nodes values to the list of root nodes of all possible BSTs that can be formed with the same number of
         nodes. When we encounter the same sub-problem again, we simply refer to this map to get the required list of
         TreeNode.

    Time complexity: the main computations are to construct all possible trees with a given root, that is actually
    Catalan number G_n. This is done n times, that results in time complexity n * G_n, that
    gives the final complexity O(4^n)
    """

    def construct_trees(lower, upper):
        # Return a list of TreeNode corresponding to all the BSTs that can be formed with [lower, upper] range of node
        # values.
        if lower > upper:
            return [None]
        if (lower, upper) in memo:
            return memo[(lower, upper)]
        res = []
        for i in range(lower, upper + 1):  # Pick a root
            left_subtrees = construct_trees(lower, i - 1)  # All possible left subtrees if i is the root
            right_subtrees = construct_trees(i + 1, upper)  # All possible right subtrees if i is the root
            # Connect left and right subtrees to the root i
            for left in left_subtrees:
                for right in right_subtrees:
                    root = TreeNode(i, left, right)
                    res.append(root)
        memo[(lower, upper)] = res
        return res

    memo = {}
    return construct_trees(1, n) if n else []

