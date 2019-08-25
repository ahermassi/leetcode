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


class BSTIteratorV2(object):
    """ if we could simulate a controlled recursion for an inorder traversal, we wouldn't really need to use any
        additional space other than the space used by the stack for our recursion simulation.
        So, this approach essentially uses a custom stack to simulate the inorder traversal i.e. we will be taking an
        iterative approach to inorder traversal rather than going with the recursive approach and in doing so, we will
        be able to easily implement the two function calls without any other additional space.
    Time complexity: O(1) for hasNext(); next() involves two major operations. One is where we pop an element from the
    stack which becomes the next smallest element to return. This is a O(1) operation. However, we then make a call
    to our helper function process_leftmost() which iterates over some nodes. However, the important thing to note
    here is that we only make such a call for nodes which have a right child. Otherwise, we simply return. Also, even
    if we end up calling the helper function, it won't always process N nodes. They will be much less.
    Thus, the amortized (average) time complexity for this function would still be O(1)
    Space complexity: O(log N) = O(height) which is occupied by our custom stack for simulating the inorder traversal
    """

    def __init__(self, root):
        """
        :type root: TreeNode
        """
        self.stack = []
        self.process_leftmost(root)

    def next(self):
        """
        @return the next smallest number
        :rtype: int
        """
        node = self.stack.pop()  # Node at the top of the stack is the next smallest element
        self.process_leftmost(node.right)  # Need to maintain the invariant. If the node has a right child, call the
        # helper function for the right child
        return node.val

    def hasNext(self):
        """
        @return whether we have a next smallest number
        :rtype: bool
        """
        return self.stack

    def process_leftmost(self, root):
        """ For a given node, add all the elements in the leftmost branch of the tree under it to the stack. """
        while root:
            self.stack.append(root)
            root = root.left
