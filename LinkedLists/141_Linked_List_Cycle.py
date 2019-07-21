""" Given a linked list, determine if it has a cycle in it. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def has_cycle_v1(head):
    """ The idea is to visit each node and replace its value with -infinity. If visited again, -infinity indicates
    the presence of a cycle.
    Time complexity: O(N), where N is the length of the linked list
    Space complexity: O(1)
    """
    while head:
        if head.val == float('-inf'):
            return True
        head.val = float('-inf')
        head = head.next
    return False


def has_cycle_v2(head):
    """ Use fast and slow pointers. Fast pointer runs 2 steps at a time and slow pointer runs 1 step at a time. They
    both start from beginning. If faster pointer catches slow pointer some time, it means linked list has a circle.
    This algorithm is called Floyd's cycle detection algorithm, or the tortoise and the hare algorithm.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    try:
        slow, fast = head, head.next
        while slow is not fast:
            slow = slow.next
            fast = fast.next.next
        return True
    except AttributeError:  # The "trick" is to not check all the time whether we have reached the end but to handle
        # it via an exception. This technique is known as Easier to Ask for Forgiveness than Permission, or EAFP.
        return False


class Test(unittest.TestCase):
    head1 = ListNode(3)
    head1.next = ListNode(2)
    head1.next.next = ListNode(0)
    head1.next.next.next = ListNode(-4)
    head1.next.next.next.next = head1.next
    head2 = ListNode(1)
    head2.next = ListNode(1)
    head2.next.next = ListNode(2)
    head2.next.next.next = ListNode(3)

    def test_next_greater_element(self):
        self.assertTrue(has_cycle_v1(self.head1))
        self.assertFalse(has_cycle_v1(self.head2))
        self.assertTrue(has_cycle_v2(self.head1))
        self.assertFalse(has_cycle_v2(self.head2))


if __name__ == '__main__':
    unittest.main()