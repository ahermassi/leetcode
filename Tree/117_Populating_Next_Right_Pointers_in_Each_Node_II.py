""" Given a binary tree

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be
set to NULL.
Initially, all next pointers are set to NULL.
"""


# Definition for a Node.
class Node(object):
    def __init__(self, val, left, right, next):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


def connect(root):
    """ The algorithm is a BFS or level order traversal. We go through the tree level by level. node is the pointer in
        the parent level, tail is the tail pointer in the child level.
        The parent level can be viewed as a singly linked list or queue, which we can traverse easily with a pointer.
        Connect the tail with every one of the possible nodes in child level, update it only if the connected node is
        not None. Do this one level by one level. The whole thing is quite straightforward.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    node = root
    dummy_head = dummy_tail = Node(0)
    while node:  # Loop for each level
        dummy_tail.next = node.left  # Since dummy_head and dummy_tail point to the same object, this means that
        # dummy_head.next = node.left as well. This is how dummy_head moves to next level
        if dummy_tail.next:
            dummy_tail = dummy_tail.next  # dummy_tail now points to a different object, not same as dummy_head
            # anymore. dummy_tail is at node's left child
        dummy_tail.next = node.right  # Connect node's left child to right child
        if dummy_tail.next:
            dummy_tail = dummy_tail.next  # dummy_tail moves to node's right child
        node = node.next  # node moves to its neighbor in the current level
        if not node:  # This is key part. as said before, dummy_head.next = node.left, so that node moves to its upper
            # level's leftmost node's left child, meaning the head of this next level
            dummy_tail = dummy_head
            node = dummy_head.next
    return root
