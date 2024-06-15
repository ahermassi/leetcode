""" Given the root of a Binary Search Tree (BST), return the minimum absolute difference between the values of any two
different nodes in the tree. """


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def get_minimum_difference_v1(root):
    """ Let's try to solve a simpler problem first. Given a sorted array of integers, find the minimum difference
        between any two integers in the array. To solve this problem, we don't need to check every pair of integers.
        Instead, checking the difference between every two consecutive integers would work. This is because the array
        is sorted. We will make use of this to solve the original problem.

        A unique property of a binary search tree is that an inorder traversal handles the nodes in sorted order.

        Iterate over inorder nodes' values starting from index 1, and for each element at index i, find the difference
        with the element at index i-1 and update the min difference variable accordingly.


    Time complexity: O(N), we visit every node exactly once and iterate over the list of size N to find the minimum
    difference
    Space complexity: O(N), for the call stack and the list of values. The maximum number of active stack calls at a
    time would be the tree's height, which in the worst case would be O(N) when the tree is skewed.
    """

    def inorder(root):
        if not root:
            return
        inorder(root.left)
        values.append(root.val)
        inorder(root.right)

    res, values = float('inf'), []
    inorder(root)
    n = len(values)
    for i in range(1, n):
        res = min(res, values[i] - values[i - 1])
    return res


def get_minimum_difference_v2(root):
    """ As we can notice in the previous approach, we only need the immediate inorder predecessor of any node to
        calculate the minimum difference. The rest of the nodes will not be needed and are stored unnecessarily in the
        list.

        Thus, we can avoid storing elements in a list if we can find the difference between consecutive nodes on the fly
        during inorder traversal. For each node in the tree, we need the previous node we have handled, and then we can
        find the difference. This can be done using another variable prev that will store the value of the node we
        processed previously in the inorder traversal. This way, we don't have to store the elements in an array and at
        the same time, don't have to re-iterate over the nodes again.


    Time complexity: O(N), we visit every node exactly once
    Space complexity: O(N), for the call stack. The maximum number of active stack calls at a
    time would be the tree's height, which in the worst case would be O(N) when the tree is skewed.
    """

    def inorder(root):
        if not root:
            return
        inorder(root.left)
        res[0] = min(res[0], root.val - prev[0])
        prev[0] = root.val
        inorder(root.right)

    res, values = [float('inf')], []
    prev = [float('-inf')]
    inorder(root)
    return res[0]


def get_minimum_difference_v3(root):
    """ The same as the previous solution but using an iterative inorder traversal


    Time complexity: O(N), we visit every node exactly once
    Space complexity: O(N), for the stack
    """
    res = float('inf')
    prev = float('-inf')
    stack, cur = [], root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        node = stack.pop()
        res = min(res, node.val - prev)  # No need for abs(); the nodes are processed in order
        prev = node.val
        cur = node.right
    return res
