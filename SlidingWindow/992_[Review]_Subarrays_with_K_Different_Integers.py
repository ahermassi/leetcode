""" Given an integer array nums and an integer k, return the number of good subarrays of nums.

A good array is an array where the number of different integers in that array is exactly k.

For example, [1,2,3,1,2] has 3 different integers: 1, 2, and 3.
A subarray is a contiguous part of an array. """

from collections import defaultdict

def subarrays_with_k_distinct(nums, k):
    """
    Pattern: Variable-Size Sliding Window — Count Valid Subarrays
             + Exactly(K) = AtMost(K) - AtMost(K - 1).

    Start from the original requirement:

        Count subarrays containing exactly k distinct integers.

    The difficulty is that sliding window naturally works well with monotonic
    conditions such as:

        at most k distinct integers

    but "exactly k" is not directly monotonic.

    Suppose [left, right] contains exactly k distinct integers. Not every suffix
    ending at `right` is guaranteed to still contain exactly k distinct values,
    so we cannot simply add:

        right - left + 1

    Example:

        nums = [1, 2, 1, 2], k = 2

    For right at the last element, the suffixes are:

        [2]          -> 1 distinct
        [1, 2]       -> 2 distinct
        [2, 1, 2]    -> 2 distinct
        [1, 2, 1, 2] -> 2 distinct

    So counting every suffix would overcount.

    ----------------------------------------------------------------------
    Transformation: Exactly(K) from AtMost(K)
    ----------------------------------------------------------------------

    Instead of counting exactly k distinct values directly, use:

        exactly(k) = atMost(k) - atMost(k - 1)

    Why?

        atMost(k)

    counts every subarray containing:

        0, 1, 2, ..., k distinct values

    while:

        atMost(k - 1)

    counts every subarray containing:

        0, 1, 2, ..., k - 1 distinct values

    Subtracting them leaves only the subarrays containing exactly k distinct
    integers.

    ----------------------------------------------------------------------
    Helper pattern: Count Valid Subarrays Ending at Right
    ----------------------------------------------------------------------

    `subarrays_distinct_at_most(limit)` counts subarrays containing at most
    `limit` distinct integers.

    `counter` stores the frequencies of the integers currently inside
    nums[left:right+1].

    As right expands:

        counter[nums[right]] += 1

    If the number of distinct integers becomes greater than `limit`, the
    window is invalid:

        len(counter) > limit

    We then shrink from the left until the invariant is restored.

    When a frequency reaches 0, that integer no longer exists in the current
    window, so its key must be deleted from `counter`.

    After shrinking:

        len(counter) <= limit

    and nums[left:right+1] is the longest valid window ending at `right`.

    ----------------------------------------------------------------------
    Counting insight
    ----------------------------------------------------------------------

    Once [left, right] contains at most `limit` distinct integers, every suffix
    ending at the same `right` also contains at most `limit` distinct values.

    Removing elements from the left can only preserve or REDUCE the number of
    distinct integers; it can never introduce a new one.

    Therefore, all of these are valid:

        nums[left:right+1]
        nums[left+1:right+1]
        nums[left+2:right+1]
        ...
        nums[right:right+1]

    The number of valid subarrays ending at this `right` is exactly:

        right - left + 1

    So for every right endpoint:

        res += right - left + 1

    Each valid subarray is counted exactly once, when its right endpoint is
    processed.

    ----------------------------------------------------------------------
    Pattern connection
    ----------------------------------------------------------------------

    Variable-Size Sliding Window — Count Valid Subarrays:

        expand right
        -> while INVALID:
               shrink left
        -> once valid:
               every suffix ending at right is also valid
               add right - left + 1

    Exact-condition transformation:

        exactly(k) = atMost(k) - atMost(k - 1)

    This is the same transformation used in LC 930:

        LC 930:
            exactly(goal sum) = atMost(goal) - atMost(goal - 1)

        LC 992:
            exactly(k distinct) = atMost(k distinct) - atMost(k - 1 distinct)

    Reusable idea:

        When an exact condition is difficult to count directly, check whether
        it can be expressed as the difference between two monotonic "at most"
        conditions that sliding window can count efficiently.

    Time complexity: O(N), because each helper moves both `left` and `right`
                     only forward, and the helper is called twice.
    Space complexity: O(N) in the general case for the frequency map.
    """
    n = len(nums)

    def subarrays_distinct_at_most(limit):
        counter = defaultdict(int)
        res = 0
        left = right = 0
        while right < n:
            counter[nums[right]] += 1
            while len(counter) > limit:
                counter[nums[left]] -= 1
                if counter[nums[left]] == 0:
                    del counter[nums[left]]
                left += 1
            # Every suffix of [left, right] ending at `right` is valid.
            res += right - left + 1
            right += 1
        return res

    return subarrays_distinct_at_most(k) - subarrays_distinct_at_most(k - 1)
