""" Given a linked list, determine if it has a cycle in it. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def has_cycle_v1(head):
    """ Floyd's cycle detection algorithm, or 'the tortoise and the hare' algorithm.
        Consider two pointers at different speed - a slow pointer and a fast pointer. The slow pointer moves one step
        at a time while the fast pointer moves two steps at a time. If there is no cycle in the list, the fast pointer
        will eventually reach the end and we can return false in this case.
        Now consider a cyclic list and imagine the slow and fast pointers are two runners racing around a circle track.
        The fast runner will eventually meet the slow runner. Why? Consider this case (we name it case A) - The fast
        runner is just one step behind the slow runner. In the next iteration, they both increment one and two steps
        respectively and meet each other.
        How about other cases? For example, we have not considered cases where the fast runner is two or three steps
        behind the slow runner yet. This is simple, because in the next or next's next iteration, this case will be
        reduced to case A mentioned above.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


def has_cycle_v2(head):
    """ We go through each node one by one and record each node's reference in a hash set. If the current node is null,
        we have reached the end of the list and it must not be cyclic. If current node’s reference is in the hash set,
        then return true.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    nodes = set()
    while head:
        if head in nodes:
            return True
        nodes.add(head)
        head = head.next
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

    def test_has_cycle(self):
        self.assertTrue(has_cycle_v1(self.head1))
        self.assertFalse(has_cycle_v1(self.head2))
        self.assertTrue(has_cycle_v2(self.head1))
        self.assertFalse(has_cycle_v2(self.head2))


if __name__ == '__main__':
    unittest.main()