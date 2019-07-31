""" You're given strings J representing the types of stones that are jewels, and S representing the stones you have.
Each character in S is a type of stone you have.  You want to know how many of the stones you have are also jewels.
"""

import unittest2 as unittest


def num_jewels_in_stones(J, S):
    """ Read J and build jewels hash set. Read S and count jewels.
        Use hash set as it's O(1) to check if it contains an element.
    Time complexity: O(N + M) where N is the length of S and M is the length of J
    Space complexity: O(1), J will consist of letters and have length at most 26
    """
    jewels, count = set(J), 0
    for stone in S:
        if stone in jewels:
            count += 1
    return count


class Test(unittest.TestCase):
    data = [('aA', 'aAAbbbb', 3),
            ('z', 'ZZ', 0)
            ]

    def test_num_jewels_in_stones(self):
        for test_jewels, test_stones, result in self.data:
            self.assertEqual(result, num_jewels_in_stones(test_jewels, test_stones))


if __name__ == '__main__':
    unittest.main()