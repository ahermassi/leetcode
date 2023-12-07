""" Given a non-empty binary tree, find the maximum path sum.
For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the
parent-child connections. The path must contain at least one node and does not need to go through the root. """

# Great visual explanation:
# https://leetcode.com/problems/binary-tree-maximum-path-sum/discuss/603423/Python-Recursion-stack-thinking-process-diagram


# Video explanation: https://www.youtube.com/watch?v=Hr5cWUld4vU
def max_path_sum(root):
    """ A path is a continuous sequence of nodes connected to each other. There will always be at least one node in a
         path. In a path, except for the starting and ending nodes, every node is connected to two other nodes in the
         sequence. These two nodes could either be the node's children, or one of them could be a child, and the other
         could be the parent node. In other words, no node can have MORE THAN TWO connections in this sequence.
         Each node contains a value, which could be negative, zero, or positive.

         Because the values could be negative or positive, a path sum could also be negative or positive. Every
         combination of two nodes in a tree can form a path by using the sequence of all nodes between them. In fact,
         every node in itself can also be considered a path (a path needs at least one node).

         One way to find the maximum path sum would be to look at all possible paths, calculate their path sums, and
         then find the maximum path sum. However, this would be a "brute force" approach. If there are N nodes in the
         tree, creating all the paths and computing their path sums would take O(N^2) time. We can do better than this.

         Consider a scenario where the path with the highest sum passes through the tree's root. There could be four
         possibilities:

            - The path starts at the root and goes down through the root's left child. We don't know how long the path
               is, but it could extend to the bottom of the left subtree.
            - The path starts at the root and goes down through the root's right child. Very similar to the previous
               case, but the direction is toward the right.
            - The path involves both the left and the right child.
            - The path doesn't involve any child. The root itself is the only element of the path with maximum sum.

        We know that the path contains the root. Therefore, in the beginning, we can assume that the path sum is the
        root node's value. To find the maximum path sum, we determine if there is a viable path leading down through the
        left or the right subtree. Please remember that a node can have negative or positive values. So a path sum
        contributed by a subtree could also be negative or positive. It would make sense to consider a path sum
        contributed by a subtree only if it is positive. If not, we can safely ignore it. In other words:

                        The path goes down the left or the right subtree only if we see a gain in the path sum

        This means we must first determine the gain in the path sum contributed by the left and the right subtree. Once
        we have both, we decide whether to include their contribution. We can see that we need to process the children
        before we process a node. This indicates that we need to perform a post-order traversal of the tree because, in
        post-order, children are processed before the parent.

         To implement post-order traversal, we implement a recursive function max_gain(node) which takes a node as an
         argument and computes the maximum contribution that this node and one/zero of its subtrees could add. In other
         words, it's a maximum gain we could have including the node (and maybe one of its subtrees) into the path.

        Hence, if we would know for sure that the max path contains root, the problem would be solved as max_gain(root).
        Unfortunately, the max path does not need to go through the root.

        We slightly tweak our algorithm to include the case when the path sum doesn't pass through the root. Now, in
        addition to returning the path sum gain contributed by the subtree, the recursive function also keeps track of
        the global maximum path sum. We update the maximum path sum whenever we find a new maximum.

        That means we need to modify the above function and check at each step what is better: to continue the
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

        The path sum gain contributed by the subtree can be derived from a path that includes at most one child of the
        Why can't we include both children? If we include both children in the path, the path would have to make a fork
        at the root. The root is already connected to its parent. Now, if we include both children as well, with three
        connections, it wouldn't be a valid path anymore. Therefore, we can say that the path would consist of at most
        one child of the root.

        A node can only appear in the sequence AT MOST ONCE. If we include both left and right branches at every node
        fork, we'd end up with a path that contains the entire tree which is an invalid path.

        When we're looking at left and right branches of a node, we only care about gains we can make. This means if the
        sum of all the nodes on either of the branches of a particular node is less than 0, that branch is not worth
        exploring at all.

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

        A note on the base case:
        Let's say our recursive algorithm reaches a node with no left child. Because there is no left child, our path
        cannot go toward the left subtree. In other words, the gain from the left subtree is 000. So, when the function
        is called on the non-existent child of the node, it returns 0. This would be true for a non-existent right child
        as well. Therefore, we can safely say that the base case is when the root is null.

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

    Time complexity: O(N), each node in the tree is visited only once. During a visit, we perform constant time
    operations, including two recursive calls and calculating the max path sum for the current node.
    Space complexity: O(h), the recursive call stack can go as deep as the tree's height. In the worst case, the tree is
    a linked list, so the height is N.
    """

    def max_gain_at_node(root):
        # max_path_sum_involving_node(root) is the maximum path sum we can get involving the node 'root' as the root
        if not root:
            return 0
        left_gain, right_gain = max_gain_at_node(root.left), max_gain_at_node(root.right)
        left_gain, right_gain = max(0, left_gain), max(0, right_gain)
        # Only add positive contributions. We only care about gains in sum.
        # The important thing is that we can only get any sort of gain IF our branches are not below zero. If they
        # are below zero, why do we even bother considering them? Just pick 0 in that case. If a branch's gain is
        # less than 0, that means we should not connect current node with that branch, since it will decrease the
        # value of the path that goes through current node anyway.
        cur_max_path = root.val + left_gain + right_gain
        # Check if cumulative sum at current node > global max sum so far. This evaluates a candidate path.
        res[0] = max(res[0], cur_max_path)
        # Add to the current node ONLY one of the children contributions in order to maintain the constraint of
        # considering only paths. Otherwise, we would be exploring the whole tree which yields an invalid path.
        return root.val + max(left_gain, right_gain)

    res = [float('-inf')]
    max_gain_at_node(root)
    return res[0]
