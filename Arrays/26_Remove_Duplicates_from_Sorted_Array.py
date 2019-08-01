""" Given a sorted array nums, remove the duplicates in-place such that each element appear only once and return the
new length.
Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra
memory. """


def remove_duplicates(nums):
    """ The goal is not to remove the elements, but to swap to the end. Since the array is already sorted,
        we can keep two pointers i and new_tail, where new_tail is the slow-runner and i is the fast-runner. As long
        as nums[i] = nums[new_tail] , we increment i to skip the duplicate. When we encounter nums[i] != nums[new_tail],
        the duplicate run has ended so we must copy its value to nums[new_tail + 1]. new_tail is then incremented and
        we repeat the same process again until i reaches the end of array.
    Time complexity: O(N) where N is the length of array nums
    Space complexity: O(1)
    """
    new_tail = 0
    for i in range(1, len(nums)):
        if nums[i] != nums[new_tail]:
            new_tail += 1
            nums[new_tail] = nums[i]
    return new_tail + 1


