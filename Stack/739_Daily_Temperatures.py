""" Given a list of daily temperatures, return a list such that, for each day in the input, tells you how many days
you would have to wait until a warmer temperature. If there is no future day for which this is possible, put 0 instead.
Note: The length of temperatures will be in the range [1, 30000]. Each temperature will be an integer in the range
[30, 100]. """

import unittest2 as unittest


# Video explanation: https://youtu.be/cTBiBSnjO3c
def daily_temperatures_v1(temperatures):
    """ The logic is similar to 503- Next Greater Element II.

         Imagine if we had multiple days in a row with decreasing temperatures, and then one very hot day -
         [40, 39, 38, 37, 36, 35, 34, 65]. The final day is the "answer" day for all the other days. Why? Because all
         the other days are in descending order (and cooler than the last day). If we make use of the fact that
         temperatures in descending order can share the same "answer" day, we can improve the time complexity.

         In the above example, we can "delay" finding the answer for the first 7 days, and upon finding a warmer
         temperature of 65 we can move backward to find the answer for all 7 days at the same time. This process of
         storing elements and then walking back through them matches the behavior of a stack.

         A monotonic stack is simply a stack where the elements are always in sorted order. How does this help us?

         We can use a monotonic decreasing stack to hold temperatures. Monotonic decreasing means that the stack will
         always be sorted in descending order. Because the problem is asking for the number of days, instead of storing
         the temperatures themselves, we store the indices of the days, and use temperatures[i] to find the temperature
         of the ith day.

         Monotonic stacks are a good option when a problem involves comparing the size of numeric elements, with their
         order being relevant.

         On each day, there are two possibilities:

            - If the current day's temperature is not warmer than the temperature at the top of the stack, we can just
               push the current day to the stack - since it is not as warm (equal or smaller). This will maintain the
               sorted property.

            - If the current day's temperature is warmer than the temperature at top of the stack, this is significant.
               It means that the current day is the FIRST day with a warmer temperature than the day associated with the
               temperature at the top of the stack. When we find a warmer temperature, the number of days is the
               difference between the current index and the index at the top of the stack.

         We can declare an answer list before iterating through the input and populate the list as we go.

         When we find a warmer temperature, we can't stop after checking only one element at the top of the stack.
         Using the example temperatures = [75, 71, 69, 72], once we arrive at the last day the stack looks like
         [0, 1, 2]. Here's what the stack looks like with each temperature associated with the day:
         [(0, 75), (1, 71), (2, 69)]. 72 (the current temperature) is greater than 69, but it is also greater than 71.
         To make sure we don't miss any days, we should pop from the stack until the top of the stack is no longer
         colder than the current temperature. Once that is the case, we can push the current day to the stack.

    Time complexity: O(N), a specific index can only be pushed once (as cur_index) and can only be popped once
    (as prev_index). Every iteration of the while loop uses 1 pop, which means the while loop will not iterate more than
    N times in total across all iterations of the for loop.
    Space complexity: O(N), if the input was non-increasing, then no element would ever be popped from the stack,
    and the stack would grow to a size of N elements at the end.
    """
    stack, res = [], [0] * len(temperatures)
    for cur_day, temperature in enumerate(temperatures):
        while stack and temperature > temperatures[stack[-1]]:
            prev_day = stack.pop()
            res[prev_day] = cur_day - prev_day
        stack.append(cur_day)
    return res


def daily_temperatures_v2(temperatures):
    """ With the monotonic stack, we iterated forward through the array and moved backwards when we found a warmer day.
         In this approach, we'll do the reverse - iterate backwards through the array, and move forwards to find the
         number of days until a warmer day.

         Our main objective is to keep the candidate temperatures on the stack that can be a next greater temperature for
         the current index.

         For a current temperature at index i, we check the top of the stack and see whether it has a temperature that
         is greater than the current one. Why do we do this? Because the stack is a LIFO structure, and we move from
         right, so the top of the stack will be the latest element/temperature that would have been pushed to the stack
         from the right of the current index i. There can be two cases:

            - 1) When the temperature at the top of the stack is less than the current temperature, then this can never
                   be a next greater element of the current temperature OR ALL THE OTHER temperatures before the current
                   temperature. Why? Because for temperatures to the left of the  current temperature (at indices < i),
                   the temperature at the current index can be their CANDIDATE for next greater element. (I'm warmer
                   than those to my right, so if anything I should be a better candidate for next warmer day for those
                   to my left). Hence, we simply pop the top of the stack until we find a warmer day or until the stack
                   becomes empty (this means there are no greater elements to the right).

            - 2) When we find a warmer day at the top of the stack, then we simply consider that temperature as the next
                   greater element and set the distance between the current temperature and the next greater temperature
                   as the answer for the current index.

         Then we simply push the current temperature to the stack as now this temperature can be a CANDIDATE for next
         greater element of the temperatures to the left of the current index.

         To summarize:

         For temperatures[i], we pop all the elements of the stack such that temperatures[stack[top]] < temperatures[i].
         We keep popping until we encounter a stack[top] satisfying temperatures[stack[top]] >= temperatures[i].
         Now, it is obvious that the current stack[top] can only act as the next greater element for temperatures[i].

         If no element remains at the top of the stack, it means no temperature greater than temperatures[i] exists to
         its right. Along with this, we also push the index of the current temperature (temperatures[i]) to the stack,
         so that temperatures[i] (or stack[top]) now acts as the next greater element for the temperatures to its left.

        Example: temperatures = [73,74,75,71,69,72,76,73]


         i 	        T[i]	    stack	    res	                                                                Description
        7	        73	    [7]	        [0,0,0,0,0,0,0,0]	        Stack was empty, so we have no next warmer temperature for T[i]. Assign res[7] = 0 and push the current day (7) to the stack.

        6	        76	    [6]	        [0,0,0,0,0,0,0,0]	        Stack's top temperature (73) is less than today's temperature (76), so pop it since it can never be the next warmer temperature for
                                                                                    any day. Again, the stack is empty and so there's no next warmer temperature for today. Assign res[6] = 0 and push current day (6) to the stack.

        5	        72	    [6,5]	        [0,0,0,0,0,1,0,0]	        Stack's top temperature (76) is warmer than today's temperature (72). So assign res[5] = 6-5 = 1 and push the current day (5) to the stack.

        4	        69	    [6,5,4]	    [0,0,0,0,1,1,0,0]	        Stack's top temperature (72) is warmer than today's temperature (69). So assign res[4] = 6-5 = 1 and and push the current day (4) to the stack.

        3	        71	    [6,5,3]	    [0,0,0,2,1,1,0,0]	        Stack's to temperature (69) is less than today's temperature (71), so pop it. Now, stack's top has a greater temperature so we break out of the
                                                                                    loop and assign res[3] = 5-3 = 2 and push the current day (3) to the stack.

        2	        75	    [6,2]	        [0,0,4,2,1,1,0,0]	        Stack's top' temperature (71) is less than today's temperature (75), so pop it. Again, stack's top temperature (72) is less than 75, so pop it again.
                                                                                    Now, stack's top temperature is greater, so we break out of the loop and assign res[2] = 6-2 = 4 and push the current day (2) to the stack.

        1	        74	    [6,2,1]	    [0,1,4,2,1,1,0,0]	        Stack's top temperature (75) is warmer than today's temperature (74), so assign res[1] = 2-1 = 1 and push the current day (1) to the stack.

        0	        73	    [6,2,1,0]	[1,1,4,2,1,1,0,0]	        Stack's top temperature (74) is warmer than today's temperature (73), so assign res[0] = 1-0 = 1 and push the current day (0) to the stack

        Example: temperatures = [89, 62, 70, 58, 47, 47, 46, 76, 100, 70].

        The first element in the stack is going to be 9 (index of 70, the last element), and the initial condition will
        be:
            {9} //stack
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0} //result vector

        We then move to the penultimate element (index 8), and since its matching element is bigger than the one in
        the stack, we remove it, we do not update the result vector (there is nothing bigger to its right), and push it
        to the stack:
            {8} //stack
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0} //result vector

        Next is index 7, matching element of value 76. Since we have something in the stack which is bigger than that,
        we update the 8th element (the one with index 7, again) of the result vector with the difference between the
        current element and the top of the stack and move on after pushing it too:
            {7, 8} //stack
            {0, 0, 0, 0, 0, 0, 0, 1, 0, 0} //result vector

        Next, we have an index 6 for element of value 46. Nothing in the stack is less than that, so no removals from
        the stack. We update the distance from the next bigger (the previous element) and we just push it:
            {6, 7 , 8} //stack
            {0, 0, 0, 0, 0, 0, 1, 1, 0, 0} //result vector

        We move to index 5 and its matching value 47. This time we pop until we have no greater values (so just once)
        and update the vector with the distance (the next bigger was 2 positions to the right), before pushing it to the
        stack:
            {5, 7 , 8} //stack
            {0, 0, 0, 0, 0, 2, 1, 1, 0, 0} //result vector

        Now, an interesting case: Index 4 matches another equal value, but equal is not greater than, so we pop all the
        way up to a value greater than 47, update the vector with the computed distance, and push the element to the
        stack:
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
            # Pop until we find the next greater element to the right
            stack.pop()
        if stack:
            # If the stack is not empty, then we have a next greater element, so we take the distance between the
            # current temperature and the next greater
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
