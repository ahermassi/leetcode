""" Given a sorted array, two integers k and x, find the k closest elements to x in the array. The result should also
be sorted in ascending order. If there is a tie, the smaller elements are always preferred. """

import unittest2 as unittest


def find_closest_elements_v1(arr, k, x):
    """ Every time a problem involves a sorted array, consider binary search. In the most naive approach, we could
         consider every single number from arr as a potential candidate for the final output. However, when arr.length
         is very large and k is very small, we do not care about a vast majority of the numbers in arr, and we should
         avoid looking at them.

         Let's start by finding the closest number to x in arr. The idea is to find the first number which is equal to or
        greater than x in arr. Then, we determine the indices of the start and the end of a subarray in arr, where the
        subarray is the final result.

         First, what is the biggest index the left boundary of this subarray could have? If there needs to be k elements,
         then the left boundary's upper limit has to be arr.length - k, because if it were any further to the right, we
         would run out of elements to include in the final answer.
         We can then apply binary search on the possible range of indices [0, arr.length-k].

         Let's consider two indices at each binary search operation, the usual mid, and some index mid+k.
         The relationship between these indices is significant because only one of them could possibly be in the final
         answer.

         For example, if mid = 2, and k = 3, then arr[2] and arr[5] could not possibly both be in the answer, since that
         would require taking 4 elements [arr[2], arr[3], arr[4], arr[5]].

         This leads us to the question: How do we move the left and right pointers?

            - If the element arr[mid] is closer to x than arr[mid + k], then that means arr[mid + k], as well as every
               element to the right of it can never be in the answer. This means we should move the right pointer to
               avoid considering them.
            - If arr[mid + k] is closer to x than arr[mid], then move the left pointer forward because every element its
               left can never be in the answer.

        The adjustment of boundaries is only possible because the array is sorted.

        At the end of the binary search, we have located the leftmost index for the final answer. Return the subarray
        starting at this index that contains k elements.

        NOTE: binary search using predicate
        f(mid) = mid is farther from x than mid+k
        -> everything to its left is going to be even farther
        -> [T, T, ..., T, F, F, ..., F]
        -> Find the first F

        x - arr[mid] > arr[mid + k] - x means that arr[mid + 1] ~ arr[mid + k] is "better" than arr[mid] ~ arr[mid+k-1].
        This means we compare below 2 windows to decide which window is "better".

        The only difference between these 2 windows are elements arr[mid] and arr[mid + k], so we only need check which
        is closer to x, so its window would be "better", i.e. all elements are closer to x compared to all elements in
        the other window:

                arr[mid], arr[mid + 1], ..., arr[mid + k - 1]
                              arr[mid + 1], ..., arr[mid + k - 1], arr[mid + k]

        The binary search is comparing the 2 windows starting at mid and mid+1. So we should be able to come to a
        similar implementation by comparing the windows starting at mid and mid-1 (not being done here):

                            arr[mid], ..., arr[mid + k - 2], arr[mid + k - 1]
            arr[mid -1], arr[mid], ..., arr[mid + k - 2]

        So it's crucial to understand that the comparison of arr[mid] and arr[mid+k] is about 2 different windows.

        If arr[mid] is closer to x, then arr[mid+k] can never be in the k length range. So we can confidently remove all
        (arr[mid+1], arr[mid+2], arr[mid+3]...) from the candidates list by setting right = mid.

        If arr[mid + k] is closer to x, then arr[mid] can never be in the k length range. So we can confidently remove
        all (...arr[mid-2], arr[mid-1], arr[mid]) from the candidates list by setting left = mid + 1.

        Note that we shouldn't compare the absolute value abs(x - arr[mid]) and abs(arr[mid + k] - x) because the
        absolute value version does not deal with the cases when x is not between arr[mid] and arr[mid + k].
        Example: arr = [1, 1, 2, 2, 2, 2, 2, 3, 3], x=3, k=3
        In the first iteration:
        3 - 2(index 2) > 2(index 5) - 3
        1              >             -1
        This will make left = mid + 1 and start searching in the right part.
        If we use abs, the result would be:
        abs(3 - 2(index 2)) > abs(2(index 5) - 3)
                   1                 <=            1
        This will make right = mid and start searching in the left part and ultimately return a wrong answer.

    Time complexity: O(log(N-k) + k), although finding the bounds only takes O(log(N−k)) time with the binary search, it
    still costs us O(k) to build the final output.
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
