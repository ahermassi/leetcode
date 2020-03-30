""" Given a list of daily temperatures, return a list such that, for each day in the input, tells you how many days
you would have to wait until a warmer temperature. If there is no future day for which this is possible, put 0 instead.
Note: The length of temperatures will be in the range [1, 30000]. Each temperature will be an integer in the range
[30, 100]. """

import unittest2 as unittest


def daily_temperatures_v1(temperatures):
    """ The logic is similar to 503- Next Greater Element II.
        We use a stack to store the indices to which we have not found answers yet. The stack is monotonous as we keep
        the indices of a decreasing sub-sequence.
        We iterate over the temperatures array from left to right. We push the index i of an element to the stack if it
        is less than the element on the top of the stack. Whenever we encounter a temperature x = temperatures[i]
        greater than temperatures[stack[-1] (don't forget that the stack stores indices not values), we pop all indices
        that correspond to temperatures less than x, and for each popped index j, its result is (i - j).
    Time complexity: O(N), a specific index can only be pushed once (as i) and can only be popped once (as j). The
    total number of times the body of the while loop executes cannot be greater than N
    Space complexity: O(N)
    """
    stack, res = [], [0] * len(temperatures)
    for i, val in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < val:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res


def daily_temperatures_v2(temperatures):
    """ We can also process the temperatures list backwards.
        If the temperature at current index i is smaller than the one seen at the previous index sitting on top of the
        stack, we simply get the difference of the indices (stack[-1] - i) and insert i into the stack.
        If the temperature at current index i is smaller than the one seen at the previous index sitting on top of the
        stack, we keep removing all the indices (since we need to find a greater temperature larger). If found, then
        great. If not, then it has result 0.
        One great reason we can just remove the smaller indices from the stack (seen to the right) is that now when we
        encounter a temperature x that is larger than its right elements, x will itself be the nearest largest
        temperature to the current one.
        Example: temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
        i = 7, stack = [7 (73)]. res[i] = 0
        i = 6, stack = [6 (76)]. ans[i] = 0
        i = 5, stack = [5 (72), 6 (76)]. ans[i] = 1
        i = 4, stack = [4 (69), 5 (72), 6 (76)]. ans[i] = 1
        i = 3, stack = [3 (71), 5 (72), 6 (76)]. ans[i] = 2
        i = 2, stack = [2 (75), 6 (76)]. ans[i] = 4
        i = 1, stack = [1 (74), 2 (75), 6 (76)]. ans[i] = 1
        i = 0, stack = [0 (73), 1 (74), 2 (75), 6 (76)]. ans[i] = 1
        Note that the final stack is increasing as opposed to the previous solution which leaves a decreasing stack.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(temperatures)
    stack, res = [], [0] * n
    for i in reversed(range(n)):
        while stack and temperatures[i] >= temperatures[stack[-1]]:
            stack.pop()
        if stack:
            res[i] = stack[-1] - i
        stack.append(i)
    return res


class Test(unittest.TestCase):
    data = [([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0])]

    def test_daily_temperatures(self):
        for test_temperatures, result in self.data:
            self.assertEqual(result, daily_temperatures_v1(test_temperatures))
            self.assertEqual(result, daily_temperatures_v2(test_temperatures))


if __name__ == '__main__':
    unittest.main()
