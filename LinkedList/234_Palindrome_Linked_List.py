""" Given a singly linked list, determine if it is a palindrome. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def is_palindrome_v1(head):
    """ The naive approach would be to run through the linked list and create an array of its values, then compare the
         array to its reverse to find out if it's a palindrome.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values == values[::-1]


def is_palindrome_v2(head):
    """ Reverse the second half of the linked list in-place (modifying the list structure), and then compare it with
        the first half.

        Imagine we have 2 runners, one fast and one slow, running down the nodes of the list. At each step, the fast
        runner moves down 2 nodes, and the slow runner just 1 node. By the time the fast runner gets to the end of the
        list, the slow runner will be half way.

        Get the reverse of the second half, after which testing for palindromicity reduces to testing if the first half
        and the reversed second half are equal. We step down the lists simultaneously ensuring the node values are
        equal. When the node we're up to in the second list is null, we know we're done. If there was a middle value
        attached to the end of the first list, it is correctly ignored by the algorithm.

        The downside of this approach is that in a concurrent environment (multiple threads and processes accessing the
        same data), access to the linked list by other threads or processes would have to be locked while this function
        is running, because the linked list is temporarily broken. This is a limitation of many in-place algorithms.



    Time complexity: O(N)
    Space complexity: O(1), we are changing the next pointers for half of the nodes. This was all memory that had
    already been allocated, so we are not using any extra memory.
    """
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    pre = None
    while slow:
        nxt = slow.next
        slow.next = pre
        pre, slow = slow, nxt
    ptr1, ptr2 = head, pre
    while ptr2:
        # After the second half is reversed, middle node's next is set to null to indicate end of list. For
        # this reason, when 'rev' reaches the middle of the list it gets the null value. Equivalent to 'while temp: ...'
        if ptr1.val != ptr2.val:
            return False
        ptr1, ptr2 = ptr1.next, ptr2.next
    return True


class Test(unittest.TestCase):
    head1 = ListNode(1)
    head1.next = ListNode(2)
    head2 = ListNode(1)
    head2.next = ListNode(2)
    head2.next.next = ListNode(2)
    head2.next.next.next = ListNode(1)

    def test_is_palindrome(self):
        self.assertFalse(is_palindrome_v1(self.head1))
        self.assertTrue(is_palindrome_v1(self.head2))
        self.assertFalse(is_palindrome_v2(self.head1))
        self.assertTrue(is_palindrome_v2(self.head2))


if __name__ == '__main__':
    unittest.main()

