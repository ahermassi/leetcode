""" Given a binary array nums and an integer goal, return the number of non-empty subarrays with a sum goal.
A subarray is a contiguous part of the array. """

from collections import defaultdict
import unittest2 as unittest

def num_subarrays_with_sum_v1(nums, goal):
    """
    Pattern: Prefix Sum + Frequency Map — Count Previous Prefixes.

    Start from the subarray-sum equation.

    Let `running_sum` be the prefix sum from index 0 through the current
    position `right`.

    Suppose some earlier prefix sum was `previous_sum`.

    Then the sum of the subarray between those two prefix boundaries is:

        subarray_sum = running_sum - previous_sum

    We want:

        subarray_sum == goal

    Therefore:

        running_sum - previous_sum = goal

    Rearranging:

        previous_sum = running_sum - goal

    This gives us the key idea:

        At each position, once we know the current `running_sum`, we need to
        know how many PREVIOUS prefix sums were equal to:

            running_sum - goal

        Every such previous prefix identifies one subarray ending at the
        current position whose sum is exactly `goal`.

    ----------------------------------------------------------------------
    State representation
    ----------------------------------------------------------------------

    `counter[prefix_sum]` stores how many times that prefix sum has appeared
    before the current position.

    For each number:

        1. Add it to `running_sum`.
        2. Look for previous prefixes equal to running_sum - goal.
        3. Add their frequency to the result.
        4. Record the current running_sum for future positions.

    The order matters:

        res += counter[running_sum - goal]
        counter[running_sum] += 1

    We must query BEFORE recording the current prefix so that we count only
    prefixes that occurred before the current position.

    ----------------------------------------------------------------------
    Why counter[0] = 1?
    ----------------------------------------------------------------------

    Before processing any elements, conceptually there is one prefix with
    sum 0: the empty prefix before index 0.

    Initializing:

        counter[0] = 1

    allows subarrays starting at index 0 to follow the exact same equation.

    Example:

        nums prefix sum = goal

    Then:

        running_sum - goal = 0

    and the initial zero-prefix contributes one valid subarray.

    This avoids needing a special case such as:

        if running_sum == goal:
            res += 1

    ----------------------------------------------------------------------
    Pattern connection
    ----------------------------------------------------------------------

    This is the general Prefix Sum + Frequency Map counting template:

        derive a relationship between:
            current prefix
            previous prefix
            desired subarray property

        rearrange it to determine:
            which previous prefix value do I need?

        count how many times that value has already appeared.

    Here:

        current_prefix - previous_prefix = goal

    becomes:

        previous_prefix = current_prefix - goal

    This pattern is especially useful for exact subarray-sum problems because
    prefix sums turn a contiguous-range sum into a difference between two
    cumulative states.

    Unlike the sliding-window approach we will consider separately for this
    problem, this prefix-sum technique does not depend on nums being binary or
    non-negative; the same reasoning works even when negative numbers exist.

    Time complexity: O(N), since each element is processed once and each
                     frequency-map lookup/update is O(1) on average.
    Space complexity: O(N), since there can be up to N distinct prefix sums.
    """
    counter = defaultdict(int)
    counter[0] = 1
    running_sum = 0
    res = 0
    for num in nums:
        running_sum += num

        # Any previous prefix with this value creates a subarray ending here
        # whose sum is exactly `goal`.
        res += counter[running_sum - goal]

        # Make the current prefix available to future positions.
        counter[running_sum] += 1

    return res

def num_subarrays_with_sum_v2(nums, goal):
    """
    Pattern: Variable-Size Sliding Window — Count Valid Subarrays
             + Exact = AtMost(goal) - AtMost(goal - 1)

    Start from the difficulty of the original condition:

        We need to count subarrays whose sum is EXACTLY equal to `goal`.

    Sliding window is naturally good at maintaining inequality conditions such as:

        sum <= target

    but exact equality is harder, because a valid window with sum == goal does
    not imply that all of its suffixes also have sum == goal.

    So instead of trying to count exact sums directly, transform the problem:

        exactly(goal)
            = at_most(goal) - at_most(goal - 1)

    Why?

        at_most(goal) contains all subarrays with sums:

            0, 1, 2, ..., goal

        at_most(goal - 1) contains all subarrays with sums:

            0, 1, 2, ..., goal - 1

    Subtracting the two removes everything except the subarrays whose sum is
    exactly `goal`.

    ----------------------------------------------------------------------
    Helper pattern: Count Valid Subarrays Ending at Right
    ----------------------------------------------------------------------

    The helper counts subarrays whose sum is <= target.

    Because nums contains only 0s and 1s, all values are non-negative.

    Therefore:

        - expanding right can only increase or preserve the running sum
        - shrinking left can only decrease or preserve the running sum

    This monotonic behavior makes variable-size sliding window valid.

    `running_sum` represents the sum of nums[left:right+1].

    As right expands:

        running_sum += nums[right]

    If the window becomes invalid:

        running_sum > target

    shrink from the left until:

        running_sum <= target

    At that point, [left, right] is the longest valid window ending at `right`.

    ----------------------------------------------------------------------
    Counting insight
    ----------------------------------------------------------------------

    Once nums[left:right+1] has sum <= target, every suffix of that window
    ending at the same `right` is also valid.

    Since all values are non-negative, removing elements from the left cannot
    increase the sum.

    Therefore, all of these are valid:

        nums[left:right+1]
        nums[left+1:right+1]
        nums[left+2:right+1]
        ...
        nums[right:right+1]

    The number of such subarrays is:

        right - left + 1

    So for each right endpoint:

        res += right - left + 1

    Every valid subarray is counted exactly once, when its right endpoint is
    processed.

    ----------------------------------------------------------------------
    Edge case: target < 0
    ----------------------------------------------------------------------

    Since nums contains only 0s and 1s, every subarray sum is >= 0.

    Therefore:

        at_most(target) = 0    when target < 0

    This matters when:

        goal = 0

    because the formula becomes:

        exactly(0)
            = at_most(0) - at_most(-1)

    and at_most(-1) must simply return 0.

    ----------------------------------------------------------------------
    Pattern connection
    ----------------------------------------------------------------------

    This builds directly on the counting-window pattern from LC 713:

        expand right
        -> while INVALID:
               shrink left
        -> count all valid suffixes ending at right
        -> add right - left + 1

    The new idea here is how to handle an EXACT condition:

        exact value
            -> difference of two monotonic "at most" counts

    Reusable idea:

        When sliding window can efficiently count values satisfying <= X but
        the problem asks for exactly X, check whether:

            exactly(X) = atMost(X) - atMost(X - 1)

        applies.

    This works here because nums is non-negative, which makes the sum monotonic
    as the window expands and shrinks.

    Time complexity: O(N), because each helper moves both left and right only
                     forward, and the helper is called twice.
    Space complexity: O(1).
    """
    n = len(nums)

    def num_subarrays_less_than_or_equal(target):
        if target < 0:
            return 0
        res = 0
        running_sum = 0
        left = right = 0
        while right < n:
            running_sum += nums[right]
            while running_sum > target:
                running_sum -= nums[left]
                left += 1
            # Every suffix of [left, right] ending at `right` is valid.
            res += right - left + 1
            right += 1
        return res

    return num_subarrays_less_than_or_equal(goal) - num_subarrays_less_than_or_equal(goal - 1)
