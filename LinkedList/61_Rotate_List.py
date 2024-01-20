""" Given a linked list, rotate the list to the right by k places, where k is non-negative. """

import unittest2 as unittest


# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# Video explanation: https://youtu.be/UcGtPs2LE_c
def rotate_right(head, k):
    """ The nodes in the list are already linked, and hence the rotation basically means:

            1- To close the linked list into a ring
            2- To break the ring after the new tail and just in front of the new head

         Where is the new head?
         In the position (n - k), where n is the number of nodes in the list. The new tail is just before, in the
         position (n - k - 1).

        Note that k may be larger than list length n. If so, it is equivalent to shifting by (k mod n).
        The algorithm is quite straightforward:

            - Find the old tail and connect it with the head to close the ring. Compute the length of the list n at the
               same time.

            - Find the new tail which is the (n - k - 1)th node from the original head, and the new head which is the
               (n - k)th node.

            - Break the ring and return the new head.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not head or not head.next:
        return head
    length, cur = 1, head
    while cur.next: # start length at 1 and stop at cur.next=None instead of cur=None to be able to form a ring
        length += 1
        cur = cur.next
    k = k % length
    if not k:
        return head
    cur.next = head  # Make a cycle by connecting the tail to the original head
    new_tail = head
    # Find the new tail : (n - k - 1)th node
    for _ in range(length - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None # Break the ring
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
