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
         skewed tree overall?

         A great way to think about recursion here is that we "trust" that recursion does all the hard work for us and
         flattens out the left and the right subtrees. What is it that we have to do then to get our final result? We
         need a right skewed tree, so we simply have to shuffle around some pointers to get the final result.

         The set of nodes that are required for rewiring the tree to the final right skewed tree are 'left', 'right',
         and 'left tail'. But what is 'left tail'? Notice that each flattened subtree actually looks like a linked list.
         Every linked list has a head node and in this case, we also need the tail node. Once the recursion does the
         hard work for us and flattens out the subtrees, we essentially get two linked lists, and we need the tail end
         of the left one to attach it to the head of the right one.

        Next, we will make the following connections:
            right = root.right
            root.right = root.left
            root.left = None
            left_tail.right = right

    Time complexity: (N logN), it takes O(height) to move to the end of the flattened left subtree
    Space complexity: O(N), occupied by the recursion stack. The problem statement doesn't mention anything about the
    tree being balanced or not and hence, the tree could be e.g. left skewed and in that case the longest branch (and
    hence the number of nodes in the recursion stack) would be N.
    """
    if not root:
        return
    flatten_v1(root.left)
    flatten_v1(root.right)
    right = root.right  # Save the flattened right subtree for later concatenation
    root.right = root.left  # Concatenate root and the flattened left subtree
    root.left = None  # Set left to null
    left_tail = root
    while left_tail.right:  # Move to the end of the newly added flattened left subtree
        left_tail = left_tail.right
    left_tail.right = right  # Concatenate the flattened left subtree and the flattened right subtree


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


def flatten_v3(root):
    """ There is a well known tree traversal out there that doesn't use any additional space at all. It's known as
        Morris Traversal. With recursion, we only re-wire the connections for the current nod" once we are already done
        processing the left and the right subtrees completely. However, the postponing of rewiring of connections on
        the current node until the left subtree is done is basically what recursion is. Recursion is all about
        postponing decisions until something else is completed. So, we will have to come up with a greedy way that will
        be costlier in terms of time, but will be space efficient in achieving the same results.

            For a current node, we will check if it has a left child or not. If it does, we will find the last node in
            the rightmost branch of the subtree rooted at this left child. Once we find this rightmost node, we will
            hook it up with the right child of the current node.

        By doing this operation for every node, we are simply trying to move stuff to the right hand side one step at
        a time.
    Time complexity: O(N), since we process each node of the tree at most twice. If you think about it, we process the
    nodes once when we actually run our algorithm on them as the current node 'cur'. The second time when we come
    across the nodes is when we are trying to find our rightmost node
    Space complexity: O(1)
    """
    cur = root
    while cur:
        if cur.left:
            rightmost = cur.left
            while rightmost.right:  # Find the rightmost node that will link to current node's right subtree
                rightmost = rightmost.right
            # Rewire the connections
            rightmost.right = cur.right
            cur.right = cur.left  # Use current node's left subtree to replace its right subtree
            cur.left = None
        cur = cur.right  # If the current node has no left child, we simply move on to the right hand side



