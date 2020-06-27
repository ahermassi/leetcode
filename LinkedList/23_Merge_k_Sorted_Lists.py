""" Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity. """

from heapq import heappush, heappop

# Definition for singly-linked list.


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def merge_k_lists_v1(lists):
    """ Compare every k nodes (head of every linked list) and get the node with the smallest value. We then extend the
        final sorted linked list with the selected nodes. Optimize the comparison process using a priority queue to
        find the next element to add. To make the implementation simple we 'monkey patch' the ListNode class to have a
        custom less-than function using setattr. Note that simply using the tuple trick and pushing (node.val, node) to
        the priority queue will not work because the lists can have equal values.
    Time complexity: O(N logK), the comparison cost will be reduced to O(logK) for every pop and insertion into the
    priority queue and there are N nodes in the final linked list
    Space complexity: O(K), for the heap
    """
    setattr(ListNode, "__lt__", lambda self, other: self.val < other.val)
    dummy = tail = ListNode(0)
    heap = []
    for head in lists:
        if head:
            heappush(heap, head)
    while heap:
        node = heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heappush(heap, node.next)
    return dummy.next
