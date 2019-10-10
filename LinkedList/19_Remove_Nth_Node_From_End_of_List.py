""" Given a linked list, remove the n-th node from the end of list and return its head. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def remove_nth_from_end_v1(head, n):
    """ Two pass approach.
        We notice that the problem could be simply reduced to another one : Remove the (L - n + 1)th node from the
        beginning in the list , where L is the list length. This problem is easy to solve once we found list length L.
    Time complexity: O(L), where L is list length
    Space complexity: O(1)
    """
    length, temp = 0, head
    while temp:
        length += 1
        temp = temp.next
    if n == length:
        return head.next
    length -= n
    temp = head
    for _ in range(length - 1):
        temp = temp.next
    temp.next = temp.next.next
    return head


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    n = 2

    def test_remove_nth_from_end(self):
        head = remove_nth_from_end_v1(self.head, self.n)
        self.assertEqual(1, head.val)
        self.assertEqual(2, head.next.val)
        self.assertEqual(3, head.next.next.val)
        self.assertEqual(5, head.next.next.next.val)


if __name__ == '__main__':
    unittest.main()