""" Given two nodes in a binary tree, design an algorithm that computes their LCA. Assume that each
node has a parent pointer. """


def lowest_common_ancestor(root, p, q):
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
