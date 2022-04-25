""" Reverse a singly linked list. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def reverse_list_v1(head):
    """ Push all nodes to a stack, then pop them in order to get the linked list in reverse order.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not head:
        return None
    stack = []
    while head:
        stack.append(head)
        head = head.next
    head = stack.pop()
    temp = head
    while stack:
        temp.next = stack.pop()
        temp = temp.next
    temp.next = None
    return head


def reverse_list_v2(head):
    """ While traversing the list, change the current node's next pointer to point to its previous element.
        Since a node does not have reference to its previous node, store its previous element beforehand. Another
        pointer is also needed to store the next node before changing the reference.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    cur, prev = head, None
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def reverse_list_v3(head):
    """ Recursive approach. Traverse the list recursively until the tail is reached. From there, reverse each two
        consecutive nodes and return the new head.

        The recursive version is slightly trickier and the key is to work backwards.
        Assume that the rest of the list had already been reversed, now how do we reverse the front part? Let's assume
        the list is:

        n1 → … → nk-1 → nk → nk+1 → … → nm → Ø
        Assume from node nk+1 to nm had been reversed, and we are at node nk:

        n1 → … → nk-1 → nk → nk+1 ← … ← nm

        We want nk+1’s next node to point to nk. So: nk.next.next = nk
        Be very careful that n1's next must point to Ø. If we forget this, the linked list will have a cycle in it.

    Time complexity: O(N)
    Space complexity: O(N), the recursion could go up to N levels deep
    """
    if not head or not head.next:  # If tail is reached, return it to become the new head
        return head
    reversed_rest = reverse_list_v2(head.next)  # When the tail is reached, 'reversed_rest' points to the tail,
    # which is the new list's head
    head.next.next = head
    head.next = None
    return reversed_rest  # Return the new head


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    reversed_list1 = reverse_list_v1(head)

    def test_reverse_list(self):
        self.assertEqual(5, self.reversed_list1.val)
        self.assertEqual(4, self.reversed_list1.next.val)
        self.assertEqual(3, self.reversed_list1.next.next.val)
        self.assertEqual(2, self.reversed_list1.next.next.next.val)
        self.assertEqual(1, self.reversed_list1.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()


