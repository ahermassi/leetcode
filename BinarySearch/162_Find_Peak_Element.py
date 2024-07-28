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
    """ We can view any given sequence in nums array as alternating ascending and descending sequences. By making
         use of this property and the fact that we can return any peak, we can use binary search to find the peak
         element.

         In the case of a regular binary search, we work on a sorted sequence of numbers and try to find the required
         number by reducing the search space at every step. For this problem, we use a modified binary search.

         We start off by finding the middle element 'mid'.

            - If mid happens to be in a descending sequence of numbers, or a local falling slope (found by comparing
               nums[i] to its left neighbor), it means that the peak will always be towards the left of mid. Thus, we
               reduce the search space to the left of mid (including itself) and perform the same process on the left
               subarray.

            - If mid is in an ascending sequence of numbers, or a rising slope (found by comparing nums[i] to its
               right neighbor), it obviously implies that the peak is towards the right of this element. Thus, we reduce
               the search space to the right of mid and perform the same process on the right subarray.

         In this way, we keep on reducing the search space until we eventually reach a state where only one element is
         remaining in the search space. This single element is the peak element.

         Binary search works here because we need to return any local peak, not necessarily the global peak.

            - If the number to the right is bigger than the middle value, then somewhere on the right there must be a
               peak - either the numbers ascend and then descend, in which case there would be a peak where the change
               from ascent to descent happens, or the numbers continue to ascend until the end of the array, in which
               case the last value in the array would be a local peak (because nums[n] = -∞).


            - If the value to the left is bigger than the middle value, then it must be that either the middle value
               itself is a peak or that there is definitely a peak on the left side of the middle value. This is because
               if the number on the left is bigger than the middle value, there are two options: either the numbers
               continue ascending in the left direction until the beginning of the array, in which case the first
               element of the array would be a peak (because nums[0] = -∞), or the values increase to the left until a
               point at which they start decreasing, and that point would be a peak.

         So binary search works because as long as we follow the slopes upward, we will for sure encounter a peak.
         Yes, we may miss some peaks during binary cuts, but there is at least 1 that will be encountered since beyond 0
         and (n - 1) are negative infinities. If it keeps going up, then it has to have a peak turn or reach either end
         of the array which by the definition are peaks.

         What is helpful is the following statement in the question description:
            "You may imagine that nums[-1] = nums[n] = -∞"
         This means a peak will always exist.

         Example: 3 is peak in following two arrays:
         -∞ | 0,1,2,3|-∞
         -∞ | 3,2,1,0|-∞
         So all we need to do is find the end of any increasing slope in the input array.

         Let's say we have a mid at index i, nums[i]. If nums[i] < nums[i+1], that means a peak element HAS TO exist in
         the right half of the array, because (since every number is unique):

            - If the numbers keep increasing on the right side, then the peak will be the last element.
            - If the numbers stop increasing and there is a 'dip', or there exists somewhere an index j such that
               nums[j] < nums[j-1], it means number[i] is a peak element.

         This same logic can be applied to the left-hand side (nums[i] < nums[i-1]).

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
