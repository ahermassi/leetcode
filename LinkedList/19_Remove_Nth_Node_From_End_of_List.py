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
    length, temp = 0, head
    while temp:
        length += 1
        temp = temp.next
    if n == length:  # This is for the case of n == length of list, which means removing head of list
        return head.next
    length -= n
    temp = head
    for _ in range(length - 1):
        temp = temp.next
    temp.next = temp.next.next
    return head


def remove_nth_from_end_v2(head, n):
    """ One-pass approach.
        The above algorithm could be optimized to one pass. We use two iterators to traverse the list. The first
        iterator is advanced by n steps from the head of the list, and then the two iterators advance in tandem. When
        the first iterator reaches the tail, the second iterator is at the (n + 1)th last node, and we can remove the
        nth node.
        We add an auxiliary dummy node, which points to the list head. The dummy node is used to simplify some corner
        cases such as a list with only one node, or removing the head of the list.
    Time complexity: O(N), where N is list length
    Space complexity: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    slow, fast = dummy, dummy.next
    for _ in range(n):
        fast = fast.next
    while fast:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next


def remove_nth_from_end_v3(head, n):
    """ Recursive solution.
        Recursively advance through the list until the tail is reached. At this point, start moving backwards and keep
        count of number of steps. (n-1)th step lands on the node that needs to be deleted.
    """

    def remove(head):
        if not head:
            return 0, None
        i, head.next = remove(head.next)
        return i + 1, (head, head.next)[i == n - 1]  # If I'm (n-1)th node from end, my previous node (my caller)
        # next pointer should point to my next node
        # Equivalent to:
        # if i == n - 1:
        #   return i + 1, head.next
        # else:
        #   return i + 1, head

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