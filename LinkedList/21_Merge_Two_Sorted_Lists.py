""" Merge two sorted linked lists and return it as a new list. The new list should be made by splicing together the
nodes of the first two lists.
Example:
Input: 1->2->4, 1->3->4
Output: 1->1->2->3->4->4
"""

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def merge_two_lists_v1(l1, l2):
    """ We can recursively define the result of a merge operation on two lists as the following:
        list1[0] + merge(list1[1:], list2)  if  list1[0]<list2[0]
        list2[0] + merge(list1, list2[1:])  otherwise
        Namely, the smaller of the two lists' heads plus the result of a merge on the rest of the elements.
    Time complexity: O(N + M), there will be exactly one call to merge_two_lists per element in each list. Therefore,
    the time complexity is linear in the combined size of the lists.
    Space complexity: O(N + M), The first call to merge_two_lists does not return until the ends of both l1 and l2 have
    been reached, so N + M stack frames consume O(N + M) space. (draw the stack frames for a clearer overview)
    """
    if not l1 or not l2:
        return l1 or l2
    if l1.val < l2.val:
        l1.next = merge_two_lists_v1(l1.next, l2)  # This is the case list1[0] + merge(list1[1:], list2)
        return l1
    else:
        l2.next = merge_two_lists_v1(l1, l2.next)  # This is the case list2[0] + merge(list1, list2[1:])
        return l2


def merge_two_lists_v2(l1, l2):
    """ We have a dummy head, and a tail indicating last node in this growing List. At each step we append either l1
        or l2 to tail, and update tail, l1 or l2 accordingly. After the loop terminates, at most one of l1 and l2 is
        non-null. Therefore (because the input lists were in SORTED order), if either list is non-null, it contains only
        elements greater than all of the previously-merged elements.
    Time complexity: O(N + M), the while loop runs for a number of iterations equal to sum of lengths of the two lists.
    Space complexity: O(1), the iterative approach only allocates a few pointers, so it has a constant overall memory
    footprint.
    """
    head = tail = ListNode(0)  # Dummy head and tail, starting at same position
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return head.next


class Test(unittest.TestCase):
    head1 = ListNode(1)
    head1.next = ListNode(2)
    head1.next.next = ListNode(4)
    head2 = ListNode(1)
    head2.next = ListNode(3)
    head2.next.next = ListNode(4)
    head = merge_two_lists_v2(head1, head2)

    def test_merge_two_lists(self):
        self.assertEqual(1, self.head.val)
        self.assertEqual(1, self.head.next.val)
        self.assertEqual(2, self.head.next.next.val)
        self.assertEqual(3, self.head.next.next.next.val)
        self.assertEqual(4, self.head.next.next.next.next.val)
        self.assertEqual(4, self.head.next.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()