""" Given a node from a cyclic linked list which is sorted in ascending order, write a function to insert a value into
the list such that it remains a cyclic sorted list. The given node can be a reference to any single node in the list,
and may not be necessarily the smallest value in the cyclic list.
If there are multiple suitable places for insertion, you may choose any place to insert the new value. After the
insertion, the cyclic list should remain sorted. """

# Definition for a Node.


class Node(object):
    def __init__(self, val, next):
        self.val = val
        self.next = next


def insert(head, insertVal):
    """ We iterate through the cyclic list using two pointers, namely 'pre' and 'cur'. When we find a suitable place
        to insert the new value, we insert it between the 'pre' and 'cur' nodes. The termination condition of the loop
        is that we get back to the starting point of the two pointers (i.e. pre == head). During the loop, at each
        step, we check if the current place bounded by the two pointers is the right place to insert the new value.
        If not, we move both pointers one step forward.
        Case 1). The value of new node sits between the values 'pre' and 'cur' pointers. As a result, it should be
        inserted within the list, right after 'pre'.
        Case 2). The value of new node goes beyond the minimal and maximal values of the current list, either less than
        the minimal value or greater than the maximal value. In either case, the new node should be added right after
        the tail node (i.e. the node with the maximal value of the list). We can locate the position of the tail node
        by finding a descending order between the adjacent, i.e. the condition (prev.val > curr.val), since the nodes
        are sorted in ascending order, the tail node 'pre' would have the greatest value of all nodes.
        Case 3). Finally, there is one case that does not fall into any of the above two cases. This is the case where
        the list contains uniform values. In this case, we would end up looping through the list and getting back to
        the starting point. The followup action is just to add the new node after any node in the list, regardless of
        the value to be inserted.
    Time complexity: O(N), where N is the size of list. In the worst case, we would iterate through the entire list.
    Space complexity: O(1)
    """
    node = Node(insertVal, None)
    if not head:
        node.next = node
        return node
    pre, cur = head, head.next
    while True:
        if pre.val <= insertVal <= cur.val:  # Case 1: found a spot between smaller and bigger node
            break
        if pre.val > cur.val and (insertVal > pre.val or insertVal < cur.val):  # Case 2: reached tipping point.
            # This is for catching 'insertVal's that are smaller than min or bigger than max
            break
        pre, cur = pre.next, cur.next  # Case 3. Put this *before* next 'if' condition to skip the very first loop
        # iteration where 'pre' points to 'head'
        if pre == head:  # Means we made a complete cycle without breaking, so all nodes have equal values
            break
    node.next = cur
    pre.next = node
    return head
