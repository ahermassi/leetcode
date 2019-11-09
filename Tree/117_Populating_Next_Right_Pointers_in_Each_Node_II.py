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
        the parent level, 'level_tail' is the tail pointer in the child level. When we are in a level, with a node in
        hand, we are looking ahead one level and connecting the children of that node.
        The parent level can be viewed as a singly linked list or queue, which we can traverse easily with a pointer.
        Connect the tail with every one of the possible nodes in child level, update it only if the connected node is
        not None. Do this one level by one level. The whole thing is quite straightforward.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    level_head = level_tail = Node(0)
    cur = root
    while cur:  # Loop for each level
        level_tail.next = cur.left  # Since level_head and level_tail point to the same object, this means that
        # level_head.next = cur.left as well. This is how level_head moves to next level
        if level_tail.next:
            level_tail = level_tail.next  # level_tail now points to a different object, not same as level_head
            # anymore. level_tail is at current node's left child
        level_tail.next = cur.right  # Connect current node's left child to right child
        if level_tail.next:
            level_tail = level_tail.next  # level_tail moves to current node's right child
        cur = cur.next  # Current node moves to its neighbor in the current level
        if not cur:  # This is key part. As said before, level_head.next = cur.left, so that current node moves to
            # its lower level's leftmost node, meaning the head of next level
            cur = level_head.next  # Remember when level_head.next = cur.left at the beginning ? This is how current
            # node moves to next level
            level_tail = level_head  # At the beginning of next iteration, level_tail.next = cur.left will result in
            # level_head.next = cur.left, which means level_head points to next level
    return root

    # tail = head = TreeLinkNode(0)
    # Afterwards in while loop, first line we make tail.next equal to cur.left which is the left node (of the current
    # node being traversed) in original tree. So in this line essentially we are also setting head.next to node.left,
    # because they are pointing towards same node.
    # tail.next = cur.left
    # Now in the last line of the function we are equating cur = head.next which is pointing to cur.left since we did
    # not move it at all in the entire loop. That is how its going to the next level.
