""" You are given two integer arrays nums1 and nums2 sorted in ascending order and an integer k.
Define a pair (u,v) which consists of one element from the first array and one element from the second array.
Find the k pairs (u1,v1),(u2,v2) ...(uk,vk) with the smallest sums. """

from heapq import heappush, heappop
import unittest2 as unittest


def k_smallest_pairs(nums1, nums2, k):
    """ It is helpful to visualize the input as an nxm matrix of sums, for example nums1= [1, 7, 11], nums2 = [2, 4, 6]:

            2   4   6
            +------------
          1 |  3   5   7
          7 |  9  11  13
         11 | 13  15  17

        Of course the smallest pair overall is in the top left corner, the one with sum 3. We don't even need to look
        anywhere else. After including that pair in the output, the next smaller pair must be the next on the right
        (sum = 5) or the next below (sum = 9). We can keep a "horizon" of possible candidates, implemented as a heap /
        priority-queue, and roughly speaking we'll grow from the top left corner towards the right/bottom.
        We start off only with the very first pairs of the first column of the matrix, and we expand from there as
        needed. Whenever a pair at cell (i,j) is chosen into the output result, the next pair in the row at cell (i,j+1)
        gets added to the priority queue of current options.
        We know that each row and each column is sorted, and we want to expand to the right and down.
        When popping off the heap, we know we can just keep going rightward in the same row. The heap obviously
        guarantees that we only get the min element. It's impossible for sum(i + 1, j) < sum(i, j) or for
        sum(i + 1, j + 1) < sum(i + 1, j).
        For every numbers in nums1, its best partner (yields min sum) always starts from nums2[0] since arrays are
        sorted. For a specific number in nums1, its next candidate should be:
            [this specific number] + nums2[current_associated_index + 1]
        unless out of boundary.
        It is actually the same as how we merge k sorted lists, where in this question the following are the k sorted
        lists:
        (1,2) -> (1,4) -> (1,6)
        (7,2) -> (7,4) -> (7,6)
        (11,2) -> (11,4) -> (11,6)
        Remember how we do to merge k sorted lists? We simply add the head of the list into the heap, and when a node
        is popped, we just add the node.next.
    Time complexity: O(K logK), heap size <= k and we do at most k heappop
    Space complexity: O(N), where N is the length of nums1
    """
    if not nums1 or not nums2 or not k:
        return None
    heap, res, n, m = [], [], len(nums1), len(nums2)
    for i in range(n):
        heappush(heap, (nums1[i] + nums2[0], nums1[i], nums2[0], 0))
    while k and heap:
        s, num1, num2, index = heappop(heap)
        res.append([num1, num2])
        k -= 1
        if index < m - 1:
            heappush(heap, (num1 + nums2[index + 1], num1, nums2[index + 1], index + 1))  # Offer potential better pair.
            # Next better pair could with be A: [after(num1), num2] or B: [num1, after(num2)]
            # For A, we've already added top possible k into queue, so A is either in the queue already, or not
            # qualified. For B, it might be a better choice, so we offer it into queue
    return res


class Test(unittest.TestCase):
    data = [([1, 7, 11], [2, 4, 6], 3, [[1, 2], [1, 4], [1, 6]]), ([1, 1, 2], [1, 2, 3], 2, [[1, 1], [1, 1]]),
            ([1, 2], [3], 3, [[1, 3], [2, 3]])]

    def test_k_smallest_pairs(self):
        for test_nums1, test_nums2, test_k, result in self.data:
            self.assertEqual(result, k_smallest_pairs(test_nums1, test_nums2, test_k))


if __name__ == '__main__':
    unittest.main()
