""" Given a sorted linked list, delete all duplicates such that each element appear only once. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def delete_duplicates(head):
    """ Because the input list is sorted, we can determine if a node is a duplicate by comparing its value to the
    node after it in the list. If it is a duplicate, we change the next pointer of the current node so that it skips
    the next node and points directly to the one after the next node.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    temp = head
    while temp and temp.next:
        if temp.val == temp.next.val:
            temp.next = temp.next.next
        else:
            temp = temp.next
    return head


class Test(unittest.TestCase):
    head1 = ListNode(1)
    head1.next = ListNode(1)
    head1.next.next = ListNode(2)
    head2 = ListNode(1)
    head2.next = ListNode(1)
    head2.next.next = ListNode(2)
    head2.next.next.next = ListNode(3)
    head2.next.next.next.next = ListNode(3)

    def test_delete_duplicates(self):
        self.assertEqual(1, delete_duplicates(self.head1).val)
        self.assertEqual(2, delete_duplicates(self.head1).next.val)
        self.assertEqual(1, delete_duplicates(self.head2).val)
        self.assertEqual(2, delete_duplicates(self.head2).next.val)
        self.assertEqual(3, delete_duplicates(self.head2).next.next.val)


if __name__ == '__main__':
    unittest.main()
