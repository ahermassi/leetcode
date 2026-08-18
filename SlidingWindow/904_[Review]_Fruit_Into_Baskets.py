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

def total_fruit(fruits):
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
