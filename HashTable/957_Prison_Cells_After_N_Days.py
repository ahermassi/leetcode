""" There are 8 prison cells in a row, and each cell is either occupied or vacant.
Each day, whether the cell is occupied or vacant changes according to the following rules:
If a cell has two adjacent neighbors that are both occupied or both vacant, then the cell becomes occupied.
Otherwise, it becomes vacant.
Given the initial state of the prison, return the state of the prison after N days (and N such changes described above.)
"""

import unittest2 as unittest


def prison_after_n_days(cells, N):
    """ Because there are at most 256 possible states for the prison, eventually the states repeat into a cycle
        rather quickly. We can keep track of when the states repeat to find the period t of this cycle, and skip days
        in multiples of t.
        Let's do a naive simulation, iterating one day at a time. For each day, we will decrement N, the number of days
        remaining, and transform the state of the prison forward (cells -> next_day).
        If we reach a state we have seen before, we know how many days ago it occurred:
            t = states[curr_state] - curr_day = states[curr_state] - N
        Then, because of this cycle, we can do N %= t.
    Time complexity: O(1), for 8 cells we can have 2^6 = 64 different states since we only have 6 bits that are
    changing (first and last bits change to 0 and stay 0)
    Space complexity: O(1), we need to remember a single state of all cells for the loop detection.
    """
    states = {tuple(cells): N}
    while N > 0:
        N -= 1
        next_day = [0] * 8
        for i in range(1, 7):
            next_day[i] = 1 if cells[i - 1] == cells[i + 1] else 0
        if tuple(next_day) in states:
            N %= states[tuple(next_day)] - N  # states[tuple(next_day)] is the last time when this same state appeared;
            # (states[tuple(next_day)] - N) is the cycle length. %= cuts down the loop times.
        states[tuple(next_day)] = N
        cells = next_day
    return cells


class Test(unittest.TestCase):
    data = [([0, 1, 0, 1, 1, 0, 0, 1], 7, [0, 0, 1, 1, 0, 0, 0, 0])]

    def test_prison_after_n_days(self):
        for test_cells, test_days, result in self.data:
            self.assertEqual(result, prison_after_n_days(test_cells, test_days))


if __name__ == '__main__':
    unittest.main()
