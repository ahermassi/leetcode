""" Given an array A of integers and integer K, return the maximum S such that there exists i < j with A[i] + A[j] = S
and S < K. If no i, j exist satisfying this equation, return -1. """

import unittest2 as unittest


def two_sum_less_than_k_v1(A, K):
    """ First, we sort the array. Then we initialize two pointers 'left' and 'right' pointing at the beginning and the
        end of the sorted array.
        Start checking if the current combination satisfies the constraint.
        If the addition >= K, then decrease the right bound and hence tentatively get a smaller addition. Otherwise,
        increase left bound to find a bigger addition.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    A.sort()
    res = -1
    left, right = 0, len(A) - 1
    while left < right:
        s = A[left] + A[right]
        if s < K:  # Candidate found
            res = max(res, s)
            left += 1
        else:
            right -= 1
    return res


def two_sum_less_than_k_v2(A, K):
    """ Since 1 <= A[i] <= 1000, we can apply the counting sort, which takes linear time. Then, we use two indexes to
        search for a pair, like in the solution above.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    bucket = [None] * 1001
    res = -1
    for num in A:
        bucket[num] = num
    left, right = 0, len(bucket) - 1
    while left < right:
        if not bucket[left]:
            left += 1
        elif not bucket[right]:
            right -= 1
        else:
            s = bucket[left] + bucket[right]
            if s < K:
                res = max(res, s)
                left += 1
            else:
                right -= 1
    return res


class Test(unittest.TestCase):
    data = [([34, 23, 1, 24, 75, 33, 54, 8], 60, 58), ([10, 20, 30], 15, -1)]

    def test_two_sum_less_than_k(self):
        for test_a, test_k, result in self.data:
            self.assertEqual(result, two_sum_less_than_k_v1(test_a, test_k))
            self.assertEqual(result, two_sum_less_than_k_v2(test_a, test_k))


if __name__ == '__main__':
    unittest.main()
