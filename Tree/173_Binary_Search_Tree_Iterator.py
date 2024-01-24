""" Implement an iterator over a binary search tree (BST). Your iterator will be initialized with the root node of a BST.
Calling next() will return the next smallest number in the BST. """

# Good read: https://leetcode.com/articles/binary-search-tree-iterator/


class BSTIteratorV1(object):

    """ Usually, an iterator simply goes over each of the elements of the container one by one. For the BST, we want
         the iterator to return elements in ascending order.

         An important property of the binary search tree is that the inorder traversal of a BST gives us the elements in
         a sorted order. Thus, the inorder traversal will be the core of the solution.

         Naturally, the easiest way to implement an iterator would be on an array like container interface. So, if we had an array, all we would need is a pointer or an index and we could easily implement the two required functions next() and hasNext().

         We will be using additional memory and will flatten the binary search tree into an array. Since we need the
         elements to be in a sorted order, we will do an inorder traversal over the tree and store the elements in a
         new array and then build the iterator functions using this new array.

         Whenever there's a call to hasNext, we simply check if the index has reached the end of the array. For the call
         to next function, we simply return the element pointed by the index. Also, after the next function call is
         made, we have to move the index one step forward to simulate the progress of the iterator.

    Time complexity: O(N) is the time taken by the constructor for the iterator as we have to visit each node once.
    next() and hasNext() are both O(1)
    Space complexity: O(N) occupied by values array, and O(h) occupied by the recursion stack for inorder traversal,
    where h is the height of the tree. So overall, space complexity is O(N)
    """

    def __init__(self, root):
        self.values = []
        self.index = 0  # Pointer to the next smallest element in the BST
        self.inorder(root)  # Flatten the input binary search tree

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


# Video explanation: https://youtu.be/RXy5RzGF5wo
class BSTIteratorV2(object):
    """ If we could simulate a controlled recursion for an inorder traversal, we wouldn't really need to use any
         additional space other than the space used by the stack for the recursion simulation.

         So, this approach essentially uses a custom stack to simulate the inorder traversal, i.e. we will be taking an
         iterative approach to inorder traversal rather than going with the recursive way and in doing so, we will be
         able to easily implement the two function calls without any other additional space.

            - Initialize an empty stack which will be used to simulate the inorder traversal for the binary search tree.
               Note that we will be following the same approach for inorder traversal as before except that now we will
               be using our own stack rather than the system stack. Since we are using a custom data structure, we can
               pause and resume the recursion at will.

            - Let's also consider a helper function that we will be calling again and again in the implementation. This
               function, called process_leftmost, will essentially add all the nodes in the leftmost branch of the tree
               rooted at the given node root to the stack, and it will keep on doing so until there is no left child of
               the root node.
               For a given node root, the next smallest element will always be the leftmost element in its tree. So, for
               a given root node, we keep on following the leftmost branch until we reach a node which doesn't have a
               left child and that will be the next smallest element. For the root of our BST, this leftmost node would
               be the smallest node in the tree. Rest of the nodes are added to the stack because they are pending
               processing.

            - The first time next() function call is made, the smallest element of the BST has to be returned and then
               the simulated recursion has to move one step forward i.e. move onto the next smallest element in the BST.
               The invariant that will be maintained in this algorithm is that the stack top always contains the element
                to be returned for the next() function call. However, there is additional work that needs to be done to
                maintain that invariant.

            - Initially, given the root node of the BST, we call the function process_leftmost and that ensures the
               invariant holds.

            - Suppose we get a call to the next() function. The node which we have to return i.e. the next smallest
               element in the binary search tree iterator is the one sitting at the top of the stack. Now, there are two
               possibilities that we have to deal with:

                    * One is where the node at the top of the stack is actually a leaf node. This is the best case and
                       here we don't have to do anything. Simply pop the node off the stack and return its value. So,
                       this would be a constant time operation.
                    * Second is where the node has a right child. We don't need to check for the left child because of
                       the way we have added nodes to the stack. The topmost node either won't have a left child or
                       would already have the left subtree processed. If it has a right child, then we call the helper
                       function on the node's right child. This would comparatively be a costly operation depending
                       upon the structure of the tree.

            - We keep on maintaining the invariant this way in the function call for next and this way we will always be
               able to return the next smallest element in the BST from the top of the stack. Again, it's important to
               understand that obtaining the next smallest element doesn't take much time. However, some time is spent
               in maintaining the invariant that the stack top will always have the node we are looking for.

    Time complexity: O(1) for hasNext(); next() involves two major operations. One is where we pop an element from the
    stack which becomes the next smallest element to return. This is a O(1) operation. However, we then make a call
    to our helper function process_leftmost() which iterates over some nodes. However, the important thing to note
    here is that we only make such a call for nodes which have a right child. Otherwise, we simply return. Also, even
    if we end up calling the helper function, it won't always process N nodes. They will be much less. Only if we have
    a skewed tree would there be N nodes for the root. But that is the only node for which we would call the helper
    function.
    Thus, the amortized (average) time complexity for next() function would still be O(1).
    When analyzing amortized time complexities, it is easier to reason that each node gets pushed and popped exactly
    once in next() when iterating over all N nodes. That comes out to 2N * O(1) over N calls to next(), making it O(1)
    on average, or O(1) amortized.
    Space complexity: O(height) which is occupied by our custom stack for simulating the inorder traversal
    """

    def __init__(self, root):
        self.stack = []
        self.process_leftmost(root)

    def next(self):
        """ Return the next smallest number """
        node = self.stack.pop()  # Node at the top of the stack is the next smallest element
        # We need to maintain the invariant. If the node has a right child, call the helper function for the
        # right child.
        self.process_leftmost(node.right)
        return node.val

    def hasNext(self):
        """ Return whether we have a next smallest number """
        return self.stack

    def process_leftmost(self, root):
        """ For a given node, add all the elements in the leftmost branch of the tree under it to the stack. """
        while root:
            self.stack.append(root)
            root = root.left
