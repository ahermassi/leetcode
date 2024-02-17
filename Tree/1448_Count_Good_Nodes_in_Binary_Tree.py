""" Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with
a value greater than X.

Return the number of good nodes in the binary tree. """

from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def good_nodes_v1(root):
    """ In this first approach, we'll be using recursion. A powerful idea for any tree or graph problem involving
         BFS/DFS is that instead of just adding nodes to the stack or stack, we can store extra data to represent state.

         For this problem, we're concerned about the greatest value seen, so instead of the recursive function only
         taking nodes as an input, such as dfs(node), let's also have each call take an integer as well, like
         dfs(node, integer). This integer will represent the greatest value on the path from the root to the associated
         node. This means that at each node, we can simply check if it is "good" by comparing this integer to the
         node's value.

         How do we calculate this number? For the root, the path from the root contains no other nodes, so we can
         initially set this value to the value of root itself. For every call afterwards, we should compare this number
         to the current node's value. If the current node's value is greater, then set this value equal to the current
         node's value before visiting this node's children.

         As we continue to traverse downwards through the tree, the number that we pass along with each node will
         increase every time it finds a new max value, which allows us to easily check when a node is "good".

    Time complexity: O(N), where N is the number of nodes in the tree. We visit every node exactly once and do a
    constant amount of work each time.
    Space complexity: O(N) worst case of skewed tree, O(logN) best case of balanced tree
    """

    def dfs(root, cur_path_max):
        if not root:
            return
        if root.val >= cur_path_max:
            res[0] += 1
        cur_path_max = max(cur_path_max, root.val)
        dfs(root.left, cur_path_max)
        dfs(root.right, cur_path_max)

    res = [0]
    dfs(root, root.val)
    return res[0]


# Video explanation: https://www.youtube.com/watch?v=7cp5imvDzl4
def good_nodes_v2(root):
    """ We can also make every dfs() call return the number of good nodes in the subtree rooted at that node.
         This eliminates the need for a global count variable.

    Time complexity: O(N)
    Space complexity: O(N) worst case of skewed tree, O(logN) best case of balanced tree
    """

    def dfs(root, cur_path_max):
        if not root:
            return 0
        good_nodes = 1 if root.val >= cur_path_max else 0
        cur_path_max = max(cur_path_max, root.val)
        good_nodes += dfs(root.left, cur_path_max) + dfs(root.right, cur_path_max)
        return good_nodes

    return dfs(root, root.val)


def good_nodes_v3(root):
    """ DFS can also be implemented iteratively. You may be thinking at this point: What kind of DFS should we use,
         preorder, postorder, or inorder? The answer is that, for this problem, it doesn't matter. For each node, there
         is only one path from the root to that node, so regardless of the order of our traversal, the integer we use to
         track the greatest value will always be the largest value between the current node and the root.

         The algorithm works the same as in the previous approach, but we will be using our own stack instead of
         recursion. We can implement the tracking integer by pairing the nodes with the integer when we push elements
         onto the stack.

         At each node, first check if node.val is greater than or equal to cur_path_max. If it is, then increment the
         result. Next, push the children onto the stack, along with the greater value between cur_path_max and node.val.

    Time complexity: O(N)
    Space complexity: O(N), in the worst case scenario, where every right child has 2 children and every left child has
    no children (or vice-versa), the stack will contain N/2 nodes at max depth
    """
    stack = [(root, root.val)]
    res = 0
    while stack:
        node, cur_path_max = stack.pop()
        if node.val >= cur_path_max:
            res += 1
            cur_path_max = node.val
        stack.extend([(child, cur_path_max) for child in (node.left, node.right) if child])
    return res


def good_nodes_v4(root):
    """ As stated in the previous approach, the order in which we perform DFS does not matter, because the extra state
         we pass along on each iteration will be correct regardless of traversal order. For this same reason, BFS and
         DFS are both valid approaches.

        The algorithm is identical to the iterative DFS approach, except we are using a queue instead of a stack.

    Time complexity: O(N)
    Space complexity: O(N), the worst case scenario for space with BFS is when the tree is full. In this scenario, the
    final level contains N/2 nodes, and the queue will hold all the nodes in the final level at some point.
    """
    queue = deque([(root, root.val)])
    res = 0
    while queue:
        node, cur_path_max = queue.popleft()
        if node.val >= cur_path_max:
            res += 1
            cur_path_max = node.val
        queue.extend([(child, cur_path_max) for child in (node.left, node.right) if child])
    return res
