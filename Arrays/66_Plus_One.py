""" Given a non-empty array of digits representing a non-negative integer, plus one to the integer.
 Example:
Input: [1,2,3]
Output: [1,2,4]
Explanation: The array represents the integer 123. """

import unittest2 as unittest


def plus_one_v1(digits):
    """ Identify the rightmost digit which is not equal to nine and increase that digit by one. All the following
         consecutive digits of nine should be set to zero.

         When all the digits are nines, we need to set all nines to zero and append 1 to the left side of the array.

            - Move along the input array starting from the end of array.

            - Set all the nines at the end of array to zero.

            - If we meet a not-nine digit, we would increase it by one. The job is done - return digits.

            - We're here because all the digits were equal to nine. Now they have all been set to zero. We then append
               the digit 1 in front of the other digits and return the result.

    Time complexity: O(N), since it's not more than one pass along the input list
    Space complexity: O(1), when input contains at least one not-nine digit, and O(N) otherwise. Although we perform the
    operation in-place (i.e. on the input list itself), in the worst scenario, we would need to allocate an intermediate
    space to hold the result, which contains the N+1 elements.
    """
    i = len(digits) - 1
    while i >= 0:
        if digits[i] == 9:
            digits[i] = 0
            i -= 1
        else:
            digits[i] += 1
            return digits
    return [1] + digits


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

