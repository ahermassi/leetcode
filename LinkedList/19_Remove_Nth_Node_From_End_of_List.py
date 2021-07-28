""" Given a linked list, remove the n-th node from the end of list and return its head. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def remove_nth_from_end_v1(head, n):
    """ Two-pass approach.
        We notice that the problem could be simply reduced to another one : Remove the (L - n + 1)th node from the
        beginning in the list , where L is the list length. This problem is easy to solve once we found list length L.
    Time complexity: O(N), where N is list length
    Space complexity: O(1)
    """
    length, cur = 0, head
    while cur:
        length += 1
        cur = cur.next
    if n == length:  # This is for the case of n == length of list, which means removing head of list
        return head.next
    cur = head
    for _ in range(length - n - 1):
        cur = cur.next
    cur.next = cur.next.next
    return head


def remove_nth_from_end_v2(head, n):
    """ One-pass approach.
        The above algorithm could be optimized to one pass. We use two pointers to traverse the list. The first
        pointer is advanced by (n+1) steps from the head of the list. Now, both pointers are separated by exactly n
        nodes apart. We maintain this constant gap by advancing both pointers in tandem. When the first pointer
        reaches the tail, the second pointer is at the (n + 1)th last node, just the right spot for it to be able to
        skip the next node.. We relink the next pointer of the node referenced by the second pointer to point to the
        node's next next node.
        We use an auxiliary dummy node, which points to the list head. The dummy node is used to simplify some corner
        cases such as a list with only one node, or removing the head of the list.
        For eg. let the list be 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9, and n = 4.

        1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> null
        ^slow               ^fast
        |<--gap of n nodes-->|

        => Now traverse till fast reaches end

        2. 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> null
                                ^slow               ^fast
                                |<--gap of n nodes-->|

        'slow' is at (n+1)th node from end.
        So just delete nth node from end by assigning slow -> next as slow -> next -> next.
    Time complexity: O(N), where N is list length
    Space complexity: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    slow = fast = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next


def remove_nth_from_end_v3(head, n):
    """ Recursive solution.
        Recursively advance through the list until the tail is reached. At this point, start moving backwards and keep
        count of number of steps. (n-1)th step lands on the node that needs to be deleted.
    Time complexity: O(N), where N is list length
    Space complexity: O(N)
    """

    def remove(node):
        if not head:
            return 0, None
        i, node.next = remove(node.next)
        # If I'm (n-1)th node from end, my previous node's (my caller) next pointer should point to my next node
        if i == n - 1:
            return i + 1, node.next
        return i + 1, node
        # Equivalent to:
        # return i + 1, (head, head.next)[i == n - 1]

    return remove(head)[1]


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
