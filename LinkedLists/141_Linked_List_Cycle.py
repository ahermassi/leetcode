""" Given a linked list, determine if it has a cycle in it. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def has_cycle(head):
    """ The idea is to visit each node and replace its value with -infinity. If visited again, -infinity indicates
    the presence of a cycle.
    Time complexity: O(N), where N is the length of the linked list
    Space complexity: O(1)
    """
    while head:
        if head.val == float('-inf'):
            return True
        head.val = float('-inf')
        head = head.next
    return False


class Test(unittest.TestCase):
    head1 = ListNode(3)
    head1.next = ListNode(2)
    head1.next.next = ListNode(0)
    head1.next.next.next = ListNode(-4)
    head1.next.next.next.next = head1.next
    head2 = ListNode(1)
    head2.next = ListNode(1)
    head2.next.next = ListNode(2)
    head2.next.next.next = ListNode(3)

    def test_next_greater_element(self):
        self.assertTrue(has_cycle(self.head1))
        self.assertFalse(has_cycle(self.head2))


if __name__ == '__main__':
    unittest.main()