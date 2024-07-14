""" Given a binary search tree, return a balanced binary search tree with the same node values.

A binary search tree is balanced if and only if the depth of the two subtrees of every node never differ by more than 1.

If there is more than one answer, return any of them. """


def balance_BST(root):
    """ We call such BSTs balanced BSTs. Balanced BSTs are efficient because they keep the tree height low, usually in
         logarithmic proportion to the number of nodes. This balance allows operations like insertion, deletion, and
         lookup to be done in logarithmic time on average. Keeping the tree balanced prevents it from becoming too deep,
         which would otherwise slow these operations down to linear time. This efficiency makes balanced BSTs ideal for
         tasks that need fast updates and quick searches.

         We can perform an inorder traversal of the tree and store all the BST nodes in a sorted array , then
         reconstruct the BST from scratch. Storing the values in sorted order ensures the new tree maintains the BST
         properties.

         The stored values in the array have a convenient property: for any given element that serves as the root, all
         elements to its left belong to the left subtree, and all elements to its right belong to the right subtree.
         To construct a balanced BST, we pick the middle element of the array as the root, ensuring the number of
         elements in the left and right subtrees differs by at most one. We then recursively apply the same process to
         the left and right sub-arrays to build the left and right subtrees. This approach ensures the balanced property
         of the BST.

        The problem becomes 108- Convert Sorted Array to Binary Search Tree.

    Time complexity: O(N), we make exactly N calls to the recursive function and spend O(1) within each call. Don't be
    fooled by the binary search nature of the solution and think the time complexity is O(logN).
    Example: nums = [2, 3, 5, 7, 11, 13, 77, 79, 23]. Split nums into 2 halves in first call, then RECURSIVELY split
    left and right halves in the subsequent calls, resulting in N calls to the recursive function, not logN calls.
    Space complexity: O(N), to store the nodes' values and the call stack of inorder function where in the worst case
    the recursion stack can grow to O(N) for a skewed BST. For balanced BST construction, there is no case of skewed
    tree because we're creating a balanced BST from the start by picking the middle element every time, so the recursion
    stack requires O(logN) space because the tree is height-balanced.
    """

    def inorder(root):
        if not root:
            return
        inorder(root.left)
        inorder_values.append(root)
        inorder(root.right)

    def build_tree(left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        root = inorder_values[mid]
        root.left = build_tree(left, mid - 1)
        root.right = build_tree(mid + 1, right)
        return root

    inorder_values = []
    inorder(root)
    return build_tree(0, len(inorder_values) - 1)
