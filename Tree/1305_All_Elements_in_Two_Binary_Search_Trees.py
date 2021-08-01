""" Given two binary search trees root1 and root2.

Return a list containing all the integers from both trees sorted in ascending order. """


def get_all_elements_v1(root1, root2):
    """ Traverse each tree, using inorder traversal, in this way for BST result will be sorted list.
        Now, we have two sorted lists, and all we need to do is to merge them using the same routine we use in merge
        sort.
    Time complexity: O(N + M), where N and M are the respective sizes of the two BSTs
    Space complexity: O(N + M), for the call stacks and the two lists
    """

    def inorder(root, vals):
        if not root:
            return
        inorder(root.left, vals)
        vals.append(root.val)
        inorder(root.right, vals)

    vals1, vals2 = [], []
    inorder(root1, vals1)
    inorder(root2, vals2)
    i, j, res = 0, 0, []
    n, m = len(vals1), len(vals2)
    while i < n and j < m:
        if vals1[i] < vals2[j]:
            res.append(vals1[i])
            i += 1
        else:
            res.append(vals2[j])
            j += 1
    if i < n:
        res.extend(vals1[i:])
    elif j < m:
        res.extend(vals2[j:])
    return res
