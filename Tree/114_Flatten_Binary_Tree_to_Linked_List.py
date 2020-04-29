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


def flatten_v1(root):
    """ The main idea behind a recursive solution is that we use the solutions for sub-problems to solve an upper level
        problem. In the case of a tree, the subtrees are essentially our sub-problems. So, a recursive solution for
        this problem is essentially based on the idea that assuming we have already transformed the left and the right
        halves of a given root node, how do we establish or modify the necessary connections so that we get a right
        skewed tree overall? Well, we simply have to shuffle around some pointers to get our final result.
        The set of nodes that are required for re-wiring the tree to our final right skewed tree are 'left', 'right',
        and 'left tail'. Once the recursion does the hard work for us and flattens out the subtrees, we will
        essentially get two linked lists and we need the tail end of the left one to attach it to the head of the
        right one.
        Next, we will make the following connections:
            right = root.right
            root.right = root.left
            root.left = None
            left_tail.right = right
    Time complexity: (N logN), it takes O(height) to move to the end of the flattened left subtree
    Space complexity: O(N)
    """
    if not root:
        return
    flatten_v1(root.left)
    flatten_v1(root.right)
    right = root.right  # Save flattened right subtree for later concatenation
    root.right = root.left  # Concatenate root with flattened left subtree
    root.left = None  # Set left to null
    left_tail = root
    while left_tail.right:  # Move to the end of the newly added flattened left subtree
        left_tail = left_tail.right
    left_tail.right = right  # Concatenate flattened left subtree with flattened right subtree


def flatten_v2(root):
    """ In the flattened tree, each node's right child points to the next node of a pre-order traversal. So we're
        basically performing a reverse post-order traversal. 'pre' is the next (right) node of current node, pointing
        initially to None.
        Example:
            1
           / \
          2   5
         / \   \
        3  4   6
        Basically, the traversing order after flattening is pre-order traversal in (root, left, right), like:
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
                      6
        If we traverse the flattened tree in the reverse way, we would notice that [6 -> 5 -> 4 -> 3 -> 2 -> 1] is in
        (right, left, root) order of the original tree:
            The reverse post-order traversal of the original tree is the reverse order of the flattened tree
        The idea is to traverse the original tree in reverse post-order and then set each node's right pointer as the
        previous one in [6 -> 5 -> 4 -> 3 -> 2 -> 1] and set the left child as null. It turns out that the previous
        node that needs to be set as the current node's right is the root node of the previous recursion.
            1
           / \
          2   5
         / \   \
        3  4   6
        -----------
        pre = None
        root = 6

            1
           / \
          2   5
         / \   \
        3  4   6
        -----------
        pre = 6
        root = 5


            1
           / \
          2   5
         / \   \
        3   4   6
        -----------
        pre = 5
        root = 4

            1
           /
          2
         / \
        3   4
             \
              5
               \
                6
        -----------
        pre = 4
        root = 3

            1
           /
          2
         /
        3
         \
          4
           \
            5
             \
              6
        -----------
        pre = 3
        root = 2

            1
           /
          2
           \
            3
             \
              4
               \
                5
                 \
                  6
        -----------
        pre = 2
        root = 1

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
                      6
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def reverse_post_order(root):
        if not root:
            return
        reverse_post_order(root.right)
        reverse_post_order(root.left)
        root.right = pre[0]
        root.left = None
        pre[0] = root

    pre = [None]
    reverse_post_order(root)



