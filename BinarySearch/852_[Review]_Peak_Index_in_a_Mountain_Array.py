import unittest2 as unittest


def peak_index_in_mountain_array_v1(arr):
    """ The mountain increases until it doesn't. The point at which it stops increasing is the peak.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    for i in range(len(arr)):
        if arr[i] > arr[i + 1]:
            return i


def peak_index_in_mountain_array_v2(arr):
    """ We can view the mountain array as two regions:

        increasing slope | decreasing slope

        For example:

            arr = [0, 2, 5, 7, 6, 3, 1]
                            ^
                           peak

        A useful way to connect this to our standard boundary-search template is
        to define the predicate:

            P(i) = arr[i] > arr[i + 1]

        In a valid mountain array, this produces:

            arr:   0  2  5  7  6  3  1
            P(i):  F  F  F  T  T  T
                            ^
                         first T
                         = peak

        Before the peak, every element is smaller than the element to its right,
        so P(i) is False.

        At the peak, the slope changes from increasing to decreasing:

            arr[peak] > arr[peak + 1]

        so the peak is exactly the first index where P(i) becomes True.

        This is therefore the familiar F F F T T T boundary-search template.

        We maintain the invariant that [left, right] always contains the peak
        and use `while left < right` because this is candidate convergence:

            many candidates -> fewer candidates -> one candidate

        When left == right, exactly one candidate remains, so that index is
        the peak.

        At each step:

        1- arr[mid] < arr[mid + 1]

            We are still on the increasing slope:

                ... 2, 5, 7, ...
                       M  M+1

            P(mid) is False, so mid cannot be the first True / peak.

            The peak must be strictly to the right:

                left = mid + 1

        2- arr[mid] > arr[mid + 1]

            We are on the decreasing slope:

                ... 7, 5, 3, ...
                    M  M+1

            P(mid) is True.

            mid could be the FIRST True, meaning mid itself could be the peak,
            so we must keep it:

                right = mid

        This follows the general binary-search rule:

            Can mid still be the answer?

                No  -> discard mid
                Yes -> keep mid

        Mental model:

            uphill   -> False -> peak strictly right -> left = mid + 1
            downhill -> True  -> peak at mid or left -> right = mid

        Important distinction:

        The F F F T T T interpretation applies because this problem guarantees
        a true mountain array: one increasing sequence followed by one decreasing
        sequence.

        For a general array with multiple local peaks, the predicate

            P(i) = arr[i] > arr[i + 1]

        is NOT necessarily monotonic.

        For example:

            [1, 3, 2, 5, 4]

        produces:

            F, T, F, T

        So a general "find any peak" problem is not literally a first-True
        boundary search.

        Binary search still works there for a different reason:

            arr[mid] < arr[mid + 1]
                -> following the uphill direction guarantees that SOME peak
                   exists to the right

            arr[mid] > arr[mid + 1]
                -> SOME peak exists at mid or to the left

        The mountain-array version is special because its single rise-then-fall
        shape turns that same slope test into a true monotonic F F F T T T boundary.

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left


class Test(unittest.TestCase):
    data = [([0, 1, 0], 1),
            ([0, 2, 1, 0], 1)
            ]

    def test_peak_index_in_mountain_array_(self):
        for test_array, result in self.data:
            self.assertEqual(result, peak_index_in_mountain_array_v1(test_array))
            self.assertEqual(result, peak_index_in_mountain_array_v2(test_array))


if __name__ == '__main__':
    unittest.main()
