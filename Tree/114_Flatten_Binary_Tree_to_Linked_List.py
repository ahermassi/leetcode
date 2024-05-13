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


# Video explanation: https://youtu.be/rKnD7rLT0lI
def flatten_v1(root):
    """ The main idea behind a recursive solution is that we use the solutions for sub-problems to solve an upper level
         problem. In the case of a tree, the subtrees are essentially the sub-problems. So, a recursive solution for
         this problem is based on the idea that, assuming we have already transformed the left and the right
         halves of a given root node, how do we establish or modify the necessary connections so that we get a right
         skewed tree?

         A better way to think about recursion is to "trust" that recursion does all the heavy lifting for us and
         flattens out the left and the right subtrees. What is it that we have to do then to get the final result? We
         need a right skewed tree, so we simply have to shuffle around some pointers to get the final result.

         The set of nodes that are required for rewiring the tree to the final right skewed tree are 'left', 'right',
         and 'left_tail'. But what is 'lef_tail'? Notice that each flattened subtree actually looks like a linked list.
         Every linked list has a head node and in this case, we also need the tail node. Once the recursion flattens out
         the subtrees, we get two linked lists, and we need the tail end of the left side list to attach it to the head
         of the right side list.

         We make the following connections:
            right = root.right
            root.right = root.left
            left_tail.right = right
            root.left = None

    Time complexity: (N logN), it takes O(height) to move to the end of the flattened left subtree
    Space complexity: O(N), occupied by the recursion stack. The problem statement doesn't mention anything about the
    tree being balanced or not and hence, the tree could be left skewed and in that case the longest branch (and the
    number of nodes in the recursion stack) would be N.
    """
    if not root:
        return
    flatten_v1(root.left)
    flatten_v1(root.right)
    right = root.right  # Save the flattened right subtree for later concatenation
    root.right = root.left  # Concatenate root and the flattened left subtree
    left_tail = root
    while left_tail.right:
        # Move to the tail / right end of the newly added flattened left subtree
        left_tail = left_tail.right
    left_tail.right = right  # Concatenate the right end of the flattened left subtree and the flattened right subtree
    root.left = None  # Set left to null


def flatten_v2(root):
    """ In the flattened tree, each node's right child is the node's successor in the preorder traversal. So we're
         basically performing a reverse postorder traversal (right -> left -> root).
         In this implementation, 'pre' is the next (right) node of the current node,  pointing initially to None.

         Example:
            1
           / \
          2   5
         / \   \
        3  4   6

        Basically, the traversal order after flattening is preorder traversal in (root, left, right), like:
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

        If we traverse the flattened tree in the reverse order, we would notice that [6 -> 5 -> 4 -> 3 -> 2 -> 1] is in
        (right, left, root) order of the original tree:

                The reverse postorder traversal of the original tree is the reverse order of the flattened tree

        The idea is to traverse the original tree in reverse postorder and then set each node's right pointer to the
        previous node in the traversal and the left child to null. It turns out the afore mentioned previous node is the
        root node of the previous recursion.

            1
           / \
          2   5
         / \   \
        3  4   6
        -----------
        pre = None
        root = 6 (first node in reverse postorder)

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
        root.right = prev[0]
        root.left = None
        prev[0] = root

    prev = [None]
    reverse_post_order(root)


def flatten_v3(root):
    """ There is a well-known tree traversal that doesn't use any additional space at all, known as Morris Traversal.
         With recursion, we only rewire the connections for the current node once we are already done processing the
         left and the right subtrees completely. However, the postponing of rewiring of connections of the current node
         until the left subtree is done is basically what recursion is.

         Recursion is all about postponing decisions until something else is completed. So, we will have to come up with
         a greedy way that will be costlier in terms of time, but will be space efficient in achieving the same results.

                For a current node, we will check if it has a left child or not. If it does, we will find the last node
                in the rightmost branch of the subtree rooted at this left child. Once we find this rightmost node,
                we will hook it up with the right child of the current node.

         By doing this operation for every node, we are simply trying to move stuff to the right-hand side one step at
         a time.

    Time complexity: O(N), since we process each node of the tree at most twice. If you think about it, we process the
    nodes once when we actually run the algorithm as the current node 'cur', and s second time we come across the
    nodes is when we are trying to find the rightmost node.
    Space complexity: O(1)
    """
    cur = root
    while cur:
        if cur.left:
            rightmost = cur.left
            while rightmost.right:
                # Find the rightmost node that will link to current node's right subtree. This is the first node in
                # the rightmost branch of the left subtree which doesn't have a right child.
                rightmost = rightmost.right
            # Rewire the connections
            rightmost.right = cur.right
            cur.right = cur.left  # Use current node's left subtree to replace its right subtree
            cur.left = None
        cur = cur.right  # If the current node has no left child, we simply move on to the right-hand side



