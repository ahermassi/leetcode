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


def remove_element_v2(nums, val):
    """ Consider cases where the array contains few elements to remove. For example, nums = [1,2,3,5,4], val = 4.
         The previous algorithm will do unnecessary copy operation of the first four elements. Another example is
         nums = [4,1,2,3,5], val = 4. It seems unnecessary to move elements [1,2,3,5] one step left as the problem
         description mentions that the order of elements could be changed.

         When we encounter nums[i]=val, we can move the current element to the end of the array and dispose of the last
         element. This essentially reduces the array's size by 1.

         Note that the last element that was swapped in could be the value we want to remove itself. But don't worry, in
         the next iteration we will still check this element.

    Time complexity: O(N), where N is the length of nums array. The number of assignment operations is equal to the
    number of elements to remove. So it is more efficient if elements to remove are rare.
    Space complexity: O(1)
    """
    n = len(nums)
    i = 0
    while i < n:
        if nums[i] == val:
            nums[i] = nums[n - 1]
            n -= 1  # Decrement the length of the array by discarding the last element
        else:
            i += 1
    return n


