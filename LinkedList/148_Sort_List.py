""" Sort a linked list in O(n log n) time using constant space complexity. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def sort_list_v1(head):
    """ The Top-Down approach for merge sort recursively splits the original list into sub-lists of equal sizes, sorts
        each sublist independently, and eventually merges the sorted lists.
        Recursively split the original list into two halves. The split continues until there is only one node in the
        linked list (Divide phase). To split the list into two halves, we find the middle of the linked list using the
        Fast and Slow pointer approach.
        Recursively sort each sublist and combine it into a single sorted list. (Merge Phase)
        The process continues until we get the original list in sorted order.
    Time complexity: O(N logN), the recursion tree expands in form of a complete binary tree, splitting the list into
    two halves recursively. The number of levels in a complete binary tree is given by logN. At each level, we merge N
    nodes which takes O(N) time. For N=16, we perform merge operation on 16 nodes in each of the 4 levels. So the time
    complexity for split and merge operation is O(N logN)
    Space complexity: O(logN), we need additional space to store the recursive call stack. The maximum depth of the
    recursion tree is logN.
    """

    def merge(head1, head2):
        head = tail = ListNode(0)
        while head1 and head2:
            if head1.val < head2.val:
                tail.next = head1
                head1 = head1.next
            else:
                tail.next = head2
                head2 = head2.next
            tail = tail.next
        tail.next = head1 or head2
        return head.next

    if not head or not head.next:  # This is the recursion base case: a single node list or empty list. When both
        # left and right halves are at this base case, it's easy to merge them
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    left, right = head, slow.next
    slow.next = None  # Cut the link so left and right halves are no longer connected
    left = sort_list_v1(left)
    right = sort_list_v1(right)
    return merge(left, right)


def sort_list_v2(head):
    """ This solution is bottom-up merge sort. It first merges pairs of adjacent arrays of 1 elements. Then merges pairs
        of adjacent arrays of 2 elements. Next merges pairs of adjacent arrays of 4 elements... Until the whole array
        is sorted.
    http://www.mathcs.emory.edu/~cheung/Courses/171/Syllabus/7-Sort/merge-sort5.html
    Time complexity: O(N logN)
    Space complexity: O(1)
    """

    # Merge two sorted lists, append the result to the node 'node', and return the tail of the two merged lists.
    def merge(p1, p2, node):
        dummy = tail = ListNode(0)
        while p1 and p2:
            if p1.val <= p2.val:
                tail.next = p1
                p1 = p1.next
            else:
                tail.next = p2
                p2 = p2.next
            tail = tail.next
        tail.next = p1 or p2
        node.next = dummy.next
        while tail.next:
            tail = tail.next
        return tail

    # Split the linked list to two lists. The first list contains n nodes. Disconnect the two lists and return the
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
    temp, length = head, 0
    while temp:
        length += 1
        temp = temp.next
    step = 1  # At each step, merge every two consecutive lists of size 2^(step-1)
    while step < length:
        cur, tail = dummy.next, dummy  # With every iteration, 'cur' points to the head of the list. During the
        # execution, 'tail' is the pointer whose next points to the 2 merged consecutive lists
        while cur:
            left = cur
            right = split(left, step)  # Remember that the return value of split() is the head of the second list
            # after splitting the list at the node at index 'step'
            cur = split(right, step)  # Now the second list whose head is 'right' has the same size as left list after
            # splitting at index 'step' again. 'cur' points to the head of the rest of the list on which we'll apply
            # the same procedure in the next iteration
            tail = merge(left, right, tail)  # We connect 'tail' to the head of the two merged lists.
            # tail.next = head_of_merged_lists has the same effect as dummy.next = tail_of_merged_lists the first time
            # this statement is executed in every iteration. After that, 'tail' can move freely as dummy.next is taking
            # the stripe of the first two merged lists. merge() returns the tail of the two merged lists, to which
            # 'tail' will now point. This ensures that 'tail' connects the two merged lists at iteration (k-1) to those
            # at iteration k.
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