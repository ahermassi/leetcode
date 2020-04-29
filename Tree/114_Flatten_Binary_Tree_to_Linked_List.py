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


next = None


def flatten(root):
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


