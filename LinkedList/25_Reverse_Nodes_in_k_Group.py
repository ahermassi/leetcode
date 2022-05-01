""" Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a
multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.
 """

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_k_group_v1(head, k):
    """ The problem statement clearly mentions that we are not to use any additional space for our solution. So
        naturally, a recursive solution is not acceptable here because of the space utilized by the recursion stack.
        However, for the sake of completeness, we shall go over the recursive approach first before moving on to the
        iterative approach. The interviewer may not specify the space constraint initially and so, a recursive solution
        would be a quick first approach followed by the iterative version.

        A Linked list is a recursive structure. A sub-list in itself is a linked list. So, if you think about it,
        reversing a list consisting of k nodes is simply a linked list reversal algorithm.

        The basic idea is to make use of our reversal function for a linked list. Usually, we start with the head of
        the list and keep running the reversal algorithm all the way to the end. However, in this case, we will only
        process k nodes.

        The problem statement also mentions that if there are < k nodes left in the linked list, then we don't have to
        reverse them. This implies that we first need to count k nodes before we get on with our reversal. If at any
        point, we find that we don't have k nodes, then we don't reverse that portion of the linked list.

        Right off the bat, this implies at least two traversals of the list overall. One for counting, and the other for
        reversals.

        Since a sub-list of a linked list is a linked list in itself, we can make use of recursion to do the heavy
        lifting for us. All we need to focus here is how we are going to reverse those k nodes. We also need to make
        sure we are hooking up the right connections as recursion backtracks. For e.g. say we are given a linked list
        [1,2,3,4,5] and we are to reverse 2 nodes at a time. When recursion backtracks, we assume that we will have
        [4,3,5]. Then, after we reverse the first two nodes thus getting [2,1], we need to ensure that we hook up 1->4
        correctly so that the overall list is what we expect.

        In every recursive call, we first count the number of nodes in the linked list. As soon as the count reaches k,
        we break.
            - If there are less than k nodes left in the list, we return the head of the list.
            - If there are at least k nodes in the list, then we reverse these nodes and recursively call
               reverse_k_group() on the kth node in the list
        So, in every recursive call, we first reverse k nodes, then recurse on the rest of the linked list. When
        recursion returns, we establish the proper connections.

    Time complexity: O(N), since we process each node exactly twice. Once when we are counting the number of nodes in
    each recursive call, and then once when we are actually reversing the sub-list.
    Space complexity: O(N / k), used up by the recursion stack. The number of recursion calls is determined by both k
    and N. In every recursive call, we process k nodes and then make a recursive call to process the rest.
    """

    if not head or not head.next:
        return head
    cur, length = head, 0
    while cur:
        length, cur = length + 1, cur.next
        if length == k:
            break
    if length < k:
        return head
    rest_reversed = reverse_k_group_v1(cur, k)  # cur points to the kth node (0-based)
    # Reverse the first k nodes
    prev, cur = None, head
    for _ in range(k):
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    # Since the recursion returns the head of the overall processed list starting from kth node, we use that and the
    # "original" head of the k nodes to re-wire the connections.
    head.next = rest_reversed
    return prev


def reverse_k_group_v2(head, k):
    """ The idea here is the same as before except that we won't be making use of the stack and rather use a couple
        additional variables to maintain the proper connections along the way. We still count k nodes at a time. If we
        find k nodes, then we reverse them.

        In addition to the head and rest_reversed variables from before, we need to know the tail node of the previous
        set of k nodes as well. The recursive approach reverses k nodes from left to right, but it establishes the
        connections from right to left or back to front. In this approach we will be reversing and establishing the
        connections while going from front to back.

        We need to maintain 3 different variables in this algorithm as we chug along:
            - cur_group_head: Will always point to the original head of the next set of k nodes.
            - prev: The tail node of the original set of k nodes yet to be reversed. Hence, this becomes the new head
               of the set of k nodes after reversal.
            - prev_group_tail: The tail node of the previous set of k nodes after reversal.
            - new_head: The tail node of the first set of k nodes, i.e. the kth node from the beginning of the original
               list. It acts as the head of the final list that we need to return as the output.

        The core algorithm remains the same as before. Given cur_group_head, we first count k nodes. If we are able to
        find at least k nodes, we reverse them and get prev, the head of the reversed set of k nodes.

        At this point we check if we already have the variable prev_group_tail set or not. It won't be set when we
        reverse the very first set of k nodes. However, if this variable is set, then we attach prev_group_tail.next to
        prev. Also, we need to update prev_group_tail to point to the tail of the reversed set of k nodes that we just
        processed. Remember, the head node becomes the new tail and hence, we set prev_group_tail = cur_group_head.

        We keep doing this until we reach the end of the list, or we encounter that there are < k nodes left in the list.

    Time complexity: O(N), since we process each node exactly twice, once when we are counting the number of nodes,
    and then once when we are actually reversing the sub-list
    Space complexity: O(1)
    """

    if not head or not head.next:
        return head
    new_head = None  # Head of the final, modified linked list
    cur_group_head, prev_group_tail = head, None
    while True:
        cur, length = cur_group_head, 0  # Start counting nodes from the head
        while cur:
            cur, length = cur.next, length + 1
            if length == k:
                break
        if length < k:
            # Attach the final, non-reversed portion
            prev_group_tail.next = cur_group_head
            break
        prev, cur = None, cur_group_head
        # Reverse k nodes starting from cur_group_head node
        for _ in range(k):
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        # At this point, prev points to the head of the just-reversed set of k nodes and cur points to the head of the
        # remaining of the list
        if prev_group_tail:  # prev_group_tail is the tail of the previous block of reversed k nodes
            prev_group_tail.next = prev
        if not new_head:
            new_head = prev
        prev_group_tail = cur_group_head
        cur_group_head = cur
    return new_head
