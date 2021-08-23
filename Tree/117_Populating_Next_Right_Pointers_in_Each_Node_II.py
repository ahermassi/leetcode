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
    """ The algorithm is a BFS or level order traversal. We go through the tree level by level.
        Once we are done establishing the next pointers between the nodes, don't they kind of represent a linked list?
        After the next connections are established, all the nodes on a particular level actually form a linked list via
        these next pointers. Based on this idea, we have the following intuition for our algorithm:

            We only move on to the level (N + 1) when we are done establishing the next pointers for the level N. So,
            since we have access to all the nodes on a particular level via the next pointers, we can use these next
            pointers to establish the connections for the next level or the level containing their children.

        When we go over the nodes of a particular level, their next pointers are already established. This is what
        helps get rid of the queue data structure and helps save space. To start on a particular level, we just need
        the leftmost node. From there on its just a linked list traversal.
        'cur' is the pointer in the parent/current level. This is just the variable we use to traverse all the nodes on
        the current level. It starts off with leftmost and then follows the next pointers all the way to the very end.
        'next_level_tail' is the tail pointer in the child level. This node is important to discover on each level
        since this would act as our head of the linked list and we will start our traversal of all the nodes on a level
        from this node onwards.
        When we are in a level, with a node in hand, we are looking ahead one level and connecting the children of that
        node. Connect 'next_level_tail' with every one of the possible nodes in child level, and update it only if the
        connected node is not null. Do this for every level.
        Once we are done with the current level, we move on to the next one. One last thing that's left here to update
        'next_level_tail' node. We need that node to start traversal on a particular level. Think of it as the head of
        the linked list. This is easy to do by using 'next_level_head' pointer. Whenever we set the value for
        'next_level_head' pointer for the first time corresponding to a level i.e. whenever we set it to its first
        node, we also set 'next_level_tail' to that node.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    next_level_head = next_level_tail = Node(0)  # next_level_head is a sentinel that keeps track of start node of
    # next level. next_level_tail keeps sewing together next level's children
    cur = root
    while cur:
        if cur.left:
            next_level_tail.next = cur.left  # Since next_level_head and next_level_tail point to the same node
            # initially, this means that next_level_head.next = cur.left as well. This is how next_level_head.next will
            # allow us to move to next level later on
            next_level_tail = next_level_tail.next
        if cur.right:
            next_level_tail.next = cur.right  # Connect current node's left child to right child
            next_level_tail = next_level_tail.next
        cur = cur.next
        if not cur:  # Reached the end of the current layer
            cur = next_level_head.next  # This is a key part. As said before, next_level_head.next = cur.left, so
            # this allows the current node to move to the lower level's leftmost node, meaning the head of next level.
            # 'cur' comes down one level below to the first available non-null node
            next_level_tail = next_level_head  # 'next_level_tail' moves back to the node from where it started
            next_level_head.next = None  # This line detaches next_level_head so that next_level_tail pointer can again
            # point it to the left node of next level which will be used then to set as 'cur' for the level after that
