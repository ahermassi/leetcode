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


# Video explanation: https://youtu.be/KT1iUciJr4g
def partition(head, x):
    """ In the reformed list, there would be a point in the linked list before which all the elements would be smaller
         than x and after which all the elements would be greater or equal to x. Let's call this point as the JOINT.

         Reverse engineering the question tells us that if we break the reformed list at the JOINT, we will get two
         smaller linked lists, one with smaller elements and the other with elements greater or equal to x. In the
         solution, our main aim is to create these two linked lists and join them.

         We can take two pointers 'less_tail' and 'equal_or_greater_tail' to keep track of the two linked lists as
         described above. These two pointers could be used two create two separate lists and then these lists could be
         combined to form the desired reformed list.

            - Initialize two pointers 'less_tail' and 'equal_or_greater_tail' with a dummy ListNode. This helps reduce
               the number of conditional checks we would need otherwise.

            - Iterate the original linked list using the 'cur' pointer.

            - If the node's value pointed by 'cur' is smaller than x, the node should be part of the 'less_tail' list.
               Else, the node should be part of 'equal_or_greater_tail' list.

            - Once we are done with all the nodes in the original linked list, we would have two lists 'less_tail' and
               'equal_or_greater_tail'. The original list nodes are part of either list depending on their values.

            - Now, these two lists can be combined to form the reformed list.

         Since we traverse the original linked list from left to right, at no point would the order of nodes change
         relatively in the two lists.

         We are not sorting the list. We have a partition, and we are simply moving all the elements less than that
         partition value to before all the elements greater than that partition value, while preserving the order.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    less_tail = ListNode(0)
    equal_or_greater_tail = ListNode(0)
    # less_head and equal_or_greater_head are used to save the heads of the two lists
    less_head, equal_or_greater_head = less_tail, equal_or_greater_tail
    cur = head
    while cur:
        if cur.val < x:
            less_tail.next = cur
            less_tail = less_tail.next
        else:
            equal_or_greater_tail.next = cur
            equal_or_greater_tail = equal_or_greater_tail.next
        cur = cur.next
    # After the loop exits we have 4 pointers in the following order:
    # less_head ->... -> less_tail equal_or_greater_head ->... -> equal_or_greater_tail ->
    # Combine the two lists by adding the connection less_tail -> equal_or_greater_head.next (remember that
    # equal_or_greater_head is a dummy node) and also removing the connection equal_or_greater_tail.next
    less_tail.next = equal_or_greater_head.next
    # Last node of equal_or_greater_tail list would also be the ending node of the reformed list. That node will
    # still point to whatever node was next in the list until we sever that link by replacing it with None.
    equal_or_greater_tail.next = None
    return less_head.next # Return the new list minus the dummy head


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
