""" There are n people standing in a queue, and they numbered from 0 to n - 1 in left to right order. You are given
an array heights of distinct integers where heights[i] represents the height of the ith person.

A person can see another person to their right in the queue if everybody in between is shorter than both of them.
More formally, the ith person can see the jth person if i < j and min(heights[i], heights[j]) > max(heights[i+1],
heights[i+2], ..., heights[j-1]).

Return an array answer of length n where answer[i] is the number of people the ith person can see to their right in
the queue. """


def can_see_persons_count_v1(heights):
    """ Monotonic Stack. Similar to 503- Next Greater Element II.

        Intuition: You can see the right next greater element. Your left next greater element can see you.

        We maintain a decreasing monotonic stack (storing indices but their corresponding values are decreasing).
        As we iterate each element 'height' in input array 'heights', assume the last element in the stack has index i.

        If the last element heights[i] <= heights, then heights[i] can see 'height', so we increment res[i].
        Because 'height' is tall and blocks the line of sight, heights[i] can't see any element after 'height', so
        that concludes the work for heights[i]. Therefore, we pop it from the stack.

        We keep doing this while heights[i] < height, where i = stack's top. If after popping the stack is not empty,
        heights[i] will be the left next greater element of 'height'. heights[i] can still see 'height', so we
        increment res[i].

    Time complexity: O(N)
    Space complexity: O(N)
    """
    res = [0] * len(heights)
    stack = []
    for i, height in enumerate(heights):
        while stack and heights[stack[-1]] <= height:
            res[stack.pop()] += 1
        if stack:
            res[stack[-1]] += 1
        stack.append(i)
    return res
