""" Reverse a linked list from position m to n. Do it in one-pass.
Note: 1 ≤ m ≤ n ≤ length of list. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# Checkout the illustration on this article: https://leetcode.com/articles/reverse-linked-list-ii/

def reverse_between_v1(head, m, n):
    """ Starting from the node at position m and all the way up to n, we reverse the next pointers for all the nodes in
        between.
        We need two pointers, prev and cur. The prev pointer should be initialized to None initially while cur is
        initialized to the head of the linked list.
        We progress the cur pointer one step at a time and the prev pointer follows it.
        We keep progressing the two pointers in this way until the cur pointer reaches the mth node from the beginning
        of the list. This is the point from where we start reversing our linked list.
        An important thing to note here is the usage of two additional pointers which we will call as tail and con.
        The tail pointer points to the mth node from the beginning of the linked list and we call it a tail pointer
        since this node becomes the tail of the reverse sublist. The con points to the node one before mth node and
        this connects to the new head of the reversed sublist.
        The tail and the con pointers are set once initially and then used in the end to finish the linked list
        reversal.
        Once we reach the mth node, we iteratively reverse the links as explained before using the two pointers. We
        keep on doing this until we are done reversing the link (next pointer) for the nth node. At that point, the
        prev pointer would point to the nth node.
        We use the con pointer to attach to the prev pointer since the node now pointed to by the prev pointer (the nth
        node from the beginning) will come in place of the mth node due after the reversal. Similarly, we will make use
        of the tail pointer to connect to the node next to the prev node i.e. (n+1)th node from the beginning.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    pre, cur = None, head
    for _ in range(m - 1):  # Move the two pointers until they reach the proper starting point in the list
        pre = cur
        cur = cur.next
    con, tail = pre, cur  # The two pointers that will fix the final connections
    for _ in range(n - m + 1):  # Iteratively reverse the nodes
        third = cur.next
        cur.next = pre
        pre = cur
        cur = third
    # Adjust the final connections
    if con:
        con.next = pre
    else:
        head = pre
    tail.next = cur
    return head


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    m = 2
    n = 4

    def test_reverse_between(self):
        head = reverse_between_v1(self.head, self.m, self.n)
        self.assertEqual(1, head.val)
        self.assertEqual(4, head.next.val)
        self.assertEqual(3, head.next.next.val)
        self.assertEqual(2, head.next.next.next.val)
        self.assertEqual(5, head.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()