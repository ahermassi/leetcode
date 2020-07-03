""" Serialization is the process of converting a data structure or object into a sequence of bits so that it can be
stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the
same or another computer environment.
Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your
serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a
string and this string can be deserialized to the original tree structure. """


from collections import deque

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# Great explanation: https://www.youtube.com/watch?v=suj1ro8TIVY


class CodecV1:
    """ The idea is simple: print the tree in pre-order traversal and use 'X' to denote null node and separate nodes
        with ','. For deserialization, we use a queue to store the pre-order traversal, and since we have 'X' as null
        node, we know exactly where to end building subtrees.
        The intuition for the deserialization is the recognition that the first node in the pre-order sequence is the
        root, and the sequence for the root's left subtree appears before all the nodes in the root's right subtree.
        It is not easy to see where the left subtree sequence ends. However, if we solve the problem recursively, we
        can assume that the routine correctly computes the left subtree, which will also tell us where the right
        subtree begins.
    """

    def serialize(self, root):
        """Encodes a tree to a single string.
        Time complexity: O(N), we visit each node exactly once
        Space complexity: O(N), we keep the entire tree
        """
        if not root:
            return 'X'
        left = self.serialize(root.left)
        right = self.serialize(root.right)
        return ','.join([str(root.val), left, right])

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        Time complexity: O(N), we visit each node exactly once
        Space complexity: O(N)
        """

        def buildTree(queue):
            if not queue:
                return None
            value = queue.popleft()
            if value == 'X':
                return None
            root = TreeNode(value)
            root.left = buildTree(queue)
            root.right = buildTree(queue)
            return root

        queue = deque(data.split(','))
        return buildTree(queue)


class CodecV2:
    """ We can also use a BFS traversal to serialize/deserialize the tree, similar to how Leetcode does it. """

    def serialize(self, root):
        """Encodes a tree to a single string.
        Time complexity: O(N)
        Space complexity: O(N)
        """
        if not root:
            return 'X'
        values, queue = [], deque([root])
        while queue:
            node = queue.popleft()
            if not node:
                values.append('X')
            else:
                values.append(str(node.val))
                queue.extend([node.left, node.right])
        return ','.join(values)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        Time complexity: O(N)
        Space complexity: O(N)
        """
        if data[0] == 'X':
            return None
        data = deque(data.split(','))
        root = TreeNode(data.popleft())
        queue = deque([root])
        while queue:
            node = queue.popleft()
            left, right = data.popleft(), data.popleft()
            node.left = TreeNode(left) if left != 'X' else None
            node.right = TreeNode(right) if right != 'X' else None
            queue.extend([kid for kid in (node.left, node.right) if kid])
        return root

