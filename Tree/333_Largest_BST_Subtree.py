""" Given the root of a binary tree, find the largest subtree, which is also a Binary Search Tree (BST), where the
largest means subtree has the largest number of nodes.

Note: A subtree must include all of its descendants. """


def largestBSTSubtree(root):
    """ Every dfs(root) call returns 3 values:
            - Minimum value in the subtree rooted at 'root'
            - Maximum value in the subtree rooted at 'root'
            - Number of nodes of the subtree rooted at 'root'
        If the current node 'root' wants to be part (i.e. root) of a BST, it must satisfy:
            - Its value is greater than the max value of its left subtree (hence greater than any left subtree node)
            - Its value is less than the min value of its right subtree (hence smaller than any right subtree node)
        This recursively checks all the valid BSTs in a bottom-up manner.
        If the current node 'root' happens to satisfy all above requirements, we return a new result for the subtree
        rooted at 'root' with:
            - Minimum value of the new BST
            - Maximum value of the new BST
            - Total size of the subtree
        If yhe current node 'root' does not satisfy all above requirements, the whole subtree rooted at 'root' will be
        invalidated. However, its left and/or right child may still be root of a valid BST, so we need to carry over
        the max of their sizes in order to return it to top level.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def dfs(root):
        if not root:
            # Since the node is null, every parent node can still form a BST, but only if
            # (max_left < node.val < min_right) condition can be satisfied later on. Returning those min and max
            # makes that possible.
            return float('inf'), float('-inf'), 0
        min_left, max_left, left_size = dfs(root.left)
        min_right, max_right, right_size = dfs(root.right)
        if max_left < root.val < min_right:  # Current subtree is a valid BST
            return min(root.val, min_left), max(root.val, max_right), 1 + left_size + right_size
        # Current subtree is not a valid BST. Since no parent subtree can be a BST if one child subtree is not a valid
        # BST, returning these min and max the condition (max_left < node.val < min_right) impossible to satisfy.
        return float('-inf'), float('inf'), max(left_size, right_size)

    if not root:
        return 0
    return dfs(root)[2]
