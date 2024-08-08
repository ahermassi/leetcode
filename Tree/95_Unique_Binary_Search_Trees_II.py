""" Given an integer n, generate all structurally unique BST's (binary search trees) that store values 1 ... n. """


# Definition of a binary tree node.
class TreeNode:
    def __init__(self, x, left=None, right=None):
        self.val = x
        self.left = None
        self.right = None


# Video explanation: https://youtu.be/m907FlQa2Yc
def generate_trees_v1(n):
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


def generate_trees_v2(n):
    """ Bottom-Up Dynamic Programming.

         Let dp[i][j] be the list of all BSTs that have node values ranging from i to j (inclusive).

         When i=j, the range contains only one node with value i. We push a single node with value i in the list
         dp[i][i] for all the values of i from 1 to n. This acts as the base case of the solution while we move in
         bottom to top manner.

         We form the answer with a smaller number of nodes having consecutive node values and move on to form answers
         for a bigger number of nodes. We run an outer loop from number_of_nodes = 2 to number_of_nodes = n,
         incrementing number_of_nodes by 1 after each iteration. This loop controls the total number of nodes under
         consideration.

         We further need to choose a node value to start with. Let's call it lower. As we have number_of_nodes nodes
         under consideration with consecutive values, the maximum node value in such a BST would be
         start+number_of_nodes-1. We move lower from 1 to n -number_of_nodes+1.

         Now we have the lower value and the upper value, we can implement the same logic that we did in the
         previous implementation: lock a value i, find all left and right subtrees, and then iterate over each
         (left, right) pair and create a new root with value i for each pair.

         As we move from bottom to top, we have a list of all the root nodes for all BSTs for every range of node values
         with fewer nodes.

         Locking a value i as the root node, we can find all left subtrees in dp[lower][i-1] and all right subtrees in
         dp[i+1][upper]. If i == lower, the left subtree would be empty. Similarly, if i == upper, the right subtree
         would be empty. We can handle these cases separately.

         We run an outer loop from number_of_nodes = 2 to n. We run an inner loop that selects the starting node value.
         It runs from lower = 1 to n-number_of_nodes+1. We define upper = lower+number_of_nodes-1. We run a third nested
         loop that selects the root of the BSTs under consideration. It runs from i = lower to upper.

         We then iterate over the both the lists of left and right subtrees. For each root node left of the left subtree
         and right of the right subtree, we create a new root node with value i and set the left and right child to left
         and right, respectively, to form all the BSTs with root node as i. We also push each BST into dp[lower][upper]
         to be used later to build answer for other dp states with larger number of nodes.

    Time complexity: the main computations are to construct all possible trees with a given root, that is actually
    Catalan number G_n. This is done n times, that results in time complexity n * G_n, that gives the final time
    complexity O(4^n)
    """
    dp = [[[] for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][i] = [TreeNode(i)]
    for number_of_nodes in range(2, n + 1):
        for lower in range(1, n - number_of_nodes + 2):
            upper = lower + number_of_nodes - 1
            for i in range(lower, upper + 1):
                left_subtrees = dp[lower][i - 1] if i != lower else [None]
                right_subtrees = dp[i + 1][upper] if i != upper else [None]
                for left in left_subtrees:
                    for right in right_subtrees:
                        root = TreeNode(i, left, right)
                        dp[lower][upper].append(root)
    return dp[1][n]

