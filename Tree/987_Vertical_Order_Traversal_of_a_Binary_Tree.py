""" Given a binary tree, return the vertical order traversal of its nodes values.
For each node at position (X, Y), its left and right children respectively will be at positions (X-1, Y-1) and
(X+1, Y-1).
Running a vertical line from X = -infinity to X = +infinity, whenever the vertical line touches some nodes, we report
the values of the nodes in order from top to bottom (decreasing Y coordinates).
If two nodes have the same position, then the value of the node that is reported first is the value that is smaller.
Return an list of non-empty reports in order of X coordinate.  Every report will have a list of values of nodes. """


def vertical_traversal(root):
    """ To find the location of every node, we can use a depth-first search. During the search, we will maintain the
        location (x, y) of the node. As we move from parent to child, the location changes to (x-1, y-1) or (x+1, y-1)
        depending on if it is a left child or right child.
            1- If a node shows up at a higher level, it will be added first
            2- If two nodes are on the same level, then they will be sorted by value
        Therefore, we sort the locations by ascending x coordinate (left to right), then descending y coordinate
        (top to bottom), then actual node value so that they are in the correct order to be added to our answer.
    Time complexity: O(N * logN)
    Space complexity: O(N)
    """

    def dfs(root, x, y):
        if not root:
            return
        positions.append((x, y, root.val))
        dfs(root.left, x - 1, y - 1)
        dfs(root.right, x + 1, y - 1)

    positions, res = [], []
    dfs(root, 0, 0)
    positions.sort(key=lambda element: (element[0], -element[1], element[2]))
    min_x = float('-infinity')
    for x, y, val in positions:
        if x > min_x:
            res.append([])
            min_x = x
        res[-1].append(val)
    return res