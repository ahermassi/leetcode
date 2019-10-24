""" You are given a doubly linked list which in addition to the next and previous pointers, it could have a child
pointer, which may or may not point to a separate doubly linked list. These child lists may have one or more children
of their own, and so on, to produce a multilevel data structure, as shown in the example below.
Flatten the list so that all the nodes appear in a single-level, doubly linked list. You are given the head of the
first level of the list. """


def flatten_v1(head):
    """ Start form the head , move one step each time to the next node.
        When a node with child is met, say node p, follow its child chain to the end and connect the tail node with
        p.next, by doing this we merge the child chain back to the main list.
        Return to p and proceed until finding next node with child.
        Repeat until reaching the end of list.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    temp = head
    while temp:
        if temp.child:
            child = temp.child
            while child.next:
                child = child.next
            nxt = temp.next
            temp.next = temp.child
            temp.next.prev = temp
            temp.child = None
            child.next = nxt
            if nxt:
                child.next.prev = child
        temp = temp.next
    return head


def flatten_v2(head):
    """ Recursive version of above algorithm.
    Time complexity: O(N)
    Space complexity: O(N) for call stack
    """
    temp = head
    while temp:
        if temp.child:
            nxt = temp.next
            temp.next = flatten_v1(temp.child)
            temp.next.prev = temp
            temp.child = None
            while temp.next:
                temp = temp.next
            if nxt:
                temp.next = nxt
                temp.next.prev = temp
        temp = temp.next
    return head




