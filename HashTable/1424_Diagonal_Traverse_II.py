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

    Time complexity: O(N * M)
    Space complexity: O(N * M)
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
    """ To avoid reversing the values, we can iterate starting from the bottom rows as theey are the starting values of
        the diagonals.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    diagonals = defaultdict(list)
    n = len(nums)
    for i in reversed(range(n)):
        for j in range(len(nums[i])):
            diagonals[i + j].append(nums[i][j])
    res = []
    for values in diagonals.values():
        res.extend(values)
    return res


def find_diagonal_order_v3(nums):
    """ We can think of the given matrix as a tree and use BFS to solve this problem.
        The top-left number, nums[0][0], is the root node. nums[1][0] is its left child, and nums[0][1] is its right
        child. Same analogy applies to all nodes nums[i][j].
        Note that nums[i][j] is both the left child of nums[i-1][j] and the right child of nums[i][j-1]. To avoid
        double counting, we only consider a number's left child when we are at the leftmost column (j == 0).
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, res = len(nums), []
    queue = deque([(0, 0)])
    while queue:
        row, col = queue.popleft()
        res.append(nums[row][col])
        if col == 0 and row < n - 1:  # We only add the number at the bottom (left child) if we are at column 0. This
            # is because this node couldn't have been added by a parent node to its left as a right child
            queue.append((row + 1, col))
        if col < len(nums[row]) - 1:  # Add the number on the right (right child)
            queue.append((row, col + 1))
    return res
