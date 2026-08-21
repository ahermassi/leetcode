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
