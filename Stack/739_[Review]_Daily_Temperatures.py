""" Given a list of daily temperatures, return a list such that, for each day in the input, tells you how many days
you would have to wait until a warmer temperature. If there is no future day for which this is possible, put 0 instead.
Note: The length of temperatures will be in the range [1, 30000]. Each temperature will be an integer in the range
[30, 100]. """

import unittest2 as unittest


# Video explanation: https://youtu.be/cTBiBSnjO3c
def daily_temperatures_v1(temperatures):
    """
    Pattern: Monotonic decreasing stack — next greater element to the right.

    The reusable idea is to scan from left to right while keeping a stack of
    elements whose "next greater" element has not been found yet.

    Here, a day stays on the stack while we are still waiting to find the first
    future day with a warmer temperature.

    For each current day:

        - If the current temperature is not warmer than the temperature of the
          day at the top of the stack, it cannot resolve that day. The current
          day is also unresolved, so we push its index onto the stack.

        - If the current temperature is warmer than the temperature at the top
          of the stack, then the current day must be the FIRST warmer day for
          that previous day. If an earlier warmer day had existed, that previous
          day would already have been removed from the stack.

          We therefore pop that previous day and set its answer to the distance
          between the two indices.

    We use a while loop rather than a single check because one warm day can
    resolve several previous unresolved days.

    Example:

        temperatures = [75, 71, 69, 72]

    Before processing 72, the stack contains the indices for:

        [75, 71, 69]

    72 > 69, so 72 is the first warmer day for 69. Pop 69.
    72 > 71, so 72 is also the first warmer day for 71. Pop 71.
    72 < 75, so 75 is still unresolved and remains on the stack.

    The stack now represents:

        [75, 72]

    Why is the stack monotonically decreasing?

    We do not start by deciding that the stack must be decreasing. Instead,
    the decreasing order is a consequence of how unresolved elements are
    maintained.

    Before pushing a new temperature, we remove every smaller temperature that
    it resolves. Therefore, once the current day is pushed, the temperature
    below it must be greater than or equal to it. Repeating this process causes
    the stack to remain monotonically decreasing from bottom to top.

    We store indices instead of temperatures because the answer asks for the
    number of days until the warmer temperature, so when day `cur_day` resolves
    `prev_day`, the answer is:

        cur_day - prev_day

    Any indices left on the stack after the scan never encounter a warmer day,
    so their answers correctly remain 0.

    Time complexity: O(N). Each index is pushed onto the stack once and popped
    at most once, so there are at most O(N) total stack operations.
    Space complexity: O(N). In the worst case, temperatures are non-increasing,
    so no index is popped and all N indices remain on the stack.
    """
    res = [0] * len(temperatures)
    stack = []  # Indices of unresolved days waiting for their first warmer day.

    for cur_day, temperature in enumerate(temperatures):
        # The current day resolves every colder unresolved day on top of the stack.
        while stack and temperature > temperatures[stack[-1]]:
            prev_day = stack.pop()
            res[prev_day] = cur_day - prev_day

        # The current day is now unresolved and waits for a future warmer day.
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
