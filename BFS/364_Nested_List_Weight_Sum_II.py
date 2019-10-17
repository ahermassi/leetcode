""" Given a nested list of integers, return the sum of all integers in the list weighted by their depth.
Each element is either an integer, or a list -- whose elements may also be integers or other lists.
Weight is defined from bottom up. i.e., the leaf level integers have weight 1, and the root level integers have the
largest weight. """


def depth_sum_inverse(nestedList):
    """ Instead of multiplying by depth, add integers multiple times by going level by level and adding the previous
        level sum to the current level sum and adding both to the final sum.
        The key fact to use when understanding this algorithm:
        Each integer gets added one extra time for the mere existence of each one level under it.
        The concept of weight here is implemented with repeated addition. This naturally implements the multiplication
        logic - lower level sums are added multiple times to total sum.
        Example: nestedList = [a, [b, [c]]]
            1st level: level sum = a; total = a
            2nd level: level sum = level sum + b = a + b; total = total + level sum = a + (a + b)
            3rd level: level sum = level sum + c = a + b + c; total = total + level sum = a + (a + b) + (a + b + c)
            --> total = 3a + 2b + c
    Time complexity: O(N), where N is the total number of NestedInteger objects
    Space complexity: O(N)
    """
    level_sum = res = 0
    while nestedList:
        next_level = []
        for elem in nestedList:
            if elem.isInteger():
                level_sum += elem.getInteger()
            else:
                next_level.extend(elem.getList())
        res += level_sum
        nestedList = next_level
    return res

