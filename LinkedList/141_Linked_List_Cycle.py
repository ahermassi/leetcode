""" Given a linked list, determine if it has a cycle in it. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# Video explanation: https://www.youtube.com/watch?v=gBTe7lFR3vc
def has_cycle_v1(head):
    """ Floyd's Cycle Detection, or 'the Tortoise and the Hare' Algorithm.

        Consider two pointers at two different speeds - a slow pointer and a fast pointer. The slow pointer moves one
        step at a time while the fast pointer moves two steps at a time. If there is no cycle in the list, the fast
        pointer will eventually reach the end, and we can return false in this case.

        Now consider a cyclic list and imagine the slow and fast pointers are two runners racing around a circle track.
        The fast runner will eventually meet the slow runner. Why? Consider this case- The fast runner is just one step
        behind the slow runner. In the next iteration, they both increment one and two steps respectively and meet each
        other.

        How about other cases? For example, we have not considered cases where the fast runner is two or three steps
        behind the slow runner yet. This is simple, because in the next or next's next iteration, this case will be
        reduced to the case mentioned above.

        Why does it work?

        Walker goes 1 step at a time, and runner goes 2 steps at a time. If we think walker is still, then runner goes 1
        step at a time. So, there is eventually a time when runner catches walker.

        If there is a cycle then there will be a time when walker will enter the cycle for the first time. At that
        moment, runner will already be present in the cycle (because he was fast and ahead).
        Now if the runner is also at the same node as walker, problem solved.
        Otherwise, if both runner and walker are at different nodes in the cycle, then relative velocity of runner with
        respect to walker is one node per iteration (because walker moves one step then runner moves two steps and
        therefore relative velocity is 2 - 1 = 1). It can we viewed as if runner is closing in on walker. So that means
        runner will surely catch the walker.

        Every step of the while loop decreases the number of nodes between walker and runner by one. Once the runner
        is directly behind the walker (no nodes in between), then the next step of the loop makes them meet. The only
        way for the runner to "skip" the walker is if they were on the same node, but the loop would've ended if that
        occurred.

    Time complexity: O(N), we consider the following two cases separately:
        - List has no cycle: the fast pointer reaches the end first and the runtime depends on the list's length, O(N)
        - List has a cycle: we break down the movement of the slow pointer into two steps, the non-cyclic part and the
           cyclic part:
            From start point to the beginning of circle/cycle, the distance is a.
            From the start point of the circle to the meeting point, the distance is b.
            From meeting point to beginning of circle is c.
            So b + c = circumference of the circle.
            When fast and slow meet, total distance of:
            slow runner = a + b
            fast runner  = a + b + (b + c) * k (k = 1, 2, 3...)
            Since fast runner = 2 * slow runner
            —> a + b + (b + c) * k  = 2 * (a + b)
            —> (b + c) * k = a + b
            We conclude that number of iterations = almost cyclic length (b+c).
        Therefore, the worst-case time complexity is O(N+(b+c)), which is O(N)
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
        we have reached the end of the list, and it must not be cyclic. If current node’s reference is in the hash set,
        then a cycle must exist.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    seen_nodes = set()
    cur = head
    while cur:
        if cur in seen_nodes:
            return True
        seen_nodes.add(cur)
        cur = cur.next
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