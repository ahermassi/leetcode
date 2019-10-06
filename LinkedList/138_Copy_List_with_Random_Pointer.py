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
    """ The iterative solution to this problem does not model it as a graph, instead simply treats it as a LinkedList.
        When we are iterating over the list, we can create new nodes via the random pointer or the next pointer
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
        else:
            copy = Node(node.val, None, None)
            copies[node] = copy
            return copy

    if not head:
        return None
    copies = {None: None}  # To avoid constantly checking if next/random is null
    temp = head
    new_head = Node(head.val, None, None)
    copies[head] = new_head
    while temp:
        new_head.next = get_node_copy(temp.next)
        new_head.random = get_node_copy(temp.random)
        temp = temp.next
        new_head = new_head.next
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
    temp = head
    while temp:
        copies[temp] = Node(temp.val, None, None)
        temp = temp.next
    temp = head
    while temp:
        copies[temp].next = copies[temp.next]  # Set the next of current node's clone to the clone of curent node's next
        copies[temp].random = copies[temp.random]
        temp = temp.next
    return copies[head]



