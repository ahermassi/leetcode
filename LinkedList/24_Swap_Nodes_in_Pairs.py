""" Given a linked list, swap every two adjacent nodes and return its head.
You may not modify the values in the list's nodes, only nodes itself may be changed.
"""

import unittest2 as unittest


# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def swap_pairs_v1(head):
    """ Do the swapping going backwards and return the new head of every 2 adjacent pairs at each call. This ensures
        the last node returned is the head of the new list.
    Time complexity: O(N)
    Space complexity: O(N) for the call stack
    """
    if not head or not head.next:
        return head
    p = swap_pairs_v1(head.next.next)  # Navigate to the last/before-last node (depends on even/odd length of the list)
    nxt = head.next
    nxt.next = head
    head.next = p
    return nxt  # After swapping, return the 'local' new head. The last one returned is the head of the entire new list


def swap_pairs_v2(head):
    """ Iterative solution.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    cur = dummy
    while cur.next and cur.next.next:
        first, second = cur.next, cur.next.next
        first.next = second.next
        cur.next = second
        second.next = first
        cur = second.next
    return dummy.next


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)

    def test_swap_pairs(self):
        head = swap_pairs_v1(self.head)
        self.assertEqual(2, head.val)
        self.assertEqual(1, head.next.val)
        self.assertEqual(4, head.next.next.val)
        self.assertEqual(3, head.next.next.next.val)


if __name__ == '__main__':
    unittest.main()