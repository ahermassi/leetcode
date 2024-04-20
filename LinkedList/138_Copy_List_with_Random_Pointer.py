""" A linked list is given such that each node contains an additional random pointer which could point to any node in
the list or null.
Return a deep copy of the list.
You must return the copy of the given head as a reference to the cloned list. """


# Definition for a Node.
class Node(object):
    def __init__(self, val, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


# Video explanation: https://youtu.be/5Y2EiZST97Y
# Video explanation: https://www.youtube.com/watch?v=OvpKeraoxW0
def copy_random_list_v1(head):
    """ We perform two passes over the linked list:

        1st pass: Map the original nodes to their clones.
        2nd pass: Give all clones their next and random pointer assignments. The hashmap lets us access an original
        node's clone in constant time.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    clones = {None: None}  # None -> None to avoid checking for nullity when accessing a node's clone
    cur = head
    while cur:
        clones[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        clones[cur].next = clones[cur.next]  # Set next of current node's clone to the clone of current node's next
        clones[cur].random = clones[cur.random]  # Set random pointer of current node's clone to the clone of current
        # node's random pointer
        cur = cur.next
    return clones[head]


def copy_random_list_v2(head):
    """ One-pass approach.

         When we are iterating over the list, we can create new nodes via the random pointer or the next pointer,
         whichever points to a node that doesn't exist in the old --> new mapping.

            - Traverse the linked list starting at the head

            - Random Pointer:
                * If the random pointer of the current node points to a node whose clone already exists in the hashmap,
                   we simply use the cloned node reference
                * If the random pointer of the current node points to a node which has not been cloned yet, we
                   create its clone and add it to the hashmap

            - Same goes for the next pointer

            - We repeat steps 2 and 3 until we reach the end of the linked list

    Time complexity: O(N), we make one pass over the original linked list
    Space complexity: O(N), we have a hashmap containing mapping from old list nodes to new list nodes
    """
    if not head:
        return None
    clones = {None: None, head: Node(head.val)}  # None -> None to avoid checking for nullity when accessing a clone
    cur = head
    while cur:
        if cur.next not in clones:
            clones[cur.next] = Node(cur.next.val)
        if cur.random not in clones:
            clones[cur.random] = Node(cur.random.val)
        clones[cur].next = clones[cur.next]
        clones[cur].random = clones[cur.random]
        cur = cur.next
    return clones[head]


# Video explanation: https://youtu.be/OvpKeraoxW0?t=637
def copy_random_list_v3(head):
    """ Instead of a separate hashmap to keep old node --> node clone mapping, we can tweak the original linked list and
         keep every cloned node next to its original node. This interleaving of old and new nodes allows us to solve
         this problem without any extra space.

            - Traverse the original list and clone the nodes as we go and place the clone next to the original node.
               This new linked list is essentially an interweaving of original and cloned nodes. The next pointer is
               used to create the weaving. Note that this operation ends up modifying the original linked list.

            - Next, iterate the list having both the new and old nodes intertwined with each other and use the original
               nodes' random pointers to assign references to random pointers for cloned nodes. For example, if B has a
               random pointer to A, this means B's clone has a random pointer to A's clone.

            - Now that the random pointers are assigned to the correct nodes, the next pointers need to be correctly
               assigned to undo the interweaving of the current linked list and get back the original list and the
               cloned list.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not head:
        return None
    # Creating a new weaved list of original and copied nodes.
    cur = head
    while cur:
        clone = Node(cur.val, cur.next)
        # Cloned node. Note that the new node's next points to current node's next, inserting the cloned node
        # just next to the original node. If A->B->C is the original linked list, after weaving cloned nodes would
        # be A->A'->B->B'->C->C'
        cur.next = clone
        cur = clone.next
    cur = head
    # Now link the random pointers of the clones nodes. Iterate over the newly created list and use the original nodes'
    # random pointers to assign references to random pointers for cloned nodes.
    while cur:
        cur.next.random = cur.random.next if cur.random else None
        cur = cur.next.next
    # Undo the interweaving of the linked list to get back the original linked list and the cloned list,
    # i.e. A->A'->B->B'->C->C' would be broken to A->B->C and A'->B'->C'
    old_head, new_head = head, head.next
    head_to_return = head.next
    while old_head.next and new_head.next:
        old_head.next = old_head.next.next
        new_head.next = new_head.next.next
        old_head = old_head.next
        new_head = new_head.next
    return head_to_return



