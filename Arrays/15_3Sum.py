""" Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? Find all unique
triplets in the array which gives the sum of zero.
Note:
The solution set must not contain duplicate triplets. """

import unittest2 as unittest


def three_sum_v1(nums):
    """ We will follow the same two pointers pattern as in other similar sum problems. It requires the array to be
        sorted, so we'll do that first. To make sure the result contains unique triplets, we need to skip duplicate
        values. It is easy to do because repeating values are next to each other in a sorted array.

        To find the combinations of 3 numbers, we iterate over the array with the first pointer. The other two pointers
        are initially set to the first and the last element respectively. We compare the sum of the three elements to
        0. If it is smaller, we increment the lower pointer. Otherwise, we decrement the higher pointer. Thus, the sum
        always moves towards 0, and we "prune" pairs that would move it further away. Again, this works only if the
        array is sorted.

        We do not need to consider i after nums[i] > 0, since sum of 3 positives will be always greater than zero. [1]

        If the number is the same as the number before, then it is equivalent to repeating the previous calculation. [2]

        Now we calculate the total:
            If the total is less than zero, we need it to be larger, so we move the left pointer
            If the total is greater than zero, we need it to be smaller, so we move the right pointer
            If the total is zero, bingo! [5]

            We need to move the left and right pointers to the next different numbers, so we do not get duplicate results
            [3], [4]

    Time complexity: O(N logN + (N^2)) ~= O(N^2)
    Space complexity: O(N), for the sort
    """
    nums.sort()
    n, res = len(nums), []
    for i in range(n - 2):
        if nums[i] > 0:  # [1]
            break
        if i > 0 and nums[i] == nums[i-1]:  # [2]
            continue
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                res.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]:  # [3]
                    left += 1
                while left < right and nums[right] == nums[right-1]:  # [4]
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return res


def three_sum_v2(nums):
    """ Since triplets must sum up to the target value, we can try the hash table approach from the Two Sum solution.

        We move our pivot element nums[i] and analyze elements to its right. We find all pairs whose sum is equal
        -nums[i] using the Two Sum: One-pass Hash Table approach, so that the sum of the pivot element (nums[i])
        and the pair (-nums[i]) is equal to zero.

        To do that, we process each element nums[j] to the right of the pivot, and check whether a complement
        -(nums[i] + nums[j]) is already in the hashset. If it is, we found a triplet. Then, we add nums[j] to the
        hashset, so it can be used as a complement from that point on.

        Like in the previous approach, we will also sort the array, so we can skip repeated values.

    Time complexity: O(N logN + N^2) = O(N^2)
    Space complexity: O(N)
    """
    nums.sort()
    n, res = len(nums), []
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        a = nums[i]
        j = i + 1
        seen = set()
        while j < n:
            b = nums[j]
            c = - (a + b)
            if c in seen:
                res.append([a, b, c])
                # Increment j while the next value is the same as before to avoid duplicates in the result
                while j < n - 1 and nums[j] == nums[j + 1]:
                    j += 1
            seen.add(b)
            j += 1
    return res


class Test(unittest.TestCase):
    data = [([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]])]

    def test_three_sum(self):
        for test_array, result in self.data:
            self.assertEqual(result, three_sum_v1(test_array))
            self.assertEqual(result, three_sum_v2(test_array))


if __name__ == '__main__':
    unittest.main()
