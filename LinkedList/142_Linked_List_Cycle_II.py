""" Given a linked list, return the node where the cycle begins. If there is no cycle, return null.
Note: Do not modify the linked list.
"""


def detect_cycle_v1(head):
    """ If we keep track of the nodes that we've seen already in a hash set, we can traverse the list and return the
         first duplicate node.

         If the node has already been seen, then it is necessarily the entrance to the cycle. If any other node were
         the entrance to the cycle, then we would have already returned that node instead. Otherwise, the if condition
         will never be satisfied, and our function will return null.

        The algorithm necessarily terminates for any list with a finite number of nodes, as the domain of input lists
        can be divided into two categories: cyclic and acyclic lists. An acyclic list resembles a null-terminated chain
        of nodes, while a cyclic list can be thought of as an acyclic list with the final null replaced by a reference
        to some previous node. If the while loop terminates, we return null, as we have traversed the entire list
        without encountering a duplicate reference. In this case, the list is acyclic. For a cyclic list, the while
        loop will never terminate, but at some point the if condition will be satisfied and cause the function to return.

    Time complexity: O(N), for both cyclic and acyclic lists, the algorithm must visit each node exactly once. This is
    transparently obvious for acyclic lists because the Nth node points to null, causing the loop to terminate. For
    cyclic lists, the if condition will cause the function to return after visiting the Nth node, as it points to some
    node that is already visited. In both cases, the number of nodes visited is exactly N
    Space complexity: O(N)
    """
    seen_nodes, cur = set(), head
    while cur:
        if cur in seen_nodes:
            return cur
        seen_nodes.add(cur)
        cur = cur.next
    return None


def detect_cycle_v2(head):
    """ Floyd's Tortoise and Hare

        What happens when a fast runner (a hare) races a slow runner (a tortoise) on a circular track? At some point,
        the fast runner will catch up to the slow runner from behind.

        Floyd's hare and tortoise algorithm is separated into two distinct phases. In the first phase, it determines
        whether a cycle is present in the list. If no cycle is present, it returns null immediately, as it is
        impossible to find the entrance to a non-existent cycle. Otherwise, it uses the located "intersection node" to
        find the entrance to the cycle.

        Here, we initialize two pointers - the fast hare and the slow tortoise. Then, until hare can no longer advance,
        we advance tortoise once and hare twice. If, after advancing them, hare and tortoise point to the same node,
        we stop at that node. Otherwise, we continue. If the while loop terminates without meeting at a node, then the
        list is acyclic, and we return null.

        Given that previous phase finds an intersection node, now we proceed to find the node that is the entrance to
        the cycle. To do so, we initialize one more pointer 'entry' which points to the head of the list, and tortoise
        will still point to the intersection. Then, we advance each of them by 1 until they meet; the node where they
        meet is the entrance to the cycle, so we return it.

        Why does it work?

        Assume: L1 is the distance from head to the start of the cycle
                      L2 is the distance from the start of the cycle to the point fast and slow meet
                      L3 is the distance from the point fast and slow meet to the start of the cycle
                      C = L2 + L3 is the circumference of the cycle

        What is the distance fast moved?
            L1 + L2 + k * (L3 + L2) = L1 + L2 + kC
        Where k is the number of times the fast pointer traveled around the cycle before meeting the slow pointer

        What is the distance slow moved?
            L1 + L2 + mC

        And their relationship?
            Using the fact that hare moves twice as quickly as tortoise:
            L1 + L2 + kC  = 2 (L1 + L2 + mC) = 2 (L1 + L2) + 2mC
            --> kC = L1 + L2 + 2mC
            --> L1 = (k-2m)C - L2
            Since C = L2 + L3 , .i.e. L2 = C - L3
            --> L1 = (k - 2m)C - C + L3 = L3 + (k - 2m - 1)C

        Therefore:
            L1 = L3 + multiples of cycle circumference

        It can be concluded that the distance between the head location and entry location is equal to the distance
        between the meeting location and the entry location along the direction of forward movement and a multiple of C
        loop traversals.

        Hence, to find the entrance to the cycle, we have two pointers traverse at the same speed -- one from the front
        of the list, and the other from the point of intersection.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    slow, fast = head, head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow == fast:
            # To find the entrance to the cycle, we have two pointers traverse at the same speed -- one from the
            # front of the list, and the other from the point of intersection.
            entry = head
            while entry != slow:
                entry, slow = entry.next, slow.next
            return slow
    return None
