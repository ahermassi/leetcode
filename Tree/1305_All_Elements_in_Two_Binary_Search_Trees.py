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


def get_all_elements_v2(root1, root2):
    """ A more elegant way here is to iteratively build inorder traversals for both trees in parallel, and at each step
        update the output list by the smallest value between both trees. That will be a one pass solution.
    Time complexity: O(N + M)
    Space complexity: O(N + M)
    """
    stack1, stack2 = [], []
    res = []
    while stack1 or stack2 or root1 or root2:
        # Update both stacks by going left till we no longer can
        while root1:
            stack1.append(root1)
            root1 = root1.left
        while root2:
            stack2.append(root2)
            root2 = root2.left
        # Add the smallest value into output, pop it from the stack, and then go one step right
        if not stack2 or stack1 and stack1[-1].val < stack2[-1].val:
            node = stack1.pop()
            res.append(node.val)
            root1 = node.right
        else:
            node = stack2.pop()
            res.append(node.val)
            root2 = node.right
    return res
