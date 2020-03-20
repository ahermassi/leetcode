""" Given an array of integers with possible duplicates, randomly output the index of a given target number. You can
assume that the given target number must exist in the array.
Note:
The array size can be very large. Solution that uses too much extra space will not pass the judge. """

from collections import defaultdict
from random import choice


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

