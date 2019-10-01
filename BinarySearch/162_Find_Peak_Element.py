""" A peak element is an element that is greater than its neighbors.
Given an input array nums, where nums[i] ≠ nums[i+1], find a peak element and return its index.
The array may contain multiple peaks, in that case return the index to any one of the peaks is fine. """


def find_peak_element_v1(nums):
    """ We can view any given sequence in numsnums array as alternating ascending and descending sequences. By making
        use of this, and the fact that we can return any peak as the result, we can make use of Binary Search to find
        the required peak element.
        In case of simple Binary Search, we work on a sorted sequence of numbers and try to find out the required
        number by reducing the search space at every step. In this case, we use a modification of this simple Binary
        Search to our advantage. We start off by finding the middle element, mid from the given nums array. If
        this element happens to be lying in a descending sequence of numbers. or a local falling slope(found by
        comparing nums[i]nums[i] to its right neighbour), it means that the peak will always lie towards the left of
        this element. Thus, we reduce the search space to the left of midmid(including itself) and perform the same
        process on left subarray.
        If the middle element, mid lies in an ascending sequence of numbers, or a rising slope(found by comparing
        nums[i] to its right neighbour), it obviously implies that the peak lies towards the right of this element.
        Thus, we reduce the search space to the right of mid and perform the same process on the right subarray.
        In this way, we keep on reducing the search space till we eventually reach a state where only one element is
        remaining in the search space. This single element is the peak element.

        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|---|---|
        | l | _ | _ | _ | m | _ | _ | _ | r |
        a[m] > a[m+1] -> r=m (Not m-1 since m is larger and it itself can be the answer)

        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|---|---|
        | l | m | _ | _ | r | X | X | X | X |
        a[m] < a[m+1] -> l = m+1 (Since m is smaller than m+1, m will for sure be not the answer)

        | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 |
        |---|---|---|---|---|---|---|---|---|
        | X | X | l | m | r | X | X | X | X |
        a[m] < a[m+1] -> l = m+1 (Since m is smaller than m+1, m will for sure be not the answer)

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
        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1
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
        else:
            return helper(nums, mid + 1, right)

    return helper(nums, 0, len(nums) - 1)


def find_peak_element_v3(nums):
    """ Linear scan.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    i = 0
    while i <= len(nums) - 1:
        while i < len(nums) - 1 and nums[i] < nums[i + 1]:
            i += 1
        return i
