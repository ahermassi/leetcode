class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def inorder(root):
    stack = [[root, False]]
    while stack:
        node, visited = stack[-1][0], stack[-1][1]
        if not node:
            stack.pop()
        elif visited:
            print(node.val)
            right = node.right
            stack.pop()
            stack.append([right, False])
        else:
            stack[-1][1] = True
            stack.append([node.left, False])


if __name__ == '__main__':
    root = TreeNode(7)
    root.left = TreeNode(3)
    root.right = TreeNode(15)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(20)
    inorder(root)