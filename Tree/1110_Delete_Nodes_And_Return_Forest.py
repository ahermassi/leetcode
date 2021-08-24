""" Given the root of a binary tree, each node in the tree has a distinct value.

After deleting all nodes with a value in to_delete, we are left with a forest (a disjoint union of trees).

Return the roots of the trees in the remaining forest. You may return the result in any order. """


def del_nodes_v1(root, to_delete):
    """ We need to keep the tree intact to traverse all the way down first. Then on the way back up, we check if the
        node's value is in the list of nodes to delete. If it is, we add the subtrees to the result and return None to
        the next level up. Otherwise, we return the current node. We then we use the returned values on the level up to
        either keep the tree connected or break it up.
        To remove a node, the child needs to notify its parent about the child's existence. To determine whether a
        node is a root node in the final forest, we need to know whether the node needs to be removed (which is
        trivial).
    Time complexity: O(N)
    Space complexity: O(h)
    """

    def dfs(root):
        # dfs(root) takes a subtree root and returns either the same root back if the root is not to be deleted, or
        # None if the subtree was detached.
        if not root:
            return
        # We assign the new values to root.left and root.right. Keep in mind that the assignment will be actually
        # completed after all recursive calls below return values, so it will be done on the way up.
        root.left = dfs(root.left)
        root.right = dfs(root.right)
        # At this point, the subtrees below have been processed, so we need to process the current value.
        if root.val in to_delete:
            res.extend([kid for kid in (root.left, root.right) if kid])  # Add the subtrees below into the result forest
            return None
        return root

    to_delete = set(to_delete)
    res = []
    if root.val not in to_delete:
        res.append(root)
    dfs(root)
    return res


def del_nodes_v2(root, to_delete):
    """ If a node is root (has no parent) and isn't deleted, when will we add it to the result.
    Time complexity: O(N)
    Space complexity: O(h)
    """

    def dfs(root, is_root):
        # is_root: The node's parent is deleted. The node is the root node of the tree in the forest.
        if not root:
            return None
        root_deleted = root.val in to_delete
        if is_root and not root_deleted:
            res.append(root)  # We only need to add the root node of every forest
        root.left = dfs(root.left, root_deleted)
        root.right = dfs(root.right, root_deleted)
        return None if root_deleted else root

    to_delete = set(to_delete)
    res = []
    dfs(root, True)
    return res

