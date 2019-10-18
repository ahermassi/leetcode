""" See description on Leetcode """

# Definition for a Node.


class Node(object):
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right
        

def tree_to_doubly_list_v1(root):
    """ Step1: in-order traversal by recursion to connect the original BST
        Step2: connect the head and tail to make it circular
        Use a dummy node to handle corner cases
    Time complexity: O(N) since each node is processed exactly once
    Space complexity: O(N), we have to keep a recursion stack of the size of the tree height, which is O(logN) for the
    best case of completely balanced tree and O(N) for the worst case of skewed tree.
    """

    def helper(node):
        global prev
        if not node:
            return
        helper(node.left)
        prev.right = node
        node.left = prev
        prev = node
        helper(node.right)

    if not root:
        return None
    dummy = Node(0, None, None)
    global prev
    prev = dummy
    helper(root)
    prev.right = dummy.right
    dummy.right.left = prev
    return dummy.right