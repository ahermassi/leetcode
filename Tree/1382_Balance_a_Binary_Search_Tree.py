""" Given a binary search tree, return a balanced binary search tree with the same node values.

A binary search tree is balanced if and only if the depth of the two subtrees of every node never differ by more than 1.

If there is more than one answer, return any of them. """


def balance_BST(root):
    """ Traverse the binary search tree in inorder to get a sorted array. The problem becomes 108- Convert Sorted Array
        to Binary Search Tree.
    Time complexity: O(N), we make exactly N calls to the recursive function and spend O(1) within each call. Don't be
    fooled by the binary search nature of the solution and think the time complexity is O(logN).
    Example: nums = [2, 3, 5, 7, 11, 13, 77, 79, 23]. Split nums into 2 halves in first call, then RECURSIVELY split
    left and right halves in the subsequent calls, resulting in N calls to the recursive function, not logN calls.
    Space complexity: O(N), to hold the nodes
    """

    def inorder(root):
        if not root:
            return
        inorder(root.left)
        nodes.append(root)
        inorder(root.right)

    def build_tree(left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        root = nodes[mid]
        root.left = build_tree(left, mid - 1)
        root.right = build_tree(mid + 1, right)
        return root

    nodes = []
    inorder(root)
    return build_tree(0, len(nodes) - 1)
