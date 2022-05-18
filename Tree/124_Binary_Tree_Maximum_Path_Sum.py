""" Given a non-empty binary tree, find the maximum path sum.
For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the
parent-child connections. The path must contain at least one node and does not need to go through the root. """

# Great visual explanation:
# https://leetcode.com/problems/binary-tree-maximum-path-sum/discuss/603423/Python-Recursion-stack-thinking-process-diagram

# Video explanation: https://www.youtube.com/watch?v=Hr5cWUld4vU


def max_path_sum(root):
    """ First, let's simplify the problem and implement a function max_gain(node) which takes a node as an argument and
         computes a maximum contribution that this node and one/zero of its subtrees could add. In other words, it's a
         maximum gain we could have including the node (and maybe one of its subtrees) into the path.

        Hence, if we would know for sure that the max path contains root, the problem would be solved as max_gain(root).
        Unfortunately, the max path does not need to go through the root.

        That means we need to modify the above function and check at each step what is better : to continue the
        current path or to start a new path with the current node as the highest node in this new path.

        We'll implement a function max_path_sum_involving_node(node). The idea is to update each node with the biggest,
        positive cumulative sum gathered by its children:

            - If both contributions are negative, no value is added
            - If both are positive, only the biggest one is added so that we don't include both children during the
               rest of the tree exploration
            - Leaves return their own values, and we recursively work our way upwards

        A global maximum sum variable 'res' is maintained so that every path can be individually checked while updating
        nodes. The key is to always choose the maximum cumulative sum path while updating the global maximum value
        from the leaves upwards.

        Why do we return root.val + max(left, right)? If the current node is at level 2, and we want to go one level up,
        say level 1, we can NOT keep both the left path and right path. We just gotta choose one path out of these two
        because a node can only appear in the sequence AT MOST ONCE. If we include both left and right branches at every
        node fork, we'd end up with a path that contains the entire tree which is an invalid path.

        When we're looking at left and right branches of a node, we only care about gains we can make. This means if the
        sum of all the nodes on either of the branches of a particular node is less than 0, that branch is not worth exploring at all.

        It is important to understand the difference between looking for the maximum path INVOLVING the current node in
        process and what we return from the node which starts the recursion stack. When going back up the recursion
        stack, we cannot just return the max value. We can only form a path involving the parent node as the root
        with EITHER of the root's branches. Therefore, we have to choose the max gain between the gain from left branch
        and the gain from right branch.

        A valid path is a "straight line" that connects all the nodes, in other words, it can't "fork".

        Each node actually has two roles when it comes to max_path_sum_involving_node(node) function. When processing
        the final result 'res', the node is treated as the highest/pivot point of a path. When calculating its return
        value, it is only PART OF a path (left or right part), and this return value will be used to calculate path sum
        of other paths with some other nodes when the result bubbles up in the recursion stack.

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

        Here there are multiple possibilities, and we need to take care of the following 4 PATHS that could be our max:
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

    Time complexity: O(N)
    Space complexity: O(h)
    """

    def max_path_sum_involving_node(root):
        # max_path_sum_involving_node(root) is the maximum path sum we can get involving the node 'root' as the root
        if not root:
            return 0
        left, right = max_path_sum_involving_node(root.left), max_path_sum_involving_node(root.right)
        left, right = max(0, left), max(0, right)  # Only add positive contributions. We only care about gains in sum.
        # The important thing is that we can only get any sort of gain IF our branches are not below zero. If they
        # are below zero, why do we even bother considering them? Just pick 0 in that case. If a branch's gain is
        # less than 0, that means we should not connect current node with that branch, since it will decrease the
        # value of the path that goes through current node anyway.
        cur_max_path = root.val + left + right
        # Check if cumulative sum at current node > global max sum so far. This evaluates a candidate path.
        res[0] = max(res[0], cur_max_path)
        return root.val + max(left, right)  # Add to the current node ONLY one of the children contributions in order
        # to maintain the constraint of considering only paths. Otherwise, we would be exploring the whole tree which
        # yields an invalid path.

    res = [float('-inf')]
    max_path_sum_involving_node(root)
    return res[0]
