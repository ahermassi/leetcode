""" Given a list of daily temperatures, return a list such that, for each day in the input, tells you how many days
you would have to wait until a warmer temperature. If there is no future day for which this is possible, put 0 instead.
Note: The length of temperatures will be in the range [1, 30000]. Each temperature will be an integer in the range
[30, 100]. """

import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=cTBiBSnjO3c


def daily_temperatures_v1(temperatures):
    """ The logic is similar to 503- Next Greater Element II.

        A monotonic stack is simply a stack where the elements are always in sorted order. How does this help us?

        We can use a monotonic decreasing stack to hold temperatures. Monotonic decreasing means that the stack will
        always be sorted in descending order. Because the problem is asking for the number of days, instead of storing
        the temperatures themselves, we should store the indices of the days, and use temperatures[i] to find the
        temperature of the ith day.

        Monotonic stacks are a good option when a problem involves comparing the size of numeric elements, with their
        order being relevant.

        On each day, there are two possibilities. If the current day's temperature is not warmer than the temperature on
        the top of the stack, we can just push the current day onto the stack - since it is not as warm (equal or smaller).
        This will maintain the sorted property.

        If the current day's temperature is warmer than the temperature on top of the stack, this is significant.
        It means that the current day is the FIRST day with a warmer temperature than the day associated with the
        temperature on top of the stack. When we find a warmer temperature, the number of days is the difference
        between the current index and the index on the top of the stack. We can declare an answer array before
        iterating through the input and populate answer as we go along.

        When we find a warmer temperature, we can't stop after checking only one element at the top. Using the
        example temperatures = [75, 71, 69, 72], once we arrive at the last day our stack looks like stack = [0, 1, 2].
        For clarity, here's what the stack looks like with each temperature associated with the day:
        stack = [(0, 75), (1, 71), (2, 69)]. 72 (the current temperature) is greater than 69, but it is also greater than
         71. To make sure we don't miss any days, we should pop from the stack until the top of the stack is no longer
         colder than the current temperature. Once that is the case, we can push the current day onto the stack.

    Time complexity: O(N), a specific index can only be pushed once (as i) and can only be popped once (as j). The
    total number of times the body of the while loop executes cannot be greater than N
    Space complexity: O(N), if the input was non-increasing, then no element would ever be popped from the stack,
    and the stack would grow to a size of N elements at the end.
    """
    stack, res = [], [0] * len(temperatures)
    for i, temperature in enumerate(temperatures):
        while stack and temperature > temperatures[stack[-1]]:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res


def daily_temperatures_v2(temperatures):
    """ We can also process the temperatures list backwards.
        If the temperature at current index i is smaller than the one seen at the previous index sitting on top of the
        stack, we simply get the difference of the indices (stack[-1] - i) and insert i into the stack.
        If the temperature at current index i is greater than the one seen at the previous index sitting on top of the
        stack, we keep removing all the indices (since we need to find a greater temperature larger). If found, then
        great. If not, then it has result 0.
        One great reason we can just remove the smaller indices from the stack (seen to the right) is that now when we
        encounter a temperature x that is larger than its right elements, x will itself be the nearest largest
        temperature to the current one.
        For an element temperatures[i] encountered, we pop all the elements stack[top] from the stack such that
        temperatures[stack[top]] < temperatures[i]. We continue the popping till we encounter a stack[top] satisfying
        temperatures[stack[top]] >= temperatures[i]. Now, it is obvious that the current stack[top] only can act as the
        next greater element for temperatures[i].
        If no element remains on the top of the stack, it means no larger element than temperatures[i] exists to its
        right. Along with this, we also push the index of the element just encountered (temperatures[i]), i.e. i over
        the top of the stack, so that temperatures[i] (or stack[top]) now acts as the next greater element for the
        elements lying to its left.
        Example: temperatures = [89, 62, 70, 58, 47, 47, 46, 76, 100, 70].
        Our first element in the stack is going to be 9 (index of 70, the last element) and our initial condition will
        be:
            {9} //stack
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0} //result vector
        We then move to the penultimate element (index 8) and since its matching element is bigger than the one in
        the stack, we remove it, we do not update the result vector (there is nothing bigger right of it) and push it
        in the stack:
            {8} //stack
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0} //result vector
        Okay, next is index 7, matching element of value 76: Since we have something in the stack which is bigger than
        that, we update the 8th element (the one with index 7, again) of the result vector with the difference between
        the current element and the top of the stack and move on after pushing it too:
            {7, 8} //stack
            {0, 0, 0, 0, 0, 0, 0, 1, 0, 0} //result vector
        Next we have index 6 for element of value 46. Nothing in the stack less than that, so no removals from the
        stack, we update the distance from the next bigger (the previous element) and we just push it:
            {6, 7 , 8} //stack
            {0, 0, 0, 0, 0, 0, 1, 1, 0, 0} //result vector
        We move to index 5 and matching value 47. This time we pop until we have no greater values (so, just once) and
        update the vector with the distance (the next bigger was 2 positions to the right), before pushing it in the
        stack:
            {5, 7 , 8} //stack
            {0, 0, 0, 0, 0, 2, 1, 1, 0, 0} //result vector
        Now, an interesting case: Index 4 matches another identical value, but identical is not greater than, so we pop
        all the way up to a value greater than 47, update the vector with the computed distance, push the element into
        the stack:
            {4, 7 , 8} //stack
            {0, 0, 0, 0, 3, 2, 1, 1, 0, 0} //result vector
        After the last few steps:
            {8} //stack
            {8, 1, 5, 4, 3, 2, 1, 1, 0, 0} //result vector
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
