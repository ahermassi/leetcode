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


def merge_k_lists_v2(lists):
    """ Instead of augmenting the ListNode class with __lt__,  we simply add a tie-breaker in our heap elements
        (tuples). This assures that the heap will never compare two variables of type ListNode. When there is a tie in
        the first value of the tuple, the heap uses the second value as the tie breaker. But since the second value is
        an object of ListNode, which has no definition of comparision, we get an error. We can define the tuple instead
        as (node.val, index, node), where 'index' keeps track of the node's index. This way the second value in the
        tuple is always unique which will break ties.
    Time complexity: O(N logK)
    Space complexity: O(K)
    """
    dummy = tail = ListNode(0)
    heap = []
    for i, head in enumerate(lists):
        if head:
            heappush(heap, (head.val, i, head))
    while heap:
        _, i, node = heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heappush(heap, (node.next.val, i, node.next))  # Recycling tie-breaker i guarantees uniqueness
    return dummy.next


def merge_k_lists_v3(lists):
    """  """

    def partition(left, right):
        if left == right:
            return lists[left]
        if left > right:
            return None
        mid = (left + right) // 2
        left, right = partition(left, mid), partition(mid + 1, right)
        return merge(left, right)

    def merge(list1, list2):
        dummy = tail = ListNode(0)
        while list1 and list2:
            if list1.val < list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next

    return partition(0, len(lists) - 1)
