""" Given an array of integers nums and an integer k, return the number of contiguous sub-arrays where the product of
all the elements in the subarray is strictly less than k.
"""

# Video explanation: https://youtu.be/Cg6_nF7YIks
def num_subarray_product_less_than_k(nums, k):
    """
    Pattern: Variable-Size Sliding Window — Count Valid Subarrays Ending at Right.

    Start from the problem:

        We need to count every contiguous subarray whose product is < k

    The brute-force approach would consider every possible subarray and compute
    its product, leading to O(N^2) work.

    The key property that makes sliding window possible is that nums contains
    only positive integers.

    Therefore:

        - expanding right multiplies the product by a value >= 1, so the
          product cannot decrease

        - shrinking left divides the product by a value >= 1, so the
          product cannot increase

    This gives us a monotonic way to restore validity.

    ----------------------------------------------------------------------
    Sliding Window invariant
    ----------------------------------------------------------------------

    `prod` represents the product of nums[left:right+1].

    As right expands:

        prod *= nums[right]

    If:

        prod >= k

    the current window is invalid, so we shrink from the left until:

        prod < k

    After the shrinking loop finishes, nums[left:right+1] is the longest
    valid window ending at `right`.

    This resembles the Variable-Size Sliding Window — Longest Valid Window
    template:

        expand right
        -> while INVALID:
               shrink left
        -> current window is valid

    However, unlike LC 3 / LC 1004 / LC 904, we are NOT trying to find the
    longest window.

    We want to COUNT all valid subarrays.

    ----------------------------------------------------------------------
    Counting insight
    ----------------------------------------------------------------------

    Once nums[left:right+1] has product < k, every suffix of that window that
    also ends at `right` is valid.

    Why?

    Because all values are positive integers >= 1. Removing elements from the
    left divides the product by values >= 1, so the product cannot increase.

    Therefore, if:

        nums[left:right+1]

    is valid, then all of these are also valid:

        nums[left:right+1]
        nums[left+1:right+1]
        nums[left+2:right+1]
        ...
        nums[right:right+1]

    These are exactly the valid subarrays that END at the current `right`.

    How many are there?

        right - left + 1

    Example:

        current valid window = [10, 5, 2]

    The valid subarrays ending at 2 are:

        [2]
        [5, 2]
        [10, 5, 2]

    There are 3 of them, which is exactly the window length.

    So after restoring a valid window for every right:

        res += right - left + 1

    This does NOT count every subarray inside the current window from scratch.
    It counts only the NEW valid subarrays whose right endpoint is the current
    index.

    Every subarray is therefore counted exactly once: when its right endpoint
    is processed.

    ----------------------------------------------------------------------
    Edge case
    ----------------------------------------------------------------------

    Since every nums[i] >= 1, every non-empty subarray has product >= 1.

    Therefore, if:

        k <= 1

    no valid non-empty subarray can exist.

    ----------------------------------------------------------------------
    Pattern connection
    ----------------------------------------------------------------------

    Variable-Size Sliding Window:

        expand right
        -> while product is invalid:
               shrink left
        -> restore product < k

    New variation — Count Valid Subarrays Ending at Right:

        once [left, right] is valid
        -> every suffix ending at right is also valid
        -> number of new valid subarrays = right - left + 1

    Reusable idea:

        In some counting problems, after restoring a valid sliding window,
        monotonicity may guarantee that every suffix ending at `right` is also
        valid. Instead of enumerating those subarrays, count them directly from
        the window length.

    Time complexity: O(N), because right moves through the array once and left
                     also moves forward at most N times.
    Space complexity: O(1).
    """
    if k <= 1:
        return 0
    n, res = len(nums), 0
    prod = 1
    left = right = 0
    while right < n:

        # Expand the window.
        prod *= nums[right]

        # Restore the invariant: product of the current window must be < k.
        while prod >= k:
            prod //= nums[left]
            left += 1

        # Every suffix of the valid window ending at `right` is also valid.
        res += right - left + 1

        right += 1

    return res
