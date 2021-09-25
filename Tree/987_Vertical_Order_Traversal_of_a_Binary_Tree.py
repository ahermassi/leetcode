""" Given a binary tree, return the vertical order traversal of its nodes values.
For each node at position (X, Y), its left and right children respectively will be at positions (X-1, Y-1) and
(X+1, Y-1).
Running a vertical line from X = -infinity to X = +infinity, whenever the vertical line touches some nodes, we report
the values of the nodes in order from top to bottom (decreasing Y coordinates).
If two nodes have the same position, then the value of the node that is reported first is the value that is smaller.
Return an list of non-empty reports in order of X coordinate.  Every report will have a list of values of nodes. """

from collections import defaultdict, deque


def vertical_traversal_v1(root):
    """ We are asked to return the vertical order of a binary tree, which implies three sub-orders (denoted as
        <column, row, value>) as follows:

        Column-wise order:
        First, we look at a binary tree vertically. Each node would be aligned to a specific column, based on its
        relative offset to the root node of the tree. Let us assume that the root node has a column index of 0, then
        its left child node would have a column index of -1, and its right child node would have a column index of +1,
        and so on.

        Row-wise order:
        Secondly, we look at the binary tree horizontally. Each node would be assigned to a specific row, based on its
        level (i.e. the vertical distance to the root node). Let us assume that the root node has a row index of 0,
        then both its child nodes would have the row index of 1. Note that the convention we adopt here is slightly
        different from the one in the problem description where the row index of a parent node is larger than the one
        of its child nodes. This, though, would not jeopardize our solution. On the contrary, it would help us to
        simplify the solution, as we will see later.

        Value-wise order:
        Finally, given the definitions of the above two sub-orders, there could be a case where two different nodes
        have the same <column, row> index. As a result, to resolve the draw situation, the node that has a smaller
        value should come first.

        Given the above definitions, we can now formulate the problem as a task to sort the nodes based on the
        3-dimensional coordinates <column, row, value> that we defined above.

        The priority of each coordinate is determined by its order. For example, the coordinate column comes first,
        therefore it has the highest priority. A node with the lowest column index would come up first, regardless the
        other two coordinates.

        As a result, the idea to solve the problem would be as intuitive as building a list where each element in the
        list corresponds to the 3-dimensional coordinates of each node in the tree, and then sorting the list based on
        the coordinates.

        To build such a list, we would need to traverse all the nodes in the tree, which we could do with either
        Breadth-First Search (BFS) or Depth-First Search (DFS). Most of the time, facing the problems of binary tree
        traversal, we need to make a choice between them. However, in this case, both of the approaches would work.
        Because both of them would lead to a list that contains the coordinates of all nodes. Though the order of
        elements in the list would differ depending on the approach, it does not matter, since we would sort the list
        anyway.

        To find the location of every node in this solution, we can use a DFS. During the search, we will maintain the
        location (row, col) of the node. As we move from parent to child, the location changes to (row + 1, col - 1) or
        (row + 1, col + 1) depending on if it is a left child or right child.

        Note that we assign a higher row index value to a node's child node. This convention is at odds with the
        denotation given in the problem description. This is done intentionally in order to keep the ordering of all
        coordinates consistent, i.e. a lower value in any specific coordinate represents a higher order. As a result,
        a sorting operation in ascending order would work for each coordinate consistently.

        Therefore, we sort the locations by ascending x coordinate (left to right), then descending y coordinate
        (top to bottom), then actual node value so that they are in the correct order to be added to our answer.
    Time complexity: O(N logN), we traverse the input tree which would take O(N) time, then we sort the obtained list
    of coordinates which contains N elements. The sorting operation would take O(N logN) time.
    Space complexity: O(N)
    """

    def dfs(root, row, col):
        if not root:
            return
        positions.append((col, row, root.val))
        dfs(root.left, row + 1, col - 1)
        dfs(root.right, row + 1, col + 1)

    positions, res = [], []
    dfs(root, 0, 0)
    positions.sort()  # Sort the node list globally, according to the coordinates
    prev_col = float('-inf')
    for col, row, val in positions:
        if col > prev_col:  # End of a column and start of the next column
            res.append([])
            prev_col = col
        res[-1].append(val)
    return res


def vertical_traversal_v2(root):
    """ Same as previous solution but keeping node's position and value in a hash map indexed by x coordinate.
    Time complexity: O(N * logN)
    Space complexity: O(N)
    """
    positions, res = defaultdict(list), []
    queue = deque([(root, 0, 0)])
    min_x = max_x = 0
    while queue:
        node, x, y = queue.popleft()
        positions[x].append((y, node.val))
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        if node.left:
            queue.append((node.left, x - 1, y - 1))
        if node.right:
            queue.append((node.right, x + 1, y - 1))
    for i in range(min_x, max_x + 1):
        res.append(val for y, val in sorted(positions[i], key=lambda element: (-element[0], element[1])))
    return res
