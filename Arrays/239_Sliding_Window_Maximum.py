""" Given an array nums, there is a sliding window of size k which is moving from the very left of the array to the
very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
Return the max sliding window.
Follow up:
Could you solve it in linear time? """

from collections import deque
import unittest2 as unittest


def max_sliding_window_v1(nums, k):
    """ Monotonic Decreasing Queue.

        Monotonic queue is like a regular queue with one key distinction in the enqueue operation: Before we push a new
        element onto the queue, we first check if adding it breaks the monotonic condition. If it does, then we pop
        the tail elements off the queue until pushing the new element no longer breaks the monotonic condition.

        Intuition: A question we can ask ourselves is "do we need to keep all the window elements in our state?"
        An important observation is for two elements arr[left] and arr[right], where left < right, arr[left] leaves the
        window earlier as we slide. If arr[right] is larger than arr[left], then there is no point keeping arr[left] in
        our window since arr[right] is always going to be larger during the time arr[left] is in the window.
        Therefore, arr[left] can never be the maximum and can be safely discarded.

        It is implicitly ensured that the front of the queue will have the largest element of the sliding window because
        any elements smaller than it would have already been dropped when it entered the queue.

        We scan the array and keep 'promising' elements in the queue. At each index i, we keep 'promising' elements,
        which are potentially max elements in window [i-k+1,i] or any subsequent window. This means:

            - If an element in the queue is outside (i - k + 1), we discard it. We just need to poll
              from the head as we are using a deque and elements are ordered as the sequence in the array.
            - Now only those elements within nums[i-k+1,i] are in the queue. We then discard elements smaller
              than nums[i] from the tail. This is because if j < i and nums[j] < nums[i], then nums[j] has no
              chance of being the max in nums[i-k+1,i] or any other subsequent window: nums[i] would always be
              a BETTER CANDIDATE.
            - As a result, elements in the queue are ordered in both sequence in array and their value.
              At each step, the head of the deque is the max element of the window.

        To summarize:
        We maintain a queue of the largest elements we've seen so far (aka 'good candidates').
        The problem is that we need to maintain sanity of this queue. To this end, we need to make sure that the queue:
            - Should NEVER point to elements smaller than current element
            - Should NEVER point to elements outside the current sliding window
        We want to ensure that the queue window only has decreasing elements. That way, the leftmost element is always
        the largest in the current window.

        At each index i:
            - Pop (from the front/right) the element at index (i-k) if it's still in the queue (falls outside the window)
            - Pop (from the end/left) the smaller elements (they'll be useless)
            - Append the current element
            - If our window has reached size k (i >= k-1), append the current window maximum to the output (queue front)
        The elements in the queue are from the current window and are decreasing. Then the first queue element is
        the largest window value.

        More formally:
        Let D be the deque which maintains a pair (i, a_i). An important property of D that we will maintain is that
        elements in D will always be in sorted order (invariant). We will first start with an empty D, and will insert
        a_i and remove elements from D accordingly as we iterate from the left to the right of array.
        Suppose that we are now at index i and considering adding a_i. Notice that when a_i is added, all elements
        (j, a_j) in D such that a_j is smaller than a_i can never be a maximum value as we go forward, hence they can be
        removed from D. Furthermore, if the element (i-k-1, a(i−k−1)) is in D (which will be located at the front of D
        if it exists), we remove that element as well. Lastly, we append a_i at the back of D. Then we will have the
        maximum as the top element in D when we reach index i. Since each element will enter and leave D only once,
        we have a total of O(N) operations.

        Example: nums = [8, 3, -1, -3, 5, 3, 6, 7], k = 3
        
        i = 0, curr element = 8, queue = [], res = []
	    Add 8 to queue
	    
        i = 1, curr element = 3, queue = [8], res = []
	    Add 3 to queue
	    
        i = 2, curr element = -1, queue = [8, 3], res = []
	    Add -1 to queue
	    Append queue[0] = 8 to res

        i = 3, curr element = -3, queue = [8, 3, -1], res = [8]
        Pop left from queue because it's outside the window's leftmost (i-k)
	    Add -3 to queue
	    Append queue[0] = 3 to res

        i = 4, curr element = 5, queue = [3, -1, -3], res = [8, 3]
	    Pop from queue because queue.top < curr element
	    Pop from queue because queue.top < curr element
	    Pop from queue because queue.top < curr element
	    Add 5 to queue
	    Append queue[0] = 5 to res

        i = 5, curr element = 3, queue = [5], res = [8, 3, 5]
	    Add 3 to queue
	    Append queue[0] = 5 to res

        i = 6, curr element = 6, queue = [5, 3], res = [8, 3, 5, 5]
	    Pop from queue because queue.top < curr element
	    Pop from queue because queue.top < curr element
	    Add 6 to queue
	    Append queue[0] = 6 to res

        i = 7, curr element = 7, queue = [6], res = [8, 3, 5, 5, 6]
	    Pop from queue because queue.top < curr element
	    Add 7 to queue
	    Append queue[0] = 7 to res

        res = [8, 3, 5, 5, 6, 7]
    Time complexity: O(N), since each element is processed exactly twice - it's added and then removed from the queue
    Space complexity: O(k), for the queue
    """
    queue, res = deque(), []
    for i, num in enumerate(nums):
        if queue and queue[0] == nums[i - k]:  # The first/left element is outside the current window
            queue.popleft()
        while queue and queue[-1] < num:  # Remove from queue all elements that are smaller than current element 'num'
            queue.pop()
        queue.append(num)
        if i >= k - 1:  # i == k-1 is the beginning of a (first) full window
            res.append(queue[0])
    return res


def max_sliding_window_v2(nums, k):
    """ Similar to previous solution, but we store indices instead of actual elements in the queue. This is because we
        need the index to know if an element is outside the boundaries of the window and we can always get the value
        using the index from the array.
    Time complexity: O(N)
    Space complexity: O(k)
    """
    queue = deque()
    res = []
    for i, num in enumerate(nums):
        if queue and queue[0] == i - k:
            queue.popleft()
        while queue and nums[queue[-1]] < num:
            queue.pop()
        queue.append(i)
        if i >= k - 1:
            res.append(nums[queue[0]])
    return res


class Test(unittest.TestCase):
    data = [([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7])]

    def test_max_sliding_window(self):
        for test_nums, test_k, result in self.data:
            self.assertEqual(result, max_sliding_window_v1(test_nums, test_k))
            self.assertEqual(result, max_sliding_window_v2(test_nums, test_k))


if __name__ == '__main__':
    unittest.main()
