""" Given a node from a cyclic linked list which is sorted in ascending order, write a function to insert a value into
the list such that it remains a cyclic sorted list. The given node can be a reference to any single node in the list,
and may not be necessarily the smallest value in the cyclic list.
If there are multiple suitable places for insertion, you may choose any place to insert the new value. After the
insertion, the cyclic list should remain sorted. """

# Definition for a Node.


class Node(object):
    def __init__(self, val, next):
        self.val = val
        self.next = next


def insert(head, insertVal):
    """ We iterate through the cyclic list using two pointers, namely 'prev' and cur. When we find a suitable place
         to insert the new value, we insert it between the 'prev' and cur nodes. The termination condition of the loop
         is that we get back to the starting point of the two pointers (i.e. cur == head).

         During the loop, at each step, we check if the current place bounded by the two pointers is the right place to
         insert the new value. If not, we move both pointers one step forward.
         
         Now, the tricky part of this problem is to sort out different cases that the algorithm should deal with within 
         the loop, and then design a concise logic to handle them sound and properly. Here we break it down into three 
         general cases:

            - Case 1: the value of new node sits between the values of prev and cur pointers. As a result, it should be
               right after prev.

            - Case 2: the value of the new node goes beyond the minimal and maximal values of the current list, either
               less than the minimal value or greater than the maximal value. In either case, the new node should be
               added right after the tail node (i.e. the node with the maximal value of the list). We can locate the
               position of the tail node by finding a descending order between the adjacent, i.e. the condition
               (prev.val > curr.val), since the nodes are sorted in ascending order, the tail node prev would have the
               greatest value amongst all nodes.
               Once we locate the tail and head nodes, we basically extend the original list by inserting the value in
               between the tail and head nodes, i.e. in between the prev and curr pointers, the same operation as in the
               Case 1.

            - Case 3: finally, there is one case that does not fall into any of the above two cases. This is the case
               where the list contains uniform values. In this case, we would end up looping through the list and
               getting back to the starting point. The followup action is just to add the new node after any node in the
               list, regardless of the value to be inserted.

        The above three cases cover the scenarios within and after the iteration loop. There is, however, one minor
        corner case we still need to deal with, where we have an empty list. This, we could easily handle before the
        loop.

    Time complexity: O(N), where N is the size of list. In the worst case, we would iterate through the entire list
    Space complexity: O(1)
    """
    node = Node(insertVal, None)
    if not head:
        node.next = node
        return node
    prev, cur = head, head.next
    while cur != head:  # If we make a complete cycle without breaking, it means all nodes have equal values
        if prev.val <= insertVal <= cur.val:
            # Case 1: found a spot between smaller and bigger node
            break
        if prev.val > cur.val and (insertVal > prev.val or insertVal < cur.val):
            # Case 2: reached tipping point. This is to catch insertVal that are smaller than min or bigger than max.
            # Example: (prev) 3 -> (cur) 1, insertVal=5 or insertVal=0
            break
        prev, cur = cur, cur.next
    node.next = cur
    prev.next = node
    return head
