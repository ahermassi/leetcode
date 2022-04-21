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

        Now, our main objective is to keep the candidate temperatures on the stack that can be a next greater
        temperature for current index.

        For a current temperature at index i, we will check the top of the stack and see whether it has temperature
        that is greater than current element. Why we do this? Because stack is a LIFO, and we came from right direction,
        so the top of the stack will be the latest element/temperature that would have been pushed into the stack from
        the right of current index i. Here can be two cases:

        Case 1: When the temperature at top of stack is less than the current temperature, then this can never be a
        next greater element of current temperature OR ALL THE OTHER temperatures before current temperature.
        Why? Because for temperatures to the left of current temperature (at indices < i), temperature at current index
        can be their CANDIDATE for the next greater element. (I'm warmer than the guys to my right, so if anything
        I should be a better candidate for next warmer day for the guys to my left). Hence, we will simply pop the top
        of the stack until we find a warmer day or until the stack gets empty (This, means no greater elements to the
        right).

        Case 2: When we find a warmer day at the top of the stack, then we will simply consider that temperature as our
        next greater element and set the distance between the current temperature and next greater element/temperature
        as our answer for current index.

        Then we will simply push our current element into the stack as now this temperature can be a CANDIDATE
        for the next greater element of the temperatures to the left of current index.

        To summarize:

        For an element temperatures[i] encountered, we pop all the elements stack[top] from the stack such that
        temperatures[stack[top]] < temperatures[i]. We continue the popping till we encounter a stack[top] satisfying
        temperatures[stack[top]] >= temperatures[i]. Now, it is obvious that the current stack[top] only can act as the
        next greater element for temperatures[i].

        If no element remains on the top of the stack, it means no larger element than temperatures[i] exists to its
        right. Along with this, we also push the index of the element just encountered (temperatures[i]), i.e. i over
        the top of the stack, so that temperatures[i] (or stack[top]) now acts as the next greater element for the
        elements lying to its left.

        Example: temperatures = [73,74,75,71,69,72,76,73]


         i 	        T[i]	    stack	    ans	                                                                Description
        7	        73	    [7]	        [0,0,0,0,0,0,0,0]	        Stack was empty. So, we found no next warmer element for T[i]. Assign ans[7] = 0and push current day 7 to stack

        6	        76	    [6]	        [0,0,0,0,0,0,0,0]	        Stack's top's temp: 73 is less than today's temperature:76. So, pop it since it can't ever be next warmer element for any day.
                                                                                    Again, stack is empty and so there's not next warmer element for today. Assign ans[6] = 0and push current day 6 to stack

        5	        72	    [6,5]	        [0,0,0,0,0,1,0,0]	        Stack's top's temp: 76 is warmer than today's temperature:72. So assign ans[5] = 6-5 = 1. Then, push current day 5 to stack

        4	        69	    [6,5,4]	    [0,0,0,0,1,1,0,0]	        Stack's top's temp: 72 is warmer than today's temperature:69. So assign ans[4] = 6-5 = 1.and push current day 4 to stack

        3	        71	    [6,5,3]	    [0,0,0,2,1,1,0,0]	        Stack's top's temp: 69 is less than today's temperature:71. So pop it. Now, stack's top has greater temp so we break out of loop and assign
                                                                                    ans[3] = 5-3 = 2.and push current day 3 to stack

        2	        75	    [6,2]	        [0,0,4,2,1,1,0,0]	        Stack's top's temp: 71 is less than today's temperature:75. So pop it. Again, stack's top temp: 72 is less than 75. So, pop it again.
                                                                                    Now, stack's top temp is greater so we break out of loop and assign ans[2] = 6-2 = 4.and push current day 2 to stack

        1	        74	    [6,2,1]	    [0,1,4,2,1,1,0,0]	        Stack's top's temp: 75 is warmer than today's temperature:74. So assign ans[1] = 2-1 = 1.and push current day 1 to stack

        0	        73	    [6,2,1,0]	[1,1,4,2,1,1,0,0]	        Stack's top's temp: 74 is warmer than today's temperature:73. So assign ans[0] = 1-0 = 1.and push current day 0 to stack

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

        Next we have an index 6 for element of value 46. Nothing in the stack less than that, so no removals from the
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
