""" You are visiting a farm that has a single row of fruit trees arranged from left to right. The trees are represented
by an integer array fruits where fruits[i] is the type of fruit the ith tree produces.

You want to collect as much fruit as possible. However, the owner has some strict rules that you must follow:

You only have two baskets, and each basket can only hold a single type of fruit. There is no limit on the amount of
fruit each basket can hold.
Starting from any tree of your choice, you must pick exactly one fruit from every tree (including the start tree) while
moving to the right. The picked fruits must fit in one of your baskets.
Once you reach a tree with fruit that cannot fit in your baskets, you must stop.
Given the integer array fruits, return the maximum number of fruits you can pick. """

from collections import defaultdict

def total_fruit_v1(fruits):
    """ Pattern: Variable-Size Sliding Window — Longest Valid Window.

        General template:
            1. Expand the right boundary and update the window state.
            2. If the window becomes invalid, shrink from the left until the invariant
               is restored.
            3. Once valid again, update the maximum window length.

        For this problem, the invariant is:
            fruits[left:right+1] contains at most 2 distinct fruit types

        We use a frequency map to represent the current window. As right expands, we
        increment the count of fruits[right].

        If the map contains more than 2 distinct keys, the window is invalid. We then
        move left forward, decrementing the frequency of each fruit that leaves the
        window. When a fruit's count reaches 0, we remove it from the map entirely,
        because len(baskets) is what tells us how many distinct fruit types are
        currently inside the window.

        Once len(baskets) <= 2 again, the invariant has been restored, so the current
        window is a candidate for the longest valid window.

        This is the same longest-valid-window template used in earlier problems; only
        the validity condition and window state change:

            LC 3:    no duplicate characters
            LC 1004: at most k zeros
            LC 904:  at most 2 distinct values

        Each element enters the window once and leaves it at most once.

    Time complexity : O(N)
    Space complexity: O(1), since the map contains at most 3 fruit types during processing before shrinking restores
    the invariant.
    """
    n = len(fruits)
    res = 0
    baskets = defaultdict(int)
    left = right = 0
    while right < n:
        baskets[fruits[right]] += 1
        while len(baskets) > 2:
            baskets[fruits[left]] -= 1
            if baskets[fruits[left]] == 0:
                del baskets[fruits[left]]
            left += 1
        res = max(res, right - left + 1)
        right += 1
    return res

def total_fruit_v2(fruits):
    """ Pattern: Variable-Size Sliding Window — Longest Valid Window.
        Optimization: Compress the window state for the special case of at most
        2 distinct values.

        The standard solution uses a HashMap and the general template:

            expand right
            -> if more than 2 fruit types exist, shrink left until valid
            -> update the longest valid window

        This solution uses the same underlying idea, but exploits the fact that
        the limit is exactly 2 distinct fruit types.

        Suppose the current valid window ends with:

            ... A B B B

        and a new third type C arrives:

            ... A B B B C

        A can no longer belong to a valid window ending at C. The only part of
        the previous window that can survive is the consecutive suffix of B's:

            B B B C

        Therefore, instead of maintaining the entire window, we only need:

            most_recent_type:
                the fruit type at the end of the current sequence

            other_type:
                the other fruit type allowed in the current window

            recent_run_length:
                how many consecutive occurrences of most_recent_type appear
                at the end

            current_length:
                length of the longest valid window ending at the current index

        When the next fruit is one of the two current types, the valid window
        simply grows by 1.

        When a third type appears, the new valid window consists only of:
            trailing run of the previous most_recent_type + the new fruit

        so:
            current_length = recent_run_length + 1

        This is a specialized optimization of the standard longest-valid-window
        template. Instead of explicitly moving a left pointer, we retain only the
        suffix that could possibly remain after a third distinct type appears.

        This trick is specific to "at most 2 distinct values"; the HashMap version
        is the general solution for "at most K distinct values".

    Time complexity : O(N)
    Space complexity: O(1)
    """
    most_recent_type = other_type = None
    recent_run_length = current_length = res = 0
    for fruit in fruits:
        # If this fruit is already one of our two allowed types,
        # the current valid window can simply grow.
        if fruit == most_recent_type or fruit == other_type:
            current_length += 1
        else:
            # A third type appeared. Only the consecutive suffix of the
            # most recent type can be preserved in a valid window.
            current_length = recent_run_length + 1

        if fruit == most_recent_type:
            # Extend the trailing run of the most recent fruit type.
            recent_run_length += 1
        else:
            # A new type is now the most recent one. The previous most
            # recent type becomes the second allowed type.
            other_type = most_recent_type
            most_recent_type = fruit
            recent_run_length = 1
        res = max(res, current_length)
    return res
