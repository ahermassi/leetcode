""" Given an array of positive integers arr (not necessarily distinct), return the lexicographically largest
permutation that is smaller than arr, that can be made with exactly one swap (A swap exchanges the positions of two
numbers arr[i] and arr[j]). If it cannot be done, then return the same array.
"""


def prev_perm_opt1(arr):
    """ This problem can be solved in a similar way (yet simpler) as 31- Next Permutation.
        If the array is already sorted in increasing order, the solution is the input array.
        If not, move from the right side of the array towards the left side looking for the longest increasing sequence
        (it's decreasing while scanning backwards), until the point where the left element is larger than the right
        element. At this point, the left element (let's call it 'left') is one of the elements that should be
        swapped. But to swap with what element?
        We actually need to swap 'left' with the largest value on its right side that is less than 'left' (let's call
        it 'right'). Since the elements on the right side of candid are all sorted, we can find the largest smaller
        number than 'left' with a simple scan.
        Example: arr = [1, 9, 5, 7, 9]
        left is at index 1 and should be swapped with the element at index 3: arr = [1, 9, 5, 7, 9]
        Note: In case of duplicate numbers, we need to swap 'left' with the leftmost largest smaller to reach a larger
        permutation. Example: arr = [3, 1, 1, 3]. left is at index 0 and should be swapped with the element (1) at
        index 1 not at index 2. This is because [1, 3, 1, 3] > [1, 1, 3, 3].
        Now borrowing the explanation from 31- Next Permutation:
        We observe that for any given sequence that is in ascending order, no previous permutation is possible.
        For example, no smaller permutation is possible for the following array: [1, 3, 4, 5, 9].
        We need to find the first pair of two successive numbers nums[i] and nums[i−1], from the right, which satisfy
        nums[i-1] > nums[i]. Now, no rearrangements to the right of nums[i-1] can create a smaller permutation since
        that subarray consists of numbers in ascending order. Thus, we need to rearrange the numbers to the left of
        nums[i-1] including itself.
        Now, what kind of rearrangement will produce the largest smaller number? We want to create the permutation just
        smaller than the current one. Therefore, we need to replace the number nums[i-1] with the number which is just
        smaller than itself among the numbers lying to its right section, say nums[j]. We swap the numbers nums[i−1]
        and nums[j].
        The key insight is that we want to decrease the permutation by as little as possible. Just like when we count
        up using numbers, we try to modify the rightmost elements and leave the left side unchanged. We will use the
        permutation (0, 3, 4, 5, 1, 2, 6) to develop this approach.
        Specifically, we start from the right, and look at the longest increasing suffix, which is (1, 2, 6)
        for our example. We cannot get the previous permutation just by modifying this suffix, since it is already the
        minimum it can be. Instead, we look at the entry e that appears just before the longest increasing suffix,
        which is 5 in this case. (If there's no such element, i.e., the longest increasing suffix is the entire
        permutation, return the permutation). Observe that e must be greater than some entries in the suffix
        (since the entry immediately after e is smaller than e). Intuitively, we should swap e with the largest entry
        s in the suffix which is smaller than e so as to minimize the change to the prefix.
        For our example, e is 5 and s is 2. Swapping s and e results in (0, 3, 4, 2, 1, 5, 6).
        We are done - the new permutation is the largest possible for all permutations smaller than the initial
        permutation.
        Summary:
        The general algorithm for computing the previous permutation is as follows:
            1- Find k such that p[k] > p[k+1] and entries after index k appear in increasing order.
            2- Find the largest p[l] such that p[l] < p[k] (such an l must exist since p[k] > p[k+1])
            3- Swap p[l] and p[k] (note that the sequence after position k remains in increasing order).
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(arr)
    i = n - 1
    while i > 0 and arr[i - 1] <= arr[i]:
        i -= 1
    if i == 0:
        return arr
    left, right = i - 1, n - 1
    while right > left:
        # Find the largest arr[right] and smallest 'right' that makes arr[right] < arr[left], where right > left
        if arr[right] < arr[left] and arr[right] != arr[right - 1]:
            break
        right -= 1
    arr[left], arr[right] = arr[right], arr[left]
    return arr
