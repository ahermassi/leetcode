""" Given an integer array nums that may contain duplicates, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order. """


# Video explanation: https://youtu.be/Vn2v6ajA7U0
def subsets_with_dup_v1(nums):
    """ This problem is a successor of 78- Subsets. We'll focus our attention on generating all subsets while
         efficiently omitting all duplicate subsets.

          When designing the recursive function, there are two main points that we need to consider at each call:

             - Whether the current number has duplicates
             - If the number has duplicates, which number among the duplicates should be considered while creating a
                subset.

         Note that the order of the subsets in the result is the preorder traversal of the recursion tree.

            - First, sort the array in ascending order. Then, start with an empty subset and the starting index 0.

            - At each function call, add a new subset to the final output list.

            - Scan through all the numbers in the nums array from the starting to the ending index. Consider one number
               at a time and decide whether to keep it or exclude it.

                    * If we haven't seen the current number before, then add it to the current subset and make a
                       recursive call with the starting index incremented by one.

                    * Otherwise, the number is a duplicate, so we skip it as it could generate a duplicate subset.
                       Thus, if in a particular call we scan through k distinct elements, there will be k different
                       branches.

         Sorting the input is required to ensure all the generated subsets are also sorted. It also helps identify
         potential duplicate subsets. For example, without sorting nums = [2,1,2], the algorithm will generate subsets
         { [], [2], [1], [2], [2, 1], [2,2], [1, 2], [2, 1, 2] }. Here, subset [1, 2] should be considered a duplicate
         of subset [2, 1]. To detect such duplicate subsets, prior sorting of the input list is required.


    Time complexity: O(2^N), in the worst case when the array consists of N distinct elements. There are 2^N subsets
    to generate. The recursive function is called 2^N times, since we have 2 choices at each iteration in nums array:
    either include nums[i] in or exclude it from the current subset.
    Space complexity: O(N), for sorting and call stack
    """

    def compute_subsets_at_index(index, subset):
        res.append(subset)
        for i in range(index, n):
            if i > index and nums[i] == nums[i - 1]:
                # If the current number is a duplicate, ignore the subset. This skips duplicates except in the first
                # iteration.
                continue
            compute_subsets_at_index(i + 1, subset + [nums[i]])

    nums.sort()
    n, res = len(nums), []
    compute_subsets_at_index(0, [])
    return res


def subsets_with_dup_v2(nums):
    """ Good ol' backtracking without the use of a for loop.

    Time complexity: O(N * 2^N)
    Space complexity: O(N)
    """

    def compute_subsets_at_index(index):
        if index == n:
            res.append(subset[:])
            return
        # Find all subsets that contain the current number by adding nums[index] to the subset
        subset.append(nums[index])
        compute_subsets_at_index(index + 1)
        # Backtrack. Explore subsets that don't contain nums[index] by removing nums[index] from the subset.
        # We also need to skip duplicates of nums[index].
        subset.pop()
        while index + 1 < n and nums[index] == nums[index + 1]:
            index += 1
        compute_subsets_at_index(index + 1)

    n, subset, res = len(nums), [], []
    nums.sort()
    compute_subsets_at_index(0)
    return res


def subsets_with_dup_v3(nums):
    """ Assume the given array has no duplicate elements. In this case, there will be a total of 2^N distinct subsets.
         To find all the subsets, we start with an empty subset. This will be the first subset. Next, we consider one
         number at a time and add it to each of the existing subsets.

         However, in this problem, the given array can have duplicate numbers which could produce duplicate subsets if
         we follow the previously mentioned approach. Thus, we need to omit the duplicate subsets.

         For this, we need to sort the given array first. To avoid adding duplicate subsets we follow this rule, where
         X designates the current number:

                        If X is encountered for the first time, we add it to all the existing subsets. After that, we
                        add the duplicates of X only to the subsets created when X was encountered for the first time.

        In other words, we treat a group of duplicate numbers as a subarray. Suppose we have a subarray [3, 3, 3]. The
        ways to add these numbers to the existing subsets are as follows:

             -Not add any 3 to any subset
             - Add one 3 to all the subsets
             - Add two 3's to all the subsets
             - Add three 3's to all the subsets

         The algorithm is as follows:

             - Initialize a variable append_index to 0. append_index is the index of the subset in the subsets list from
                where we should start appending the current number if the number has duplicates. In other words, it's
                the index of the first subset generated in the previous step.

             - Iterate over the nums array considering one number at a time.

             - If we haven't seen the current number before, we need to add it to all the previously generated subsets.
                Therefore, set start_index to 0.

             - If the current number is a duplicate, add it only to the subsets that were created in the previous
                iteration. This means we skip every subset that was created earlier than the previous iteration.
                So instead of setting start_index to 0, set it equal to append_index.

             - Set append_index to the size of the current list of subsets. This will be the starting index of the
                subsets generated in the next iteration.

             - Add the current number to all the subsets in the subsets list created before the current iteration
                starting from start_index.

    Time complexity: O(N * 2^N), in the worst case, i.e., with an array of N distinct integers, we will have a total of
    2^N subsets, and the O(N) to copy them into output list as the maximum number of elements in a subset will be N.
    Space complexity: O(N), for sorting
    """
    nums.sort()
    power_set = [[]]
    append_index = 0
    for i, num in enumerate(nums):
        # append_index refers to the starting index of the subsets to which we will append the current number.
        start_index = append_index if i > 0 and nums[i] == nums[i - 1] else 0
        subsets = []
        for j in range(start_index, len(power_set)):
            subsets.append(power_set[j] + [num])
        # This will be the value of start_index in the next iteration if a duplicate number is encountered
        append_index = len(power_set)
        power_set.extend(subsets)
    return power_set


def subsets_with_dup_v4(nums):
    """  If we store the last created subsets in a list, the previous solution might be slightly easier to understand.
    """
    nums.sort()
    all_subsets = [[]]
    prev_subsets = []
    for i, num in enumerate(nums):
        if i > 0 and nums[i] == nums[i - 1]:
            cur_subsets = [subset + [num] for subset in prev_subsets]
        else:
            cur_subsets = [subset + [num] for subset in all_subsets]
        all_subsets.extend(cur_subsets)
        prev_subsets = cur_subsets
    return all_subsets
