""" Given inorder and postorder traversal of a tree, construct the binary tree. """

import unittest2 as unittest


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# Video explanation: https://youtu.be/vm63HuIU7kw
def build_tree(inorder, postorder):
    """ The two key observations are:

            - Postorder traversal follows Left -> Right -> Root, therefore, so given the postorder array, we have easy
               access to the root which is postorder[-1].

            - Inorder traversal follows Left -> Root -> Right, so the value picked from postorder traversal splits the
               inorder traversal into left and right subtrees. Therefore, if we know the position of root in the inorder
               list, we can recursively split the entire array into two subtrees.

        A postorder traversal sequence consists of the postorder traversal sequence of the left subtree, followed by the
        postorder traversal sequence of the right subtree, followed by the root. We know the number k of nodes in the
        left subtree from the location of the root in the inorder traversal sequence. Therefore, the subsequence of k
        nodes before the root in the postorder traversal sequence is the postorder traversal sequence for the RIGHT
        subtree.

        Now the idea should be clear enough. We will design a recursive function that will set the last element of
        postorder as the root, and then proceed recursively first to construct the right subtree and then to construct
        the left subtree. To find the left and right subtrees, it will look for the index of root in inorder list, so
        that everything on the left should be the left subtree, and everything on the right should be the right subtree.
        Both subtrees can be constructed by making another recursive call.

        It is worth noting that we should build a hashmap to record the relation of value -> index for inorder, so that
        we can find the position of root in constant time. Furthermore, if we don't want to mutate the postorder list,
        we can instead use an integer variable postorderIndex to keep track of the element that will be used to
        construct the root.

        Note also that we can't form a binary tree with only 1 traversal. For e.g. inorder = [9,3,15,20,7], here we
        don't know which is the root node of the tree and their children. It could start with any node as root and form
        a valid binary tree. Similarly, postorder = [9,15,7,20,3], here we know 3 is the root node since the traversal
        ended with it, however we are not sure of its children. It could have been all rest nodes on right side as
        (root)3 -> 20 -> 7 -> 15 -> 9 or all on left side as 9 <- 15 <- 7 <- 20 <- 3(root) or any intermediate of
        these.

    Time complexity: O(N), the recursive method has a cost of O(1) for each call and is called once for each of the N
    nodes, giving a total of O(N)
    Space complexity: O(N) for hash map, O(N) worst case / O(logN) average case for call stack
    """
    def build(inorder_left, inorder_right):
        # The boundaries denote the current range in inorder that the subtree will lie in
        if inorder_left > inorder_right:  # If there are no elements to construct subtrees
            return None
        root = TreeNode(postorder.pop())
        index = indexes[root.val]
        root.right = build(index + 1, inorder_right)
        # Pay attention to the order: right THEN left. Postorder traversal goes 'Left-Right-Parent', and postorder.pop()
        # picks the rightmost element of the postorder list, that means it should go 'Parent-(one of parents of) Right
        # (subtree) - Left'. So, switching the order doesn't work.
        # In other words, because that's the order they appear in the postorder list starting from the back to front.
        # preorder: root --> left --> right
        # postorder: left --> right --> root
        # For preorder, we start at root, and naturally follow up with left.
        # With postorder though, root is at the end, so we need to go backwards. Going backwards, we can see that
        # right comes "after" root. Since we are popping nodes from the end from postorder list, we come across nodes
        # in the order: node, node.right and then node.left.
        root.left = build(inorder_left, index - 1)
        return root

    indexes = {v: i for i, v in enumerate(inorder)}  # Build a map of indices of the values as they appear in in-order
    return build(0, len(inorder) - 1)


class Test(unittest.TestCase):
    postorder = [9, 15, 7, 20, 3]
    inorder = [9, 3, 15, 20, 7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    def test_build_tree(self):
        root = build_tree(self.inorder, self.postorder)
        self.assertEqual(3, root.val)
        self.assertEqual(9, root.left.val)
        self.assertEqual(20, root.right.val)
        self.assertEqual(15, root.right.left.val)
        self.assertEqual(7, root.right.right.val)


if __name__ == '__main__':
    unittest.main()
