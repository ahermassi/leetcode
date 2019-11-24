""" Given a linked list, swap every two adjacent nodes and return its head.
You may not modify the values in the list's nodes, only nodes itself may be changed.
"""

import unittest2 as unittest


# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def swap_pairs(head):
    """ Do the swapping going backwards and return the new head of every 2 adjacent pairs at each call. This ensures
        the last node returned is the head of the new list.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not head or not head.next:
        return head
    p = swap_pairs(head.next.next)  # Navigate to the last/before-last node (depends on even/odd length of the list)
    nxt = head.next
    nxt.next = head
    head.next = p
    return nxt  # After swapping, return the 'local' new head. The last one returned is the head of the entire new list


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)

    def test_swap_pairs(self):
        head = swap_pairs(self.head)
        self.assertEqual(2, head.val)
        self.assertEqual(1, head.next.val)
        self.assertEqual(4, head.next.next.val)
        self.assertEqual(3, head.next.next.next.val)


if __name__ == '__main__':
    unittest.main()