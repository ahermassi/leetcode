""" Sort a linked list in O(n log n) time using constant space complexity. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def sort_list_v1(head):
    """ This solution doesn't use constant space due to recursion. Top-down merge sort.
        The idea behind this problem is easy : merge sort.
        Recursively split the list into two halves, left and right, and then merge the two halves to get a sorted
        sub list. Proceed until the entire list is sorted.
        How to split a linked list into two separate linked lists? Use two pointers: walker and runner.
    Time complexity: O(N logN)
    Space complexity: O(logN)
    """

    def merge(h1, h2):
        dummy_head = tail = ListNode(0)
        while h1 and h2:
            if h1.val < h2.val:
                tail.next = h1
                h1 = h1.next
            else:
                tail.next = h2
                h2 = h2.next
            tail = tail.next
        tail.next = h1 or h2
        return dummy_head.next

    if not head or not head.next:  # This is the recursion base case: a single node list or empty list. When both
        # left and right halves are at this base case, it's easy to merge them
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    left, right = head, slow.next
    slow.next = None  # Don't forget to cut the link so left and right halves are no longer connected
    left = sort_list_v1(left)
    right = sort_list_v1(right)
    return merge(left, right)


class Test(unittest.TestCase):
    head = ListNode(-1)
    head.next = ListNode(5)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(0)

    def test_has_cycle(self):
        head = sort_list_v1(self.head)
        self.assertEqual(-1, head.val)
        self.assertEqual(0, head.next.val)
        self.assertEqual(3, head.next.next.val)
        self.assertEqual(4, head.next.next.next.val)
        self.assertEqual(5, head.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()