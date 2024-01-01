""" You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse
order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# Video explanation: https://youtu.be/wgFPrzTjm7s
def add_two_numbers(l1, l2):
    """ A singly linked list whose nodes contain digits can be viewed as an integer, with the least significant digit
         coming first. Such a representation can be used to represent unbounded integers.

         Note that we cannot simply convert the lists to integers, since the integer word length is fixed by the machine
         architecture, and the lists can be arbitrarily long. Instead, we mimic the grade-school algorithm, i.e., we
         compute the sum of the digits in corresponding nodes in the two lists.

        A key nuance of the computation is handling the carry-out. Keep track of the carry using a variable and simulate
        digits-by-digits sum starting from the head of list, which contains the least-significant digit.

        Just like how we would sum two numbers on a piece of paper, we begin by summing the least-significant digits,
        which is the head of l1l1 and l2l2. Since each digit is in the range of 0…9, summing two digits may "overflow".
        For example 5 + 7 = 125+7=12. In this case, we set the current digit to 2 and bring over the carry = 1 to the
        next iteration.

        Note that we use a dummy head to simplify the code. Without a dummy head, we would have to write extra
        conditional statements to initialize the head's value.

        The algorithm continues processing input until both lists are exhausted and there is no remaining carry.

    Time complexity: O(max(N, M)), where N and M are the length of l1 and l2 respectively
    Space complexity: O(1)
    """
    dummy = tail = ListNode(0)
    carry = 0
    while l1 or l2 or carry:
        val1, val2 = l1.val if l1 else 0, l2.val if l2 else 0
        s = val1 + val2 + carry
        tail.next = ListNode(s % 10)
        carry = s // 10
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
        tail = tail.next
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
