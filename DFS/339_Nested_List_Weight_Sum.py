""" Given a nested list of integers, return the sum of all integers in the list weighted by their depth.
Each element is either an integer, or a list -- whose elements may also be integers or other lists. """


def depth_sum_v1(nestedList):
    """ Because the input is nested, it is natural to think about the problem in a recursive way. We iterate over
        the list of nested integers one by one, keeping track of the current depth. If a nested integer is an
        integer n, we calculate its sum as n * depth. If the nested integer is a list, we calculate the sum of
        this list recursively using the same process but with (depth + 1).
    Time complexity: O(N), where N is the total number of nested elements in the input list. For example, the list
    [ [[[[1]]]], 2 ] contains 4 nested lists and 2 nested integers (1 and 2), so N = 6
    Space complexity: at most O(D) recursive calls are placed on the stack, where D is the maximum level of nesting
    in the input. For example, D = 2 for the input [[1,1],2,[1,1]], and D = 3 for the input [1,[4,[6]]].
    """

    def dfs(nested_list, depth):
        res = 0
        for nested_integer in nested_list:
            if nested_integer.isInteger():
                res += nested_integer.getInteger() * depth
            else:
                res += dfs(nested_integer.getList(), depth + 1)
        return res

    return dfs(nestedList, 1)


def depth_sum_v2(nestedList):
    """ Same as above, but emulating the recursion call using an actual stack.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    res, stack = 0, []
    stack = [(nested_integer, 1) for nested_integer in nestedList]
    while stack:
        elem, depth = stack.pop()
        if elem.isInteger():
            res += elem.getInteger() * depth
        else:
            stack.extend([(val, depth + 1) for val in elem.getList()])
    return res
