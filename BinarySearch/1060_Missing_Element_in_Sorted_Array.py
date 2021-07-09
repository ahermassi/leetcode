""" Given a sorted array A of unique numbers, find the K-th missing number starting from the leftmost number of the
array. """

import unittest2 as unittest


def missing_element_v1(nums, k):
    """ Linearly scan the array and use a variable 'missing' to calculate the number of missing numbers between the
        previous index and the current index.
            1- If missing >= k, return previous index's value + k
            2- Otherwise, subtract 'missing' from k to discard the previous missing numbers and continue
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    for i in range(1, n):
        missing = nums[i] - nums[i - 1] - 1  # The key is to understand that the number of the missing numbers between
        # nums[left] and nums[right] is (nums[right] - nums[left] + 1) - (right - left + 1)
        # = (nums[right] - nums[left]) - (right - left)
        # = number of values in the interval if no element was missing - interval length
        # Therefore, missing = (nums[i] - nums[i-1] + 1) - (i - (i - 1) + 1)
        #                    = (nums[i] - nums[i-1] + 1) - 2
        #                    =  nums[i] - nums[i-1] - 1
        if missing >= k:
            return nums[i - 1] + k
        k -= missing
    return nums[-1] + k


def missing_element_v2(nums, k):
    """ We can replace the linear search by a binary search. Let's first assume that we have a function missing(idx)
        that returns how many numbers are missing until the element at index 'idx'. The key insight is that
        missing(idx) produces a sorted array if applied to all the indices of 'nums'. We exploit this property to use
        binary search.
        The idea is to find the leftmost index such that:

            missing(idx - 1) < k <= missing(idx).

        In other words, that means that kth missing number is between nums[idx - 1] and nums[idx]. Therefore, we can
        return kth missing:

            kth missing = nums[idx - 1] + k - missing(idx - 1)

        Let's consider an array element at index 'idx'. If there is no numbers missing, the element should be equal to
        nums[idx] = nums[0] + idx. If k numbers are missing, the element should be equal to
        nums[idx] = nums[0] + idx + k. Hence the number of missing elements from the beginning of nums up to 'idx'
        is equal to:

            missing = nums[idx] - nums[0] - idx

        Without loss of generality, the number of missing elements between two indices 'left' and 'right' is equal to:

            missing = (nums[right] - nums[left]) - (right - left)

        Let 'missing' be the number of missing values in the entire array. Two cases need to be handled:
            1- missing < k, then return nums[-1] + k - missing
            2- missing >= k, then use binary search to find the index in the array where the kth missing number will be
               located. This index verifies:
                    nums[index] < missing number <= nums[index + 1]
               in which case return nums[index] + k

        Notes:
        Why do we do right = mid if missing == k ?
        Let's say at index i we have 3 missing numbers and are looking for the 3rd missing, meaning missing == k.
        If you think about it, this still means that our missing number is on the left side and therefore we can limit
        our search to the left side of mid.
        What happens after the binary search ends?
        Because of our termination condition (left + 1 < right), we will end up with a range of length 2. In other
        words, 'left' and 'right' are going to be adjacent to each other and mark the start and end of our range.
        So we can use 'left' (or even 'right' if we want) to calculate the final answer.
        Why don't we use (right = mid - 1) and (left = mid + 1) ?
        Because at each iteration we don't have enough information to decide whether we should remove 'mid' or not.
        No matter if missing(mid) > k or missing(mid) < k or missing(mid) == k, the element 'mid' itself might still
        end up being your 'left' or 'right'.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    n = len(nums)
    missing = (nums[-1] - nums[0] + 1) - n
    if k > missing:
        return nums[-1] + k - missing
    left, right = 0, n - 1
    while left + 1 < right:  # This guarantees we stop when the interval length is 2 and 'left' is the sought index
        mid = (left + right) // 2
        missing = nums[mid] - nums[left] - (mid - left)
        # In fact, missing = number of values in the interval if no element was missing - interval length
        #                  = (nums[mid] - nums[left] + 1) - (mid - left + 1)
        #                  = nums[mid] - nums[left] - (mid - left)
        if missing < k:  # If at this index we have, for example, 2 missing numbers and we're looking for the 3rd
            # missing. We know that our range should be the upper half.
            k -= missing
            left = mid
        else:  # If at this index we have, for example, 5 missing numbers and we're looking for the 3rd missing. We know
            # that our range should be the lower half.
            right = mid  # When 'missing' is larger than k, then the index won't be located in [mid + 1, right]
    return nums[left] + k


class Test(unittest.TestCase):
    data = [([4, 7, 9, 10], 1, 5), ([4, 7, 9, 10], 3, 8), ([1, 2, 4], 3, 6)]

    def test_missing_element(self):
        for test_nums, test_k, result in self.data:
            self.assertEqual(result, missing_element_v1(test_nums, test_k))
            self.assertEqual(result, missing_element_v2(test_nums, test_k))


if __name__ == '__main__':
    unittest.main()
