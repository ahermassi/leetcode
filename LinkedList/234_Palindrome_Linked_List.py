""" Given a singly linked list, determine if it is a palindrome. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def is_palindrome_v1(head):
    """ Insert the nodes' values in an array and check for reversibility.
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
        Get the reverse of the second half, after which testing palindromicity of the original list reduces to testing
        if the first half and the reversed second half are equal. This approach changes the list passed in, but the
        reversed sublist can be reversed again to restore the original list.
    Time complexity: O(N)
    Space complexity: O(1), we are changing the next pointers for half of the nodes. This was all memory that had
    already been allocated, so we are not using any extra memory.
    """

    def reverse(node):
        pre, cur = None, node
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre

    slow, fast = head, head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    rev = reverse(slow)
    temp = head
    while rev:  # After the second half is reversed, middle node's next is set to null to indicate end of list. For
        # this reason, when 'rev' reaches the middle of the list it gets the null value. Equivalent to 'while temp: ...'
        if temp.val != rev.val:
            return False
        temp = temp.next
        rev = rev.next
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

