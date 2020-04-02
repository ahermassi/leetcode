""" Given a sorted array, two integers k and x, find the k closest elements to x in the array. The result should also
be sorted in ascending order. If there is a tie, the smaller elements are always preferred. """

import unittest2 as unittest


def find_closest_elements_v1(arr, k, x):
    """ The array is sorted. If we want find the one number closest to x, we don't have to check one by one. It's
        straightforward to use binary search.
        The idea is to find the first number which is equal to or greater than x in arr. Then, we determine the
        indices of the start and the end of a sub-array in arr, where the sub-array is our result.
        Assume we are taking A[i] ~ A[i + k], which is a window of size k and our final result.
        We can binary search i. We compare the distance between x - A[mid] and A[mid + k] - x at each step.
        If x - A[mid] > A[mid + k] - x, it means A[mid + 1] ~ A[mid + k] is better than A[mid] ~ A[mid + k],
        so assign left = mid + 1. In other words, if arr[mid] is farther from target than arr[mid + k] which is k
        places ahead of mid, then we need to pull 'left' to (mid + 1); otherwise we can pull 'right' at mid.
        Just think in terms of distance.
        At the end, we'll end up with a window contained by 'left' index which can be the starting index of our
        solution.
        Note that we shouldn't compare the absolute value abs(x - A[mid]) and abs(A[mid + k] - x) because the absolute
        value version does not deal with the cases when x is not between A[mid] and A[mid+k].
        Example: arr = [1, 1, 2, 2, 2, 2, 2, 3, 3]
        In the first run, we will see:
        3 - 2(index 2) > 2(index 5) - 3
        1              >             -1
        This will make left = mid + 1 and start searching in the right part.
        If we use abs, the result would be:
        abs(3 - 2(index 2)) > abs(2(index 5) - 3)
        1                   <= 1
        This will make right = mid and start searching in the left part and ultimately return a wrong answer.
    Time complexity: O(log(N - k) + k)
    Space complexity: O(1)
    """
    left, right = 0, len(arr) - k
    while left < right:
        mid = (left + right) // 2
        if x - arr[mid] > arr[mid + k] - x:
            left = mid + 1
        else:
            right = mid
    return arr[left:left + k]


def find_closest_elements_v2(arr, k, x):
    """ Simpler version without using binary search. Note that we don't need to use abs() because the only case that
        we need to worry about is when x is less than 0th element, but in that case the condition itself is false,
        moving the high pointer down (to finally return arr[:k]).
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, right = 0, len(arr) - 1
    while right - left >= k:
        if x - arr[left] > arr[right] - x:
            left += 1
        else:
            right -= 1
    return arr[left:right + 1]


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5], 4, 3, [1, 2, 3, 4]), ([1, 2, 3, 4, 5], 4, -1, [1, 2, 3, 4])]

    def test_find_closest_elements(self):
        for test_arr, test_k, test_x, result in self.data:
            self.assertEqual(result, find_closest_elements_v1(test_arr, test_k, test_x))
            self.assertEqual(result, find_closest_elements_v2(test_arr, test_k, test_x))


if __name__ == '__main__':
    unittest.main()
