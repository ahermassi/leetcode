""" You are given a perfect binary tree where all leaves are on the same level, and every parent has two children.
The binary tree has the following definition:

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be
set to NULL.
Initially, all next pointers are set to NULL. """

from collections import deque


# Excellent explanation: https://leetcode.com/problems/populating-next-right-pointers-in-each-node/editorial/
def connect_v1(root):
    """ Since we are manipulating tree nodes at the same level, it's easy to come up with a very standard BFS solution
         using a queue. But because of next pointer, we actually don't need a queue to store the order of tree nodes at
         each level, we just use a next pointer like it's a linked list at each level.

        Let's look at the two types of next pointer connections we need to establish for a given tree:

            - The first case is the one where we establish the next pointers between the two children of a given node.
               This is the easier of the two cases since both the children are accessible via the same node. We can
               simply do the following to establish this connection:  node.left.next = node.right

            - The next case is not too straightforward to handle. In addition to establishing the next pointers between
               the nodes having a common parent, we also need to set up the correct pointers between nodes which
               have a different parent. More specifically, it's the link between the right child of a node and the left
               child of the next node. Since we already have the next pointers set up at the current level, we use that
               to set up the correct pointers on the next level: node.right.next = node.next.left

        The basic idea for this approach is based on the fact that:

                We only move to level (N+1) when we are done establishing the next pointers for level N.
                Since we have access to all the nodes at a particular level via the next pointers, we can use
                these next pointers to establish the connections for the next level or the level containing
                their children.

         We establish the next pointers for level N while we are still at level (N−1), and once we are done
         establishing these new connections, we move on to N and do the same thing for level (N+1).

         When we go over the nodes of a particular level, their next pointers are already established. This is what
         helps get rid of the queue data structure and save space. To start on a particular level, we just need the
         leftmost node. From there on out, it's just a linked list traversal.

    Time complexity: O(N), since we process each node exactly once
    Space complexity: O(1)
    """
    cur = root  # Assign root to cur and operate on cur to avoid losing the pointer to original root
    while cur.left:  # We don't operate on last level as its nodes have been already connected in previous level
        left = cur.left  # We keep this pointer to the leftmost node of next level
        while cur:
            cur.left.next = cur.right
            cur.right.next = cur.next.left if cur.next else None
            cur = cur.next # Progress along the list (nodes at the current level)
        cur = left  # Use left everytime cur is the last node at that level to move to the next level
    return root


def connect_v2(root):
    """ We need to link all the nodes together which lie on the same level and the level order or the breadth first
        traversal gives us access to all such nodes. At each step, we record the size of the queue and that always
        corresponds to all the nodes on a particular level. Once we have this size, we only process these many elements
        and no more. By the time we are done processing size number of elements, the queue would contain all the nodes
        on the next level.
        When we pop a node, we add its children at the back of the queue. Also, the element at the head of the queue is
        the next element in order, on the current level. So, we can easily establish the new pointers.
    Time complexity: O(N), since we process each node exactly once
    Space complexity: O(N), this is a perfect binary tree which means the last level contains N/2 nodes. The space
    complexity for breadth first traversal is the space occupied by the queue which is dependent upon the maximum
    number of nodes in particular level.
    """
    if not root:
        return None
    queue = deque([root])
    while queue:
        n = len(queue)
        for i in range(n):
            node = queue.popleft()
            if i < n - 1:  # This check is important. We don't want to establish any wrong connections. The queue will
                # contain nodes from 2 levels at most at any point in time. This check ensures we only don't establish
                # next pointers beyond the end of a level
                node.next = queue[0]
            queue.extend([child for child in (node.left, node.right) if child])
    return root


def connect_v3(root):
    """ Doing it recursively. We use the fact that the tree is a perfect binary tree in the base case of recursion.
    Time complexity: O(N)
    Space complexity: O(logN) as recursion tree can go as deep as height of the tree
    """
    if not root or not root.left:
        return root
    root.left.next = root.right
    root.right.next = root.next.left if root.next else None
    root.left = connect_v3(root.left)
    root.right = connect_v3(root.right)
    return root
