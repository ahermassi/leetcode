""" You are given two integer arrays nums1 and nums2 sorted in ascending order and an integer k.
Define a pair (u,v) which consists of one element from the first array and one element from the second array.
Find the k pairs (u1,v1),(u2,v2) ...(uk,vk) with the smallest sums. """

from heapq import heappush, heappop
import unittest2 as unittest


def k_smallest_pairs(nums1, nums2, k):
    """ It is helpful to visualize the input as a N x M matrix of sums, for example nums1= [1, 7, 11], nums2 = [2, 4, 6]:

            2   4   6
            +------------
          1 |  3   5   7
          7 |  9  11  13
         11 | 13  15  17

         Because the arrays are sorted, the pair with the smallest sum is undoubtedly the one in the top left corner,
         with sum 3. The next pair with a sum that is just greater than (or equal to) the sum of the previous pair would
         be formed by selecting either the first element of nums1 and the second element of nums2, (1, 4), or the second
         element of nums1 and the first element of nums2, (7, 2), whichever has smaller sum. We only need to look at
         these two pairs because the sum of all the other pairs will be greater than this pair.

         We can keep a "horizon" of possible candidates, implemented as a heap / priority-queue, and roughly speaking
         we'll grow from the top left corner towards the right/bottom. We must store the information of the indices of
         nums1 and nums2 that lead to the formation of a particular sum in the heap in order to return the pair of
         integers.

         In the heap, we would store a triplet of integers: the pair's sum, the first element's index in nums1, and the
         second element's index in nums2.

         We start off only with the very first pairs of the first column of the matrix, consisting of the combinations
         of every number in nums1 and the first number in nums2, and we expand from there as needed.

         To obtain the minimum sum of a pair among all the pairs under consideration, the top of the heap is popped out.
         We save the triplet in _, i and j. We add the pair (nums1[i], nums2[j]) to the output. The next pair in the row
         at cell (i, j+1) gets added to the priority queue of current options.

         We know that each row and each column is sorted, and we want to expand to the right and down. When popping off
         the heap, we know we can just keep going rightward in the same row. The heap obviously guarantees that we only
         get the min element. It's impossible that sum(i + 1, j) < sum(i, j) or that sum(i + 1, j + 1) < sum(i + 1, j).

         For every number in nums1, its best partner (yields min sum) always starts from nums2[0] since arrays are
         sorted. For a specific number in nums1, its next candidate should be:

                [this specific number] + nums2[current_associated_index + 1]

         unless out of boundary.

         The logic in this implementation is actually similar to how we merge k sorted lists, where in this question the
         following are the k sorted lists:
         (1,2) -> (1,4) -> (1,6)
         (7,2) -> (7,4) -> (7,6)
         (11,2) -> (11,4) -> (11,6)

         Remember what we do to merge k sorted lists? We simply add the head of the list into the heap, and when a node
         is popped, we just add node.next.

    Time complexity: O(K logN), where N is the size of nums1. We do at most k heap pops.
    Space complexity: O(N), where N is the size of nums1
    """
    n, m = len(nums1), len(nums2)
    heap, res = [], []
    for i, num in enumerate(nums1):
        heappush(heap, (num + nums2[0], i, 0))
    while k and heap:
        _, i, j = heappop(heap)
        res.append([nums1[i], nums2[j]])
        if j < m - 1:
            # Offer a potential better pair.
            # The next better pair could with be A: [after(num1), num2] or B: [num1, after(num2)]
            # For A, we've already added top possible k into queue, so A is either in the queue already, or not
            # qualified. For B, it might be a better choice, so we add it to queue.
            heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
        k -= 1
    return res


class Test(unittest.TestCase):
    data = [([1, 7, 11], [2, 4, 6], 3, [[1, 2], [1, 4], [1, 6]]), ([1, 1, 2], [1, 2, 3], 2, [[1, 1], [1, 1]]),
            ([1, 2], [3], 3, [[1, 3], [2, 3]])]

    def test_k_smallest_pairs(self):
        for test_nums1, test_nums2, test_k, result in self.data:
            self.assertEqual(result, k_smallest_pairs(test_nums1, test_nums2, test_k))


if __name__ == '__main__':
    unittest.main()
