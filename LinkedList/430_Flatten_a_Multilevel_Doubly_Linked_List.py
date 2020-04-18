""" You are given a doubly linked list which in addition to the next and previous pointers, it could have a child
pointer, which may or may not point to a separate doubly linked list. These child lists may have one or more children
of their own, and so on, to produce a multilevel data structure, as shown in the example below.
Flatten the list so that all the nodes appear in a single-level, doubly linked list. You are given the head of the
first level of the list. """

# Definition for a Node.


class Node(object):
    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child


def flatten_v1(head):
    """ If we turn the list 90 degrees around the clock, then suddenly a binary tree appears in front of us, and the
        flatten operation is basically what we call pre-order DFS traversal (Depth-First Search). We could consider the
        child pointer as the left pointer in binary tree which points to the left sub-tree (sublist). Similarly, the
        next pointer can be considered as the right pointer in binary tree. Then if we traverse the tree in pre-order
        DFS, it would generate the same visiting sequence as the flatten operation in our problem.
    Time complexity: O(N), the DFS algorithm traverses each node once
    Space complexity: O(N), for call stack
    """
    cur = head
    while cur:
        if cur.child:
            nxt = cur.next
            cur.next = flatten_v1(cur.child)
            cur.next.prev = cur
            cur.child = None
            while cur.next:
                cur = cur.next
            if nxt:
                cur.next = nxt
                cur.next.prev = cur
        cur = cur.next
    return head


def flatten_v2(head):
    """ Start form the head , move one step each time to the next node.
        When a node 'cur' with child is met, follow its child chain to the end and connect the tail node with cur.next,
        by doing this we merge the child chain back to the main list.
        Return to 'cur' and proceed until finding next node with child.
        Repeat until reaching the end of list.
        This is more like a top-down flattening. When we encounter a node with child node, we directly flatten the
        current node, then move to the next node.
        This solution performs multiple passes over the list as nodes could be visited more than once, as many as there
        are levels in the list.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    cur = head
    while cur:
        if cur.child:
            child = cur.child
            while child.next:
                child = child.next
            nxt = cur.next
            cur.next = cur.child
            cur.next.prev = cur
            cur.child = None
            child.next = nxt
            if nxt:
                child.next.prev = child
        cur = cur.next
    return head


def flatten_v3(head):
    """ Another iterative solution using a stack.
        The stack data structure helps us to construct the iteration sequence as the one created by recursion.
        We create a stack and then we push the head node to the stack. In addition, we create a node called 'pre' which
        would help us to track the precedent node at each step during the iteration.
        Within the loop, at each step, we first pop out a node 'cur' from the stack. Then we establish the links
        between 'pre and 'cur'. Then in the following steps, we take care of the nodes pointed by the cur.next and
        cur.child pointers respectively, and strictly in this order.
        If cur.next does exist (i.e. there exists a right subtree), we then push the node into the stack for the next
        iteration.
        If cur.child does exist (i.e. there exists a left subtree), we then push the node into the stack. In addition,
        we need to clean up the cur.child pointer since it should not be present in the final result.
        Due to the LIFO order of the stack, a child node (if it exists) is popped out in the next iteration before the
        next pointer's node, which is the essence of flattening.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not head:
        return None
    dummy = Node(0, None, head, None)
    pre = dummy
    stack = [head]
    while stack:
        cur = stack.pop()
        cur.prev = pre
        pre.next = cur
        if cur.next:
            stack.append(cur.next)
        if cur.child:
            stack.append(cur.child)
            cur.child = None
        pre = pre.next
    dummy.next.prev = None
    return dummy.next





