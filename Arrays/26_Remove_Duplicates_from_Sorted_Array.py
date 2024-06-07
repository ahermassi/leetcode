""" Given a sorted array nums, remove the duplicates in-place such that each element appear only once and return the
new length.
Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra
memory. """


# Video explanation: https://youtu.be/DEJAZBq0FDA
def remove_duplicates(nums):
    """ The problem would have been simpler if we are allowed to use extra space. We can create a hashmap which stores
         all unique array elements as the key and element frequency as the value. After populating the map, we get all
         the unique elements from the array. We then iterate the map and push all the keys in the input array.
         However, without using extra space it makes it a bit tricky as we have to modify the existing input array.

         Since the array is sorted, repeated elements must appear one the other, so we do not need an auxiliary data
         structure to check if an element appeared before. Therefore, if we know the position of one of the elements, we
         also know the positioning of all the duplicate elements.

         We need to modify the array in-place and the size of the final array would potentially be smaller than the size
         of the input array. The goal is not to remove the elements, but to swap to the end. So, we ought to use a
         two-pointer approach here. One, called i, that would keep track of the current element in the original array
         and another one, called write_index, that represents the tail of the sequence of unique elements and is used to
         bypass the duplicates.

         As long as nums[i] == nums[write_index] , we increment i to skip the duplicates. When we encounter the first
         nums[i] != nums[write_index], it means the duplicate run has ended, so we must copy nums[i] to
         nums[write_index+1]. We repeat the same process until i reaches the end of the array.

         The invariant of this algorithm is:

                    All elements up to write_index (included) are unique. All elements between write_index and i are
                    duplicate of nums[write_index].

    Time complexity: O(N), where N is the length of nums array
    Space complexity: O(1)
    """
    write_index = 0  # write_index is the tail of the sequence of unique elements
    n = len(nums)
    for i in range(n):
        if nums[i] != nums[write_index]:
            write_index += 1
            nums[write_index] = nums[i]
    return write_index + 1


