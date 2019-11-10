""" Given a nested list of integers, return the sum of all integers in the list weighted by their depth.
Each element is either an integer, or a list -- whose elements may also be integers or other lists. """


def depthSum_v1(nestedList):
    """ Because the input is nested, it is natural to think about the problem in a recursive way. We go through
        the list of nested integers one by one, keeping track of the current depth. If a nested integer is an
        integer n, we calculate its sum as n * depth. If the nested integer is a list, we calculate the sum of
        this list recursively using the same process but with depth + 1.
    Time complexity: O(N) where N is the total number of nested elements in the input list. For example, the list
    [ [[[[1]]]], 2 ] contains 4 nested lists and 2 nested integers (1 and 2), so N = 6
    Space complexity: at most O(D) recursive calls are placed on the stack, where D is the maximum level of nesting
    in the input. For example, D = 2 for the input [[1,1],2,[1,1]], and D = 3 for the input [1,[4,[6]]].
    """

    def process(nestedList, depth):
        sum = 0
        for lst in nestedList:
            if lst.isInteger():
                sum += lst.getInteger() * depth
            else:
                l = lst.getList()
                sum += process(l, depth + 1)
        return sum

    return process(nestedList, 1)


def depthSum_v2(nestedList):
    """ Same as above, but emulating the recursion call using actual stack.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    sum, stack = 0, []
    stack = [(lst, 1) for lst in nestedList]
    while stack:
        elem, depth = stack.pop()
        if elem.isInteger():
            sum += elem.getInteger() * depth
        else:
            stack.extend([(l, depth+1) for l in elem.getList()])
    return sum
