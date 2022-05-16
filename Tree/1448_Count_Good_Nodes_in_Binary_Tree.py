""" Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with
a value greater than X.

Return the number of good nodes in the binary tree. """

# Video explanation: https://www.youtube.com/watch?v=7cp5imvDzl4


def good_nodes_v1(root):
    """ In this first approach, we'll be using recursion. A powerful idea for any tree or graph problem involving
         BFS/DFS is that instead of just adding nodes to the stack or queue, we can store extra data to represent state.

         For this problem, we're concerned about the greatest value seen, so instead of the recursive function only
         taking nodes as an input, such as dfs(node), let's also have each call take an integer as well, like
         dfs(node, integer). This integer will represent the greatest value on the path from the root to the associated
         node. This means that at each node, we can simply check if it is "good" by comparing this integer to the node's value.

        How do we calculate this number? For the root, the path from the root contains no other nodes, so we can
        initially set this value to the value of root itself. For every call afterwards, we should compare this number to
        the current node's value. If the current node's value is greater, then set this value equal to the current
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
            cur_path_max = root.val
        dfs(root.left, cur_path_max)
        dfs(root.right, cur_path_max)

    res = [0]
    dfs(root, root.val)
    return res[0]


def good_nodes_v2(root):
    """ We can also make every dfs() call return the number of good nodes in the subtree rooted at that node.
         This eliminates the need for a global count variable.

    Time complexity: O(N)
    Space complexity: O(N) worst case of skewed tree, O(logN) best case of balanced tree
    """

    def dfs(root, cur_path_max):
        if not root:
            return 0
        good = 1 if root.val >= cur_path_max else 0
        cur_path_max = max(cur_path_max, root.val)
        good += dfs(root.left, cur_path_max) + dfs(root.right, cur_path_max)
        return good

    return dfs(root, root.val)