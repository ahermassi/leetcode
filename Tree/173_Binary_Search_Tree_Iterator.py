""" Implement an iterator over a binary search tree (BST). Your iterator will be initialized with the root node of a BST.
Calling next() will return the next smallest number in the BST. """

# Good read: https://leetcode.com/articles/binary-search-tree-iterator/


class BSTIteratorV1(object):

    """ Usually, an iterator goes over each of the elements of the container one by one. For the BST, we want the
         iterator to return elements in ascending order.

         An important property of the BST is that the inorder traversal yields the elements in sorted order. Thus, the
         inorder traversal is the core of the solution.

         Naturally, the easiest way to implement an iterator would be on an array-like container interface. So, if we
         had an array, all we would need is a pointer or an index, and we could easily implement the two required
         functions next() and hasNext().

         We use additional memory to flatten the BST into an array. Since we need the elements to be in sorted order, we
         perform an inorder traversal over the tree and store the elements in an array and then build the iterator
         functions using this list of values.

         Whenever there's a call to hasNext(), we check if the read index has reached the end of the array. For the call
         to next() function, we return the element pointed at by the index. Also, after next() function call, we have to
         increment the index to simulate the progress of the iterator.

    Time complexity: O(N) is the time taken by the constructor of the iterator as we have to visit each node once.
    next() and hasNext() are both O(1).
    Space complexity: O(N) used by the values array, and O(h) used by the recursion stack for inorder traversal, where h
    is the height of the tree. So overall, space complexity is O(N).
    """

    def __init__(self, root):
        self.values = []
        self.index = 0  # Pointer to the next smallest element in the BST
        self.inorder(root)  # Flatten the input BST

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

         So, this approach essentially uses a custom stack to simulate the inorder traversal, i.e. we take an iterative
         approach to inorder traversal rather than going with the recursive way and in doing so, we are able to easily
         implement the two function calls without any other additional space.

         Note that the recursive inorder traversal adds the nodes to the call stack pending processing, and what we are
         doing here is make explicit use of that same stack following the same order of push and (implicit) pop
         operations of the recursion.

            - Initialize an empty stack which is used to simulate the inorder traversal for the BST. Note that we are
               following the same approach for inorder traversal as before except that now we're using our own stack
               rather than the system stack. Since we are using a custom data structure, we can pause and resume the
               recursion at will.

            - Let's also consider a helper function, process_leftmost(), that adds all the nodes of the left branch of
               the tree rooted at any given node to the stack, and it keeps on doing so until there is no left child of
               that node.
               For a given node root, the next smallest element is always the leftmost element in its left subtree. So,
               for a given root node, we keep on following the leftmost branch until we reach a node that doesn't have a
               left child and that is the next smallest element. For the root of the BST, this leftmost node is the
               smallest node in the tree. Rest of the nodes are added to the stack because they are pending processing.

            - The first time next() function call is made, the smallest element of the BST has to be returned and then
               the simulated recursion has to move one step forward i.e. move onto the next smallest element in the BST.
               The invariant that is maintained in this algorithm is that the stack top always contains the element
                to be returned for the next() function call. However, there is additional work that needs to be done to
                maintain that invariant.

            - Initially, given the root node of the BST, we call the function process_leftmost(root) and that ensures
               the invariant holds.

            - Suppose we get a call to the next() function. The node we have to return i.e. the next smallest element in
               the BST iterator is the one sitting at the top of the stack. Now, there are two possibilities that we
               have to deal with:

                    * The node at the top of the stack is actually a leaf node. This is the best case, and we don't have
                       to do anything. Pop the node off the stack and return its value. So, this is a constant time
                       operation.
                    * The node has a right child. We don't need to check for the left child because of the way we have
                       added nodes to the stack. The topmost node either won't have a left child or would already have
                       its left subtree processed. If it has a right child, then we call the helper function on the
                       node's right child. This would comparatively be a costly operation depending on the structure of
                       the tree.

            - We keep on maintaining the invariant this way in the function call for next() and this way we're always
               able to return the next smallest element in the BST from the top of the stack.

        It's important to understand that obtaining the next smallest element isn't the most expensive operation.
        However, some time is spent maintaining the invariant that the stack top always has the next smallest element.

    Time complexity: O(1) for hasNext(); next() involves two major operations. One is where we pop an element from the
    stack which becomes the next smallest element to return. This is a O(1) operation. However, we then make a call
    to the helper function process_leftmost() which iterates over some nodes. However, the important thing to note
    here is that we only make such a call for nodes which have a right child. Otherwise, we return. Also, even if we end
    up calling the helper function, it doesn't always process N nodes. Only if we have a skewed tree would there be N
    to either side of the root. But that is the only node for which we would call the helper function.
    Thus, the amortized (average) time complexity for next() function would still be O(1).
    !! IMPORTANT!!
    When analyzing amortized time complexities, it is easier to reason that each node gets pushed and popped exactly
    once in next() when iterating over all N nodes. That comes out to 2N * O(1) over N calls to next(), making it O(1)
    on average, or O(1) amortized.
    Space complexity: O(height), used by the custom stack to simulate the inorder traversal
    """

    def __init__(self, root):
        self.stack = []
        self.process_leftmost(root)

    def next(self):
        """ Return the next smallest element. """
        node = self.stack.pop()  # The node at the top of the stack is the next smallest element.
        # We need to maintain the invariant. If the node has a right child, call the helper function on that child.
        self.process_leftmost(node.right)
        return node.val

    def hasNext(self):
        """ Return whether we have a next smallest element. """
        return self.stack

    def process_leftmost(self, root):
        """ For a given node, add all the elements of the left subtree to the stack. """
        while root:
            self.stack.append(root)
            root = root.left
