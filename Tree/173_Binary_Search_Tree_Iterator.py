""" Implement an iterator over a binary search tree (BST). Your iterator will be initialized with the root node of a BST.
Calling next() will return the next smallest number in the BST. """

# Good read: https://leetcode.com/articles/binary-search-tree-iterator/


class BSTIteratorV1(object):

    """ Usually, an iterator simply goes over each of the elements of the container one by one. For the BST, we want
        the iterator to return elements in an ascending order.
        We will be using additional memory and we will flatten the binary search tree into an array. Since we need the
        elements to be in a sorted order, we will do an in-order traversal over the tree and store the elements in a
        new array and then build the iterator functions using this new array.
    Time complexity: O(N) is the time taken by the constructor for the iterator as we have to visit each node once.
    next() and hasNext() are both O(1)
    Space complexity: O(N) occupied by values array, and O(logN) occupied by the recursion stack for in-order traversal.
    So overall, space complexity is O(N)
    """

    def __init__(self, root):
        self.values = []
        self.index = 0  # Pointer to the next smallest element in the BST
        self.inorder(root)  # Call to flatten the input binary search tree

    def next(self):
        """ Return the next smallest number """
        self.index += 1
        return self.values[self.index - 1]

    def hasNext(self):
        """ Return whether we have a next smallest number """
        return self.index < len(self.values)

    def inorder(self, root):
        if not root:
            return
        self.inorder(root.left)
        self.values.append(root.val)
        self.inorder(root.right)


class BSTIteratorV2(object):
    """ If we could simulate a controlled recursion for an in-order traversal, we wouldn't really need to use any
        additional space other than the space used by the stack for our recursion simulation.
        So, this approach essentially uses a custom stack to simulate the in-order traversal, i.e. we will be taking an
        iterative approach to in-order traversal rather than going with the recursive approach and in doing so, we will
        be able to easily implement the two function calls without any other additional space.
    Time complexity: O(1) for hasNext(); next() involves two major operations. One is where we pop an element from the
    stack which becomes the next smallest element to return. This is a O(1) operation. However, we then make a call
    to our helper function process_leftmost() which iterates over some nodes. However, the important thing to note
    here is that we only make such a call for nodes which have a right child. Otherwise, we simply return. Also, even
    if we end up calling the helper function, it won't always process N nodes. They will be much less.
    Thus, the amortized (average) time complexity for this function would still be O(1).
    When analyzing amortized time complexities, it is easier to reason that each node gets pushed and popped exactly
    once in next() when iterating over all N nodes. That comes out to 2N * O(1) over N calls to next(), making it O(1)
    on average, or O(1) amortized.
    Space complexity: O(logN) = O(height) which is occupied by our custom stack for simulating the in-order traversal
    """

    def __init__(self, root):
        self.stack = []
        self.process_leftmost(root)

    def next(self):
        """ Return the next smallest number """
        node = self.stack.pop()  # Node at the top of the stack is the next smallest element
        # Suppose we get a call to the next() function. The node which we have to return i.e. the next smallest
        # element in the binary search tree iterator is the one sitting at the top of our stack. So, for the example
        # above, that node would be 2 which is the correct value. Now, there are two possibilities that we have to
        # deal with:
        # One is where the node at the top of the stack is actually a leaf node. This is the best case and
        # here we don't have to do anything. Simply pop the node off the stack and return its value. So, this would
        # be a constant time operation.
        # Second is where the node has a right child. We don't need to check for the  left child because of the way we
        # have added nodes onto the stack. The topmost node either won't have a left child or would already have the
        # left subtree processed. If it has a right child, then we call our helper function on the node's right child.
        # We keep on maintaining the invariant this way in the function call for next and this way we will always be
        # able to return the next smallest element in the BST from the top of the stack.
        self.process_leftmost(node.right)  # Need to maintain the invariant. If the node has a right child, call the
        # helper function for the right child
        return node.val

    def hasNext(self):
        """ Return whether we have a next smallest number """
        return self.stack

    def process_leftmost(self, root):
        """ For a given node, add all the elements in the leftmost branch of the tree under it to the stack. """
        while root:
            self.stack.append(root)
            root = root.left
