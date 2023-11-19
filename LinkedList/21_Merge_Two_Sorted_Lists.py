""" Merge two sorted linked lists and return it as a new list. The new list should be made by splicing together the
nodes of the first two lists.
Example:
Input: 1->2->4, 1->3->4
Output: 1->1->2->3->4->4
"""

import unittest2 as unittest


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# Video explanation: https://www.youtube.com/watch?v=GfRQvf7MB3k

def merge_two_lists_v1(l1, l2):
    """ We create a dummy head and a dummy tail indicating last node in this growing List.

        At each step, if the value at l1 is less than or equal to the value at l2, then we connect l1 to the previous
        node and advance l1. Otherwise, we do the same, but for l2. Then, regardless of which list we connected, we
        advance the tail to keep it one step behind one of our list heads.

        After the loop terminates, at most one of l1 and l2 is non-null. Therefore, (because the input lists were in
        SORTED order), if either list is non-null, it contains only elements greater than all the previously-merged
        elements.

        How come dummy_head.next is returned when it never gets set?

        This code can be confusing because we never see dummy_head.next get explicitly set to anything, but the
        reason is that both dummy_head and dummy_tail are simply references to the same object in memory.

        Notice that dummy_head is the only object we create. The variable dummy_tail isn't created the same way.
        So there is only ONE ListNode object actually in memory.

        When we see "dummy_tail = dummy_head", we might think that all we're doing is assigning a copy of dummy_head
        to dummy_tail, and then we have two separate variables, but that is false. When we say
        "dummy_tail = dummy_head", what we're actually saying is that both of these variables are now pointing to the
        exact same object in memory; It doesn't get cloned.

        So in the first pass of the while loop, when dummy_tail.next = l1 or dummy_tail.next = l2, what we're actually
        doing is changing the reference of the object dummy_head. So dummy_head.next also gets set to either l1 or
        l2 at that point.

        This only happens on the first pass of the while loop, because at that point, we change the references when we
        do "dummy_tail = dummy_tail.next" at the end of the while loop iteration. The variable dummy_tail changes
        references on every pass of the while loop, and that's how we actually traverse the lists - dummy_tail is
        always changed to reference the next node in the sorted list, and that reference is then what changes the .next
        of the current node, whereas dummy_head never gets set to anything else, so it's always pointing to the
        beginning of the new merged list.

    Time complexity: O(N + M), the while loop runs for a number of iterations equal to sum of lengths of the two lists
    Space complexity: O(1), the iterative approach only allocates a few pointers so it has a constant overall memory
    footprint
    """
    # Dummy head and tail, starting at same position
    dummy_head = ListNode(0)
    dummy_tail = dummy_head
    while l1 and l2:
        if l1.val <= l2.val:
            dummy_tail.next = l1
            l1 = l1.next
        else:
            dummy_tail.next = l2
            l2 = l2.next
        dummy_tail = dummy_tail.next
    # If we exhausted either list, we just append the other list to the end of the merged list since the list still
    # standing will have all elements greater than the last item in the merged list so far (and is in sorted order)
    dummy_tail.next = l1 or l2
    return dummy_head.next


def merge_two_lists_v2(l1, l2):
    """ We can recursively define the result of a merge operation on two lists as the following:

            list1[0] + merge(list1[1:], list2)  if  list1[0] <= list2[0]
            list2[0] + merge(list1, list2[1:])  otherwise

        Namely, the smaller of the two lists' heads plus the result of a merge on the rest of the elements.

        We model the above recurrence directly, first accounting for edge cases. Specifically, if either of l1 or l2 is
        initially null, there is no merge to perform, so we simply return the non-null list. Otherwise, we determine
        which of l1 and l2 has a smaller head value, and recursively set the next value for that head to the next merge
        result. Given that both lists are null-terminated, the recursion will eventually terminate.

    Time complexity: O(N + M), there will be exactly one call to merge_two_lists per element in each list. Therefore,
    the time complexity is linear to the combined size of the lists.
    Space complexity: O(N + M), the first call to merge_two_lists does not return until the ends of both l1 and l2 have
    been reached, so (N + M) stack frames consume O(N + M) space
    """
    if not l1 or not l2:
        return l1 or l2
    if l1.val <= l2.val:
        l1.next = merge_two_lists_v1(l1.next, l2)  # This is the case list1[0] + merge(list1[1:], list2)
        return l1
    l2.next = merge_two_lists_v1(l1, l2.next)  # This is the case list2[0] + merge(list1, list2[1:])
    return l2


class Test(unittest.TestCase):
    head1 = ListNode(1)
    head1.next = ListNode(2)
    head1.next.next = ListNode(4)
    head2 = ListNode(1)
    head2.next = ListNode(3)
    head2.next.next = ListNode(4)
    head = merge_two_lists_v2(head1, head2)

    def test_merge_two_lists(self):
        self.assertEqual(1, self.head.val)
        self.assertEqual(1, self.head.next.val)
        self.assertEqual(2, self.head.next.next.val)
        self.assertEqual(3, self.head.next.next.next.val)
        self.assertEqual(4, self.head.next.next.next.next.val)
        self.assertEqual(4, self.head.next.next.next.next.next.val)


if __name__ == '__main__':
    unittest.main()