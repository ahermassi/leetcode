""" Given an integer array nums sorted in non-decreasing order, remove some duplicates in-place such that each unique
element appears at most twice. The relative order of the elements should be kept the same.

Since it is impossible to change the length of the array in some languages, you must instead have the result be placed
in the first part of the array nums. More formally, if there are k elements after removing the duplicates, then the
first k elements of nums should hold the final result. It does not matter what you leave beyond the first k elements.

Return k after placing the final result in the first k slots of nums.
Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra
memory. """


def remove_duplicates(nums):
    """ The input array is already sorted and hence, all the duplicates appear next to each other. The problem statement
         mentions that we are not allowed to use any additional space, and we have to modify the array in-place.
         The easiest approach for in-place modifications would be to overwrite the unwanted duplicates.

         We won't be able to achieve this using a single pointer. We will be using a two-pointer approach where one
         pointer iterates over the original set of elements and another one that keeps track of the next "empty"
         location in the array or the next location that can be overwritten in the array.

            - We define two pointers, i and write_index. The pointer i iterates of the array processing one element at
               a time and write_index keeps track of the next location in the array where we can overwrite an element.

            - If we find that the current element is the same as two elements before write_index i.e.
               nums[i] == nums[write_index-2], it means there are already two occurrences of this element and this is an
               unwanted duplicate element. In this case, we simply move forward i.e. we increment i but not write_index.

            - If we find that the current element is not the same as nums[write_index-2], then it means either:
                    * we have a new element at hand, or
                    * we have a second duplicate (remember that we're only allowed two duplicates per element),
               and so accordingly we move this element to index write_index.

            - It goes without saying that whenever we copy a new element to nums[write_index], we have to update the
               value of write_index as well since write_index always points to the location where the next element can
               be copied to in the array.

         The invariant of this algorithm is:

                    All elements up to write_index (excluded) appear AT MOST twice

    Time complexity: O(N)
    Space complexity: O(1)
    """
    # write_index is the tail of the sequence of elements that appear AT MOST twice but NOT including nums[write_index].
    # The next element that didn't appear at most twice will be written at nums[write_index].
    write_index = 0
    for num in nums:
        if write_index < 2 or nums[write_index - 2] != num:
            # nums[write_index-2] is the "head" of last sequence of potentially duplicate elements of length 2.
            # write_index < 2 ensures the first 2 elements are included in the output. After all, each of them can
            # only appear at most twice.
            nums[write_index] = num
            write_index += 1
    return write_index


