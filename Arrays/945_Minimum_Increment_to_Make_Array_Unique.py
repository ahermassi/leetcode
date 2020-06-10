""" Given an array of integers A, a move consists of choosing any A[i], and incrementing it by 1.
Return the least number of moves to make every value in A unique. """

import unittest2 as unittest


def min_increment_for_unique_v1(A):
    """ The idea is to sort the input array, then we move forward from the beginning of the array till the end.
        As soon as we find a condition that the current element is less than or equal to the previous elements, then we
        need to update the current array element.
        Example: A = [3, 2, 1, 2, 1, 7], sorted A = [1, 1, 2, 2, 3, 7]
        After reaching the second 1 in the array, the condition is satisfied A[i] <= A[i-1], so we need to update A[i]
        by A[i-1] + 1. At the same time we need to keep track of the result: res += A[i-1]+ 1 - A[i]
        The rest of iterations are as follows :
        A = [1, 2, 2, 2, 3, 7], res= 1
        A = [1, 2, 3, 2, 3, 7], res= 2
        A = [1, 2, 3, 4, 3, 7], res= 4
        A = [1, 2, 3, 4, 5, 7], res= 6
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    A.sort()
    res = 0
    for i in range(1, len(A)):
        if A[i] <= A[i - 1]:
            res += A[i - 1] + 1 - A[i]
            A[i] = A[i - 1] + 1
    return res


def min_increment_for_unique_v2(A):
    """ We use bucket sort instead of sorting the input array. Let's count the quantity of each element. Clearly, we
        want to increment the duplicated values.
    Time complexity: O(N)
    Space complexity: O(max(A))
    """
    bucket, res = [0 for _ in range(80000)], 0  # Why 80000? Consider the case in which all the elements are 40000,
    # then we need to increment all of them (except the first one)
    for num in A:
        bucket[num] += 1
    for i in range(len(bucket) - 1):
        if bucket[i] > 1:
            duplicates = bucket[i] - 1
            res += duplicates
            bucket[i + 1] += duplicates  # We propagate the duplicates to the following number and repeat
    return res


class Test(unittest.TestCase):
    data = [([1, 2, 2], 1), ([3, 2, 1, 2, 1, 7], 6)]

    def test_min_increment_for_unique(self):
        for test_a, result in self.data:
            self.assertEqual(result, min_increment_for_unique_v2(test_a))
            self.assertEqual(result, min_increment_for_unique_v1(test_a))


if __name__ == '__main__':
    unittest.main()
