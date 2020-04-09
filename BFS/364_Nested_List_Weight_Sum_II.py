""" Given a nested list of integers, return the sum of all integers in the list weighted by their depth.
Each element is either an integer, or a list -- whose elements may also be integers or other lists.
Weight is defined from bottom up. i.e., the leaf level integers have weight 1, and the root level integers have the
largest weight. """

from collections import deque


def depth_sum_inverse_v1(nestedList):
    """ Instead of multiplying by depth, add integers multiple times by going level by level and adding the previous
        level sum to the current level sum and adding both to the final sum.
        The key fact to use when understanding this algorithm:
        Each integer gets added one extra time for the mere existence of each one level under it.
        The concept of weight here is implemented with repeated addition. This naturally implements the multiplication
        logic - lower level sums are added multiple times to total sum.
        Example: nestedList = [a, [b, [c]]], queue = [a, [b, [c]]]
            1st level: level sum = a; total = a; queue = [b, [c]]
            2nd level: level sum = level sum + b = a + b; total = total + level sum = a + (a + b); queue = [c]
            3rd level: level sum = level sum + c = a + b + c; total = total + level sum = a + (a + b) + (a + b + c)
            --> total = 3a + 2b + c
    Time complexity: O(N), where N is the total number of NestedInteger objects
    Space complexity: O(N)
    """
    level_sum = res = 0
    queue = deque(nestedList)
    while queue:
        n = len(queue)
        for _ in range(n):
            elem = queue.popleft()
            if elem.isInteger():
                level_sum += elem.getInteger()
            else:
                queue.extend(elem.getList())
        res += level_sum
    return res


def depth_sum_inverse_v2(nestedList):
    """ The idea is to pass the previously accumulated integer sum into the next level of recursion, so that we don't
        have to count the number of levels in the nested list beforehand.
        This idea is different in that it always carries over the previous sum. How many times it goes deep, how many
        times the previous sum will be passed. Thus the previous sum will be included very naturally.
        Much like the previous solution, it achieves the multiplication effect using repeated addition.
    Time complexity: O(N), where N is the total number of nested elements in the input list. For example, the list
    [ [[[[1]]]], 2 ] contains 4 nested lists and 2 nested integers (1 and 2), so N = 6.
    Space complexity: at most O(D) recursive calls are placed on the stack, where D is the maximum level of nesting
    in the input. For example, D = 2 for the input [[1,1],2,[1,1]], and D = 3 for the input [1,[4,[6]]].
    """

    def dfs(nested_list, pre_sum):
        cur_sum = pre_sum  # The sum of nestedIntegers always starts off with the previous sum
        next_level = []
        for elem in nested_list:
            if elem.isInteger():
                cur_sum += elem.getInteger()
            else:
                next_level.extend(elem.getList())
        next_level_sum = 0 if not next_level else dfs(next_level, cur_sum)
        return cur_sum + next_level_sum

    return dfs(nestedList, 0)

