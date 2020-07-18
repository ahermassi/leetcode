""" Given a non-empty binary tree, find the maximum path sum.
For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the
parent-child connections. The path must contain at least one node and does not need to go through the root. """

# Great visual explanation:
# https://leetcode.com/problems/binary-tree-maximum-path-sum/discuss/603423/Python-Recursion-stack-thinking-process-diagram


def max_path_sum(root):
    """ The idea is to update each node with the biggest, positive cumulative sum gathered by its children:
            - If both contributions are negative, no value is added
            - If both are positive, only the biggest one is added so that we don't include both children during the
              rest of the tree exploration
            - Leaves return their own values and we recursively work our way upwards
        A global maximum sum variable 'res' is maintained so that every path can be individually checked while updating
        nodes.
        The key is to always choose the maximum cumulative sum path while updating the global maximum value from the
        leaves upwards.
        Now consider the following example:
            10
           /  \
         null null
        In this simple case, we know that the max sum would be just the root node itself and the answer would be 10.
        So for all leaf nodes the max path sum is the value of the node itself.
        Now let's consider the following example:
            20
           /  \
          10  30
        Here there are multiple possibilities and we need to take care of the following 4 PATHS that could be our max:
        1- The root itself : 20
        2- The root with the maximum from its left subtree:
            20
	       /
         10

        3- 2- The root with the maximum from its right subtree:
            20
		      \
	           30

	    4- The root with its left, right and itself:
	        20
           /  \
          10  30

        Why do we return max(root.val + left, root.val + right)? If the current node is at level 2 and we want to go
        one level up, say level 1, we can NOT keep both the left paths and right paths. We just gotta choose one path
        out of these two.
    Time complexity: O(N)
    Space complexity: O(h)
    """

    def dfs(root):  # dfs(root) is the maximum path sum we can get involving the node 'root' as the root
        if not root:
            return 0
        left, right = dfs(root.left), dfs(root.right)
        left, right = max(0, left), max(0, right)  # Only add positive contributions. We only care about gains in sum.
        # The important thing is that we can only get any sort of gain IF our branches are not below zero. If they are
        # below zero, why do we even bother considering them? Just pick 0 in that case
        res[0] = max(res[0], root.val + left + right)  # Check if cumulative sum at current node > global max sum so
        # far. This evaluates a candidate path
        return max(root.val + left, root.val + right)  # Add to the current node ONLY one of the children contributions
        # in order to maintain the constraint of considering only paths. Otherwise, we would be exploring the whole
        # tree which is against the problem definition

    res = [float('-inf')]
    dfs(root)
    return res[0]
