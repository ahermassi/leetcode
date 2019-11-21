""" Implement next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers.
If such arrangement is not possible, it must rearrange it as the lowest possible order (ie, sorted in ascending order).
The replacement must be in-place and use only constant extra memory.
"""

import unittest2 as unittest


def next_permutation(nums):
    """ The key insight is that we want to increase the permutation by as little as possible. We will use the
        permutation (6,2,1,5,4,3,0) to develop this approach.
        Specifically, we start from the right, and look at the longest decreasing suffix, which is (5,4,3,0)
        for our example. We cannot get the next permutation just by modifying this suffix, since it is already the
        maximum it can be. Instead, we look at the entry e that appears just before the longest decreasing suffix,
        which is 1 in this case. (If there's no such element, i.e., the longest decreasing suffix is the entire
        permutation, reverse the entire permutation). Observe that e must be less than some entries in the suffix
        (since the entry immediately after e is greater than e). Intuitively, we should swap e with the smallest entry
        s in the suffix which is larger than e so as to minimize the change to the prefix.
        For our example, e is 1 and s is 3. Swapping s and e results in (6,2,3,5,4,1,0)
        We are not done yet - the new prefix is the smallest possible for all permutations greater than the initial
        permutation, but the new suffix may not be the smallest. We can get the smallest suffix by sorting the entries
        in the suffix from smallest to largest. For our working example, this yields the suffix (0,1,4,5).
        As an optimization, it is not necessary to call a full blown sorting algorithm on suffix. Since the suffix was
        initially decreasing, and after replacing s by e it remains decreasing, reversing the suffix has the effect of
        sorting it from smallest to largest.
        Summary:
        The general algorithm for computing the next permutation is as follows:
            1- Find k such that p[k] < p[k+1] and entries after index k appear in decreasing order.
            2- Find the smallest p[l] such that p[l] > p[k] (such an l must exist since p[k] < p[k+1])
            3- Swap p[l] and p[k] (note that the sequence after position k remains in decreasing order).
            4-  Reverse the sequence after position k.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    i = j = len(nums) - 1
    while i > 0 and nums[i-1] >= nums[i]:  # Looking for the longest decreasing suffix
        i -= 1
    if i == 0:  # If the entire sequence is decreasing, then the current permutation is the last in order. Reverse it.
        nums.reverse()
        return nums
    k = i - 1  # This is the index just before the starting index of the longest decreasing suffix
    while nums[j] <= nums[k]:  # Looking for the smallest element greater than the value at k. We want to increase
        # the permutation by as little as possible
        j -= 1
    nums[j], nums[k] = nums[k], nums[j]
    l, r = k + 1, len(nums) - 1
    while l < r:  # Reverse the suffix
        nums[l], nums[r] = nums[r], nums[l]
        l += 1
        r -= 1
    return nums


class Test(unittest.TestCase):
    data = [([1, 2, 3], [1, 3, 2]),
            ([3, 2, 1], [1, 2, 3]),
            ([1, 1, 5], [1, 5, 1])]

    def test_next_permutation(self):
        for test_array, result in self.data:
            self.assertEqual(result, next_permutation(test_array))


if __name__ == '__main__':
    unittest.main()
