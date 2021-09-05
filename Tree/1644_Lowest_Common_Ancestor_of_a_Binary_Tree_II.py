""" Given the root of a binary tree, return the lowest common ancestor (LCA) of two given nodes, p and q. If either
node p or q does not exist in the tree, return null. All values of the nodes in the tree are unique.

According to the definition of LCA on Wikipedia: "The lowest common ancestor of two nodes p and q in a binary tree T
is the lowest node that has both p and q as descendants (where we allow a node to be a descendant of itself)".
A descendant of a node x is a node y that is on the path from node x to some leaf node. """


def lowest_common_ancestor_v1(root, p, q):
    """ Similar to 236- Lowest Common Ancestor of a Binary Tree.
        If we have parent pointers for each node, we can traverse back from p and q to get their ancestors. The first
        common node we get during this traversal would be the LCA node. We can save the parent pointers in a dictionary
        as we traverse the tree. Note that if after we traverse the entire tree and either p or q wasn't found, we
        can return immediately.
        Once we have found both p and q, we get all the ancestors for p using the parent dictionary and add to a set
        called 'p_ancestor'. Similarly, we traverse through ancestors for node q. If the ancestor is present in the
        ancestors set for p, this means this is the first ancestor common between p and q (while traversing UPWARDS)
        and hence this is the LCA node.
    Time complexity: O(N), in the worst case we might be visiting all the nodes of the binary tree
    Space complexity: O(N), in the worst case space utilized by the stack, the parent pointer dictionary and the
    ancestor set, would be N each, since the height of a skewed binary tree could be N
    """
    parent, stack = {}, [(root, None)]
    while stack:
        node, par = stack.pop()
        parent[node] = par
        stack.extend([(kid, node) for kid in (node.left, node.right) if kid])
    if p not in parent or q not in parent:
        return None
    p_ancestor = set()
    while p:
        p_ancestor.add(p)
        p = parent[p]
    while q not in p_ancestor:
        q = parent[q]
    return q
