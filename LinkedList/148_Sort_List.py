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
    """ This solution is bottom-up merge sort. It first merges pairs of adjacent arrays of 1 elements. Then merges pairs
    of adjacent arrays of 2 elements. Next merges pairs of adjacent arrays of 4 elements... Until the whole array is
    merged.
    http://www.mathcs.emory.edu/~cheung/Courses/171/Syllabus/7-Sort/merge-sort5.html
    Time complexity: O(N logN)
    Space complexity: O(1)
    """

    # Merge 2 sorted lists, append the result to head, and return the tail of the merged two lists.
    def merge2(p1, p2, head):
        dummy = ListNode(0)
        tail = dummy
        while p1 and p2:
            if p1.val <= p2.val:
                tail.next = p1
                p1 = p1.next
            else:
                tail.next = p2
                p2 = p2.next
            tail = tail.next
        tail.next = p1 or p2
        head.next = dummy.next
        while tail.next:
            tail = tail.next
        return tail

    # Split the linked list into two lists. The first list contains n nodes. Disconnect the two lists and return the
    # head of second list.
    def split(head, n):
        for _ in range(n - 1):
            if head:
                head = head.next  # Move the head for a window of size n
            else:
                break
        if not head:  # If head is null, then the head of the second list is null.
            return None
        second = head.next
        head.next = None  # Disconnect the first and second lists
        return second

    if not head or not head.next:
        return head
    dummy = ListNode(0)
    dummy.next = head
    tmp, length = head, 0
    while tmp:
        tmp = tmp.next
        length += 1
    step = 1  # At each step, merge every 2 consecutive lists of size 2^(step-1)
    while step < length:
        cur, tail = dummy.next, dummy  # With every iteration, 'cur' points to the head of the list. During the
        # execution, 'tail' is the pointer whose next points to the merged 2 consecutive lists
        while cur:
            left = cur
            right = split(left, step)  # Remember that the return value of split() is the head of the second list
            # after splitting the list at the node at index 'step'
            cur = split(right, step)  # Now the second list whose head is 'right' has the same size as left list after
            # splitting at index 'step' again. 'cur' points to the head of the rest of the list on which we'll apply
            # the same procedure in the next iteration
            tail = merge2(left, right, tail)  # We connect 'tail' to the head of the merged 2 lists. tail.next =
            # head_of_merged_lists has the same effect as dummy.next = tail_of_merged_lists the first time this
            # statement is executed in every iteration. After that, 'tail' can move freely as dummy.next is taking
            # the stripe of the first merged 2 lists. merge2() returns the tail of the merged 2 lists, to which 'tail'
            # will now point. This ensures that 'tail' connects the merged 2 lists at iteration (k-1) to those at
            # iteration k.
        step *= 2  # Now go and merge consecutive lists of next order of size.
    return dummy.next


class Test(unittest.TestCase):
    head = ListNode(-1)
    head.next = ListNode(5)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(0)

    def test_sort_list(self):
        head = sort_list_v1(self.head)
        self.assertEqual(-1, head.val)
        self.assertEqual(0, head.next.val)
        self.assertEqual(3, head.next.next.val)
        self.assertEqual(4, head.next.next.next.val)
        self.assertEqual(5, head.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()