"""" Given a binary tree, flatten it to a linked list in-place.

For example, given the following tree:

    1
   / \
  2   5
 / \   \
3   4   6
The flattened tree should look like:

1
 \
  2
   \
    3
     \
      4
       \
        5
         \
          6 """

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


next = None


def flatten(root: TreeNode):
    """ In the flattened tree, each node's right child points to the next node of a pre-order traversal. So we're
        basically performing a reverse pre-order traversal. 'next' variable is the next node of current node in a
        pre-order traversal, with 'next' pointing initially to None.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not root:
        return
    flatten(root.right)
    flatten(root.left)
    root.right = next
    root.left = None
    next = root


