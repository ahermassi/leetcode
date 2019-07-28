""" Write a program to find the node at which the intersection of two singly linked lists begins. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def get_intersection_node_v1(headA, headB):
    """ Maintain two pointers pa and pb initialized at the head of A and B, respectively. Then let them both traverse
        through the lists, one node at a time. When pa reaches the end of list A, then redirect it to the head of B ;
        similarly when pb reaches the end of list B, redirect it the head of A. If at any point pa meets pb, then pa
        (or pb) is the intersection node.
        The idea is if you switch head, the possible difference between lengths would be countered. On the second
        traversal, they either hit or miss. If they didn't meet, they will hit the end at the same iteration,
        pa == pb == None, return either one of them is the same, None.
    Time complexity: O(M + N)
    Space complexity: O(1), exactly two pointers are used whatever N and M.
    """
    if headA and headB:
        pa, pb = headA, headB
        while pa != pb:
            pa = pa.next if pa else headB
            pb = pb.next if pb else headA
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

    def test_merge_two_lists(self):
        self.assertEqual(self.eight, get_intersection_node_v1(self.head1, self.head2))


if __name__ == '__main__':
    unittest.main()