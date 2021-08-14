""" Given the root of a binary tree, find the maximum value v for which there exist different nodes a and b where
v = |a.val - b.val| and a is an ancestor of b.

A node a is an ancestor of b if either: any child of a is equal to b or any child of a is an ancestor of b. """


def max_ancestor_diff_v1(root):
    """ Since the problem asks us the maximum difference, we only need to compare the ancestors with maximum value and
        minimum value of their descendants.
        For each root of each subtree, find the minimum value and maximum value of its left and right subtrees.
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


def max_ancestor_diff_v2(root):
    """ For a given node, we only need the maximum value and the minimum value from the root to this node.
        To achieve this, we can define a helper function to start recursion, which receives a current node and two
        integers, the maximum and minimum values along the root to the current node. In the helper, we need to update
        the maximum difference, the current maximum value, and the current minimum value seen so far.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def dfs(root, min_so_far, max_so_far):
        if not root:
            return
        # min_so_far is the minimum over all node values, which are above our node, that is the minimum among parent,
        # parent of parent, parent of parent of parent and so on
        min_so_far = min(root.val, min_so_far)
        max_so_far = max(root.val, max_so_far)
        res[0] = max(res[0], max_so_far - min_so_far)
        dfs(root.left, min_so_far, max_so_far)
        dfs(root.right, min_so_far, max_so_far)

    res = [float('-inf')]
    dfs(root, root.val, root.val)
    return res[0]
