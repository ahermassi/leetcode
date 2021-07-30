""" Given a list of lists of integers, nums, return all elements of nums in diagonal order as shown in the below images.
"""

from collections import defaultdict


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
