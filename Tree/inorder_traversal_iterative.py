class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def inorder(root):
    stack = [[root, False]]
    while stack:
        node, visited = stack[-1][0], stack[-1][1]
        if visited:
            stack.pop()
            print(node.val)
            if node.right:
                stack.append([node.right, False])
        else:
            stack[-1][1] = True
            if node.left:
                stack.append([node.left, False])


def inorder_v2(root):
    """ For a given node root of a BST, the next smallest element will always be the leftmost element in its tree. So,
        for a given root node, we keep on following the leftmost branch until we reach a node which doesn't have a left
        child and that will be the next smallest element. For the root of our BST, this leftmost node would be the
        smallest node in the tree. Rest of the nodes are added to the stack because they are pending processing.
        Now, there are two possibilities that we have to deal with:
        One is where the node at the top of the stack is actually a leaf node. This is the best case and here we don't
        have to do anything. Simply pop the node off the stack and return its value. So, this would be a constant time
        operation.
        Second is where the node has a right child. We don't need to check for the left child because of the way we
        have added nodes onto the stack. The topmost node either won't have a left child or would already have the left
        subtree processed. If it has a right child, then we call our helper function on the node's right child.
    """

    def process_leftmost(root):
        while root:
            stack.append(root)
            root = root.left

    stack = []
    process_leftmost(root)
    while stack:
        node = stack.pop()
        print(node.val)
        process_leftmost(node.right)


if __name__ == '__main__':
    root = TreeNode(7)
    root.left = TreeNode(3)
    root.right = TreeNode(15)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(20)
    inorder_v2(root)