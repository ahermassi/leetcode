""" Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a
multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.
 """


def reverse_k_group(head, k):
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
    rest_reversed = reverse_k_group(cur, k)  # cur points to the kth node (0-based)
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
