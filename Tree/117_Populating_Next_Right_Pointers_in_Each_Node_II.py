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
    def __init__(self, val, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


def connect(root):
    """ The algorithm is a BFS or level order traversal. We go through the tree level by level. 'cur' is the pointer in
        the parent level, 'tail' is the tail pointer in the child level. When we are in a level, with a node in hand,
        we are looking ahead one level and connecting the children of that node.
        The parent level can be viewed as a singly linked list or queue, which we can traverse easily with a pointer.
        Connect 'tail' with every one of the possible nodes in child level, update it only if the connected node is
        not None. Do this level by level. The whole thing is quite straightforward.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    dummy = tail = Node(0)
    cur = root
    while cur:
        if cur.left:
            tail.next = cur.left  # Since dummy and tail point to the same node initially, this means that
            # dummy.next = cur.left as well. This is how dummy.next will allow us later to move to next level
            tail = tail.next
        if cur.right:
            tail.next = cur.right  # Connect current node's left child to right child
            tail = tail.next
        cur = cur.next
        if not cur:  # This is key part. As said before, dummy.next = cur.left, so that current node moves to the lower
            # level's leftmost node, meaning the head of next level
            cur = dummy.next  # 'cur' comes down one level below to the first available non null node
            tail = dummy  # 'tail' moves back to the node from where it started
            dummy.next = None  # This line detaches the dummy node so that 'tail' pointer can again point it to the
            # left node of next level which will be used then to set as 'cur' for the level after that
    return root
