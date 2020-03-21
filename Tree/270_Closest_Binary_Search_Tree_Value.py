""" Given a non-empty binary search tree and a target value, find the value in the BST that is closest to the target.
Note:
Given target value is a floating point.
You are guaranteed to have only one unique value in the BST that is closest to the target. """

# Definition for a binary tree node.


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def closest_value_v1(root, target):
    """ It makes sense to use a binary search: go left if target is smaller than current root value, and go right
        otherwise. Choose the closest to target value at each step. The logic is similar to 285- In-order Successor in
        BST.
    Time complexity: O(h)
    Space complexity: O(1)
    """
    candidate = root
    while root:
        if abs(root.val - target) < abs(candidate.val - target):
            candidate = root
        if root.val > target:
            root = root.left
        else:
            root = root.right
    return candidate.val


def closest_value_v2(root, target):
    """ Let's optimise the previous solution in the case when index k of the closest element is much smaller than the
        tree height.
        We can do an iterative in-order traversal of the tree and search the closest value at the same time. We stop
        just after identifying the closest value, there is no need to traverse the whole tree. The closest value is
        found if the target value is between two in-order elements: in-order[i] <= target < in-order[i + 1]. Then the
        closest value is one of these two elements.
            1- Initiate stack as an empty array and predecessor value as a very small number
            2- To build an in-order traversal iteratively, go left as far as you can and add all nodes on the way into
               stack.
            3- Pop the last element from stack node = stack.pop()
            4- If target is between predecessor and node.val, return the closest between these two elements
            5- Set predecessor value to be equal to node.val and go one step right: root = node.right
        If we couldn't identify the closest value, that means that the closest value is the last value in the in-order
        traversal, i.e. current predecessor value. Return it.
    Time complexity: O(h + k), where k is the index of closest element in the in-order traversal of the tree
    Space complexity: O(h), to keep the stack in the case of unbalanced tree, in the average case of a balanced tree
    the stack always contains a few elements
    """
    stack, pre = [], float('-inf')
    while stack or root:
        while root:
            stack.append(root)
            root = root.left
        root = stack.pop()
        if pre <= target < root.val:
            return pre if abs(pre - target) < abs(root.val - target) else root.val
        pre = root.val
        root = root.right
    return pre

