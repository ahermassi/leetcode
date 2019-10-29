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
