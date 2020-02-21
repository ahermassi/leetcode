""" Given an integer n, generate all structurally unique BST's (binary search trees) that store values 1 ... n. """

# Definition for a binary tree node.


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def generate_trees(n):
    """ Note that 1..n is the in-order traversal for any BST with nodes 1 to n. So if we pick ith node as root, the
        left subtree will contain elements 1 to (i - 1), and the right subtree will contain elements (i + 1) to n.
        Let's pick up number i out of the sequence 1..n and use it as the root of the current tree. Then there are
        (i - 1) elements available for the construction of the left subtree and (n - i) elements available for the
        right subtree. As we've already seen in 96- Unique Binary Search Trees, that results in G(i - 1) different
        left subtrees and G(n - i) different right subtrees, where G is a Catalan number.
        Now let's repeat the step above for the sequence 1 ... i - 1 to construct all left subtrees, and then for the
        sequence i + 1 ... n to construct all right subtrees.
        This way we have a root i and two lists for the possible left and right subtrees. The final step is to loop
        over both lists to link left and right subtrees to the root (cartesian product).
    Time complexity: the main computations are to construct all possible trees with a given root, that is actually
    Catalan number G_n as was discussed above. This is done n times, that results in time complexity n * G_n, that
    gives the final complexity O(4^n)
    """

    def helper(lower, upper):
        if lower > upper:
            return [None]
        if lower == upper:
            return [TreeNode(lower)]
        res = []
        for i in range(lower, upper + 1):  # Pick a root
            left = helper(lower, i - 1)  # All possible left subtrees if i is chosen to be a root
            right = helper(i + 1, upper)  # All possible right subtrees if i is chosen to be a root
            # Connect left and right subtrees to the root i
            for l in left:
                for r in right:
                    root = TreeNode(i)
                    root.left = l
                    root.right = r
                    res.append(root)
        return res

    return helper(1, n) if n else []

