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


def connect_v1(root):
    """ Since we are manipulating tree nodes on the same level, it's easy to come up with a very standard BFS solution
        using queue. But because of next pointer, we actually don't need a queue to store the order of tree nodes at
        each level, we just use a next pointer like it's a linked list at each level.
        Simply do it level by level, using the next-pointers of the current level to go through the current level and
        set the next-pointers of the next level.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not root:
        return None
    cur = root  # Assign root to cur and operate on cur to avoid losing the pointer to original root
    next = cur.left
    while cur.left:
        cur.left.next = cur.right
        if cur.next:
            cur.right.next = cur.next.left
            cur = cur.next
        else:  # Exchange cur and next every time cur is the last node at each level
            cur = next
            next = next.left
    return root