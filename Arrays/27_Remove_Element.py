""" Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the
elements may be changed. Then return the number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following
things:

Change the array nums such that the first k elements of nums contain the elements which are not equal to val.
The remaining elements of nums are not important as well as the size of nums.
Return k. """


# Video explanation: https://youtu.be/Pcd1ii9P9ZI
def remove_element_v1(nums, val):
    """ We need to modify the array in-place and the size of the final array would potentially be smaller than the size
         of the input array. The goal is not to remove the element per se, but to bypass all its occurrences. So, we
         ought to use a two-pointer approach here. One, called i, that would keep track of the current element in the
         original array and another one, called write_index, that represents the tail of the sequence of elements that
         are not equal to val.

         As long as nums[i] == val , we increment i to skip the duplicates. When we encounter the first nums[i] != val,
         we copy nums[i] to nums[write_index] and increment write_index. We repeat the same process until i reaches the
         end of the array.

         The invariant of this algorithm is:

                    All elements up to write_index (included) are not equal to val

    Time complexity: O(N), where N is the length of nums array
    Space complexity: O(1)
    """
    write_index = 0  # write_index is the tail of the sequence of elements that are not equal to val
    for num in nums:
        if num != val:
            nums[write_index] = num
            write_index += 1
    return write_index


