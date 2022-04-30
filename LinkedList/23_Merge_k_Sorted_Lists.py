""" Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity. """

from heapq import heappush, heappop

# Definition for singly-linked list.


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

# Video explanation: https://www.youtube.com/watch?v=ptYUCjfNhJY


def merge_k_lists_v1(lists):
    """ Compare every k nodes (head of every linked list) and get the node with the smallest value. We then extend the
        final sorted linked list with the selected nodes.

        Optimize the comparison process using a priority queue to find the next element to add. To make the
        implementation simpler, we define the __lt__ method of the ListNode class to make ListNode objects comparable.

        Note that simply using the tuple trick pushing (node.val, node) to the priority queue will not work because the
        lists can have equal values.

        Algorithm invariant: The priority queue holds a single node from each list at a time which has the smallest
        value. Since the lists are sorted, simply advancing to the next of each popped node maintains this property.

    Time complexity: O(N logK), where N is the total number of nodes across the lists. The comparison cost will be
    reduced to O(logK) for every pop and insertion into the priority queue
    Space complexity: O(K), for the heap
    """
    ListNode.__lt__ = lambda self, other: self.val < other.val
    dummy_head = dummy_tail = ListNode(0)
    heap = []
    for head in lists:
        if head:
            heappush(heap, head)
    while heap:  # While some nodes remain in the queue, so O(N)
        node = heappop(heap)  # O(logK)
        dummy_tail.next = node
        if node.next:
            heappush(heap, node.next)  # O(logK)
        dummy_tail = dummy_tail.next
    return dummy_head.next


def merge_k_lists_v2(lists):
    """ Instead of augmenting the ListNode class with __lt__,  we simply add a tie-breaker in our heap elements
        (tuples). This assures that the heap will never compare two variables of type ListNode. When there is a tie in
        the first value of the tuple, the heap uses the second value as the tie breaker. But since the second value is
        an object of ListNode, which has no definition of comparision, we get an error. We can define the tuple instead
        as (node.val, index, node), where 'index' keeps track of the node's index. This way the second value in the
        tuple is always unique which will break ties. With 3 tuples as described above, it is not possible to have the
        same values for both the (node.val, index) values of the tuple, thus never needing to compare using the
        ListNode object.
    Time complexity: O(N logK)
    Space complexity: O(K)
    """
    dummy_head = dummy_tail = ListNode(0)
    heap = []
    for i, head in enumerate(lists):
        if head:
            heappush(heap, (head.val, i, head))
    while heap:
        _, index, node = heappop(heap)
        dummy_tail.next = node
        if node.next:
            heappush(heap, (node.next.val, index, node.next))  # Recycling tie-breaker 'index' guarantees uniqueness
        dummy_tail = dummy_tail.next
    return dummy_head.next


def merge_k_lists_v3(lists):
    """ Recursive merge sort.
    Time complexity: O(N logK), where N is the total number of nodes and K is the number of lists. Recursion depth is
    logK, and in each level we need to merge N nodes. The time complexity for each level is O(N) (e.g. if we have 4
    lists with 10, 20, 30, 40 nodes, to merge list 1 and list 2 we need 30x operations while to merge list 3 and 4 we
    need 70x operations, and 100x in total)
    Space complexity: O(logK)
    """

    def merge(left, right):
        # This function returns the head of the merged lists[left:right+1]
        if left == right:
            return lists[left]
        if left > right:
            return None
        mid = (left + right) // 2
        left, right = merge(left, mid), merge(mid + 1, right)
        return merge_two_lists(left, right)

    def merge_two_lists(list1, list2):
        dummy_head = dummy_tail = ListNode(0)
        while list1 and list2:
            if list1.val < list2.val:
                dummy_tail.next = list1
                list1 = list1.next
            else:
                dummy_tail.next = list2
                list2 = list2.next
            dummy_tail = dummy_tail.next
        dummy_tail.next = list1 or list2
        return dummy_head.next

    return merge(0, len(lists) - 1)
