""" Given a singly linked list L: L0→L1→…→Ln-1→Ln,
reorder it to: L0→Ln→L1→Ln-1→L2→Ln-2→…
You may not modify the values in the list's nodes, only nodes itself may be changed. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def reorder_list_v1(head):
    """ Find the middle of the list. Reverse the half after middle. Start reordering one by one.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not head:
        return None
    slow, fast = head, head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    pre, node = None, slow
    while node:
        pre, node.next, node = node, pre, node.next
    first, second = head, pre  # 'pre' points to the head of second reversed half, which used to be the last node
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    return head


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)

    def test_reorder_list(self):
        head = reorder_list_v1(self.head)
        self.assertEqual(1, head.val)
        self.assertEqual(5, head.next.val)
        self.assertEqual(2, head.next.next.val)
        self.assertEqual(4, head.next.next.next.val)
        self.assertEqual(3, head.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()
