""" Given a sorted linked list, delete all duplicates such that each element appear only once. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def delete_duplicates_v1(head):
    """ Because the input list is sorted, we can determine if a node is a duplicate by comparing its value to the
        node after it in the list. If it is a duplicate, we change the next pointer of the current node so that it
        skips the next node and points directly to the one after the next node.
        The loop invariant is: all nodes in the list up to the pointer current do not contain duplicate elements.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    cur = head
    while cur:
        if cur.next and cur.next.val == cur.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head


def delete_duplicates_v2(head):
    """ The previous solution deletes the duplicate node as the cur pointer traverses the list. This solution first
        locates the range of duplicate nodes and then deletes them all at once.
        The loop invariant is: all nodes in the list up to the pointer 'cur' do not contain duplicate elements, and
        all nodes between 'cur' and 'temp' are duplicate.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    cur, temp = head, head
    while cur:
        while temp and temp.val == cur.val:  # 'temp' will stop at the node right after the last duplicate node of 'cur'
            temp = temp.next
        cur.next = temp
        cur = cur.next
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
        self.assertEqual(1, delete_duplicates_v1(self.head1).val)
        self.assertEqual(2, delete_duplicates_v1(self.head1).next.val)
        self.assertEqual(1, delete_duplicates_v1(self.head2).val)
        self.assertEqual(2, delete_duplicates_v1(self.head2).next.val)
        self.assertEqual(3, delete_duplicates_v1(self.head2).next.next.val)


if __name__ == '__main__':
    unittest.main()
