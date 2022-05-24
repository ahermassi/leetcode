""" Given an integer array nums that may contain duplicates, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order. """


def subsets_with_dup(nums):
    """ This problem is a successor to 78- Subsets. The key to this problem is figuring out how to avoid duplicate
         subsets.

         When designing our recursive function, there are two main points that we need to consider at each function call:

            - Whether the element under consideration has duplicates or not.
            - If the element has duplicates, which element among the duplicates should be considered while creating a
               subset.

        First, sort the array in ascending order. Then, start with an empty list and the starting index set to 0.

        At each function call, add a new subset to the output list of subsets.

        Scan through all the elements in the nums array from the starting index to the end. Consider
        one element at a time and decide whether to keep it or not. If we haven't seen the current element before, then
        add it to the current list and make a recursive function call with the starting index incremented by one.
        Otherwise, the subset is a duplicate, and so we ignore it. Thus, if in a particular function call we scan
        through k distinct elements, there will be k different branches.

        Sorting is required to ensure all the generated subsets will also be sorted. This helps to identify duplicates
        and remove them and ensures all the generated subsets will also be sorted. For example, subsets {3, 1, 3},
        {1, 3, 3}, {3, 3, 1} will become {1, 3, 3}.


    Time complexity: O(N* 2^N), in the worst case when the array consists of N distinct elements. There are 2^N subsets
    to generate. The recursive function is called 2^N times, since we have 2 choices at each iteration in nums array:
    Either we include nums[i] in the current set, or we exclude nums[i].
    Space complexity: O(N), for sorting and call stack
    """

    def compute_subsets_at_index(index, subset):
        res.append(subset)
        for i in range(index, n):
            if i != index and nums[i] == nums[i - 1]:  # If the current element is a duplicate, ignore.
                continue
            compute_subsets_at_index(i + 1, subset + [nums[i]])

    nums.sort()
    n, res = len(nums), []
    compute_subsets_at_index(0, [])
    return res
