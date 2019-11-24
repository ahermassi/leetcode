""" Write a program to find the node at which the intersection of two singly linked lists begins. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def get_intersection_node_v1(headA, headB):
    """ Maintain two pointers pa and pb initialized at the head of A and B, respectively. Then let them both traverse
        through the lists, one node at a time. When pa reaches the end of list A, then redirect it to the head of B;
        similarly when pb reaches the end of list B, redirect it to the head of A. If at any point pa meets pb, then pa
        (or pb) is the intersection node.
        The idea is if you switch head, the possible difference between lengths would be countered. On the second
        traversal, they either hit or miss. If they didn't meet, they will hit the end at the same iteration,
        pa == pb == None, return either one of them is the same, None.
        This works because pointer A walks through List A AND List B (since once it hits null, it goes to List B's
        head). Pointer B also walks through List B AND List A. Regardless of the length of the two lists, the sum of
        the lengths are the same (i.e. a+b = b+a), which means that the pointers sync up at the point of intersection.
        If the lists never intersected, it's fine too, because they'll sync up at the end of each list, both of which
        are null.
    Time complexity: O(M + N)
    Space complexity: O(1), exactly two pointers are used whatever N and M.
    """
    if not headA or not headB:
        return None
    pa, pb = headA, headB
    while pa != pb:
        pa = pa.next if pa else headB
        pb = pb.next if pb else headA
    return pa


def get_intersection_node_v2(headA, headB):
    """ To find the first overlapping node, we first compute the length of each list. The first overlapping node is
        determined by advancing through the longer list by the difference in lengths, and then advancing through both
        lists in tandem, stopping at the first common node. If we reach the end of a list without finding a common
        node, the lists do not overlap.
    Time complexity: O(N + M)
    Space complexity: O(1)
    """

    def length(head):
        count = 0
        temp = head
        while temp:
            count += 1
            temp = temp.next
        return count

    len1, len2 = length(headA), length(headB)
    pa, pb = headA, headB
    for _ in range(len1 - len2):
        pa = pa.next
    for _ in range(len2 - len1):
        pb = pb.next
    while pa != pb:
        pa, pb = pa.next, pb.next
    return pa


class Test(unittest.TestCase):
    eight = ListNode(8)
    eight.next = ListNode(4)
    eight.next.next = ListNode(5)
    head1 = ListNode(4)
    head1.next = ListNode(1)
    head1.next.next = eight
    head2 = ListNode(5)
    head2.next = ListNode(0)
    head2.next.next = ListNode(1)
    head2.next.next.next = eight

    def test_get_intersection_node(self):
        self.assertEqual(self.eight, get_intersection_node_v1(self.head1, self.head2))
        self.assertEqual(self.eight, get_intersection_node_v2(self.head1, self.head2))


if __name__ == '__main__':
    unittest.main()