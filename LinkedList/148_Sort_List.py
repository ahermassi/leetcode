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


def sort_list_v2(head):
    """ This solution is bottom-up merge sort.It first merges pairs of adjacent arrays of 1 elements. Then merges pairs
    of adjacent arrays of 2 elements. Next merges pairs of adjacent arrays of 4 elements... Until the whole array is
    merged.
    http://www.mathcs.emory.edu/~cheung/Courses/171/Syllabus/7-Sort/merge-sort5.html
    Time complexity: O(N logN)
    Space complexity: O(1)
    """

    # merge 2 sorted lists, and append the result to head
    # return the tail
    def merge2(p1, p2, head):
        dummy = ListNode(0)
        p = dummy
        while p1 and p2:
            if p1.val <= p2.val:
                p.next = p1
                p1 = p1.next
                p = p.next
            else:
                p.next = p2
                p2 = p2.next
                p = p.next
        p.next = p1 or p2
        head.next = dummy.next
        while p.next:
            p = p.next
        return p

    # divide the linked list into two lists
    # first linked list contains n nodes
    # return the head of second linked list
    def split(head, n):
        for _ in range(n - 1):
            if head:
                head = head.next
            else:
                break
        if not head:
            return None
        second = head.next
        head.next = None
        return second

    if not head or not head.next:
        return head
    dummy = ListNode(0)
    dummy.next = head
    tmp = head
    length = 0
    while tmp:
        tmp = tmp.next
        length += 1
    step = 1
    while step < length:
        cur, tail = dummy.next, dummy
        while cur:
            left = cur
            right = split(left, step)
            cur = split(right, step)
            tail = merge2(left, right, tail)
        step *= 2
    return dummy.next


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