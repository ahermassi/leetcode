""" Given a binary tree containing digits from 0-9 only, each root-to-leaf path could represent a number.
An example is the root-to-leaf path 1->2->3 which represents the number 123.
Find the total sum of all root-to-leaf numbers. """


def sum_numbers_v1(root):
    """ Recursive pre-order traversal is extremely simple: follow Root->Left->Right direction, i.e. do all the business
        with the node (update the current total and root-to-leaf sum), and then do the recursive calls for the left and
        right child nodes.
    Time complexity: O(N)
    Space complexity: O(h), to keep the recursion stack, where h is tree height
    """

    def dfs(root, total):
        if not root:
            return
        total = total * 10 + root.val
        if not root.left and not root.right:
            res[0] += total
        else:
            dfs(root.left, total)
            dfs(root.right, total)

    res = [0]
    dfs(root, 0)
    return res[0]


def sum_numbers_v2(root):
    """ Here we implement standard iterative pre-order traversal with the stack.
    Time complexity: O(N)
    Space complexity: O(h), to keep the recursion stack, where h is tree height
    """
    if not root:
        return 0
    res, stack = 0, [(root, 0)]
    while stack:
        node, total = stack.pop()
        total = total * 10 + node.val
        if not node.left and not node.right:
            res += total
        else:
            stack.extend([(child, total) for child in (node.left, node.right) if child])
    return res

