""" You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes
first and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def add_two_numbers_v1(l1, l2):
    """ Start by adding leading zeroes to the shortest linked list. Once that done, it's easy to add the 2 linked lists
        when they have equal length. Recursively, traverse to the end of each list and then start adding values going
        backwards. Pay attention to cases that produce an addition carry. With each call, return that carry and the
        last created node that contains the last sum.
    Time complexity: O(N + M)
    Space complexity: O(max(N, M)), for the call stack
    """
    len1, len2 = get_length(l1), get_length(l2)
    l1 = add_leading_zeroes(len2 - len1, l1)
    l2 = add_leading_zeroes(len1 - len2, l2)
    carry, head = combine_lists(l1, l2)
    if carry:
        temp = ListNode(carry)
        temp.next = head
        head = temp
    return head


def get_length(head):
    length = 0
    while head:
        length += 1
        head = head.next
    return length


def add_leading_zeroes(n, head):
    for _ in range(n):
        new_node = ListNode(0)
        new_node.next = head
        head = new_node
    return head


def combine_lists(l1, l2):
    if not l1 and not l2:
        return 0, None
    carry, next_node = combine_lists(l1.next, l2.next)
    s = l1.val + l2.val + carry
    new_node = ListNode(s % 10)
    new_node.next = next_node
    carry = s // 10
    return carry, new_node


def add_two_numbers_v2(l1, l2):
    """ Iterative, stack based solution. Instead of reversing the linked lists or traveling to their tails to add the
        numbers recursively, traverse the two lists and store the values of their nodes in 2 separate stacks. Then pop
        elements off the stacks to construct a new list.
    Time complexity: O(N + M)
    Space complexity: O(N + M)
    """
    stack1, stack2 = [], []
    p1, p2 = l1, l2
    while p1:
        stack1.append(p1.val)
        p1 = p1.next
    while p2:
        stack2.append(p2.val)
        p2 = p2.next
    nxt, carry = None, 0
    while stack1 or stack2 or carry:
        val1 = stack1.pop() if stack1 else 0
        val2 = stack2.pop() if stack2 else 0
        s = val1 + val2 + carry
        node = ListNode(s % 10)
        node.next = nxt
        nxt, carry = node, s // 10
    return node


class Test(unittest.TestCase):
    l1 = ListNode(7)
    l1.next = ListNode(2)
    l1.next.next = ListNode(4)
    l1.next.next.next = ListNode(3)
    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)

    def test_add_two_numbers(self):
        l = add_two_numbers_v1(self.l1, self.l2)
        self.assertEqual(7, l.val)
        self.assertEqual(8, l.next.val)
        self.assertEqual(0, l.next.next.val)
        self.assertEqual(7, l.next.next.next.val)


if __name__ == '__main__':
    unittest.main()
