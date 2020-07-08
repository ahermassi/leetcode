""" Given an array nums, there is a sliding window of size k which is moving from the very left of the array to the
very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
Return the max sliding window.
Follow up:
Could you solve it in linear time? """

from collections import deque
import unittest2 as unittest


def max_sliding_window(nums, k):
    """ Monotonous decreasing queue.
        We scan the array ,and keep 'promising' elements in the deque. At each index i, we keep 'promising' elements,
        which are potentially max elements in window [i-k+1,i] or any subsequent window. This means:
            1- If an element in the deque and it is out of (i - k + 1), we discard it. We just need to poll from the
               head as we are using a deque and elements are ordered as the sequence in the array.
            2- Now only those elements within nums[i-k+1,i] are in the deque. We then discard elements smaller than
               nums[i] from the tail. This is because if nums[x] < nums[i] and x < i, then nums[x] has no chance to be
               the max in nums[i-k+1,i], or any other subsequent window: nums[i] would always be a better candidate.
            3- As a result, elements in the deque are ordered in both sequence in array and their value. At each step,
               the head of the deque is the max element of the window.
        To summarize:
        We maintain a deque of the largest elements we've seen (aka 'good candidates').
        The problem is that we need to maintain sanity of this deque. To this end we need to make sure about two things:
            - Deque should NEVER point to elements smaller than current element
            - Deque should NEVER point to elements outside our sliding window
        Then the first deque element is the largest window value.
        At each index i:
            - Pop (from the front) the element at index i - k if it's still in the deque (it falls out of the window)
            - Pop (from the end) the smaller elements (they'll be useless)
            - Append the current element
            - If our window has reached size k (i >= k-1), append the current window maximum to the output (deque front)
        The elements in the deque are from the current window and are decreasing. Then the first deque element is the
        the largest window value.
        Example: nums = [8, 3, -1, -3, 5, 3, 6, 7], k = 3
        
        i = 0, curr element = 8, deque = [], res = []
	    Add 8 to deque
	    
        i = 1, curr element = 3, deque = [8], res = []
	    Add 3 to deque
	    
        i = 2, curr element = -1, deque = [8, 3], res = []
	    Add -1 to deque
	    Append deque[0] = 8 to res

        i = 3, curr element = -3, deque = [8, 3, -1], res = [8]
        Pop left from deque because it's outside the window's leftmost (i-k)
	    Add -3 to deque
	    Append deque[0] = 3 to res

        i = 4, curr element = 5, deque = [3, -1, -3], res = [8, 3]
	    Pop from deque because deque.top < curr element
	    Pop from deque because deque.top < curr element
	    Pop from deque because deque.top < curr element
	    Add 5 to deque
	    Append deque[0] = 5 to res

        i = 5, curr element = 3, deque = [5], res = [8, 3, 5]
	    Add 3 to deque
	    Append deque[0] = 5 to res

        i = 6, curr element = 6, deque = [5, 3], res = [8, 3, 5, 5]
	    Pop from deque because deque.top < curr element
	    Pop from deque because deque.top < curr element
	    Add 6 to deque
	    Append deque[0] = 6 to res

        i = 7, curr element = 7, deque = [6], res = [8, 3, 5, 5, 6]
	    Pop from deque because deque.top < curr element
	    Add 7 to deque
	    Append deque[0] = 7 to res

        res = [8, 3, 5, 5, 6, 7]
    Time complexity: O(N), since each element is processed exactly twice - it's added and then removed from the deque
    Space complexity: O(k), for the deque
    """
    queue, res = deque(), []
    for i, num in enumerate(nums):
        if queue and queue[0] == nums[i - k]:  # The first/left element is out of the current window
            queue.popleft()
        while queue and queue[-1] < num:  # Remove from deque all elements that are smaller than current element 'num'
            queue.pop()
        queue.append(num)
        if i >= k - 1:  # i == k-1 is the beginning of a (first) full window
            res.append(queue[0])
    return res


class Test(unittest.TestCase):
    data = [([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7])]

    def test_max_sliding_window(self):
        for test_nums, test_k, result in self.data:
            self.assertEqual(result, max_sliding_window(test_nums, test_k))


if __name__ == '__main__':
    unittest.main()
