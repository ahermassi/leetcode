""" Given the root of a binary tree, the depth of each node is the shortest distance to the root.

Return the smallest subtree such that it contains all the deepest nodes in the original tree.

A node is called the deepest if it has the largest depth possible among any node in the entire tree.

The subtree of a node is tree consisting of that node, plus the set of all descendants of that node. """

from collections import deque


def subtree_with_all_deepest_v1(root):
    """ The problem statement can be reformulated as:
            If the deepest level has only one node, return that node. Otherwise, return the lowest common ancestor of
            all the nodes in the deepest level.
        We identify the nodes of the tree whose descendants are the deepest nodes. To do this, we have to annotate the
        height (not depth) of each node. We can do this with a depth first search. Afterwards, we will use that
        annotation to help us find the answer:
            - If both the left and right child of a node have the same height, then the answer is this parent node.
            - Otherwise, if some child has a larger height, then the answer is that child.
            - Otherwise, the answer for this subtree doesn't exist.
        At each node, we keep a pair (height_of_node, node). At a given node, if we realize that the
        left_height == right_height, it means we have found the smallest subtree with all deepest nodes rooted at the
        current node. If left_height > right_height, it means the smallest subtree with all deepest nodes must be
        rooted at left child. If right_height > left_height, it means the smallest subtree with all deepest nodes must
        be rooted at right child.
        Which traversal allows us to traverse from bottom-up? Postorder! So we use it in the code.
        To summarize:
        If left subtree height is greater, then the result is whatever returned by the left as it has highest depth
        elements. Similarly, if right subtree height is greater, then the result is whatever returned by the right as
        it has highest depth elements. If heights of both left and right subtrees are equal, then the current node is
        the lowest common ancestors of the deepest leaves.
    Time complexity: O(N), where N is the number of nodes in the tree
    Space complexity: O(N)
    """

    def dfs(root):
        # dfs(root) answers two questions:
        # 1- What's the height of node 'root' ?
        # 2- What's the root of the smallest subtree that contains ALL the deepest nodes such that it's a subtree of
        # the tree rooted at node 'root' ? Smallest here is synonymous of the lowest common ancestor.
        if not root:
            return 0, None
        left_height, smallest_left_subtree = dfs(root.left)
        right_height, smallest_right_subtree = dfs(root.right)
        cur_height = max(left_height, right_height) + 1
        if left_height == right_height:  # Left and right subtrees have an equal height, which means the deepest node
            # in the left subtree has the same depth as the deepest node in the right subtree. As such, we should
            # return the current node as it is the root of the current subtree that contains the deepest nodes on the
            # left and right subtree and is the LCA.
            return cur_height, root
        if left_height > right_height: # Left subtree has a greater height than the right subtree. This means ALL the
            # deepest nodes can only be situated in the (last level of) left side. Therefore, search to the left.
            return cur_height, smallest_left_subtree
        return cur_height, smallest_right_subtree

    return dfs(root)[1]


def subtree_with_all_deepest_v2(root):
    """ Find all deepest nodes by traversing the tree using BFS. The root of the smallest subtree with all deepest
        nodes is nothing but the LCA of all the deepest nodes. Finding LCA of all nodes at the same level is equivalent
        to finding LCA of the leftmost and rightmost node. Therefore, we keep track of the leftmost node and the
        rightmost node while doing BFS and finally return their LCA.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def lowest_common_ancestor(root, left, right):
        if not root or root == left or root == right:
            return root
        left_search = lowest_common_ancestor(root.left, left, right)
        right_search = lowest_common_ancestor(root.right, left, right)
        if left_search and right_search:
            return root
        return left_search or right_search

    leftmost_node = rightmost_node = None
    queue = deque([root])
    while queue:
        n = len(queue)
        for i in range(n):
            node = queue.popleft()
            if i == 0:
                leftmost_node = node
            if i == n - 1:
                rightmost_node = node
            queue.extend([kid for kid in (node.left, node.right) if kid])
    return lowest_common_ancestor(root, leftmost_node, rightmost_node)


def subtree_with_all_deepest_v3(root):
    """ Similar to the first solution, more straightforward, but unnecessarily recomputes the heights. It checks
        whether the children of the current node have an equal height. If so, then the current node is the lowest
        common ancestor of all deepest leaves. If not, we recall the function on the taller subtree.
    Time complexity: O(N^2)
    Space complexity: O(N)
    """

    def height(root):
        if not root:
            return 0
        return 1 + max(height(root.left), height(root.right))

    if not root:
        return None
    left_height, right_height = height(root.left), height(root.right)
    if left_height == right_height:
        return root
    if left_height > right_height:
        return subtree_with_all_deepest_v3(root.left)
    return subtree_with_all_deepest_v3(root.right)

