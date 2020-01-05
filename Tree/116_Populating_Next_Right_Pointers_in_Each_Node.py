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


def connect_v1(root):
    """ Since we are manipulating tree nodes on the same level, it's easy to come up with a very standard BFS solution
        using queue. But because of next pointer, we actually don't need a queue to store the order of tree nodes at
        each level, we just use a next pointer like it's a linked list at each level.
        Simply do it level by level, using the next pointers of the current level to go through the current level and
        set the next pointers of the next level.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    cur = root  # Assign root to cur and operate on cur to avoid losing the pointer to original root
    while cur and cur.left:  # We don't operate on last level as its nodes have been already connected in previous level
        left = cur.left  # We keep this pointer to the leftmost node of next level
        while cur:
            cur.left.next = cur.right
            cur.right.next = cur.next.left if cur.next else None
            cur = cur.next
        cur = left  # Exchange cur and left every time cur is the last node at each level to move on to next level
    return root


def connect_v2(root):
    """ Standard BFS using Python deque.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    queue = deque([root])
    while queue:
        next_queue = deque()  # If we don't create a new queue, the last node at each level will get its next pointing
        # the leftmost node of the next level. This is because we use the same queue to append next level's nodes
        while queue:
            node = queue.popleft()
            node.next = queue[0] if queue else None
            next_queue.extend([kid for kid in (node.left, node.right) if kid])
        queue = next_queue
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