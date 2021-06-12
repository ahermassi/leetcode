""" See description on Leetcode """

# Definition for a Node.


class Node(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        

def tree_to_doubly_list_v1(root):
    """ Step 1: in-order traversal by recursion to connect the original BST
        Step 2: connect the head and tail to make it circular
        Use a dummy node to handle corner cases
    Time complexity: O(N), since each node is processed exactly once
    Space complexity: O(N), we have to keep a recursion stack of the size of the tree height, which is O(logN) for the
    best case of completely balanced tree and O(N) for the worst case of skewed tree
    """

    def inorder(root):
        global dummy_tail
        if not root:
            return
        inorder(root.left)
        dummy_tail.right = root
        root.left = dummy_tail
        dummy_tail = dummy_tail.right
        inorder(root.right)

    if not root:
        return None
    dummy_head = Node(0)
    global dummy_tail
    dummy_tail = dummy_head
    inorder(root)
    dummy_tail.right = dummy_head.right  # After inorder() exits, dummy_tail would point to the last node in the
    # sorted circular doubly-linked list. dummy_tail's right (or next) should point to the first node which is nothing
    # but dummy_head.right
    dummy_head.right.left = dummy_tail  # The first node in the sorted list should have its left (or prev) point to
    # the last node in the list which is nothing but dummy_tail
    return dummy_head.right


def tree_to_doubly_list_v2(root):
    """ Same as previous algorithm, but iteratively. The classic iterative in-order BST traversal.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    dummy = tail = Node(0)
    stack, cur = [], root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        node = stack.pop()
        tail.right = node
        node.left = tail
        tail = node
        cur = node.right
    tail.right = dummy.right  # At this stage, 'tail' points to the last node in the doubly linked list. In order to
    # close the circle, the last node's next should point to the first node ...
    dummy.right.left = tail  # ... and the first node's prev should point to the last node.
    return dummy.right