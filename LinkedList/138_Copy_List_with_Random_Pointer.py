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


def copy_random_list_v1(head):
    """ We perform two passes over the linked list:

        1st pass: We map the original nodes to their clones.
        2nd pass: Give all clones their next and random pointer assignments. Our hash map lets us reach an original
        node's clone in O(1) time.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    clones, cur = {None: None}, head
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
    """ When we are iterating over the list, we can create new nodes via the random pointer or the next pointer,
        whichever points to a node that doesn't exist in our old --> new dictionary.
        1- Traverse the linked list starting at head of the linked list.
        2- Random Pointer
            - If the random pointer of the current node i points to node j, and a clone of j already exists in
              the 'clones' dictionary, we will simply use the cloned node reference from the 'clones' dictionary.
            - If the random pointer of the current node i points to node j which has not been created yet, we create a
              new node corresponding to j and add it to the 'clones' dictionary.
        3- Same goes for next pointer
        4- We repeat steps 2 and 3 until we reach the end of the linked list.
    Time complexity: O(N), we make one pass over the original linked list
    Space complexity: O(N), we have a dictionary containing mapping from old list nodes to new list nodes
    """

    clones = {None: None}  # To avoid constantly checking if next/random is null
    cur = head
    while cur:
        if cur not in clones:
            clones[cur] = Node(cur.val)
        if cur.next not in clones:
            clones[cur.next] = Node(cur.next.val)
        if cur.random not in clones:
            clones[cur.random] = Node(cur.random.val)
        clones[cur].next = clones[cur.next]
        clones[cur].random = clones[cur.random]
        cur = cur.next
    return clones[head]


def copy_random_list_v3(head):
    """ Instead of a separate dictionary to keep the old node --> new node mapping, we can tweak the original linked
        list and keep every cloned node next to its original node. This interleaving of old and new nodes allows us to
        solve this problem without any extra space.
        1- Traverse the original list and clone the nodes as we go and place the cloned copy next to its original node.
           This new linked list is essentially an interweaving of original and cloned nodes.
        2- Iterate the list having both the new and old nodes intertwined with each other and use the original nodes'
           random pointers to assign references to random pointers for cloned nodes. For eg. if B has a random pointer
           to A, this means B' has a random pointer to A'.
        3- Now that the random pointers are assigned to the correct node, the next pointers need to be correctly
        assigned to unweave the current linked list and get back the original list and the cloned list.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not head:
        return None
    # Creating a new weaved list of original and copied nodes.
    cur = head
    while cur:
        node = Node(cur.val, cur.next)   # Cloned node. Note that node's next points to current node's next
        # Inserting the cloned node just next to the original node.
        # If A->B->C is the original linked list, after weaving cloned nodes would be A->A'->B->B'->C->C'
        cur.next = node
        cur = cur.next.next
    cur = head
    # Now link the random pointers of the new nodes created. Iterate over the newly created list and use the original
    # nodes random pointers to assign references to random pointers for cloned nodes.
    while cur and cur.next:
        cur.next.random = cur.random.next if cur.random else None
        cur = cur.next.next
    # Unweave the linked list to get back the original linked list and the cloned list, i.e. A->A'->B->B'->C->C' would
    # be broken to A->B->C and A'->B'->C'
    p1 = head
    p2 = head.next
    new_head = head.next
    while p1.next and p2.next:
        p1.next = p2.next
        p1 = p1.next
        p2.next = p1.next
        p2 = p2.next
    return new_head



