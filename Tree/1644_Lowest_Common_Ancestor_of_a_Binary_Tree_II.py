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


def lowest_common_ancestor_v2(root, p, q):
    """ Similar to the second solution of 236- Lowest Common Ancestor of a Binary Tree, but with some tweaks.
        Question 236 has two important premises:
            1- It is guaranteed that both p and q are in the tree
            2- A node can be a descendant of itself
        Because of these premises, we can return either p OR q as soon as we find one of them.
        But for this question, the premises are different:
            1- It is NOT guaranteed that both p and q are in the tree
            2- A node can still be a descendant of itself.
        Hence:
            - We need a way to record if we've seen both p and q
            - We need to traverse the entire tree even after we've found one of the nodes p/q
        Use can use either boolean or integers as flags. Moreover, we need to recurse on the left and right subtrees
        before checking if the current node matches p or q. Otherwise, we'd return and won't traverse the rest of the
        tree. It is important that we keep searching the entire tree: We cannot instantly return the node we found
        because we don't know if both p and q exist in the tree.
    Time complexity: O(N)
    Space complexity: O(h), or O(N) in the case of a skewed tree
    """

    def find_lca(root):
        if not root:
            return None
        search_left = find_lca(root.left)  # This is to find nodes p and q NOT the LCA
        search_right = find_lca(root.right)
        if root == p or root == q:  # Once we found either p or q, we have to update the counter
            nodes_found[0] += 1
            return root
        if search_left and search_right:  # # We got something back on the left AND right. That means this node is the
            # LCA because our recursion returns from bottom to top, so we return what we hold: 'root'
            return root
        # Either one of the children returned a node, meaning either p or q found on left or right branch. Return
        # whatever we got.
        return search_left or search_right

    nodes_found = [0]
    lca = find_lca(root)
    return lca if nodes_found[0] == 2 else None
