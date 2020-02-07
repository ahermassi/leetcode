""" Given a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the
original list. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def delete_duplicates(head):
    """ Pretty straightforward. Use two pointers, 'pre' to track the node before the duplicate node, and 'cur' to find
        the last node of duplicates.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    dummy = ListNode(float('inf'))
    dummy.next = head
    pre, cur = dummy, head
    while cur and cur.next:
        if cur.val != cur.next.val:
            pre, cur = cur, cur.next
        else:  # Duplicate node detected
            while cur and cur.next and cur.val == cur.next.val:  # Advance to last duplicate node whose value is cur.val
                cur = cur.next
            cur = cur.next
            pre.next = cur
    return dummy.next


class Test(unittest.TestCase):
    head1 = ListNode(1)
    head1.next = ListNode(1)
    head1.next.next = ListNode(1)
    head1.next.next.next = ListNode(2)
    head1.next.next.next.next = ListNode(3)
    head2 = ListNode(2)
    head2.next = ListNode(3)

    def test_delete_duplicates(self):
        self.assertEqual(2, delete_duplicates(self.head1).val)
        self.assertEqual(3, delete_duplicates(self.head1).next.val)


if __name__ == '__main__':
    unittest.main()