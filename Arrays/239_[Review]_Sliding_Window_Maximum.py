""" Given an array nums, there is a sliding window of size k which is moving from the very left of the array to the
very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
Return the max sliding window.
Follow up:
Could you solve it in linear time? """

from collections import deque

# Video explanation: https://www.youtube.com/watch?v=DfljaUwZsOk
def max_sliding_window(nums, k):
    """
    Pattern: Monotonic decreasing deque — sliding window maximum.

    The goal is to find the maximum value in every window of size k.

    A normal deque can efficiently add and remove elements from both ends, but
    by itself it does not tell us the maximum. The key idea is that we do not
    need to keep every element in the current window.

    Instead, we keep only elements that are still useful candidates for being
    the maximum of the CURRENT or some FUTURE window.

    The deque stores indices, not values, because we need to know when an
    element has moved outside the current window.

    The indices in the deque are maintained so that their corresponding values
    are in monotonically decreasing order:

        nums[queue[0]] >= nums[queue[1]] >= nums[queue[2]] ...

    Therefore, the value at the FRONT of the deque is always the maximum of the
    current window.

    There are two ways an element in the queue can become useless:

    1. It expires from the window.

       If the index at the front is no longer inside the current window, remove
       it from the front.

       For a current index i and window size k, an index is expired when:

           i - queue[0] >= k

    2. It is dominated by the current element.

       Suppose an older element has value 3 and the current element has value 5:

           ... 3 ... 5

       Once 5 appears, 3 can never become the maximum of any future window.

       Why?

           - 5 is greater than 3.
           - 5 is newer than 3, so 3 will leave the window before 5.

       There can therefore never be a future window that contains 3 but does
       not also contain 5.

       So 3 is permanently useless as a maximum candidate and can be removed.

       More generally, before pushing the current element, we pop from the BACK
       while the current value is greater than or equal to the value there.

       We keep doing this because the current value may dominate several older
       candidates.

    After removing expired and dominated elements, we push the current index.

    Because all smaller/equal values behind the current value were removed
    before it was pushed, the deque naturally remains monotonically decreasing.

    Once we have processed at least k elements, the first complete window
    exists, and:

        nums[queue[0]]

    is its maximum.

    Example walkthrough:

        nums = [1, 3, -1, -3, 5]
        k = 3

        i = 0, num = 1

            queue is empty
            push index 0

            queue indices: [0]
            queue values:  [1]

            No complete window yet.


        i = 1, num = 3

            3 >= 1, so 1 is dominated.
            Pop index 0 from the back.

            Push index 1.

            queue indices: [1]
            queue values:  [3]

            No complete window yet.


        i = 2, num = -1

            -1 does not dominate 3, so nothing is popped.

            Push index 2.

            queue indices: [1, 2]
            queue values:  [3, -1]

            First complete window:

                [1, 3, -1]

            Front of deque = index 1 -> value 3

            result = [3]


        i = 3, num = -3

            Check expiration:

                i - queue[0] = 3 - 1 = 2

            Since 2 < k, index 1 is still inside the window.

            -3 does not dominate -1, so nothing is popped from the back.

            Push index 3.

            queue indices: [1, 2, 3]
            queue values:  [3, -1, -3]

            Current window:

                [3, -1, -3]

            Front = 3

            result = [3, 3]


        i = 4, num = 5

            First remove expired indices.

                4 - 1 = 3 >= k

            So index 1 has left the window.
            Pop it from the front.

            queue values are now:

                [-1, -3]

            Now remove dominated candidates from the back:

                5 >= -3 -> pop -3
                5 >= -1 -> pop -1

            Push index 4.

            queue indices: [4]
            queue values:  [5]

            Current window:

                [-1, -3, 5]

            Front = 5

            result = [3, 3, 5]


    The reusable invariant is:

        Front:
            remove candidates that expired from the window.

        Back:
            remove candidates dominated by the new element
            because the new element is greater/equal and newer.

        Push current index.

        Front of deque = maximum of the current window.

    Time complexity: O(N). Each index is pushed into the deque once and removed
    at most once. Even though there are while loops, there are only O(N) total
    deque removals across the entire traversal.
    Space complexity: O(K). The deque contains only indices that are still
    inside the current window, so it can contain at most K indices.
    """
    queue = deque()
    res = []
    for i, num in enumerate(nums):
        # Remove indices that have fallen out of the left side of the window.
        while queue and i - queue[0] >= k:
            queue.popleft()
        # Remove older candidates that the current value dominates.
        while queue and num >= nums[queue[-1]]:
            queue.pop()
        queue.append(i)
        # Once the first complete window exists, the front is its maximum.
        if i >= k - 1:
            res.append(nums[queue[0]])
    return res
