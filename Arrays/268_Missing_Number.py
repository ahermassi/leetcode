""" Given an array containing n distinct numbers taken from 0, 1, 2, ..., n, find the one that is missing from the
array. """

import unittest2 as unittest


def missing_number_v1(nums):
    """ We can compute the sum of nums in linear time, and by Gauss' formula, we can compute the sum of the first n
        natural numbers in constant time. Therefore, the number that is missing is simply the result of Gauss' formula
        minus the sum of nums.
    Time complexity: O(N), although Gauss' formula can be computed in O(1) time, summing nums costs O(n) time, so the
    algorithm is overall linear.
    Space complexity: O(1)
    """
    n = len(nums)
    return n * (n + 1) / 2 - sum(nums)


# Vide explanation: https://youtu.be/WnPLSRLSANE
def missing_number_v2(nums):
    """ We can compute the missing number by computing the XOR of all the integers from 0 to n, inclusive, and
         XORing that with the XOR of all the elements in the array. Every element in the array, except for the missing
         element, cancels out with an integer from the first set. Therefore, the resulting XOR equals the missing
         element.

        Since the INDICES of the given nums list range from 0 to n-1, adding n to this list of indices gives
        us the list of all the integers from 0 to n. This is the list we need to XOR with the XOR of the array values.
        Therefore, if we initialize an integer to n and XOR it with every index and value, we will be left with the
        missing number.

        A better way to understand XOR solution is that if each number at an index was equal to its corresponding index,
         i.e. nums[i] == i, then taking the XOR of all the indices and all the values would have resulted in a perfect
         cancellation (zero out) and thus yielding the missing number as n ( the highest number in the range ). Now that
          can give a better clue that not only all the indices and values but also the highest number in the range (n)
          need to be XOR'd to get the missing number

    Time complexity: O(N), assuming that XOR is a constant-time operation
    Space complexity: O(1)
    """
    missing = len(nums)
    for i, num in enumerate(nums):
        missing ^= i ^ num
    return missing


def missing_number_v3(nums):
    """  An easier to understand version of the XOR solution.

         Think of the "missing" variable as something like a singularity: we can stuff all the expected numbers into a
         single variable, remove the numbers that are found in the list, and get back the missing value.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    missing = 0
    for i in range(n+1):
        # Using XOR, "add" each number in 0 ... n that "should be" in the list
        missing ^= i
    for num in nums:
        # Using XOR, "subtract" each number that we actually find in the list
        missing ^= num
    # We've removed every number except the missing value, so this must be it
    return missing


def missing_number_v4(nums):
    """ A brute force method would be to simply check for the presence of each number that we expect to be present. Use
         a set to get constant time containment queries and overall linear runtime.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    num_set = set(nums)
    for number in range(len(nums) + 1):
        if number not in num_set:
            return number


class Test(unittest.TestCase):
    data = [([3, 0, 1], 2), ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8)]

    def test_missing_number(self):
        for test_array, result in self.data:
            self.assertEqual(result, missing_number_v1(test_array))
            self.assertEqual(result, missing_number_v2(test_array))
            self.assertEqual(result, missing_number_v3(test_array))
            self.assertEqual(result, missing_number_v4(test_array))


if __name__ == '__main__':
    unittest.main()
