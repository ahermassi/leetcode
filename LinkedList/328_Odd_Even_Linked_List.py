""" Given a singly linked list, group all odd nodes together followed by the even nodes. Please note here we are
talking about the node number and not the value in the nodes.
You should try to do it in place. The program should run in O(1) space complexity and O(nodes) time complexity. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def odd_even_list(head):
    """ Put the odd nodes in a linked list and the even nodes in another. Then link the tail of the odd list to the
        even list.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not head or not head.next:
        return head
    odd, even, nxt = head, head.next, head.next
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = nxt
    return head


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)

    def test_odd_even_list(self):
        head = odd_even_list(self.head)
        self.assertEqual(1, head.val)
        self.assertEqual(3, head.next.val)
        self.assertEqual(5, head.next.next.val)
        self.assertEqual(2, head.next.next.next.val)
        self.assertEqual(4, head.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()
