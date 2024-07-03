""" Given an array of integers nums and an integer k, return the number of contiguous sub-arrays where the product of
all the elements in the subarray is strictly less than k.
"""


# Video explanation: https://youtu.be/Cg6_nF7YIks
def num_subarray_product_less_than_k(nums, k):
    """ The brute force method involves finding all the sub-arrays and then selecting those whose products are less than
         k. However, this approach becomes costly in terms of time complexity, reaching O(N^2).

         For a more efficient approach, let's use the sliding window pattern. This pattern is applicable when the
         problem entails achieving a goal using sub-arrays, and individual elements cannot be independently selected.

         We maintain a window that continuously expands from the right by adding elements and computing their product
         until the condition is met. Once the condition is satisfied, we adjust the window by shrinking it from the left
         until the condition is met again.

         As we slide the window across the array, the objective is to identify all sub-arrays in the nums array where
         the product of its elements remains less than k. For each right position, if the product of the window's
         elements from left to right is less than k, adding the element at the right generates new sub-arrays with
         products less than k.

         The count of such sub-arrays is determined by (right - left + 1), which represents the number of sub-arrays
         that end at right and start at any element between right and left, inclusive. In essence, this count
         encompasses the subarray consisting solely of the current element itself, as well as all possible sub-arrays
         extending back to the left boundary of the window (left).

         Consider an example window containing elements 3, 4, and 5. If we include 6 in the window, we need to count all
         possible sub-arrays that end with 6. These sub-arrays can be formed by starting at any element within the
         current window and extending to 6. Therefore, the sub-arrays would be:

         [6] (subarray consisting only of 6)
         [5, 6] (subarray starting from 5 and ending at 6)
         [4, 5, 6] (subarray starting from 4 and ending at 6)
         [3, 4, 5, 6] (subarray starting from 3 and ending at 6)

         ALSO, if we remove the leftmost element, 3 in this case, the sub-arrays are now:
         [6], [5, 6], [4, 5, 6], a total of (right - left + 1) = 3.

         By calculating (right - left + 1), we enumerate all sub-arrays that end with the current element of the window
         (nums[right]). This ensures that we count all possible sub-arrays as we slide the window across the array.
         As we can observe, adding element 6 to the window created 4 new sub-arrays.

         !!! IMPORTANT !!!
         Each step introduces x NEW sub-arrays, where x is the size of the current window (right - left + 1).
         Don't confuse it with the number of possible sub-arrays between left and right, which is in the order of
         (right - left)^2.

         Example: nums = [1,2,3,4], target = 100
         [] -> [] // Step 0. We have 0 sub-arrays
         [1] -> [1] // Step 1, we grow the sliding window and see that the current window is less than target, we have 1
         possible contiguous subarray
         [1,2] -> [1,2], [1], [2] // Step 2. we grow the sliding window and see that the current window is less than
         target, by adding the 2, we can now make 3 total contiguous sub-arrays. (2 more than before)
         [1,2,3] -> [1,2], [1], [2], [1,2,3] , [2,3], [3] // Step 3. we grow the sliding window and see that the current
         window is less than target, by adding the 3, we can now make 6 total contiguous sub-arrays. (3 more than before)
         [1,2,3,4] -> [1,2], [1], [2], [1,2,3] , [2,3], [3], [1,2,3,4], [2,3,4], [3,4], [4] // Step 4. we grow the
         sliding window and see that the current window is less than target, by adding the 4, we can now make 10 total
         contiguous sub-arrays. (4 more than before)
         For every new element, we are adding window's length new sub-arrays.

         The crucial insight is that once the product becomes less than k, all possible sub-arrays formed by selecting
         subsets of elements within the current window (from left to right) will also have a product strictly less than k.

         Hence, whenever the product is valid, we add the current window size (right - left + 1) to the total count.

    Time complexity: O(N), each element in the array is visited at most twice
    Space complexity: O(1)
    """
    n, res = len(nums), 0
    prod = 1
    left = right = 0
    while right < n:
        # Expand the window by including the element at the right pointer
        prod *= nums[right]
        while left <= right and prod >= k:
            # Shrink the window from the left while the product is greater than or equal to k.
            # Remove the element at the left pointer from the product
            prod //= nums[left]
            left += 1
        # Update the total count by adding the number of valid sub-arrays with the current window size
        res += right - left + 1
        right += 1
    return res
