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
    """
    Pattern: Monotonic decreasing stack — next greater element to the right,
    processed from right to left.

    Unlike the left-to-right version, where the stack contains unresolved days
    waiting to find their first warmer day, here we scan from right to left and
    maintain a stack of useful CANDIDATES that could be the next warmer day for
    the current day or for days further to the left.

    The stack stores indices because the answer requires the distance between
    the current day and its next warmer day.

    For the current day i, we first remove any candidate whose temperature is
    less than or equal to temperatures[i]:

        while stack and temperatures[i] >= temperatures[stack[-1]]:
            stack.pop()

    Why can those days be permanently discarded?

    Suppose the current temperature is 72 and the candidate at the top of the
    stack is 69:

        ... 72 ... 69
            i

    The 69 cannot be the next warmer day for 72 because it is colder.

    More importantly, 69 can never be useful for any day further to the left
    either. The current 72 is now a better candidate:

        - 72 is closer to every future day we process on the left.
        - 72 is warmer than 69.

    Therefore, if 69 could have been a valid warmer day for some temperature
    to the left, 72 would also be warmer and would be encountered first.
    The 69 is dominated by 72 and can safely be removed.

    We also pop EQUAL temperatures. The problem requires a STRICTLY warmer
    temperature, so an equal temperature cannot answer the current day.
    Furthermore, the current occurrence of that temperature is closer to every
    day on the left, making the farther equal occurrence useless.

    After removing all candidates that are less than or equal to the current
    temperature, one of two things is true:

        1. The stack is empty.

           There is no warmer temperature to the right, so the answer for this
           day remains 0.

        2. The stack is not empty.

           The temperature at stack[-1] is strictly warmer than the current
           temperature. Because the top represents the nearest surviving useful
           candidate to the right, it is the current day's next warmer day.

           Therefore:

               res[i] = stack[-1] - i

    Finally, we push the current index onto the stack because the current day
    can now be a candidate warmer day for temperatures further to the left.

    Example:

        temperatures = [75, 71, 69, 72]

    Scan from right to left.

        72:
            stack is empty
            push 72

            stack temperatures: [72]

        69:
            72 > 69, so 72 is the next warmer day for 69
            push 69

            stack temperatures: [72, 69]

        71:
            71 >= 69, so 69 is useless and gets popped.
            Now 72 > 71, so 72 is the next warmer day for 71.
            Push 71.

            stack temperatures: [72, 71]

        75:
            75 >= 71 -> pop 71
            75 >= 72 -> pop 72
            stack is empty, so 75 has no warmer day to its right.
            Push 75.

    Notice that the temperatures represented by the stack remain monotonically
    decreasing from bottom to top.

    Just like in the left-to-right version, we do not choose a decreasing stack
    arbitrarily. The monotonic property follows from the removal rule: before
    pushing the current temperature, we remove every temperature less than or
    equal to it. Therefore, anything remaining underneath it must be strictly
    warmer.

    Time complexity: O(N). Each index is pushed onto the stack once and popped
    at most once, so there are O(N) total stack operations.
    Space complexity: O(N). In the worst case, all N indices can remain on the
    stack.
    """
    n = len(temperatures)
    res = [0] * n
    stack = []  # Useful candidate warmer days to the right.

    for i in reversed(range(n)):
        # Remove candidates dominated by the current day.
        # They are no warmer and are farther away from every day to the left.
        while stack and temperatures[i] >= temperatures[stack[-1]]:
            stack.pop()

        # The nearest surviving candidate is strictly warmer.
        if stack:
            res[i] = stack[-1] - i

        # The current day becomes a candidate for days further to the left.
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
