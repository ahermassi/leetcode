""" Given an array of integers that is already sorted in ascending order, find two numbers such that they add up to a
specific target number.
Your returned answers (both index1 and index2) are not zero-based.
"""

import unittest2 as unittest


def two_sum_v1(numbers, target):
    """ While we iterate and insert elements into the hash table, we also look back to check if current element's
        complement already exists in the hash table. If it exists, we found a solution and return immediately.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    indices = {}
    for i, val in enumerate(numbers, 1):  # enumerate(numbers, 1) to account for 1-based indexing
        if target - val in indices:
            return [indices[target - val], i]
        indices[val] = i


def two_sum_v2(numbers, target):
    """ Make use of the property that the input array is sorted. We use two indices, initially pointing to the first
        and last element, respectively. Compare the sum of these two elements with target. If the sum is equal to
        target, we found the solution. If it is less than target, we increase the smaller index by one. If it is
        greater than target, we decrease the larger index by one. Move the indices and repeat the comparison until the
        solution is found.

    Time complexity: O(N), each of the N elements is visited at most once
    Space complexity: O(1)
    """
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]
        if s < target:
            left += 1
        else:
            right -= 1


def two_sum_v3(numbers, target):
    """ For each element x in the array, try to find its complement (target - x) using binary search.
    Time complexity: O(N logN), array pass + binary search
    Space complexity: O(1)
    """
    n = len(numbers)
    for i in range(n):
        left, right = i + 1, n - 1
        temp = target - numbers[i]
        while left <= right:
            mid = (left + right) // 2
            if numbers[mid] == temp:
                return [i + 1, mid + 1]
            if numbers[mid] < temp:
                left = mid + 1
            else:
                right = mid - 1


class Test(unittest.TestCase):
    data = [([2, 7, 11, 15], 9, [1, 2])]

    def test_two_sum(self):
        for test_numbers, test_target, result in self.data:
            self.assertEqual(result, two_sum_v1(test_numbers, test_target))
            self.assertEqual(result, two_sum_v2(test_numbers, test_target))
            self.assertEqual(result, two_sum_v2(test_numbers, test_target))


if __name__ == '__main__':
    unittest.main()
