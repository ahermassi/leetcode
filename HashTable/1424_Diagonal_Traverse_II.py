""" Given a list of lists of integers, nums, return all elements of nums in diagonal order as shown in the below images.
"""

from collections import defaultdict, deque


def find_diagonal_order_v1(nums):
    """ The crux of the problem is figuring out how to identify the diagonals and how to iterate over them. We will make
         use of an important property of diagonals in this approach.

         Let's say we are currently at the start of a diagonal (bottom-left) and the coordinates are (row, col). How do
         we get to the next value in the diagonal? We go up and right. By going up, we move to row-1. By going right, we
         move to col+1. That is, the row decreases by 1, and the col increases by 1.

         This is true for any given point in any given diagonal. If we were to consider the sum row+col, it would be
         constant along the diagonal since the -1 from moving up cancels out the +1 from moving right.

         For each square, we will use the sum row+col as an identifier to the diagonal that it belongs to. We use a
         'diagonals' hashmap where diagonals[x] is a list of all values that appear in the diagonal with identifier x.

         To collect the cells on each diagonal in the correct order, reverse the order of each stored diagonal. This is
         because the diagonals move upward and to the right, but we're collecting them top to bottom, right to left.

    Time complexity: O(N), where N is the number of integers in the grid
    Space complexity: O(N)
    """
    diagonals = defaultdict(list)
    for i, row in enumerate(nums):
        for j, cell in enumerate(row):
            diagonals[i + j].append(cell)
    res = []
    for values in diagonals.values():
        res.extend(values[::-1])
    return res


def find_diagonal_order_v2(nums):
    """ To avoid reversing the values, we iterate through each row from left to right starting with the bottom row.
         The reason we choose the bottom-up, left-to-right order is that the diagonals move upward and to the right, so
         by iterating to the upper right, we will visit the squares in the correct order.

         Note that, for this implementation, we need to find out the number of diagonals before collecting the cells.

    Time complexity: O(N), where N is the number of integers in the grid
    Space complexity: O(N)
    """
    diagonals = defaultdict(list)
    n, res = len(nums), []
    for i in reversed(range(n)):
        row = nums[i]
        for j, cell in enumerate(row):
            diagonals[i + j].append(cell)
    max_diagonal = max(diagonals.keys())
    for diagonal in range(max_diagonal + 1):
        res.extend(diagonals[diagonal])
    return res


def find_diagonal_order_v3(nums):
    """ In the previous approaches, we require two passes. The first pass populates the hashmap, and the second pass
         populates the output list. Can we do better, perhaps solving the problem in one pass?

        We can think about the grid as a graph. Each square is a node, and we can imagine each node having an edge to
        the squares below and to the right (if they exist).

        A node with identifier x has edges to nodes with identifier x+1. If we consider the top-left square (0,0) as a
        "source" node, then each square's identifier is exactly equal to its distance from the source. This allows us to
        visit the diagonals in order using BFS.

        The top-left cell, nums[0][0], is the root node. nums[1][0] is its left child, and nums[0][1] is its right
        child. Same analogy applies to all nodes nums[i][j].

        We start a BFS from (0,0). At each node (row, col), we first push (row+1, col) to the queue and then
        (row, col+1). Note that we only add a square to the queue if it both exists and has not been visited yet.

        How do we know if a square has been visited yet? We could use a hash set to keep track of visited squares, but
        there is a simpler way. We only need to consider the square (row+1, col) (down) if we are at the start of a
        diagonal. Otherwise, for every other square on the diagonal, the square below it has already been visited by the
        right edge of the previous square.

        The level-wise nature of BFS will ensure that we visit all squares in a diagonal with identifier x before we
        visit any square in a diagonal with identifier x+1. This means we visit the diagonals in the correct order.
        Because we add the square (row+1, col) before (row, col+1), we also traverse over each diagonal in the correct
        order as well.

        In other words, nums[row][col] is both the left child of nums[row-1][col] and the right child of nums[col][row-1].
        To avoid double counting, we only consider a number's left child when we are at the leftmost column (col == 0).

    Time complexity: O(N), where N is the number of integers in the grid
    Space complexity: O(sqrt(N)), the largest size queue will be is proportional to the size of the largest diagonal
    """
    n, res = len(nums), []
    queue = deque([(0, 0)])
    while queue:
        row, col = queue.popleft()
        res.append(nums[row][col])
        if col == 0 and row + 1 < n:
            # We only add the number at the bottom (left child) if we are at column 0. This is because this node
            # couldn't have been added by a parent node to its left as a right child
            queue.append((row + 1, col))
        if col + 1 < len(nums[row]):
            # Add the number on the right (right child)
            queue.append((row, col + 1))
    return res
