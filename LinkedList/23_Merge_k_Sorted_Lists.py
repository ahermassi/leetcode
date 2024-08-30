""" Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity. """

from collections import deque
from heapq import heappush, heappop

# Definition for singly-linked list.


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# Video explanation: https://www.youtube.com/watch?v=ptYUCjfNhJY
def merge_k_lists_v1(lists):
    """ The idea is to compare every k nodes (head of every linked list) and get the node with the smallest value.
         We then extend the final sorted linked list with the selected nodes.

         We can optimize the comparison process using a priority queue to find the next element to add. To make the
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
    """ Instead of augmenting the ListNode class with __lt__,  we simply add a tie-breaker to the heap elements
         (tuples). This ensures that the heap never compares two variables of type ListNode.

        If the heap tuple contains only information about the node value and the node reference, when there is a tie in
        the first value of the tuple, the heap uses the second value as the tie-breaker. But since the second value is
        an object of ListNode, which has no definition of comparison, we get an error.

        We can define the tuple instead as (node.val, list_index, node), where 'list_index' is the linked list index in
        the input list. This way, the second value in the tuple is always unique which will break ties. With 3-element
        tuples, it is not possible to have the same values for both the entire tuple (node.val, list_index), thus never
        having to compare ListNode objects.

    Time complexity: O(N logK)
    Space complexity: O(K)
    """
    dummy_head = dummy_tail = ListNode(0)
    heap = []
    for i, head in enumerate(lists):
        if head:
            heappush(heap, (head.val, i, head))
    while heap:
        _, list_index, node = heappop(heap)
        dummy_tail.next = node
        if node.next:
            # Recycling tie-breaker 'list_index' guarantees uniqueness
            heappush(heap, (node.next.val, list_index, node.next))
        dummy_tail = dummy_tail.next
    return dummy_head.next


def merge_k_lists_v3(lists):
    """ Recursive merge sort.

    Time complexity: O(N logK), where N is the total number of nodes and K is the number of lists. Recursion depth is
    logK, and in each level we need to merge N nodes. The time complexity for each level is O(N) (e.g. if we have 4
    lists with 10, 20, 30, 40 nodes, to merge list 1 and list 2 we need 30x operations while to merge list 3 and 4 we
    need 70x operations, and 100x in total)

            sort   l1, l2, l3, l4
                   /              \
      sort l1, l2            sort l3, l4
               |    |             |    |
        sort l1 sort l2   sort l3   sort l4
               \    /            \     /
        merge(l1, l2)    merge(l3, l4)
                    \             /
                merge(l1, l2, l3, l4)

    Sort stage: We call sort 1 + 2 + 4 (+ ...) times; Time complexity is O(N).
    Merge stage: K =4 (four lists), and merge recursion tree has two levels (i.e. log(4)). In merge(l1, l2) and
    merge(l3, l4), we go over every single element in all four lists. In the final step merge(l1, l2, l3, l4), we still
    go over every single element in the two merged lists, which is still every single element of all four lists. So for
    each level of the merge states recursion tree, time complexity is O(N). Moreover, we have total of logK levels of
    merge recursion tree. Therefore, total Time Complexity: Sort stage (O(N)) + Merge stage (O(N logK)) = O(N + NlogK)
    = O(N logK).
    The divide-and-conquer approach for merging K sorted linked lists is often O(N log k) due to the way the merge
    operations are organized. Here's why:
    Divide Stage: We have K sorted linked lists, and we divide them into pairs. We keep doing this until each pair is
    merged into a single sorted list. The total number of lists is halved in each iteration. The number of times we can
    halve K until we get to 1 is logK (base 2).
    Conquer (Merge) Stage: In each of these logK stages, we are performing merge operations. Each merge operation for
    two lists with a total of N elements would be O(N).
    The total time complexity for these operations is, therefore, logK stages of O(N) merge operations, resulting in a
    time complexity of O(N logK).
    Space complexity: O(logK), for the recursion stack
    """

    def merge(left, right):
        # This function returns the head of the merged linked lists lists[left:right+1]
        if left > right:
            return None
        if left == right:
            return lists[left]
        mid = (left + right) // 2
        left_half, right_half = merge(left, mid), merge(mid + 1, right)
        return merge_two_lists(left_half, right_half)

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


# Video explanation: https://youtu.be/q5a5OiGbT6Q
def merge_k_lists_v4(lists):
    """  We can convert merging K lists into merging 2 lists (K-1) times with the help of a queue.

    Time complexity: O(N * K), where N is the total number of nodes across the lists
    Space complexity: O(N), for the queue
    """

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

    if not lists:
        return None
    queue = deque(lists)
    while len(queue) > 1:
        queue.append(merge_two_lists(queue.popleft(), queue.popleft()))
    return queue.popleft()
