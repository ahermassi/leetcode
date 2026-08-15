""" A peak element is an element that is greater than its neighbors.
Given an input array nums, where nums[i] ≠ nums[i+1], find a peak element and return its index.
The array may contain multiple peaks, in that case return the index to any one of the peaks is fine. """

# Some useful templates
# https://leetcode.com/problems/find-peak-element/discuss/788474/General-Binary-Search-Thought-Process-%3A-4-Templates


def find_peak_element_v1(nums):
    """ Linear scan.

         In this approach, we make use of the fact that two consecutive numbers nums[i] and nums[i+1] are never equal.
         Thus, we can traverse the nums array starting from the beginning. Whenever we find a number nums[i], we only
         need to check if it is larger than the next number nums[i+1] to determine if nums[i] is the peak element.

            - Case 1: all the numbers appear in ascending order. In this case, we keep on comparing nums[i] with
               nums[i+1] to determine if nums[i] is the peak element. None of the elements satisfies the criteria,
               indicating that we are currently on a rising slope and not on a peak. Thus, at the end, we need to return
               the last element as the peak element, which turns out to be correct (because nums[n] = -∞). In this case
               also, we need not compare nums[i] with nums[i−1].

            - Case 2: all the numbers appear in descending order. In this case, the first element corresponds to the
               peak. We start off by checking if the current element is larger than the next one. The first element
               satisfies the criteria, and is hence identified as the peak correctly. In this case too, we didn't reach
               a point where we needed to compare nums[i] with nums[i−1].

            - Case 3: the peak appears somewhere in the middle. In this case, when we are traversing the rising slope,
               as in case 1, none of the elements satisfies nums[i] > nums[i+1]. We don't need to compare nums[i] with
               nums[i-1] on the rising slope as discussed above. When we finally reach the peak element, the condition
               nums[i] > nums[i+1] is satisfied. We again don't need to compare nums[i] with nums[i-1]. This is because
               we could reach the current nums[i] only when the check nums[i] > nums[i+1] failed for the previous
               (i−1)th element.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    for i in range(n-1):
        if nums[i] > nums[i + 1]:
            return i
    return n - 1


def find_peak_element_v2(nums):
    """ We can think of the array as a sequence of rising and falling slopes.

        We do NOT need to find the global maximum. We only need to find ANY local peak.
        That is what makes binary search possible.

        This is a boundary / candidate-convergence style binary search:

            while left < right

        The invariant is:

            [left, right] always contains at least one peak.

        We keep shrinking that interval until only one candidate remains.
        When left == right, that index must be a peak.

        At each step, compare nums[mid] with nums[mid + 1]:

        1- nums[mid] < nums[mid + 1]

            Example:

                ... 2, 3, 5, 7, ...
                       M  M+1

            We are on a rising slope.

            If we continue moving right:

                - either the values eventually stop increasing and start decreasing,
                  in which case the turning point is a peak,

                - or the values keep increasing all the way to the end of the array,
                  in which case the last element is a peak because the problem defines
                  nums[n] = -infinity.

            Therefore, at least one peak must exist strictly to the right of mid.

            mid itself cannot be the peak because nums[mid + 1] > nums[mid], so we
            can safely discard it:

                left = mid + 1


        2- nums[mid] > nums[mid + 1]

            Example:

                ... 7, 5, 3, 2, ...
                     M  M+1

            We are on a falling slope.
            This means a peak exists at mid or somewhere to its left.

            mid itself could already be a peak, so we must keep it:

                right = mid

            This follows the same general binary-search rule:

                If mid can still be the answer, do NOT discard it.


        Why `while left < right`?

            This is not an exact-target search.

            We maintain the guarantee that [left, right] contains a peak and keep
            shrinking the candidate interval:

                many candidates
                    ->
                fewer candidates
                    ->
                one candidate

            Once left == right, exactly one candidate remains, so we stop and
            return that index.

        Why is nums[mid + 1] always safe to access?

            The loop only runs while:

                left < right

            Therefore mid is always strictly less than right, so mid + 1 is always
            a valid index.

        Why does a peak always exist?

            The problem lets us imagine:

                nums[-1] = nums[n] = -infinity

            Therefore, if we keep following an increasing slope, one of two things
            must eventually happen:

                - the slope turns downward -> we found a local peak
                - it reaches the end       -> the last element is a peak

            The same reasoning applies when following a falling slope toward the left.

        So the mental model is simply:

            nums[mid] < nums[mid + 1]
                -> uphill
                -> a peak exists strictly right
                -> discard mid
                -> left = mid + 1

            nums[mid] > nums[mid + 1]
                -> downhill
                -> a peak exists at mid or left
                -> keep mid
                -> right = mid

        In other words:

            Follow the slope uphill.
            A peak is guaranteed to be waiting in that direction.

        Example:
        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|
        | l | _ | _ | _ | m | _ | _ | _ | r    |
        nums[mid] > nums[mid+1] -> r=mid (not mid-1 since mid can be the answer)

        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|
        | l | _ | m | _ | r | X | X | X | X   |
        nums[mid] < nums[m+1] -> l = mid+1 (since nums[mid] < nums[mid+1], mid can't be the answer)

        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|
        | X | X | X |l,m | r | X | X | X | X|
        nums[mid] < nums[m+1] -> l = mid+1 (since nums[mid] < nums[mid+1], mid can't be the answer)

        | 1 | 2 | 3 | 4 | 5   | 4 | 3 | 2 | 1 |
        |---|---|---|---|-----|---|---|
        | X | X | X | X | l,r | X | X | X | X |
        l=5 is the answer

                 5   5                            5
                / \ / \                         / \
               4   4   4                       4  -∞
              /          \                      /
             3           3           3        3
            /             \         / \      /
           2               2       2   2   2
          /                 \     /      \ /
        -∞                 1   1       1
                               \ /
                                0
        0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19   (indices)
        2, 3, 4, 5, 4, 5, 4, 3, 2, 1, 0,  1,  2,  3,  2,  1,  2,  3,  4,  5    (nums)
        l                                   m                                              r     l=0, r=19, m=9
        l               m                 r                                                      l=0, r=9, m=4
                            l      m      r                                                      l=5, r=9, m=7
                            l  m r                                                               l=5, r=7, m=6
                      m=l  r                                                                    l=5, r=6, m=5
                  r=m=l                                                                       l=5, r=5, m=5
        peak = nums[l] = nums[5] = 5

    Time complexity: (logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return right


# NOTE: binary search using a predicate

# f(mid) = nums[mid] < nums[mid + 1]
# -> [T, T,...,T, F, F,..., F]
# Find the first F
# That's the reason if nums[mid] < target we completely discard [left, mid] because it's filled with T's.
# HOWEVER, this binary search case requires the existence of at least TWO ELEMENTS in the array,
# otherwise nums[mid] < nums[mid + 1] would cause an index out of bound error. For this reason,
# the left <= right version doesn't work here.
