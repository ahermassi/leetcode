""" Given a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or
equal to x.
You should preserve the original relative order of the nodes in each of the two partitions.
"""

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def partition(head, x):
    """ In the reformed list, there would be a point in the linked list before which all the elements would be smaller
        than x and after which all the elements would be greater or equal to x. Let's call this point as the JOINT.
        Reverse engineering the question tells us that if we break the reformed list at the JOINT, we will get two
        smaller linked lists, one with lesser elements and the other with elements greater or equal to x. In the
        solution, our main aim is to create these two linked lists and join them.
        We can take two pointers 'less_tail' and 'equal_or_greater_tail' to keep track of the two linked lists as
        described above. These two pointers could be used two create two separate lists and then these lists could be
        combined to form the desired reformed list.
        Since we traverse the original linked list from left to right, at no point would the order of nodes change
        relatively in the two lists.
        We are not sorting the list. We have a partition and we are simply moving all the elements less than that
        partition value to before all the elements greater than that partition value, while preserving the order.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    less_head = less_tail = ListNode(0)
    equal_or_greater_head = equal_or_greater_tail = ListNode(0)
    cur = head
    while cur:
        if cur.val < x:
            less_tail.next = cur
            less_tail = less_tail.next
        else:
            equal_or_greater_tail.next = cur
            equal_or_greater_tail = equal_or_greater_tail.next
        cur = cur.next
    less_tail.next = equal_or_greater_head.next
    equal_or_greater_tail.next = None
    return less_head.next


class Test(unittest.TestCase):
    head1 = ListNode(1)
    head1.next = ListNode(4)
    head1.next.next = ListNode(3)
    head1.next.next.next = ListNode(2)
    head1.next.next.next.next = ListNode(5)
    head1.next.next.next.next.next = ListNode(2)
    head2 = partition(head1, 3)

    def test_partition(self):
        self.assertEqual(1, self.head2.val)
        self.assertEqual(2, self.head2.next.val)
        self.assertEqual(2, self.head2.next.next.val)
        self.assertEqual(4, self.head2.next.next.next.val)
        self.assertEqual(3, self.head2.next.next.next.next.val)
        self.assertEqual(5, self.head2.next.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()
