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


# Great explanation: https://www.youtu.be/suj1ro8TIVY
# Another one: https://youtu.be/u4JAi2JJhI8
class CodecV1:
    """ DFS is better adapted for our needs, since the linkage among the adjacent nodes is naturally encoded in the
         order, which is rather helpful for the later task of deserialization.

         The idea is simple: print the tree in preorder traversal, use 'X' to denote null nodes, and separate nodes
         with ','. For deserialization, we use a queue to store the preorder traversal, and since we have 'X' as null
         node, we know exactly where to end building subtrees.

         The intuition for the deserialization is recognizing that the first node in the preorder sequence is the root,
         and the sequence for the root's left subtree appears BEFORE all the nodes in the root's right subtree.

         It is not easy to see where the left subtree sequence ends. However, if we solve the problem recursively, we
         can assume that the routine correctly computes the left subtree, which will also tell us where the right
         subtree begins.

         Note that serialization contains information about the node values as well as the information about the tree
         structure. 'X' appears for each leaf to mark the absence of left and right child node. This is how we save the
          tree structure during the serialization.
    """

    def serialize(self, root):
        """Encodes a tree to a single string.

        Time complexity: O(N), we visit each node exactly once
        Space complexity: O(N), we keep the entire tree
        """

        def preorder(root):
            if not root:
                values.append('X')
                return
            values.append(root.val)
            preorder(root.left)
            preorder(root.right)

        values = []
        preorder(root)
        return ','.join(map(str, values))

    def deserialize(self, data):
        """Decodes the encoded data to tree.

        Time complexity: O(N), we visit each node exactly once
        Space complexity: O(N)
        """

        def build_tree():
            value = queue.popleft()
            if value == 'X':
                return None
            root = TreeNode(value)
            root.left = build_tree()
            root.right = build_tree()
            return root

        queue = deque(data.split(','))
        return build_tree()


class CodecV2:
    """ We can also use a BFS traversal to serialize/deserialize the tree, similar to how Leetcode does it.
         We use 'X' to represent null values. When deserializing the string, we assign left and right child for each
         non-null node, and add the non-null children to the queue, waiting to be processed later.
    """

    def serialize(self, root):
        """Encodes a tree to a single string.

        Time complexity: O(N)
        Space complexity: O(N)
        """
        values = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if not node:
                values.append('X')
            else:
                values.append(node.val)
                queue.extend(child for child in (node.left, node.right))
        return ','.join(map(str, values))

    def deserialize(self, data):
        """Decodes the encoded data to tree.

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
            left_val, right_val = data.popleft(), data.popleft()
            node.left = TreeNode(left_val) if left_val != 'X' else None
            node.right = TreeNode(right_val) if right_val != 'X' else None
            queue.extend(child for child in (node.left, node.right) if child)
        return root


class CodecV3:
    """ Same BFS approach, but during deserialization we use a read pointer/index to process the elements in the data
         list without turning it into a queue.
    """

    def serialize(self, root):
        """Encodes a tree to a single string.

        Time complexity: O(N)
        Space complexity: O(N)
        """
        values = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if not node:
                values.append('X')
            else:
                values.append(node.val)
                queue.extend(child for child in (node.left, node.right))
        return ','.join(map(str, values))

    def deserialize(self, data):
        """Decodes the encoded data to tree.

        Time complexity: O(N)
        Space complexity: O(N)
        """
        if data[0] == 'X':
            return None
        data = data.split(',')
        root = TreeNode(data[0])
        queue = deque([root])
        index = 1
        while queue:
            node = queue.popleft()
            if data[index] != 'X':
                node.left = TreeNode(data[index])
            index += 1
            if data[index] != 'X':
                node.right = TreeNode(data[index])
            index += 1
            queue.extend(child for child in (node.left, node.right) if child)
        return root

