""" Sort a linked list in O(n log n) time using constant space complexity. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# Video explanation: https://youtu.be/TGveA1oFhrc
def sort_list_v1(head):
    """ Merge sort is one of the efficient sorting algorithms that is popularly used for sorting linked lists. The merge
         sort algorithm runs in O(N logN) time in all the cases. Quicksort is also one of the efficient algorithms with
         the average time complexity of O(N logN), but the worst-case time complexity is O(N^2). Also, variations of the
         quick sort like randomized quicksort are not efficient for the linked list because unlike arrays, random access
         in the linked list is not possible in O(1) time.

        The top-down approach for merge sort recursively splits the original list into sub-lists of equal sizes, sorts
        each sublist independently, and eventually merges the sorted lists.

            - Recursively split the original list into two halves. The split continues until there is only one node in
               the linked list (divide phase). To split the list into two halves, we find the middle of the linked list
               using the Fast and Slow pointer approach.

            - Recursively sort each sublist and combine it into a single sorted list (merge phase).

        The process continues until we get the original list in sorted order.

    Time complexity: O(N logN), the recursion tree expands in form of a complete binary tree, splitting the list into
    two halves recursively. The number of levels in a complete binary tree is given by logN. At each level, we merge N
    nodes which takes O(N) time. For N=16, we perform merge operation on 16 nodes in each of the 4 levels. So the time
    complexity for split and merge operation is O(N logN)
    Space complexity: O(logN), we need additional space to store the recursive call stack. The maximum depth of the
    recursion tree is logN.
    """

    def merge(head1, head2):
        dummy = tail = ListNode(0)
        while head1 and head2:
            if head1.val < head2.val:
                tail.next = head1
                head1 = head1.next
            else:
                tail.next = head2
                head2 = head2.next
            tail = tail.next
        tail.next = head1 or head2
        return dummy.next

    if not head or not head.next:
        # This is the recursion base case: a single node list or empty list. When both left and right halves
        # are at this base case, it's easy to merge them
        return head
    prev, slow, fast = None, head, head
    # 'prev' is the node preceding 'slow'. When the while loop exits, 'prev' will point to the node preceding the head
    # of the second half of the list
    while fast and fast.next:
        prev, slow, fast = slow, slow.next, fast.next.next
    left, right = head, slow
    prev.next = None  # Cut the link so left and right halves are no longer connected
    left = sort_list_v1(left)
    right = sort_list_v1(right)
    return merge(left, right)


def sort_list_v2(head):
    """ The Top-Down Approach for merge sort uses O(logN) extra space due to recursive call stack. We can implement
        merge sort with constant extra space using the Bottom-Up approach.
        The Bottom-Up approach for merge sort starts by splitting the problem into the smallest sub-problems and
        iteratively merges the result to solve the original problem.
        First, the list is split into sub-lists of size 1 and merged iteratively in sorted order. The merged list is
        solved similarly. The process continues until we sort the entire list.
        Start with splitting the list into sub-lists of size 1. Each adjacent pair of sub-lists of size 1 is merged in
        sorted order. After the first iteration, we get the sorted lists of size 2. A similar process is repeated for
        a sublist of size 2. In this way, we iteratively split the list into sub-lists of size 1, 2, 4, 8.. and so on
        until we reach N.
        http://www.mathcs.emory.edu/~cheung/Courses/171/Syllabus/7-Sort/merge-sort5.html
    Time complexity: O(N logN)
    Space complexity: O(1)
    """

    # Merge two sorted lists, append the result to 'node', and return the tail of the two merged lists.
    def merge(head1, head2, node):
        dummy = tail = ListNode(0)
        while head1 and head2:
            if head1.val <= head2.val:
                tail.next = head1
                head1 = head1.next
            else:
                tail.next = head2
                head2 = head2.next
            tail = tail.next
        tail.next = head1 or head2
        node.next = dummy.next  # This connects 'node' to the head of the two merged lists
        while tail.next:
            tail = tail.next  # Advance 'tail' all the way to the end of the two merged lists
        return tail

    # Split the linked list to two sub-lists. The first list contains 'sublist_size' nodes. Disconnect the two
    # sub-lists and return the head of second sublist.
    def split(sublist_head, sublist_size):
        i = 1
        while i < sublist_size and sublist_head:
            sublist_head = sublist_head.next  # Move the sublist head for a window of size 'sublist_size'
            i += 1
        second = sublist_head.next if sublist_head else None  # If head is null, then the head of the second sublist is
        if head:
            head.next = None  # Disconnect the first and second lists
        return second

    if not head or not head.next:
        return head
    dummy = ListNode(0)
    dummy.next = head
    cur, size = head, 0
    while cur:
        size += 1
        cur = cur.next
    step = 1  # At each step, merge every two consecutive lists of size 2^(step-1)
    while step < size:
        tail = dummy
        cur = dummy.next  # At the start of every iteration, 'cur' points to the head of the original list. During
        # the iteration, 'tail' is the pointer whose preceding the 2 merged consecutive lists
        while cur:
            first_sublist_head = cur
            second_sublist_head = split(first_sublist_head, step)  # Remember that the return value of split() is the
            # head of the second list after splitting the list at the node at index 'step'
            cur = split(second_sublist_head, step)  # After this call, the second sublist whose head is
            # 'second_sublist_head' has the same size as the first sublist after splitting at index 'step' again.
            # 'cur' points to the head of the rest of the list on which we'll apply the same procedure in the next
            # iteration
            tail = merge(first_sublist_head, second_sublist_head, tail)  # We connect 'tail' to the head of the two
            # merged lists.
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
