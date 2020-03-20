""" Given an array of integers with possible duplicates, randomly output the index of a given target number. You can
assume that the given target number must exist in the array.
Note:
The array size can be very large. Solution that uses too much extra space will not pass the judge. """

from collections import defaultdict
from random import choice, randint


class SolutionV1:
    """ Create a value-to-index map. Then, for each target value randomly pick an index from the corresponding list of
        indices.
    Time complexity: O(N) init, O(1) pick
    Space complexity: O(N)
    """

    def __init__(self, nums):
        self.indices = defaultdict(list)
        for i, num in enumerate(nums):
            self.indices[num].append(i)

    def pick(self, target: int) -> int:
        return choice(self.indices[target])


class SolutionV2:
    """ We use a variable count to track the number of occurrences of the target number in nums.
        Say we now we have nums = [1, 5, 5, 6, 5, 7, 9, 5] and the target is 5.
        When i=1, we get the first target number, count = 1, and by randint(1, count) we select a random number between
        [1, 1], which means actually we could only select 1, so the probability of making res = 1 is 1.
        Keep going. In the loop where i=2, we get the second number, so count = 2. Now we have to get a random number
        in {1, 2}. So what should we do if we want to keep res = 1? It's simple: we have to make sure that, at this
        time, the random number generated should be 2 rather than 1 (otherwise the value of result will be changed),
        so the  probability of keeping res = 1 is 1 * 1/2 = 1/2
        It is similar when we get the third target number, i.e., i=4, so count = 3. Now we have to get a random number
        in {1, 2, 3}. If we still wish to keep res = 1, the only way is to randomly get number 1 or 2 rather than 3,
        and the probability is 2/3. So the total probability of keeping res = 1 will be 1 * 1/2 * 2/3 = 1/3
        When i=7, count = 4. Now we have to get a random number in {1, 2, 3, 4}. The final probability of keeping
        res = 1 would be 1 * 1/2 * 2/3 * 3/4 = 1/4.
        Therefore, the probability of picking index 1 is 1/4 as the problem required. The probability is the same if
        we wish to pick another index.
        Equal possibility return explanation:
        In the loop, the index closer to the start is easier to be picked, but also easier to be replaced since more
        iterations are yet to come.
        For example, let's say we have 5 duplicates of target in total.
        For the 2nd index, the chance it gets returned is: 1/2(pick) * 2/3(not replaced) * 3/4(not replaced) *
        4/5(not replaced) = 1/5.
        For the 5th index, the chance it gets returned is: 1/5(pick) = 1/5 , no chance to be replaced since no more
        iterations left.
        So we can say that when we now has n values and there is still another value in the next iteration, we can
        pick the other value with prob= 1/(n+1), also keep original value with prob = n/(n+1), then we can secure each
        value is picked with same prob = 1/(n+1), because prob = 1 * 1/2 * 2/3 * ···· * n/(n+1) = 1/(n+1).
        At first try, the first index will be selected with a probability of 100%, but what's next? Let's try to
        multiply 1 * (1 - 1/2) * (1 - 1/3) * (1 - 1/4) * ... * (1 - 1/n) = 1 * 1/2 * 2/3 * 3/4 * ... * n-1/n = = 1 / n
        Another example: nums = [1, 2, 3, 3, 3], target 3.
        We have to select indices 2,3,4 with a probability of 1/3 each.
        2 : Its probability of selection is:
            1 (selected first time) * 1/2 (index 3 not selected) * 2/3 (index 4 not selected) = 1/3
        3 : Its probability of selection is:
            1/2 (index 2 not selected) * 2/3 (index 4 not selected) = 1/3
        4 : Its probability of selection is just 1/3
        So they are each randomly selected.
    """

    def __init__(self, nums):
        self.nums = nums

    def pick(self, target: int) -> int:
        count, res = 0, None
        for i, num in enumerate(self.nums):
            if num == target:
                count += 1
                if randint(1, count) == 1:
                    res = i
        return res  # How does it guarantee that res won't be None at the end ? When we hit the first target (and we
        # are guaranteed that there is at least one target element), count = 1 and randint(1, count) = 1. Therefore,
        # res gets updated.

