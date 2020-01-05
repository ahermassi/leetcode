""" A peak element is an element that is greater than its neighbors.
Given an input array nums, where nums[i] ≠ nums[i+1], find a peak element and return its index.
The array may contain multiple peaks, in that case return the index to any one of the peaks is fine. """


def find_peak_element_v1(nums):
    """ We can view any given sequence in nums array as alternating ascending and descending sequences. By making
        use of this, and the fact that we can return any peak as the result, we can make use of Binary Search to find
        the required peak element.
        In case of simple Binary Search, we work on a sorted sequence of numbers and try to find out the required
        number by reducing the search space at every step. In this case, we use a modification of this simple Binary
        Search to our advantage. We start off by finding the middle element 'mid' from the given nums array. If
        this element happens to be lying in a descending sequence of numbers, or a local falling slope (found by
        comparing nums[i] to its right neighbour), it means that the peak will always lie towards the left of this
        element. Thus, we reduce the search space to the left of 'mid' (including itself) and perform the same process
        on left sub-array.
        If the middle element 'mid' lies in an ascending sequence of numbers, or a rising slope (found by comparing
        nums[i] to its right neighbour), it obviously implies that the peak lies towards the right of this element.
        Thus, we reduce the search space to the right of 'mid' and perform the same process on the right sub-array.
        In this way, we keep on reducing the search space till we eventually reach a state where only one element is
        remaining in the search space. This single element is the peak element.
        Binary search works here because we need to return any local peak, not necessarily the global peak.
        If the number to its right is higher than the middle value, then somewhere on the right there must be a peak -
        either the numbers ascend and then descend, in which case there would be a peak where the change from ascent
        to descent happens, or the numbers continue to ascend until the end of the array, in which case the last value
        in the array would be a local peak (because nums[n] = -∞)
        The same with the other way. If the value on the left of the middle value is bigger than the middle value, then
        it must be that either the middle value itself is a peak or that there is definitely a peak on the left side
        of the middle value. This is because if the number on the left is bigger than the middle value, there are two
        options: either the numbers continue ascending in the left direction until the end, in which case the first
        value of the array would be a peak (because nums[0] = -∞), or the values increase to the left until a point at
        which they start decreasing, and that point would be a peak.
        So by seeing what happens at the middle and choosing the continuation accordingly, we can be sure to eventually
        arrive at a peak.

        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|---|---|
        | l | _ | _ | _ | m | _ | _ | _ | r |
        a[m] > a[m+1] -> r=m (Not m-1 since m is larger and it itself can be the answer)

        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|---|---|
        | l | _ | m | _ | r | X | X | X | X |
        a[m] < a[m+1] -> l = m+1 (Since m is smaller than m+1, m will for sure not be the answer)

        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|---|---|
        | X | X | X |l,m | r | X | X | X | X |
        a[m] < a[m+1] -> l = m+1 (Since m is smaller than m+1, m will for sure not be the answer)

        | 1 | 2 | 3 | 4 | 5   | 4 | 3 | 2 | 1 |
        |---|---|---|---|-----|---|---|---|---|
        | X | X | X | X | l,r | X | X | X | X |
        l is the answer

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
    return left


def find_peak_element_v2(nums):
    """ Recursive version of previous algorithm.
    Time complexity: (logN)
    Space complexity: O(logN), the depth of recursion tree
    """
    def helper(nums, left, right):
        if left == right:
            return left
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            return helper(nums, left, mid)
        return helper(nums, mid + 1, right)

    return helper(nums, 0, len(nums) - 1)


def find_peak_element_v3(nums):
    """ Linear scan.
        In this approach, we make use of the fact that two consecutive numbers nums[i] and nums[i+1] are never equal.
        Thus, we can traverse over the nums array starting from the beginning. Whenever, we find a number nums[i], we
        only need to check if it is larger than the next number nums[i+1] for determining if nums[i] is the peak
        element.
        Case 1: All the numbers appear in a descending order. In this case, the first element corresponds to the peak
        element. We start off by checking if the current element is larger than the next one. The first element
        satisfies this criteria, and is hence identified as the peak correctly.
        Case 2: All the elements appear in ascending order. In this case, we keep on comparing nums[i] with nums[i+1]
        to determine if nums[i] is the peak element or not. None of the elements satisfy this criteria, indicating that
        we are currently on a rising slope and not on a peak. Thus, at the end, we need to return the last element as
        the peak element, which turns out to be correct (because nums[n] = -∞)
        Case 3: The peak appears somewhere in the middle. In this case, when we are traversing on the rising edge, as
        in Case 2, none of the elements will satisfy nums[i] > nums[i+1]. We need not compare nums[i] with nums[i-1]
        on the rising slope as discussed above. When we finally reach the peak element, the condition
        nums[i] > nums[i+1] is satisfied. We again need not compare nums[i] with nums[i-1]. This is because we could
        reach nums[i] as the current element only when the check nums[i] > nums[i+1] failed for the previous (i−1)th
        element.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    for i in range(1, n-1):
        if nums[i] > nums[i + 1]:
            return i
    return n - 1
