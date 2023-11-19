""" Given a singly linked list L: L0→L1→…→Ln-1→Ln,
reorder it to: L0→Ln→L1→Ln-1→L2→Ln-2→…
You may not modify the values in the list's nodes, only nodes itself may be changed. """

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

# Video explanation: https://www.youtube.com/watch?v=S5bfdUTrKLM


def reorder_list_v1(head):
    """ Reverse the second half of the list and merge the two halves.

        Let's use two pointers, slow and fast. While the slow pointer moves one step forward, the fast pointer moves
        two steps forward, i.e. fast traverses twice as fast as slow. When the fast pointer reaches the end of the list,
        the slow pointer should be in the middle.

        Let's traverse the list starting from the middle node slow and its virtual predecessor None. For each current
        node, save its neighbours: The previous node prev and the next node nxt = cur.next.
        While we're moving along the list, change the node's next pointer to point to the previous node and shift the
        current node to the right for the next iteration

        Let's pick the first node of each list - first_head and second_head, and save their successors. While we're
        traversing the list, set first_head node's next pointer to point to second_head, and second_head node's next
        pointer to point to the successor of first_head. For this iteration the job is done, and for the next iteration
        move to the previously saved nodes' successors.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    slow, fast = head, head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    cur, prev = slow, None
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    # That's equivalent to the more Pythonic following block:
    # while cur:
    #     prev, cur.next, cur = cur, prev, cur.next
    # 'prev' points to the head of second reversed half, which used to be the last 'cur'
    first_head, second_head = head, prev
    while second_head.next:
        nxt1, nxt2 = first_head.next, second_head.next
        # Rewire the nodes
        first_head.next = second_head
        second_head.next = nxt1
        first_head, second_head = nxt1, nxt2


def reorder_list_v2(head):
    """ Straightforward stack solution. Push all nodes to stack and connect them by alternation.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not head or not head.next:
        return
    cur, stack, = head, []
    while cur:
        stack.append(cur)
        cur = cur.next
    size = len(stack)
    cur = head
    for _ in range(size // 2):  # Between every two nodes insert the one in the top of the stack
        nxt = cur.next
        top = stack.pop()
        cur.next = top
        top.next = nxt
        cur = nxt
    cur.next = None
    return head


class Test(unittest.TestCase):
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)

    def test_reorder_list(self):
        head = reorder_list_v1(self.head)
        self.assertEqual(1, head.val)
        self.assertEqual(5, head.next.val)
        self.assertEqual(2, head.next.next.val)
        self.assertEqual(4, head.next.next.next.val)
        self.assertEqual(3, head.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()
