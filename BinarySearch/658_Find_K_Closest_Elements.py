""" Given a sorted array, two integers k and x, find the k closest elements to x in the array. The result should also
be sorted in ascending order. If there is a tie, the smaller elements are always preferred. """

import unittest2 as unittest


def find_closest_elements_v1(arr, k, x):
    """ The array is sorted. If we want find the one number closest to x, we don't have to check one by one. It's
        straightforward to use binary search.
        The idea is to find the first number which is equal to or greater than x in arr. Then, we determine the
        indices of the start and the end of a sub-array in arr, where the sub-array is our result.
        First of all, what is the biggest index the left bound could be? If there needs to be k elements, then the left
        bound's upper limit is arr.length - k, because if it were any further to the right, we would run out of
        elements to include in the final answer. We can apply binary search in a unique way to move our left and right
        pointers closer and closer to the left bound of our answer.
        Let's consider two indices at each binary search operation, the usual mid, and some index (mid + k). The
        relationship between these indices is significant because only one of them could possibly be in a final answer.
        For example, if mid = 2, and k = 3, then A[2] and A[5] could not possibly both be in the answer, since that
        would require taking 4 elements [A[2], A[3], A[4], A[5]].
        This leads us to the question: How do we move our pointers left and right? If the element at A[mid] is closer
        to x than A[mid + k], then that means A[mid + k], as well as every element to the right of it can never be
        in the answer. This means we should move our right pointer to avoid considering them. The logic is the same
        vice-versa - if A[mid + k] is closer to x, then move the left pointer.
        At the end of the binary search, we have located the leftmost index for the final answer. Return the sub-array
        starting at this index that contains k elements.
        If x - A[mid] > A[mid + k] - x, it means that A[mid + 1] ~ A[mid + k] is better than
        A[mid] ~ A[mid + k - 1]. This means we compare below 2 windows to decide which window is 'better'.
        The only difference between these 2 windows are element A[mid] and A[mid + k], so we only need check who
        is closer to x, so its window would be 'better', i.e. all elements are closer to x compared to all elements in
        the other window:

            A[mid], A[mid + 1], ..., A[mid + k - 1]
                    A[mid + 1], ..., A[mid + k - 1], A[mid + k]

        The above solution is comparing the 2 windows, starting at mid and (mid + 1). So we should be able to come to a
        similar implementation by comparing the windows starting at mid and (mid - 1) (not being done here):

                       A[mid], ..., A[mid + k - 1], A[mid + k - 1]
            A[mid -1], A[mid], ..., A[mid + k - 2]

        So it's crucial to understand that the comparison of A[mid] and A[mid + k] is about 2 different windows.
        If A[mid] is closer to x, then A[mid + k] can never be in the k length range. So we can confidently remove all
        (A[mid+1], A[mid+2], A[mid+3]...) from the candidates list by setting right = mid.
        If A[mid + k] is closer to x, then A[mid] can never be in the k length range. So we can confidently remove all
        (...A[mid-2], A[mid-1], A[mid]) from the candidates list by setting left = mid + 1.
        Note that we shouldn't compare the absolute value abs(x - A[mid]) and abs(A[mid + k] - x) because the absolute
        value version does not deal with the cases when x is not between A[mid] and A[mid + k].
        Example: arr = [1, 1, 2, 2, 2, 2, 2, 3, 3], x=3, k=3
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
