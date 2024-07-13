""" See description on Leetcode """

# Definition for a Node.


class Node(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        

def tree_to_doubly_list_v1(root):
    """ The standard inorder traversal follows left -> node -> right order, where left and right parts are the recursion
         calls, and node part is where all processing is done.

         Processing here is basically to link the previous node with the current one, and because of that we have to
         track the last node which is the largest node in a new doubly linked list so far. We have to keep the first, or
         the smallest, node as well to close the ring of the doubly linked list.

         We use a dummy head node to handle corner cases.

         By definition, an in-place algorithm is an algorithm which transforms input using no auxiliary data structure.
         This implementation uses no auxiliary data structure and hence it's an in-place solution.

    Time complexity: O(N), each node is processed exactly once
    Space complexity: O(N), we have to keep a recursion stack of the size of the tree height, which is O(logN) for the
    best case of a completely balanced tree and O(N) for the worst case of a skewed tree
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
    # After inorder() exits, dummy_tail points to the last node in the sorted circular doubly-linked list. dummy_tail's
    # right (or next) should point to the first node which is dummy_head.right
    dummy_tail.right = dummy_head.right
    # The first node in the sorted list should have its left (or prev) point to the list's last node which is dummy_tail
    dummy_head.right.left = dummy_tail
    return dummy_head.right


def tree_to_doubly_list_v2(root):
    """ Same as previous algorithm, but iteratively. The classic iterative in-order BST traversal.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    dummy_head = dummy_tail = Node(0)
    stack, cur = [], root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        node = stack.pop()
        dummy_tail.right = node
        node.left = dummy_tail
        dummy_tail = dummy_tail.right
        cur = node.right
    dummy_tail.right = dummy_head.right  # At this stage, 'tail' points to the last node in the doubly linked list.
    # In order to close the circle, the last node's next should point to the first node ...
    dummy_head.right.left = dummy_tail  # ... and the first node's prev should point to the last node.
    return dummy_head.right