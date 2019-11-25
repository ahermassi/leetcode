""" You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse
order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def add_two_numbers(l1, l2):
    """ Keep track of the carry using a variable and simulate digits-by-digits sum starting from the head of list,
        which contains the least-significant digit.
        Note that we use a dummy head to simplify the code. Without a dummy head, we would have to write extra
        conditional statements to initialize the head's value.
    Time complexity: O(max(N, M)), where N and M are the length of l1 and l2 respectively
    Space complexity: O(1)
    """
    dummy = ListNode(0)
    tail, temp1, temp2, carry = dummy, l1, l2, 0
    while temp1 or temp2:
        val1 = temp1.val if temp1 else 0
        val2 = temp2.val if temp2 else 0
        s = val1 + val2 + carry
        tail.next = ListNode(s % 10)
        carry = s // 10
        tail = tail.next
        temp1 = temp1.next if temp1 else None
        temp2 = temp2.next if temp2 else None
    if carry:
        tail.next = ListNode(carry)
    return dummy.next


class Test(unittest.TestCase):
    l1 = ListNode(2)
    l1.next = ListNode(4)
    l1.next.next = ListNode(3)
    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)

    def test_add_two_numbers(self):
        l = add_two_numbers(self.l1, self.l2)
        self.assertEqual(7, l.val)
        self.assertEqual(0, l.next.val)
        self.assertEqual(8, l.next.next.val)


if __name__ == '__main__':
    unittest.main()