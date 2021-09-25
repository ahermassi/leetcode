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
    """ BFS implementation of the previous algorithm.
    Time complexity: O(N logN)
    Space complexity: at any given moment the queue contains no more than two levels of nodes in the tree. The maximal
    number of nodes at one level is N/2 which is the number of the leaf nodes in a balanced binary tree. As a result,
    the space needed for the queue would be O(N/2 * 2) = O(N)
    """
    queue = deque([(root, 0, 0)])
    positions = []
    while queue:
        node, row, col = queue.popleft()
        if not node:
            continue
        positions.append((col, row, node.val))
        queue.append((node.left, row + 1, col - 1))
        queue.append((node.right, row + 1, col + 1))
    positions.sort()
    res = []
    prev_col = float('-inf')
    for col, row, val in positions:
        if col > prev_col:
            prev_col = col
            res.append([])
        res[-1].append(val)
    return res


def vertical_traversal_v3(root):
    """ As we can see in the above approaches, the overall time complexity is dominated by the sorting operation on
        the list of coordinates. In order to further optimize the solution, we can try to do something with the sorting.

        It would be hard, if not impossible, to eliminate the sorting operation, since we still need a means to resolve
        the draw situation when two nodes share the same <column, row> index. One might argue that we could use the
        heap data structure to maintain the list of coordinates. The elements in the heap data structure are ordered
        automatically, and this does eliminate the sorting operation. However, to maintain the elements in order, each
        insertion operation in heap would take O(logN) time complexity. In other words, we can consider the heap data
        structure as another form of sorting, which amortizes the cost of sorting operating over each insertion.

        That being said, one thing that we can do is reduce the scope of sorting by partitioning the list of
        coordinates into subgroups based on the column index. Although we would still need to sort the subgroups
        respectively, it would be faster to sort a series of subgroups than sorting them all together in a single
        group. Here is a not-so-rigid proof:

        Suppose that we have a list of N elements. It would then take O(N logN) time to sort this list. Next, we divide
        the list into k sub-lists equally. Each list would contain N/k elements. Similarly, it would take O(N/k logN/k)
        time to sort each sublist. In total, to sort all the k sub-lists, it would take O(k * N/k logN/k)=O(N logN/k),
        which is less than the time complexity of sorting the original list (i.e. O(N logN)).

        More importantly, another rationale to partition the list into column-based groups is that this is also the
        format of results that are asked in the problem.

        We traverse the input tree by either BFS or DFS. During the traversal, we populate the hash map. Meanwhile, we
        could also note down the minimal and maximal column index during the traversal (not done in this DFS
        implementation). The minimal and maximal column index defines the range of column index. With this range, we
        could iterate through columns in order without the need for sorting.

        Once we populate the above hash map, we then sort the values in each entry of the map, i.e. we sort each group
        of coordinates led by the column index.

    Time complexity: O(N logN/k), where k is the width of the tree i.e. the number of columns in the result
    Space complexity: O(N)
    """

    def dfs(root, row, col):
        if not root:
            return
        positions[col].append((row, root.val))
        dfs(root.left, row + 1, col - 1)
        dfs(root.right, row + 1, col + 1)

    positions, res = defaultdict(list), []
    dfs(root, 0, 0)
    for col in sorted(positions.keys()):
        values = positions[col]
        res.append([val for row, val in sorted(values)])  # sort first by 'row', then by 'value', in ascending order
    return res
