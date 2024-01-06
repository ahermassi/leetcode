""" Given a collection of distinct integers, return all possible permutations. """


# Video explanation: https://www.youtube.com/watch?v=GCm7m5671Ps
def permute_v1(nums):
    """ Backtracking is an algorithm for finding all solutions by exploring all potential candidates. If the solution
         candidate turns to be not a solution (or at least not the last one), backtracking algorithm discards it by
         making some changes on the previous step, i.e. backtrack and then try again.

         In backtracking, we generate all solutions one element at a time. This problem is asking us to generate all
         possible permutations, so we will generate permutations one element at a time.

         To generate a permutation one element at a time, we will use an array 'path' that represents the current
         permutation we are building. To start, we add the first element in nums. We have path = [nums[0]]. We are
         LOCKING in this first value, and we will now find all permutations that start with nums[0].

        To find all permutations that start with nums[0], we start by adding the next element, which is nums[1]. We now
        have path = [nums[0], nums[1]]. We are LOCKING in this second element, and we will now find all permutations
         that start with [nums[0], nums[1]].

        This continues until we use all elements, i.e. path.length == nums.length. Let's say that we have finished
        finding all permutations that start with [nums[0], nums[1]]. Now what? We backtrack by removing nums[1], and we
        have path = [nums[0]] again. Now, we add the second element that comes after nums[0], which is nums[2]. We have
        path = [nums[0], nums[2]], and now we need to find all permutations that start with [nums[0], nums[2]].

        Once we find all the permutations that start with [nums[0]], we backtrack by removing nums[0] from path and
        adding the next element. We have path = [nums[1]], and now we need to find all permutations that start with
        nums[1].

        This process is recursive in nature. Each time we add an element, we solve a new version of the problem (find
        all permutations that start with 'path'). The initial version of the problem is to find all permutations that
        start with [], which represents all possible permutations.

        To summarize: try all numbers in the first position. For each number in the first position, try all other
        numbers in the second position. For each pair of numbers in the first and second positions, try all other
        numbers in the third position, and so on.

        We use a backtracking function which takes as argument the index of the first integer to consider.

            - If the current integer has an index n, that means that the current permutation is finished.
            - Otherwise, iterate over the integers from the current index to index (n - 1).
                - Place ith integer first in the permutation, i.e. swap(nums[index], nums[i]).
                - Proceed to create all permutations which starts from ith integer : backtrack(index + 1).
                - Now backtrack, i.e. swap(nums[index], nums[i]) back.

        A good approach is to recognize that once a value has been chosen for an entry, we do not want to repeat it.
        Specifically, every permutation of A begins with one of A[0],A[1] ,. . . ,A[n - 1]. The idea is to generate all
        permutations that begin with A[0], then all permutations that begin with A[1], and so on.

        Computing all permutations beginning with A[0] entails computing all permutations of A[1,n - 1], which suggests
        the use of recursion.

        To compute all permutations beginning with A[1], we swap A[0] with A[1] and compute all permutations
        of the updated A[1.,n - 1]. We then restore the original state before embarking on computing all permutations
        beginning with A[2], and so on.

        For example, for the array [7, 3, 5], we would first generate all permutations starting with 7. This entails
        generating all permutations of [3, 5], which we do by finding all permutations of [3, 5] beginning with 3.
        Since [5] is an array of length 1, it has a single permutation. This implies [3, 5] has a single permutation
        beginning with 3. Next we look for permutations of [3, 5] beginning with 5. To do this, we swap 3 and 5, and
        find, as before, there is a single permutation of [3, 5] beginning with 5, namely,[5, 3]. Hence,there are two
        permutations of A beginning with 7, namely [7, 3, 5] and [7, 5, 3].
        We swap 7 with 3 to find all permutations beginning with 3, namely [3, 7, 5] and [3, 5, 7].
        The last two permutations we add are [5, 3, 7] and [5, 7, 3].
        There are six permutations in total.

    Time complexity: O(N * N!), we generate N! permutations and there is a loop inside the recursive call which in the
    worst case makes N iterations. This can be seen in this way: To find a single permutation it takes N computations
    (height of recursion tree), and there are N! permutations in total
    Space complexity: O(N), for the recursive call stack (max depth of call tree)
    """
    def compute_permutations_at_index(index, path):
        if index == n:
            res.append(path)
            return
        for i in range(index, n):
            # We're using here the same principle of recursion. Given a subarray starting at index 'index', loop over
            # the elements of the subarray, and at each iteration:
            # 1- Bring the current element to the head of the subarray at starting index 'index'
            # 2- TRUST that the recursive call will compute the permutations of the subarray at (index + 1)
            # 3- Undo the swap to bring the subarray to its initial state and move on to the next element
            nums[index], nums[i] = nums[i], nums[index]
            compute_permutations_at_index(index + 1, path + [nums[index]])
            nums[index], nums[i] = nums[i], nums[index]  # Second swap: backtracking. Think of it as moving back up
            # in the tree to explore the next branch. When we moved down one level, we swapped 2 elements (1st
            # swap in the code). So when we go back up in the tree we need to swap these 2 elements back to their
            # original order at the parent node level (2nd swap in the code). This is called backtracking = done
            # exploring a branch, let's go back up and explore more branches.

    n, res = len(nums), []
    compute_permutations_at_index(0, [])
    return res


def permute_v2(nums):
    """ Second solution.

        Visualization:

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
            # return
            # backtracking
        for i in range(len(nums)):
            dfs(nums[:i] + nums[i + 1:], path + [nums[i]])

    res = []
    dfs(nums, [])
    return res



