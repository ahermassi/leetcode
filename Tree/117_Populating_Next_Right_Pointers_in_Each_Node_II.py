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


def connect_v1(root):
    """ Similarly to the BFS solution in 116- Populating Next Right Pointers in Each Node, the reason we'd need a queue
         is that we have no idea about the structure of the tree and the kind of branches it has, and we need to access
         all the nodes on a common level, together, and establish connections between them.

         However, once we are done establishing the next pointers between the nodes, don't they behave like the nodes of
         a linked list? In fact, after the next connections are established, all the nodes at a particular level form a
         linked list via the next pointers.
         Based on this idea, we have the following intuition for the space-efficient algorithm:

                    We only move to level N+1 when we are done establishing the next pointers of level N.
                    Since we have access to all the nodes at any level via the next pointers, we can use these
                    next pointers to establish the connections for the next level.

         When we go over the nodes of the current level, the next pointers of these nodes were already established in
         the previous iteration . This helps get rid of the explicit queue and save space. To move to the next level, we
         only need its leftmost node. From there on, it's just a linked list traversal.

            - 'cur' is the pointer at the current level. This is what we use to traverse all the nodes of the current
               level. It starts at the leftmost node and then follows the next pointers all the way to the very end.

            - 'next_level_tail' is the tail pointer in the next level. This node is important to discover at each level
               since this would act as the head of the linked list of the next level.

         When we are at a level, with a node in hand, we are looking ahead one level and connecting the children of that
         node. Connect 'next_level_tail' with every one of the possible nodes in the child level, and update it only if
         the connected node is not null. Do this for every level.

         Once we are done with the current level, we move on to the next one. One last thing that's left is to update
         'next_level_tail' node. We need that node to start traversal on a particular level. Think of it as the
         "stitching" node of the linked list. This is easy to do by using 'next_level_head' pointer. Whenever we set
         'next_level_head' pointer for each level for the first time, we also set 'next_level_tail' to that node.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    # next_level_head is a sentinel that keeps track of the start node of next level.
    # next_level_tail keeps "sewing together" next level's nodes.
    next_level_head = next_level_tail = Node(0)
    cur = root
    while cur:
        if cur.left:
            # Since next_level_head and next_level_tail point to the same node initially, this means that
            # next_level_head.next = cur.left as well. This is how next_level_head.next will allow us to move
            # to next level when we're done with the current one.
            next_level_tail.next = cur.left
            next_level_tail = next_level_tail.next
        if cur.right:
            next_level_tail.next = cur.right  # Connect current node's left child to right child
            next_level_tail = next_level_tail.next
        cur = cur.next
        if not cur:  # Reached the end of the current level
            # This is a key part. As mentioned above, next_level_head.next = cur.left, so this allows the
            # current node to move to the lower/next level's leftmost node, i.e. the head of next level.
            # 'cur' moves one level below to the first available non-null node
            cur = next_level_head.next
            # 'next_level_tail' moves back to the node from where it started. This line detaches next_level_head so that
            # next_level_tail pointer can again point to the left node of next level which will be used then as 'cur'
            # for the following level.
            next_level_tail = next_level_head
            next_level_head.next = None


def connect_v2(root):
    """ Same algorithm but using an extra while loop to finish the wiring of complete child level at each iteration of
         the outer loop. The previous algorithm moves 'cur' to its next node but finishes the wiring of child level at
         the following iteration.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    next_level_head = next_level_tail = Node(0)
    cur = root
    while cur:
        while cur:
            if cur.left:
                next_level_tail.next = cur.left
                next_level_tail = next_level_tail.next
            if cur.right:
                next_level_tail.next = cur.right
                next_level_tail = next_level_tail.next
            cur = cur.next
        cur = next_level_head.next
        next_level_tail = next_level_head
        next_level_head.next = None
    return root
