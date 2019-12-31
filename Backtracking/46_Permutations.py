""" Given a collection of distinct integers, return all possible permutations. """


def permute_v1(nums):
    """ Here is a backtracking function which takes the index of the first integer to consider.
        A good approach is to recognize that once a value has been chosen for an entry, we do not want to repeat it.
        Specifically, every permutation of A begins with one of A[0],A[1] ,. . . ,A[n - 1]. The idea is to generate all
        permutations that begin with A[0], then all permutations that begin with A[1], and so on. Computing all
        permutations beginning with A[0] entails computing all permutations of A[1,n - 1], which suggests the use of
        recursion. To compute all permutations beginning with A[1] we swap A[0] with A[1] and compute all permutations
        of the updated A[1.,n - 1]. We then restore the original state before embarking on computing all permutations
        beginning with A[2], and so on.
        If the first integer to consider has index n, that means there is nothing to compute.
        Iterate over the integers from 'index' to index (n - 1), the end of the array.
            - Place (index)th integer first in the permutation, i.e. swap(nums[index], nums[i]).
            - Proceed to create all permutations which start from (index+1)th integer:
              compute_permutations_at_index(index + 1).
            - Now backtrack, i.e. swap(nums[index], nums[i]) back.
    Time complexity: O(N * N!), because we generate N! permutations and each permutation requires O(N) to copy into res
    Space complexity: O(N) for the recursive call stack (max depth of call tree)
    """
    def compute_permutations_at_index(index):
        if index == n:
            res.append(nums[:])
            return
        for i in range(index, n):
            # We're using here the same principle of recursion. Given a sub-array starting at index 'index',
            # loop over the elements of the sub-array, and at each iteration:
            # 1- Bring the current element to the head of the sub-array at starting index 'index'
            # 2- TRUST that the recursive call will compute the permutations of the sub-array at (index + 1)
            # 3- Undo the swap to bring the sub-array to its initial state and move on to the next element
            nums[index], nums[i] = nums[i], nums[index]
            compute_permutations_at_index(index + 1)
            nums[index], nums[i] = nums[i], nums[index]  # Second swap: backtracking. Think of it as moving back up
            # in the tree to explore the next branch. When we moved down of one level, we swapped 2 elements (1st
            # swap in the code). So when we go back up in the tree we need to swap these 2 elements back to their
            # original order at the parent node level (2nd swap in the code). This is called backtracking = done
            # exploring a branch, let's go back up and explore more branches.

    n, res = len(nums), []
    compute_permutations_at_index(0)
    return res


def permute_v2(nums):
    """ Second solution.
        Visualisation:
        dfs(nums = [1, 2, 3] , path = [] , result = [] )
        |____ dfs(nums = [2, 3] , path = [1] , result = [] )
        |      |___dfs(nums = [3] , path = [1, 2] , result = [] )
        |      |    |___dfs(nums = [] , path = [1, 2, 3] , result = [[1, 2, 3]] ) # added a new permutation to the result
        |      |___dfs(nums = [2] , path = [1, 3] , result = [[1, 2, 3]] )
        |           |___dfs(nums = [] , path = [1, 3, 2] , result = [[1, 2, 3], [1, 3, 2]] ) # added a new permutation to the result
        |____ dfs(nums = [1, 3] , path = [2] , result = [[1, 2, 3], [1, 3, 2]] )
        |      |___dfs(nums = [3] , path = [2, 1] , result = [[1, 2, 3], [1, 3, 2]] )
        |      |    |___dfs(nums = [] , path = [2, 1, 3] , result = [[1, 2, 3], [1, 3, 2], [2, 1, 3]] ) # added a new permutation to the result
        |      |___dfs(nums = [1] , path = [2, 3] , result = [[1, 2, 3], [1, 3, 2], [2, 1, 3]] )
        |           |___dfs(nums = [] , path = [2, 3, 1] , result = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1]] ) # added a new permutation to the result
        |____ dfs(nums = [1, 2] , path = [3] , result = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1]] )
            |___dfs(nums = [2] , path = [3, 1] , result = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1]] )
            |    |___dfs(nums = [] , path = [3, 1, 2] , result = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2]] ) # added a new permutation to the result
            |___dfs(nums = [1] , path = [3, 2] , result = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2]] )
                |___dfs(nums = [] , path = [3, 2, 1] , result = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]] ) # added a new permutation to the result
    Time complexity: O(N!)
    Space complexity: O(N)
    """
    def dfs(nums, path):
        if not nums:
            res.append(path)
            # return # backtracking
        for i in range(len(nums)):
            dfs(nums[:i] + nums[i + 1:], path + [nums[i]])

    res = []
    dfs(nums, [])
    return res



