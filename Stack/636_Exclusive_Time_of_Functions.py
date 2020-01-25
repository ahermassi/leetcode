""" See description on Leetcode. """

import unittest2 as unittest


def exclusive_time_v1(n, logs):
    """ The idea is simple. Every time we see a start, we just push it to the stack. Now when we reach an end, we are
        guaranteed that the top of the stack is a start with the same id as the current item because all completed
        start/ends in between this start and end have been removed already. We just add current item timestamp - stack
        top timestamp + 1 to res[i].
        However, what if there are function calls in between the start and end of the current function ?
        So, we know that the time it takes for the most recent element in the stack to complete comes at a 'cost' of
        the next element in the stack, i.e a function takes longer than supposed to because it must wait for the
        'inner' function to complete. But we want to find how much time the function takes without interference.
        Therefore, we need to subtract the time it took for the 'inner' function we just popped (the 'res' array
        element is most likely negative at this point).
        In other words, we try to record the 'penalty' a function takes. For example, if function 0 is running at time
        [1, 10], and function 1 runs at time [3, 5], then we know function 0 ran for 10 units of time, less a 3 unit
        penalty. The idea is this: Whenever a function completes using T time, any functions that were running in the
        background take a penalty of T.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    res, stack = [0] * n, []
    for log in logs:
        id, type, timestamp = log.split(':')
        id, timestamp = int(id), int(timestamp)
        if type == 'start':
            stack.append((id, timestamp))
        else:
            elapsed = timestamp - stack.pop()[1] + 1
            res[id] += elapsed
            if stack:
                res[stack[-1][0]] -= elapsed  # The enclosing (outer) function gets a penalty
    return res


class Test(unittest.TestCase):
    data = [(2, ['0:start:0', '1:start:2', '1:end:5', '0:end:6'], [3, 4]),
            (1, ['0:start:0', '0:start:1', '0:start:2', '0:end:3', '0:end:4', '0:end:5'], [6])]

    def test_exclusive_time(self):
        for test_n, test_logs, result in self.data:
            self.assertEqual(result, exclusive_time_v1(test_n, test_logs))


if __name__ == '__main__':
    unittest.main()
