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
    if n == length:  # This is for the case of n is equal to the length of list, which means removing head of list
        return head.next
    cur = head
    for _ in range(length - n - 1):
        cur = cur.next
    cur.next = cur.next.next
    return head


def remove_nth_from_end_v2(head, n):
    """ One-pass approach.

        First we will add an auxiliary "dummy" node, which points to the list head. The "dummy" node is used to simplify
        some corner cases such as a list with only one node, or removing the head of the list.

        The above algorithm could be optimized to one pass. We use two pointers to traverse the list. The first
        pointer is advanced by (n+1) steps from the dummy head of the list. Now, both pointers are separated by exactly
         n nodes apart.

         We maintain this constant gap by advancing both pointers in tandem. When the first pointer
        reaches the tail, the second pointer is at the (n + 1)th last node, just the right spot for it to be able to
        skip the next node. We relink the next pointer of the node referenced by the second pointer to point to the
        node's next next node.

        For eg. let the list be 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9, and n = 4.

        dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> null
        ^                                                 ^
       slow                                            fast
        |<--      gap of n+1 nodes    -->|

        => Now traverse till fast reaches end

        dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> null
                                                           ^                                        ^
                                                         slow                                     fast
                                                           |<-- gap of n+1 nodes-->|

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
    while fast:  # Move fast to the end, maintaining the gap
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next


def remove_nth_from_end_v3(head, n):
    """ One-pass without using a dummy head node.

        To do that, we can simply stagger our two pointers by n nodes by giving the first pointer (fast) a head start
        before starting the second pointer (slow). Doing this will cause slow to reach the nth node from the end at the
        same time that fast reaches the end.

        This will unfortunately cause a problem when n is the same as the length of the list, which would make the
        first node the target node, and thus make it impossible to find the node before the target node. If that's the
        case, however, we can just return head.next without needing to stitch together the two sides of the target node.

        Since we will need access to the node before the target node in order to remove the target node, we can use
        fast.next == null as our exit condition, rather than fast == null, so that we stop one node earlier.

        Otherwise, once we successfully find the node before the target, we can then stitch it together with the node
        after the target, and then return head.

        For eg. let the list be 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9, and n = 4.

        1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> null
        ^                               ^
       slow                          fast
        |<-- gap of n nodes -->|

        => Now traverse till fast reaches end

        1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> null
                                          ^                               ^
                                        slow                          fast
                                       |<-- gap of n nodes -->|

    Time complexity: O(N)
    Space complexity: O(1)
    """

    fast = head
    for _ in range(n):
        fast = fast.next
    if not fast:
        # If fast is null at the end of the for loop, it means that the nth node from the end is actually the first
        # node. The while loop is an attempt to move slow to the node before the node to be removed, which obviously
        # can't happen if the node to be removed is the first node, as there is no node before it. So if fast == null,
        # then we should just return the list with the first node removed, or head.next.
        return head.next
    slow = head
    while fast.next:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
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
