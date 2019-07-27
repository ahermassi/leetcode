""" Reverse a singly linked list. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def reverse_list_v1(head):
    """ Push all nodes to a stack, then pop them in order to get the linked list in reverse order.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not head:
        return None
    stack = []
    while head:
        stack.append(head)
        head = head.next
    head = stack.pop()
    temp = head
    while stack:
        temp.next = stack.pop()
        temp = temp.next
    temp.next = None
    return head


def reverse_list_v2(head):  # Iterative approach
    curr, prev = head, None
    while curr:
        temp = curr.next
        curr.next = prev
        prev = curr
        curr = temp
    return prev


def reverse_list_v3(head):  # Recursive approach
    if not head or not head.next:
        return head
    p = reverse_list_v2(head.next)
    head.next.next = head
    head.next = None
    return p


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    reversed_list1 = reverse_list_v1(head)

    def test_reverse_list(self):
        self.assertEqual(5, self.reversed_list1.val)
        self.assertEqual(4, self.reversed_list1.next.val)
        self.assertEqual(3, self.reversed_list1.next.next.val)
        self.assertEqual(2, self.reversed_list1.next.next.next.val)
        self.assertEqual(1, self.reversed_list1.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()


