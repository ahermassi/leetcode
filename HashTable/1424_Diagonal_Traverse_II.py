""" Given a list of lists of integers, nums, return all elements of nums in diagonal order as shown in the below images.
"""

from collections import defaultdict, deque


def find_diagonal_order_v1(nums):
    """ Similar to 498- Diagonal Traverse.
        In a 2D matrix, elements in the same diagonal have the same sum of their indices. So if we have all elements
        with the same sum of their indices together, then it’s just a matter of printing those elements in order.
        We can loop through the matrix, store each element by the sum of its indices in a hash map. We end up with
        a collection of all elements on shared diagonals.
        Note: Here, diagonals are from bottom to top, but we traverse the input matrix from first row to last row.
        Hence we need to print the elements in reverse order.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    diagonals = defaultdict(list)
    n = len(nums)
    for i in range(n):
        for j in range(len(nums[i])):
            diagonals[i + j].append(nums[i][j])
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
