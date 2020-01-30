""" Given an unsorted array nums, reorder it in-place such that nums[0] <= nums[1] >= nums[2] <= nums[3].... """


def wiggle_sort(nums):
    """ The rule is:
            1- If i is even, nums[i] <= nums[i+1]
            2- If i is odd, nums[i] >= nums[i+1]
        Iterating through the array and swapping A[i] and A[i+1] when i is even and A[i] > A[i+1] or i is odd and
        A[i] < A[i+1] achieves the desired configuration.
        Proof: Suppose sequence [1, 2, ..., i] follows the rule.
        If i is odd, we need to prove by swapping, i+1 will follow the rule as well.
            - If nums[i] >= nums[i+1], it follows the rule. Nothing to be done.
            - If nums[i] < nums[i+1], swap nums[i] and nums[i+1]
        Before         After
        e  o  e        e   o  e
        i-1 i i+1      i-1 i+1 i
        Because sequence [1, 2, ..., i] follows the rule, nums[i-1] <= num[i], and nums[i] < nums[i+1]. Therefore,
        nums[i-1] < nums[i+1]. After swapping, the rule sustains.
        The proof of i being even is similar.
        Suppose nums[0 .. i - 1] is wiggled. For position i:
        If i is odd, we already have nums[i-2] >= nums[i-1]
            - If nums[i-1] <= nums[i], then we do not need to do anything, it's already wiggled.
            - If nums[i-1] > nums[i], then we swap nums[i-1] and nums[i]. Due to previous wiggled elements
              (nums[i-2] >= nums[i-1]), we know that after swapping the sequence is ensured to be
              nums[i-2] > nums[i-1] < nums[i], which is wiggled.
        Similarly, if i is even, we already have, nums[i-2] <= nums[i-1]
            - If nums[i-1] >= nums[i], then we do not need to do anything, it's already wiggled.
            - If nums[i-1] < nums[i], then after swapping we are sure to have nums[i-2] < nums[i-1] > nums[i]
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    for i in range(n - 1):
        if i % 2 == 0 and nums[i] > nums[i + 1] or i % 2 == 1 and nums[i] < nums[i + 1]:
            nums[i], nums[i + 1] = nums[i + 1], nums[i]
