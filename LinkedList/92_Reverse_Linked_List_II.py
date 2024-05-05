""" Reverse a linked list from position m to n. Do it in one-pass.
Note: 1 ≤ m ≤ n ≤ length of list. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# Check out the illustration on this article: https://leetcode.com/articles/reverse-linked-list-ii/
# Video explanation: https://youtu.be/RF_M9tX4Eag
def reverse_between_v1(head, left, right):
    """ Starting from the node at 'left' position and all the way up to 'right', we reverse the next pointers for all
         the nodes in between.

            - We need two pointers, prev and cur. The prev pointer is initialized to None while cur is initialized to
               the head of the linked list.

            - We progress cur pointer one step at a time and the prev pointer follows it.

            - Keep progressing the two pointers in this way until cur pointer reaches the node at 'left' position.
               This is the point from where we start reversing the linked list.

            - Create two additional pointers called reversed_list_tail and connector. reversed_list_tail points to the
               node at 'left' position from the beginning of the linked list, since this node becomes the tail of the
               reversed sublist. The connector points to the node before 'left' and connects to the head of the reversed
               sublist.

            - reversed_list_tail and connector pointers are set once initially and then used at the end to finish the
               linked list reversal.

            - Once we reach the 'left' node, we iteratively reverse the links. We keep doing this until we are done
               reversing the link (next pointer) for the 'right' node. At that point, the prev pointer points to the
               'right' node.

            - Use the connector pointer to attach to the prev pointer since the node now pointed at by the prev pointer
               (the 'right' node) will come in place of the 'left' node after the reversal. Similarly, we make use of
               reversed_list_tail pointer to connect to the node next to the prev node i.e. (right+1)th node.

        To summarize:

            1- Walk (left - 1) steps to reach the first node of the range we want to reverse
            2- Reverse the range [left ... right]
            3- Fix the connections for the start and the end of the reversed list

    Time complexity: O(N)
    Space complexity: O(1)
    """
    prev, cur = None, head
    for _ in range(left - 1):
        # Move the two pointers until they reach the proper starting point in the list
        prev, cur = cur, cur.next
    connector, reversed_list_tail = prev, cur  # The two pointers that will fix the final connections
    for _ in range(right - left + 1):
        # Iteratively reverse the nodes
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    # Adjust the final connections.
    # 'connector' always points to the node preceding the leftmost node of the sublist before reversal.
    # At the end of reversal, 'prev' points to the head of the reversed sublist (the node at 'right' position)
    if connector:
        connector.next = prev
    else:
        # The case where the head of the linked list is the leftmost node of the sublist to reverse. We have 2 facts:
        # 1- 'connector' always points to the node preceding the leftmost node of the sublist before reversal.
        # 2- At the end of reversal, 'prev' points to the head of the reversed sublist (the node at 'right' position)
        # 1- and 2- combined mean that if the head of the linked list is the leftmost node of the sublist to reverse,
        # then the final linked list to return should have 'prev' as head.
        head = prev
    reversed_list_tail.next = cur
    return head


def reverse_between_v2(head, left, right):
    """ The use of a dummy head greatly simplifies the edge cases.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    prev, cur = dummy, head
    for _ in range(left - 1):
        prev, cur = cur, cur.next
    connector, reversed_list_tail = prev, cur
    for _ in range(right - left + 1):
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    connector.next = prev
    reversed_list_tail.next = cur
    return dummy.next


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    m = 2
    n = 4

    def test_reverse_between(self):
        head = reverse_between_v1(self.head, self.m, self.n)
        self.assertEqual(1, head.val)
        self.assertEqual(4, head.next.val)
        self.assertEqual(3, head.next.next.val)
        self.assertEqual(2, head.next.next.next.val)
        self.assertEqual(5, head.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()