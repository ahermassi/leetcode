""" Given a sorted array nums, remove the duplicates in-place such that each element appear only once and return the
new length.
Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra
memory. """


def remove_duplicates(nums):
    """ The goal is not to remove the elements, but to swap to the end. Since the array is already sorted, we can keep
        two pointers i and write_index, where write_index is the slow-runner and i is the fast-runner.
        As long as nums[i] == nums[write_index-1] , we increment i to skip the duplicates. When we encounter
        nums[i] != nums[write_index-1], the duplicate run has ended so we must copy its value to nums[write_index].
        write_index is then incremented and we repeat the same process again until i reaches the end of array.
        The invariant of this algorithm is: all elements before write_index are unique. All elements between write_index
        and i are duplicate of nums[write_index - 1].
    Time complexity: O(N) where N is the length of array nums
    Space complexity: O(1)
    """
    if not nums:
        return 0
    write_index = 1  # This variable is the index where we'll write the next non-duplicate element
    for i in range(1, len(nums)):
        if nums[i] != nums[write_index - 1]:
            nums[write_index] = nums[i]
            write_index += 1
    return write_index


