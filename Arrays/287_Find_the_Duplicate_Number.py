""" Given an array nums containing n + 1 integers where each integer is between 1 and n (inclusive), prove that at
least one duplicate number must exist. Assume that there is only one duplicate number, find the duplicate one. """

import unittest2 as unittest


def find_duplicate_v1(nums):
    """ If the numbers are sorted, then any duplicate numbers will be adjacent in the sorted array.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    nums.sort()
    n = len(nums)
    for i in range(1, n):
        if nums[i] == nums[i - 1]:
            return nums[i]


def find_duplicate_v2(nums):
    """ If we store each element in a set as we iterate over the array, we can simply check each element as we iterate.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)


def find_duplicate_v3(nums):
    """ Floyd's Tortoise and Hare (Cycle Detection).
        Because each number in nums is between 1 and n, it will necessarily point to an index that exists. Therefore,
        the list can be traversed infinitely, which implies that there is a cycle. Additionally, because 0 cannot
        appear as a value in nums, nums[0] cannot be part of the cycle because there is no value in nums that can take
        to 0. Therefore, traversing the array in this manner from nums[0] is equivalent to traversing a cyclic linked
        list. nums[a] = b can be seen as a.next = b
        Note: We need second loop because in first loop both pointers might end up at the same index and hence we will
        get a number which might not be a duplicate. The first loop just gives us the intersection of the indexes, the
        second loop returns the index to the duplicate number.
        According to Floyd's algorithm, first step, if a cycle does exist, and you advance the tortoise one node each
        unit of time but the hare two nodes each unit of time, then they will eventually meet. This is what the first
        while loop does. The first while loop finds their meeting point.
        Second step, take tortoise or hare to the start point of the list (i.e. let one of the animals be 0) and keep
        the other one staying at the meeting point. Now, advance both of the animals one node each unit of time, the
        meeting point is the starting point of the cycle. This is what the second while loop does. The second while
        loop finds their meeting point.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    tortoise = hare = nums[0]  # tortoise = hare = 0 is also correct
    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break
    # Find the entrance to the cycle.
    tortoise = nums[0]  # hare = 0 is also correct
    while tortoise != hare:
        tortoise = nums[tortoise]
        hare = nums[hare]
    return tortoise


def find_duplicate_v4(nums):
    """ This solution uses binary search, based on pigeonhole principle.
        Originally, there are n + 1 objects and n holes, this condition complies to pigeonhole principle, so at least
        one hole has two objects, that is one number appears twice.
        Each time we select a number mid (which is the one in the middle) and count all the numbers equal to or less
        than mid. Then if the count is more than mid, the search space will be [1 .. mid] otherwise [mid+1 .. n]. We do
        this until search space is only one number.
        Or less formally:
        We know that the whole range is 'too crowded' and thus that the first half or the second half of the range is
        too crowded (if both weren't, then neither would be the whole range). So we check to know whether the first
        half is too crowded, and if it isn't, we know that the second half is.
        Note that although the values are not ordered, the INDICES are still ordered. That's why binary search can
        still be used.
        Example: nums = [2, 6, 4, 1, 3, 1, 5]
        left = 1, right = 6 --> mid = 3, count = 4: There are 4 strictly positive integers less than or equal to 3
        --> The duplicate has to be between left and 3
        left = 1, right = 3 --> mid = 2, count = 3: There are 3 strictly positive integers less than or equal to 2
        --> The duplicate has to be between left and 2
        left = 1, right = 2 --> mid = 1, count = 2: There are 2 strictly positive integers less than or equal to 1
        --> The duplicate has to be between left and 1
        left = 1, right = 1: exit and return 1.
    Time complexity: O(N logN)
    Space complexity: O(1)
    """
    left, right = 1, len(nums) - 1  # We use binary search on the range of POSSIBLE numbers, so left starts from 1 not 0
    while left < right:
        mid = (left + right) // 2
        count = sum(num <= mid for num in nums)
        if count <= mid:
            left = mid + 1
        else:
            right = mid
    return left


class Test(unittest.TestCase):
    data = [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3)]

    def test_find_duplicate(self):
        for test_array, result in self.data:
            self.assertEqual(result, find_duplicate_v1(test_array))
            self.assertEqual(result, find_duplicate_v2(test_array))
            self.assertEqual(result, find_duplicate_v3(test_array))


if __name__ == '__main__':
    unittest.main()
