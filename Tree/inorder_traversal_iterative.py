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