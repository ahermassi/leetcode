""" Implement an iterator over a binary search tree (BST). Your iterator will be initialized with the root node of a BST.
Calling next() will return the next smallest number in the BST. """

# Good read: https://leetcode.com/articles/binary-search-tree-iterator/


class BSTIteratorV1(object):

    """ Usually, an iterator simply goes over each of the elements of the container one by one. For the BST,
        we want the iterator to return elements in an ascending order.
        We will be using additional memory and we will flatten the binary search tree into an array. Since we need the
        elements to be in a sorted order, we will do an inorder traversal over the tree and store the elements in a new
        array and then build the iterator functions using this new array.
    Time complexity: O(N) is the time taken by the constructor for the iterator as we have to visit each node once.
    next() and hasNext() are both O(1)
    Space complexity: O(N) occupied by values array, and O(log N) occupied by the recursion stack for inorder traversal.
    So overall, space complexity is O(N)
    """

    def __init__(self, root):
        """
        :type root: TreeNode
        """
        self.values = []
        self.index = 0  # Pointer to the next smallest element in the BST

        self.inorder(root)  # Call to flatten the input binary search tree

    def next(self):
        """
        @return the next smallest number
        :rtype: int
        """
        self.index += 1
        return self.values[self.index - 1]

    def hasNext(self):
        """
        @return whether we have a next smallest number
        :rtype: bool
        """
        return self.index < len(self.values)

    def inorder(self, root):
        if not root:
            return
        self.inorder(root.left)
        self.values.append(root.val)
        self.inorder(root.right)
