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
    """ If there is tipping point in the list, which means that there are at least 2 distinct values, we name the node
        that has the max value to be the tipping point, the node after tipping point has the min value (min != max).
            1- If the to be inserted value x is in a climbing stage, which means there is a node satisfying
               node.val <= x <= node.next.val, we insert x after this node
            2- If the to be inserted value x is the new min or max value after its insertion, x needs to be inserted
               after the tipping point
        If there is NO tipping point in the list, which means that all nodes in the list have the same value, we just
        insert x before we traverse back to start node.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    node = Node(insertVal, None)
    if not head:
        node.next = node
        return node
    pre, cur = head, head.next
    while True:
        if pre.val <= insertVal <= cur.val:  # Found a spot between smaller and bigger node
            break
        if pre.val > cur.val and (insertVal > pre.val or insertVal < cur.val):  # Reached tipping point. This is
            # for catching `insertVal`s that are smaller than min or bigger than max
            break
        pre, cur = pre.next, cur.next  # Put this *before* next 'if' condition to skip the very first loop iteration
        # when 'pre' is always 'head'
        if pre == head:  # Means we made a complete cycle without breaking, meaning all nodes are equal
            break
    node.next = cur
    pre.next = node
    return head
