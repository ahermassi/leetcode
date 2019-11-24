""" You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes
first and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def add_two_numbers(l1, l2):
    """ Start by adding leading zeroes to the shortest linked list. Once that done, it's easy to add the 2 linked lists
        when they have equal length. Recursively, traverse to the end of each list and then start adding values going
        backwards. Pay attention to cases that produce an addition carry. With each call, return that carry and the
        last created node that contains the last sum.
    Time complexity: O(N + M)
    Space complexity: O(max(N, M)) for the call stack
    """
    len1, len2 = get_length(l1), get_length(l2)
    l1 = add_leading_zeroes(len2 - len1, l1)
    l2 = add_leading_zeroes(len1 - len2, l2)
    carry, last_node = combine_lists(l1, l2)
    if carry:
        l3 = ListNode(carry)
        l3.next = last_node
        last_node = l3
    return last_node


def get_length(node):
    i = 0
    while node:
        i += 1
        node = node.next
    return i


def add_leading_zeroes(n, node):
    for _ in range(n):
        new_node = ListNode(0)
        new_node.next = node
        node = new_node
    return node


def combine_lists(l1, l2):
    if not l1 and not l2:
        return 0, None
    carry, last_node = combine_lists(l1.next, l2.next)
    s = l1.val + l2.val + carry
    new_node = ListNode(s % 10)
    new_node.next = last_node
    carry = s // 10
    return carry, new_node


class Test(unittest.TestCase):
    l1 = ListNode(7)
    l1.next = ListNode(2)
    l1.next.next = ListNode(4)
    l1.next.next.next = ListNode(3)
    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)

    def test_add_two_numbers(self):
        l = add_two_numbers(self.l1, self.l2)
        self.assertEqual(7, l.val)
        self.assertEqual(8, l.next.val)
        self.assertEqual(0, l.next.next.val)
        self.assertEqual(7, l.next.next.next.val)


if __name__ == '__main__':
    unittest.main()
