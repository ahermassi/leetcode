""" Given a sorted array, two integers k and x, find the k closest elements to x in the array. The result should also
be sorted in ascending order. If there is a tie, the smaller elements are always preferred. """

import unittest2 as unittest


def find_closest_elements_v1(arr, k, x):
    """ The logic for this problem would dwell down to finding k elements by finding the starting element. So find the
        first index i so that arr[i] is better than arr[i+k] (with "better" we mean closer to or equally close to x).
        If the starting element is found, [i, i+k] elements can be returned.
        Given that k < len(arr); we can always use the 'right' index as length(arr)-k and 'left' as 0.
        Consider binary search paradigm:
        If arr[mid] is farther from target than arr[mid+k] which is k places ahead of mid, then we need to pull 'left'
        to mid with 1 offset; otherwise we can pull 'right' at mid. Just think in terms of distance and don't assume
        one is gonna be larger or smaller than the other. No assumption like that is made.
        At the end, we'll end up with a value contained by 'left' index which can be the starting index of our solution.
        Note that we shouldn't compare the absolute value abs(x - A[mid]) and abs(A[mid + k] - x) because the absolute
        value version does not deal with the cases when x is not between A[mid] and A[mid+k].
        Example: arr = [1, 2, 3, 4, 5], k = 4, x = -1; x is not in arr.
        The magic of this solution is about binary search which is used here to find the best left index rather than
        finding the closest element to x
    Time complexity: O(log(N - k))
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
