""" Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? Find all unique
triplets in the array which gives the sum of zero.
Note:
The solution set must not contain duplicate triplets. """

import unittest2 as unittest


# Video explanation: https://youtu.be/jzZsG8n2R9A
def three_sum_v1(nums):
    """ We follow the same two pointers pattern as in other similar sum problems. It requires the array to be sorted, so
         we do that first.

         To make sure the result contains unique triplets, we need to skip duplicate values. It is easy to do because
         repeating values are next to each other in a sorted array.

        To find the combinations of 3 numbers, we iterate over the array with the first pointer. The other two pointers
        are initially set to the first and the last element respectively. We compare the sum of the three elements to
        0. If it is smaller, we increment the lower pointer. Otherwise, we decrement the higher pointer. Thus, the sum
        always moves towards 0, and we "prune" pairs that would move it further away. Again, this works only if the
        array is sorted.

        We do not need to consider i after nums[i] > 0, since sum of 3 positives will be always greater than zero. [1]

        If the number is the same as the number before, then it is equivalent to repeating the previous calculation. [2]

        Now we calculate the total:

            - If the total is less than zero, we need it to be larger, so we move the left pointer
            - If the total is greater than zero, we need it to be smaller, so we move the right pointer
            - If the total is zero, bingo! [5]

            We need to move the left (and right, but not necessarily) pointers to the next different numbers, so we do
            not get duplicate results [3], [4]

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
                # while left < right and nums[right] == nums[right-1]:  # [4]
                #     right -= 1
                left += 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return res


def three_sum_v2(nums):
    """ Since triplets must sum up to the target value, we can try the hashmap approach from the Two Sum solution.

         We move the pivot element nums[i] and analyze elements to its right. We find all pairs whose sum is equal
         to -nums[i] using the Two Sum: One-pass Hash Table approach, so that the sum of the pivot element (nums[i])
         and the pair is equal to zero. Note that in this implementation we use a hash set instead of a hashmap since we
         don't need to store the index information.

         To do that, we process each element nums[j] to the right of the pivot and check whether a complement
         -(nums[i] + nums[j]) is already in the hashset. If it is, we found a triplet. Then, we add nums[j] to the
         hashset so it can be used as a complement from that point on.

         Like in the previous approach, we also sort the array so we can skip duplicate values.

    Time complexity: O(N logN + N^2) = O(N^2)
    Space complexity: O(N)
    """

    def twoSum(left, right, target):
        seen = set()
        while left <= right:
            complement = target - nums[left]
            if target - nums[left] in seen:
                res.append([-target, complement, nums[left]])
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
            seen.add(nums[left])
            left += 1

    nums.sort()
    n, res = len(nums), []
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        a = nums[i]
        # Find a pair of numbers (b, c) in [i + 1, n - 1] whose sum is equal to -a
        twoSum(i + 1, n - 1, -a)
    return res


def three_sum_v3(nums):
    """ What if we cannot modify the input array, and we want to avoid copying it due to memory constraints?
         We can adapt the hashset approach to work for an unsorted array.

            - We add the result triplets to a hashset to avoid duplicates.

            - Values in a triplet should be ordered (e.g. ascending). Otherwise, we would have results with the same
               values in the different positions.

            - We also use another 'start_of_triplet' hashset to skip duplicates in the outer loop.

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    def twoSum(left, right, target):
        seen = set()
        while left <= right:
            complement = target - nums[left]
            if target - nums[left] in seen:
                res.append(tuple(sorted([-target, complement, nums[left]])))
            seen.add(nums[left])
            left += 1

    n, res = len(nums), set()
    start_of_triplet = set()
    for i in range(n - 2):
        if nums[i] in start_of_triplet:
            continue
        a = nums[i]
        start_of_triplet.add(a)
        # Find a pair of numbers (b, c) in [i + 1, n - 1] whose sum is equal to -a
        twoSum(i + 1, n - 1, -a)
    return map(list, res)


class Test(unittest.TestCase):
    data = [([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]])]

    def test_three_sum(self):
        for test_array, result in self.data:
            self.assertEqual(result, three_sum_v1(test_array))
            self.assertEqual(result, three_sum_v2(test_array))
            self.assertEqual(result, three_sum_v3(test_array))


if __name__ == '__main__':
    unittest.main()
