""" A linked list is given such that each node contains an additional random pointer which could point to any node in
the list or null.
Return a deep copy of the list.
You must return the copy of the given head as a reference to the cloned list. """


# Definition for a Node.
class Node(object):
    def __init__(self, val, next, random):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list_v1(head):
    """ When we are iterating over the list, we can create new nodes via the random pointer or the next pointer,
        whichever points to a node that doesn't exist in our old --> new dictionary.
        1- Traverse the linked list starting at head of the linked list.
        2- Random Pointer
            - If the random pointer of the current node i points to the a node j and a clone of j already exists in
              the 'copies' dictionary, we will simply use the cloned node reference from the 'copies' dictionary.
            - If the random pointer of the current node i points to the a node j which has not been created yet, we
              create a new node corresponding to j and add it to the 'copies' dictionary.
        3- Same goes for Next Pointer
        4- We repeat steps 2 and 3 until we reach the end of the linked list.
    Time complexity: O(N) because we make one pass over the original linked list
    Space complexity: O(N) as we have a dictionary containing mapping from old list nodes to new list nodes
    """

    def get_node_copy(node):
        if node in copies:
            return copies[node]
        copy = Node(node.val, None, None)
        copies[node] = copy
        return copy

    if not head:
        return None
    copies = {None: None}  # To avoid constantly checking if next/random is null
    new_head = Node(head.val, None, None)
    copies[head] = new_head
    cur = head
    while cur:
        new_head.next = get_node_copy(cur.next)
        new_head.random = get_node_copy(cur.random)
        cur, new_head = cur.next, new_head.next
    return copies[head]


def copy_random_list_v2(head):
    """ Same as previous approach, but performing two passes over the linked list.
        1st pass: We map the original node to its clone.
        2nd pass: Give all clones their next and random pointer assignments. Our hash map lets us reach an original
        node's clone in O(1) time.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    copies = {None: None}
    cur = head
    while cur:
        copies[cur] = Node(cur.val, None, None)
        cur = cur.next
    cur = head
    while cur:
        copies[cur].next = copies[cur.next]  # Set next of current node's clone to the clone of current node's next
        copies[cur].random = copies[cur.random]
        cur = cur.next
    return copies[head]


def copy_random_list_v3(head):
    """ Instead of a separate dictionary to keep the old node --> new node mapping, we can tweak the original linked
        list and keep every cloned node next to its original node. This interleaving of old and new nodes allows us to
        solve this problem without any extra space.
        1- Traverse the original list and clone the nodes as you go and place the cloned copy next to its original node.
           This new linked list is essentially a interweaving of original and cloned nodes.
        2- Iterate the list having both the new and old nodes intertwined with each other and use the original nodes'
           random pointers to assign references to random pointers for cloned nodes. For eg. If B has a random pointer
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
        node = Node(cur.val, cur.next, None)   # Cloned node. Note that node's next points to current node's next
        # Inserting the cloned node just next to the original node.
        # If A->B->C is the original linked list,
        # Linked list after weaving cloned nodes would be A->A'->B->B'->C->C'
        cur.next = node
        cur = cur.next.next
    cur = head
    # Now link the random pointers of the new nodes created.
    # Iterate the newly created list and use the original nodes random pointers,
    # to assign references to random pointers for cloned nodes.
    while cur and cur.next:
        cur.next.random = cur.random.next if cur.random else None
        cur = cur.next.next
    # Unweave the linked list to get back the original linked list and the cloned list.
    # i.e. A->A'->B->B'->C->C' would be broken to A->B->C and A'->B'->C'
    p1 = head
    p2 = head.next
    new_head = head.next
    while p1:
        p1.next = p1.next.next
        p2.next = p2.next.next if p2.next else None
        p1 = p1.next
        p2 = p2.next
    return new_head



