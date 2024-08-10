""" Given an unsorted array of integers, find the length of the longest increasing subsequence. """

import unittest as unittest


# Video explanation: https://www.youtube.com/watch?v=fV-TF4OvZpk
# Video explanation: https://youtu.be/cjWnW0hdF1Y
def length_of_lis_v1(nums):
    """ Let dp[i] be the length of the longest increasing subsequence that ends with the ith element, or nums[:i].

         The default answer is 1. Every element on its own is technically an increasing subsequence.

         We need a way to transition between states, such as dp[5] and dp[7]. Let's say we know dp[0], dp[1], and dp[2].
         How can we find dp[3] given this information? Well, since dp[2] represents the length of the longest increasing
         subsequence that ends with nums[2], if nums[3] > nums[2], then we can simply take the subsequence ending at =2
         and append nums[3] to it, increasing the length by 1. The same can be said for nums[0] and nums[1] if nums[3]
         is larger. Of course, we should try to maximize dp[3], so we need to check all 3. Formally, the recurrence
         relation is:

                    dp[i] = max(dp[j] + 1) for all j < i, where nums[j] < nums[i]

         At the end, the maximum out of all the dp[i]'s determines the final result.

         Example: nums = [-1, 3, 4, 5, 2, 8]

         At index 0 we always know that we can have a subsequence of length 1.

         We then look at index 1. We need to ask ourselves if the item at index 1 can lengthen the LIS found at index 0.
         We check if 3 is greater than -1... it is. Great. Index 1 can be tacked on, but should we?
         dp[1] = 1, dp[0] = 1. It makes sense because if we tack 3 onto the LIS we found for the sub-problem [-1], then
         at index 1 we will also have a LIS. So what we basically do is build a table and ask ourselves these questions
         all along the way.

         Each cell represents the answer to the sub-problem asked against the sub-sequence from index 0 to index i
         (including the element at index i).

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n = len(nums)
    dp, max_len = [1] * n, 1
    for i in range(n):
        # We want to check if we can append the item at nums[i] to extend the Longest Increasing Subsequence built
        # from index j=0...i-1. We want to solve for dp[i] if the value at i is greater than the value at j
        for j in range(i):
            if nums[i] > nums[j]:
                # The value of dp[j] is the length of the LIS from 0...j, we conceptually 'append' the current element
                # to this LIS by adding 1 to that sub-problem answer, yielding a potentially new answer for LIS[0..i]
                dp[i] = max(dp[i], dp[j] + 1)
        max_len = max(max_len, dp[i])  # We have an answer for LIS[0...i]. Compare it with the best LIS length so far.
    return max_len


# For more details:
# https://leetcode.com/problems/longest-increasing-subsequence/discuss/74824/JavaPython-Binary-search-O(nlogn)-time-with-explanation
def length_of_lis_v2(nums):
    """ This approach is known as Patience Sorting.

         As stated in the previous approach, the difficult part of this problem is deciding if an element is worth
         using. Let's try to build an increasing subsequence starting with an empty one.

         The best way to build an increasing subsequence is: for each element num, if num is greater than the largest
         element in the subsequence, then add it to the subsequence. Otherwise, perform a linear scan through the
         subsequence starting from the smallest element and replace the first element that is greater than or equal to
         num with num. This opens the door for elements that are greater than num but less than the element replaced to
         be included in the sequence.

         Consider the example nums = [8, 1, 6, 2, 3, 10], longest_increasing_subs = [].

         At the first element 8, we might as well take it since it's better than nothing, so longest_increasing_sub=[8].

         At the second element 1, we can't increase the length of the subsequence since 8 >= 1, so we have to choose
         only one element to keep. Well, this is an easy decision, let's take the 1 since there MAY be elements later on
         that are greater than 1 but less than 8, now we have longest_increasing_sub = [1].

         At the third element 6, we can build on the subsequence since 6 > 1, now longest_increasing_sub = [1, 6].

         At the fourth element 2, we can't build on the subsequence since 6 >= 2, but can we improve on it for the
         future? Similar to the decision we made at the second element, if we replace the 6 with 2, we will open the
         door to using elements that are greater than 2 but less than 6 in the future, so longest_increasing_sub = [1, 2].

         At the fifth element 3, we can build on the subsequence since 3 > 2. Notice that this was only possible because
         of the swap we made in the previous step, so longest_increasing_sub = [1, 2, 3].

         At the last element 10, we can build on the subsequence since 10 > 3, giving a final subsequence
         longest_increasing_sub = [1, 2, 3, 10]. The length of longest_increasing_sub is the answer.

         Since longest_increasing_sub is in sorted order, we can use binary search instead of linear search to find the
         insertion index of the current element in longest_increasing_sub if we were to keep it sorted.

         Why does this work ?
         When we replace longest_increasing_sub[i] with the current num, we don't change the length of the LIS, but we
         change the POTENTIAL BEST CANDIDATE. Replacing longest_increasing_sub[i] with the first element that is
         smaller than or equal to it increases the chance of extending the LIS because longest_increasing_sub[i] is
         smaller than that element. When we replace an element in longest_increasing_sub, we're not extending the
         length of the sequence, but we are making the increasing sequence that we can potentially build later MORE
         FLEXIBLE, i.e., able to accommodate smaller subsequent numbers.

         !!! IMPORTANT !!!
         This algorithm does not always generate a valid subsequence of the input due to the order being potentially
         mixed up as a result of replacements, but the length of the subsequence will always equal the length of the
         longest increasing subsequence.
         For example, with the input [3, 4, 5, 1], at the end we will have longest_increasing_sub = [1, 4, 5], which
         isn't a subsequence, but the length is still correct. The length remains correct because the length only
         changes when a new element is larger than any element in the subsequence. In that case, the element is appended
         to the subsequence instead of replacing an existing element.

        So the main idea is:

                    Use binary search to extend the increasing sequence with larger numbers, or minimize existing values
                                    with smaller ones, so we can use larger numbers to extend it.

        Example: nums = [0, 8, 4, 12, 2]
        i = 0, increasing_sub_sequence = [0]
        i = 1, increasing_sub_sequence = [0, 8]
        i = 2, increasing_sub_sequence = [0, 4]
        i = 3, increasing_sub_sequence = [0, 4, 12]
        i = 4, increasing_sub_sequence = [0 , 2, 12] which is not the longest increasing sub-sequence, but its length
        is the length of LIS.

    Time complexity: O(N logN), binary search takes logN time and is called N times
    Space complexity: O(N)
    """

    def find_insertion_index(val):
        left, right = 0, len(longest_increasing_subsequence) - 1
        while left <= right:
            mid = (left + right) // 2
            if longest_increasing_subsequence[mid] < val:
                left = mid + 1
            else:
                right = mid - 1
        return left

    longest_increasing_subsequence = []
    for num in nums:
        if not longest_increasing_subsequence or num > longest_increasing_subsequence[-1]:
            longest_increasing_subsequence.append(num)
        else:
            index = find_insertion_index(num)
            longest_increasing_subsequence[index] = num
    return len(longest_increasing_subsequence)


class Test(unittest.TestCase):
    data = [([10, 9, 2, 5, 3, 7, 101, 18], 4)]

    def test_length_of_LIS(self):
        for test_array, result in self.data:
            self.assertEqual(result, length_of_lis_v1(test_array))
            self.assertEqual(result, length_of_lis_v2(test_array))


if __name__ == '__main__':
    unittest.main()
