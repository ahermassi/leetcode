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

            - We need two pointers, prev and cur. The prev pointer should be initialized to None initially while cur is
               initialized to the head of the linked list.

            - We progress cur pointer one step at a time and the prev pointer follows it.

            - Keep progressing the two pointers in this way until cur pointer reaches the node at 'left' position.
               This is the point from where we start reversing the linked list.

            - Create two additional pointers called tail and connector. The tail pointer points to the node at 'left'
               position from the beginning of the linked list, and we call it a tail pointer since this node becomes the
               tail of the reversed sublist. The connector points to the node before 'left' node and connects to the
               head of the reversed sublist.

            - The tail and the connector pointers are set once initially and then used at the end to finish the linked
               list reversal.

            - Once we reach the 'left' node, we iteratively reverse the links. We keep doing this until we are done
               reversing the link (next pointer) for the 'right' node. At that point, the prev pointer points to the
               'right' node.

            - Use the connector pointer to attach to the prev pointer since the node now pointed at by the prev pointer
               (the 'right' node) will come in place of the 'left' node after the reversal. Similarly, we make use of
               the tail pointer to connect to the node next to the prev node i.e. (right+1)th node.

        To summarize:

            1- Walk (left - 1) steps to reach the first node of the range we want to reverse
            2- Reverse the range [left ... right]
            3- Fix the connections for the start and the end of the reversed list

    Time complexity: O(N)
    Space complexity: O(1)
    """
    pre, cur = None, head
    for _ in range(left - 1):
        # Move the two pointers until they reach the proper starting point in the list
        pre = cur
        cur = cur.next
    connector, tail = pre, cur  # The two pointers that will fix the final connections
    for _ in range(right - left + 1):
        # Iteratively reverse the nodes
        node_to_reverse = cur.next
        cur.next = pre
        pre = cur
        cur = node_to_reverse
    # Adjust the final connections
    if connector:
        connector.next = pre
    else:
        head = pre
    tail.next = cur
    return head


def reverse_between_v2(head, m, n):
    """ Another iterative version using a dummy head. The difference between the 2 solutions is that the first solution
        makes (n-m+1) reversals starting from the head of the sublist and reversing ALL the nodes of the sublist,
        while the second solution makes (n-m) reversals starting from the second node of the sublist and reversing
        (len(sublist) - 1) nodes.
        The invariants of this algorithm are the following:
            pre.next always points to the last node that's been just reversed
            cur.next always points to the node to reverse in the following iteration
        During the execution, pre.next will keep pointing to the last reversed node until the entire sublist is
        reversed. At this point, pre.next points to the head of the new reversed sublist. This is equivalent to
        con.next = pre in the previous solution where we connect the node before the head of the sublist (before
        reversal) to the head of the new reversed sublist.
        During the execution, cur.next will keep pointing to the following node to reverse until the entire sublist is
        reversed. At this point, cur.next points to the node just after the tail of the old sublist. This is equivalent
        to tail.next = cur in the previous solution.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    pre = dummy  # Make a pointer 'pre' as a marker for the node before reversing
    for _ in range(m - 1):
        pre = pre.next
    cur = pre.next  # Pointer to the beginning of the sub-list that will be reversed
    node_to_reverse = cur.next  # Pointer to the node that will be reversed
    # 1 - 2 -3 - 4 - 5 ; m=2; n =4 ---> pre = 1, cur = 2, node_to_reverse = 3
    # dummy-> 1 -> 2 -> 3 -> 4 -> 5
    for _ in range(n - m):
        cur.next = node_to_reverse.next  # cur.next always points to the node to reverse in the following iteration
        node_to_reverse.next = pre.next
        pre.next = node_to_reverse  # pre.next always points to the node that's been just reversed
        node_to_reverse = cur.next  # Move on and reverse the next node
    # First reversing : dummy->1 -> 3 -> 2 -> 4 -> 5; pre = 1, cur = 2, node_to_reverse = 4
    # Second reversing: dummy->1 -> 4 -> 3 -> 2 -> 5; pre = 1, cur = 2, node_to_reverse = 5 (finish)
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