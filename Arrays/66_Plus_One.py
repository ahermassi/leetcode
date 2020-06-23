""" Given a non-empty array of digits representing a non-negative integer, plus one to the integer.
 Example:
Input: [1,2,3]
Output: [1,2,4]
Explanation: The array represents the integer 123. """

import unittest2 as unittest


def plus_one_v1(digits):
    """ Read array from end, and replace each digit with 0 as long as it is a 9. Otherwise, add 1 and return.
    Time complexity: O(N)
    Space complexity: O(1), when digits contains at least one not-nine digit, and O(N) otherwise
    """
    i = len(digits) - 1
    while i >= 0 and digits[i] == 9:
        digits[i] = 0
        i -= 1
    if i >= 0:
        digits[i] += 1
    else:
        digits = [1] + digits
    return digits


def plus_one_v2(digits):
    """ Same as above but recursively.
    Time complexity: O(N), where N is the length of the array
    Space complexity: O(N), for the call stack in the worst case of all array elements are equal to 9
    """
    if len(digits) == 1 and digits[0] == 9:
        return [1, 0]
    if digits[-1] != 9:
        digits[-1] += 1
    else:
        digits[-1] = 0
        digits[:-1] = plus_one_v2(digits[:-1])
    return digits


class Test(unittest.TestCase):
    data = [([1, 2, 3], [1, 2, 4]),
            ([9], [1, 0]),
            ([1, 9, 9], [2, 0, 0])
            ]

    def test_plus_one(self):
        for test_array, result in self.data:
            self.assertEqual(result, plus_one_v1(test_array))
            self.assertEqual(result, plus_one_v2(test_array))


if __name__ == '__main__':
    unittest.main()

