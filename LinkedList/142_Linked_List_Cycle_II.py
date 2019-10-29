""" Given a linked list, return the node where the cycle begins. If there is no cycle, return null.
Note: Do not modify the linked list.
"""


def detect_cycle_v1(head):
    """ If we keep track of the nodes that we've seen already in a hash map (or set), we can traverse the list and
        return the first duplicate node.
    Time complexity: O(N), for both cyclic and acyclic lists, the algorithm must visit each node exactly once. This is
    transparently obvious for acyclic lists because the Nth node points to null, causing the loop to terminate. For
    cyclic lists, the if condition will cause the function to return after visiting the Nth node, as it points to some
    node that is already visited. In both cases, the number of nodes visited is exactly N
    Space complexity: O(N)
    """
    nodes, temp = {}, head
    while temp:
        if temp in nodes:
            return temp
        nodes[temp] = 1
        temp = temp.next
    return None


def detect_cycle_v2(head):
    """ Floyd's hare and tortoise algorithm is separated into two distinct phases. In the first phase, it determines
        whether a cycle is present in the list. If no cycle is present, it returns null immediately, as it is
        impossible to find the entrance to a non-existent cycle. Otherwise, it uses the located "intersection node" to
        find the entrance to the cycle.
        Assume: the distance from head to the start of the loop is L1,
                the distance from the start of the loop to the point fast and slow meet is L2,
                the distance from the point fast and slow meet to the start of the loop is L3
        What is the distance fast moved?
            L1 + L2 + L3 + L2
        What is the distance slow moved?
            L1 + L2
        And their relationship?
            Using the fact that hare moves twice as quickly as tortoise: L1 + L2 + L3 + L2 = 2(L1 + L2)
        --> L1 = L3
        Hence, to find the entrance to the cycle, we have two pointers traverse at the same speed -- one from the front
        of the list, and the other from the point of intersection.
        More generally:
        Distance slow moved: L1 + L2
        Distance fast moved: L1 + L2 + nC, where C is the length of the cycle
        --> L1 + L2 + nC = 2(L1 + L2)
        --> L1 + L2 = nC
        --> L1 = nC - L2
        --> L1 = nC - (C - L3), since C = L2 + L3
        --> L1 = L3 + (n-1)C
        It can be concluded that the distance between the head location and entry location is equal to the distance
        between the meeting location and the entry location along the direction of forward movement and a multiple of C
        loop traversals.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    slow, fast, entry = head, head, head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow == fast:
            while entry != slow:
                entry = entry.next
                slow = slow.next
            return slow
    return None
