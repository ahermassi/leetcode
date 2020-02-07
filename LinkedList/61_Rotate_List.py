""" Given a linked list, rotate the list to the right by k places, where k is non-negative. """

import unittest2 as unittest


# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def rotate_right(head, k):
    """ The nodes in the list are already linked, and hence the rotation basically means:
            1- To close the linked list into the ring
            2- To break the ring after the new tail and just in front of the new head
        Note that k may be larger than list length n. If so, it is equivalent to shifting by k mod n.
        Use the fact that linked lists can be cut and the sub-lists reassembled very efficiently.
        First we find the tail node t. Since the successor of the tail is the original head, we update t's successor.
        The original head is to become the kth node from the start of the new list. Therefore, the new head is the
        (n - k)th node in the initial list.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not head or not head.next:
        return head
    length, cur = 1, head
    while cur.next:
        length += 1
        cur = cur.next
    k = k % length
    if not k:
        return head
    cur.next = head  # Make a cycle by connecting the tail to the head
    temp = head
    for _ in range(length - k - 1):
        temp = temp.next
    new_head = temp.next
    temp.next = None
    return new_head


class Test(unittest.TestCase):
    head1 = ListNode(1)
    head1.next = ListNode(2)
    head1.next.next = ListNode(3)
    head1.next.next.next = ListNode(4)
    head1.next.next.next.next = ListNode(5)
    head2 = rotate_right(head1, 2)

    def test_rotate_right(self):
        self.assertEqual(4, self.head2.val)
        self.assertEqual(5, self.head2.next.val)
        self.assertEqual(1, self.head2.next.next.val)
        self.assertEqual(2, self.head2.next.next.next.val)
        self.assertEqual(3, self.head2.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()
