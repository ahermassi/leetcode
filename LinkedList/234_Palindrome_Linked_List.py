""" Given a singly linked list, determine if it is a palindrome. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def is_palindrome_v1(head):
    """ Insert the nodes' values in an array and check for reversibility.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    return vals == vals[::-1]


class Test(unittest.TestCase):
    head1 = ListNode(1)
    head1.next = ListNode(2)
    head2 = ListNode(1)
    head2.next = ListNode(2)
    head2.next.next = ListNode(2)
    head2.next.next.next = ListNode(1)

    def test_next_greater_element(self):
        self.assertFalse(is_palindrome_v1(self.head1))
        self.assertTrue(is_palindrome_v1(self.head2))


if __name__ == '__main__':
    unittest.main()

