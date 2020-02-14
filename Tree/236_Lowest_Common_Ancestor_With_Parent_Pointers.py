""" Given two nodes in a binary tree, design an algorithm that computes their LCA. Assume that each
node has a parent pointer. """


def lowest_common_ancestor(p, q):
    """ We know the two nodes have a common ancestor, namely the root. If the nodes are at the same depth, we can move
        up the tree in tandem from both nodes, stopping at the first common node, which is the LCA. However, if they
        are not the same depth, we need to keep the set of traversed nodes to know when we find the first common node.
        We can circumvent having to store these nodes by ascending from the deeper node to get the same depth as the
        shallower node, and then performing the tandem upward movement.
        This is similar to 160- Intersection of Two Linked Lists.
    Time complexity: O(logN) best case, O(N) worst-case of a skewed tree
    Space complexity: O(1)
    """

    def get_depth(root):
        depth = -1
        while root:
            depth += 1
            root = root.par
        return depth

    depth_p, depth_q = get_depth(p), get_depth(q)
    if depth_p > depth_q:  # Make q the deeper node in order to simplify the code
        p, q = q, p
    for _ in range(abs(depth_p - depth_q)):  # Ascend from the deeper node
        q = q.par
    while p != q:  # Now ascend both nodes until we reach the LCA
        p, q = p.par, q.par
    return p

# The previous algorithm entails traversing all the way to the root even if the nodes whose LCA is being computed are
# very close to their LCA. The following algorithm's time complexity should depend only on the distance from the nodes
# to the LCA.
# 236- Lowest Common Ancestor of a Binary Tree can benefit from this optimization as well.


def lowest_common_ancestor_optimized(p, q):
    """ The previous approach is suboptimal because it potentially processes nodes well above the LCA. We can avoid
        this by alternating moving upwards from the two nodes and storing the nodes visited as we move up in a hash
        set. Each time we visit a node, we check to see if it has been visited before.
    Time complexity: O(D0 + D1), where D0 is the distance from the LCA to the first node, and D1 is the distance from
    the LCA to the second node. In the worst case, the nodes are leaves whose LCA is the root, and we end up using O(h)
    time and space, where h is the height of the tree
    """
    ancestors = set()
    while p or q:  # Ascend tree in tandem for these two nodes
        if p:
            if p in ancestors:
                return p
            ancestors.add(p)
            p = p.parent
        if q:
            if q in ancestors:
                return q
            ancestors.add(q)
            q = q.parent

