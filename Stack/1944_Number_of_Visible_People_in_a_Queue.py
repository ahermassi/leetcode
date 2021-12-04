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


def can_see_persons_count_v2(heights):
    """ Similar to the previous approach, but we process the input array going backwards.

        We use a monotonic stack which stores heights in increasing order.
        For each person, we remove all smaller heights from the stack, increasing number of people this person can see.
        If there is a larger height in the stack, we can see one more person.
        Finally, we push the current person's height to the stack.

        So we traverse from right to left, with a stack maintained such that at each person, we pop out all the people
        who have heights less than the current person. All these popped out people will be visible to the current
        person, so count the people we have popped out. If the stack is non-empty, then we can also see the person
        who's currently at the top of the stack because everyone between them had shorter height. The thing to realize
        is that there won't be any other person visible. Because right now, we just popped out all the people who are
        gonna be masked by the current person in the future. Similarly, every person we didn't pop out and comes to the
        right would be masked by some person.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(heights)
    res, stack = [0] * n, []
    for i in reversed(range(n)):
        height = heights[i]
        while stack and stack[-1] <= height:
            stack.pop()  # ith person will obscure the shorter people on the right side. Remove shorter people on the
            # right side because they can't be seen anymore.
            res[i] += 1  # ith person can see those shorter people
        if stack:
            # If stack is not empty then ith person can see one more person which is taller than him
            res[i] += 1
        stack.append(height)
    return res
