""" Design an algorithm to serialize and deserialize a binary search tree. There is no restriction on how your
serialization/deserialization algorithm should work. You just need to ensure that a binary search tree can be serialized
to a string and this string can be deserialized to the original tree structure.
The encoded string should be as compact as possible. """

import unittest2 as unittest
from collections import deque


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class CodecPreorder:
    """ Let's use here the fact that BST could be constructed from preorder or postorder traversal only.
        Inorder traversal is not a unique identifier for the BST. For example, 1-2-3 inorder traversal could correspond
        to at least 3 different trees: with the root equal to 1, with the root 2, and with the root 3.
        By contrary, both preorder and postorder traversals are unique identifiers of BST. That’s because from these
        traversals one could restore the inorder one: inorder = sorted(postorder) = sorted(preorder).

        This class uses preorder traversal for serialization. To deserialized, use a queue to recursively get root
        node, left subtree and right subtree.
        Pre order traversal of BST will output root node first, then left children, then right:
        root left1 left2 leftX right1 rightX

    """

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        values = []

        def preorder(root):
            if root:
                values.append(root.val)
                preorder(root.left)
                preorder(root.right)

        preorder(root)
        return ' '.join([str(val) for val in values])

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """

        def build(lower, upper):
            if queue and lower < queue[0] < upper:  # Verifying if first element in queue meets BST properties
                val = queue.popleft()
                root = TreeNode(val)
                root.left = build(lower, val)  # BST property for left child: less than parent value
                root.right = build(val, upper)  # BST property for right child: greater than parent value
                return root

        if not data:
            return None
        values = [int(val) for val in data.split(' ')]
        queue = deque(values)
        return build(float('-inf'), float('inf'))  # Use lower and upper bounds to verify BST properties before each
        # attempt to create right/left child.


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(4)

    def test_is_alien_sorted1(self):
        codec_preorder = CodecPreorder()
        root_preorder = codec_preorder.deserialize(codec_preorder.serialize(self.root))
        self.assertEqual(5, root_preorder.val)
        self.assertEqual(3, root_preorder.left.val)
        self.assertEqual(6, root_preorder.right.val)
        self.assertEqual(1, root_preorder.left.left.val)
        self.assertEqual(4, root_preorder.left.right.val)


if __name__ == '__main__':
    unittest.main()