""" Given the root of a binary tree, find the maximum value v for which there exist different nodes a and b where
v = |a.val - b.val| and a is an ancestor of b.

A node a is an ancestor of b if either: any child of a is equal to b or any child of a is an ancestor of b. """


def max_ancestor_diff_v1(root):
    """ For each root of each subtree, find the minimum value and maximum value of its left and right subtrees.
        The maximum difference between the subtree root and one of its descendants is the max of:
            - The current max calculated so far
            - The (absolute) difference between the root value and the smallest value amongst all its descendants
            - The (absolute) difference between the root value and the largest value amongst all its descendants
    Time complexity: O(N), since we visit all nodes once
    Space complexity: O(N), since we need stacks to do recursion, and the maximum depth of the recursion is the height
    of the tree, which is O(N) in the worst case and O(log(N)) in the best case
    """

    def dfs(root):
        if not root:
            return float('inf'), float('-inf')
        if not root.left and not root.right:
            return root.val, root.val
        min_left, max_left = dfs(root.left)  # Smallest and largest value in left subtree
        min_right, max_right = dfs(root.right)  # Smallest and largest value in right subtree
        min_descendant = min(min_left, min_right)  # Smallest value amongst all descendants (in left + right subtrees)
        max_descendant = max(max_left, max_right)  # # Largest value amongst all descendants (in left + right subtrees)
        res[0] = max(res[0], abs(root.val - min_descendant), abs(root.val - max_descendant))
        # Return a pair:
        # (smallest value in the entire tree rooted at 'root', largest value in the entire tree rooted at 'root')
        return min(root.val, min_descendant), max(root.val, max_descendant)

    res = [float('-inf')]
    dfs(root)
    return res[0]
