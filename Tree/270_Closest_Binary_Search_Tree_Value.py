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
    """ Similar to 285- In-order Successor in BST.

        It makes sense to use a binary search: go left if target is smaller than current root value, and go right
         otherwise. Choose the closest to target value at each step.

    Time complexity: O(h)
    Space complexity: O(1)
    """
    candidate = root.val
    cur = root
    while cur:
        if abs(target - cur.val) < abs(target - candidate):
            candidate = cur.val
        elif abs(target - cur.val) == abs(target - candidate):
            # Edge case: target is at the same distance of two nodes. In that case, pick the smallest node value.
            candidate = min(candidate, cur.val)
        if target < cur.val:
            cur = cur.left
        else:
            cur = cur.right
    return candidate


def closest_value_v2(root, target):
    """ Let's optimize the previous solution in the case when index k of the closest element is much smaller than the
        tree height.

        We can do an iterative inorder traversal of the tree and search for the closest value at the same time. We stop
        just after identifying the closest value, there is no need to traverse the whole tree.

        The closest value is found if the target value is between two in-order elements:

                        inorder[i] <= target < inorder[i+1]

        Then the closest value is one of these 2 elements.

            - Initialize the stack and inorder predecessor value as a very small number

            - To build an inorder traversal iteratively, go left as far as you can and add all nodes on the way to
               stack.

            - Pop the last element added to the stack: node = stack.pop()

            - If target is between inorder predecessor and node.val, return the closest between these two elements

            - Set inorder predecessor value to be equal to node.val and go one step right: cur = node.right

        If we couldn't identify the closest value, that means the closest value is the last value in the inorder
        traversal, i.e. current predecessor value. Return it.

    Time complexity: O(h + k), where k is the index of the closest element in the inorder traversal of the tree.
    The worst case is a completely unbalanced tree, where we first push h elements into the stack and then pop out k
    elements.
    Space complexity: O(h), to keep the stack in the case of unbalanced tree, in the average case of a balanced tree
    the stack always contains a few elements
    """
    stack, cur = [], root
    inorder_predecessor = float('-inf')
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        node = stack.pop()
        if inorder_predecessor <= target <= node.val:
            if abs(target - inorder_predecessor) < abs(target - node.val):
                return inorder_predecessor
            if abs(target - inorder_predecessor) == abs(target - node.val):
                # Edge case: target is at the same distance of two nodes. In that case, pick the smallest node value.
                return min(inorder_predecessor, node.val)
            return node.val
        inorder_predecessor = node.val
        cur = node.right
    return inorder_predecessor

