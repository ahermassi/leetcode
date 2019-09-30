""" There are 8 prison cells in a row, and each cell is either occupied or vacant.
Each day, whether the cell is occupied or vacant changes according to the following rules:
If a cell has two adjacent neighbors that are both occupied or both vacant, then the cell becomes occupied.
Otherwise, it becomes vacant.
Given the initial state of the prison, return the state of the prison after N days (and N such changes described above.)
"""

import unittest2 as unittest


def prison_after_n_days(cells, N):
    """ Because there are at most 256 possible states for the prison, eventually the states repeat into a cycle
    rather quickly. Somehow, the cycle is equal to 14.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    if N % 14 == 0:  # When N % 14 == 0, then we do not want the 0th state, but the 14th state, that is the last state.
        N = 14
    else:
        N = N % 14
    for _ in range(N):
        temp = [0] * 8  # Easier than changing the cells array itself simultaneously
        for i in range(1, 7):
            if cells[i - 1] == cells[i + 1]:
                temp[i] = 1
            else:
                temp[i] = 0
        cells = temp
    return cells


class Test(unittest.TestCase):
    data = [([0, 1, 0, 1, 1, 0, 0, 1], 7, [0, 0, 1, 1, 0, 0, 0, 0])]

    def test_prison_after_n_days(self):
        for test_cells, test_days, result in self.data:
            self.assertEqual(result, prison_after_n_days(test_cells, test_days))


if __name__ == '__main__':
    unittest.main()
