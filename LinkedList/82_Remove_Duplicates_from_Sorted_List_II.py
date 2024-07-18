""" Given a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the
original list. """

import unittest2 as unittest


# Definition of singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def delete_duplicates(head):
    """ Let's start from the most challenging situation: the list head is to be removed.

         The standard way to handle this use case is to use the so-called Sentinel Node. Sentinel nodes are widely used
         for trees and linked lists such as pseudo-heads, pseudo-tails, etc. They are purely functional and usually
         don't hold any data. Their primary purpose is to standardize the situation to avoid edge case handling.

         Let's use here a pseudo-head with +inf value to ensure that the situation "delete the list head" could never
         happen, and all nodes to delete are "inside" the list.

         The input list is sorted, and we can determine if a node is a duplicate by comparing its value to the node
         after it in the list. Step by step, we could identify the current sublist of duplicates.

         Now it's time to delete it using pointer manipulations. Note that the first node in the duplicates sublist
         should be removed as well. That means that we have to track the predecessor of the duplicates sublist, i.e.,
         the last node before the sublist of duplicates.

         Having the predecessor, we skip the entire duplicate sublist and make the predecessor point to the node after
         the sublist.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    dummy = ListNode(float('inf'))
    dummy.next = head
    pre, cur = dummy, head
    while cur and cur.next:
        if cur.val != cur.next.val:
            pre, cur = cur, cur.next
        else:
            # Duplicate node detected
            # Advance to the last duplicate of the current node
            while cur.next and cur.val == cur.next.val:
                cur = cur.next
            cur = cur.next
            # Skip all duplicates
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