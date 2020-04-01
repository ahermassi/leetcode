""" Given a linked list, swap every two adjacent nodes and return its head.
You may not modify the values in the list's nodes, only nodes itself may be changed.
"""

import unittest2 as unittest


# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def swap_pairs_v1(head):
    """ The basic intuition is to reach to the end of the linked list in steps of two using recursion, and while
        backtracking the nodes can be swapped. In every function call we take out two nodes which would be swapped and
        the remaining nodes are passed to the next recursive call. Assuming the recursion would return the swapped
        remaining list of nodes, we just swap the current two nodes and attach the remaining list we get from recursion
        to these two swapped pairs. Every recursion call is responsible for swapping a pair of nodes.
        Once we get the pointer to the remaining swapped list from the recursion call, we can swap the first node and
        second node i.e. the nodes in the current recursive call and then return the pointer to the second node since
        it will be the new head after swapping.
        Once all the pairs are swapped in the backtracking step, we would eventually be returning the pointer to the
        head of the now swapped list. This head will essentially be the second node in the original linked list.
    Time complexity: O(N)
    Space complexity: O(N) for the call stack
    """
    if not head or not head.next:
        return head
    p = swap_pairs_v1(head.next.next)  # Navigate to the last/before-last node (depends on even/odd length of the list)
    nxt = head.next
    nxt.next = head
    head.next = p
    return nxt  # After swapping, return the 'local' new head. The last one returned is the head of the entire new list


def swap_pairs_v2(head):
    """ Iterative solution.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    cur = dummy
    while cur.next and cur.next.next:
        first, second = cur.next, cur.next.next
        cur.next = second  # This will set the stage to swapping the following pair and makes dummy.next point to the
        # first swapped pair
        first.next = second.next
        second.next = first
        cur = second.next  # second.next = first and first.next = second.next which is the first node in the (following)
        # pair to swap. This ensures that cur's next always points to the first node in the pair, which is an invariant.
    return dummy.next


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)

    def test_swap_pairs(self):
        head = swap_pairs_v1(self.head)
        self.assertEqual(2, head.val)
        self.assertEqual(1, head.next.val)
        self.assertEqual(4, head.next.next.val)
        self.assertEqual(3, head.next.next.next.val)


if __name__ == '__main__':
    unittest.main()