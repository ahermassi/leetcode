""" Given a nested list of integers, return the sum of all integers in the list weighted by their depth.
Each element is either an integer, or a list -- whose elements may also be integers or other lists. """
from collections import deque


def depth_sum_v1(nested_list):
    """ Because the input is nested, it is natural to think about the problem in a recursive way.

         We iterate over the list of nested integers one by one, keeping track of the current depth.

            - If the nested integer is an integer n, we calculate its sum as n * depth.

            - If the nested integer is a list, we calculate the sum of this list recursively using the same process but
               with (depth + 1).

    Time complexity: O(N), where N is the total number of nested elements in the input list. For example, the list
    [ [[[[1]]]], 2 ] contains 4 nested lists and 2 nested integers (1 and 2), so N = 6. The recursive function is called
    exactly once for each nested list. As N also includes nested integers, we know that the number of recursive calls
    has to be less than N. On each nested list, it iterates over all the nested elements directly inside that list (in
    other words, not nested further). As each nested element can only be directly inside one list, we know that there
    must only be one loop iteration for each nested element. This is a total of N loop iterations.
    Space complexity: at most O(D) recursive calls are placed on the stack, where D is the maximum level of nesting
    in the input. For example, D=2 for input [[1,1],2,[1,1]], and D=3 for input [1,[4,[6]]]. In the worst case, D=N
    (e.g. the list [[[[[[]]]]]]), so the worst-case space complexity is O(N).
    """

    def dfs(nested_list, depth):
        res = 0
        for nested_integer in nested_list:
            if nested_integer.isInteger():
                res += nested_integer.getInteger() * depth
            else:
                res += dfs(nested_integer.getList(), depth + 1)
        return res

    return dfs(nested_list, 1)


def depth_sum_v2(nested_list):
    """ We can also solve the problem using a breadth-first search. The algorithm for this is closely based on the
        standard breadth-first search template. The algorithm fully processes each depth before moving to the next one.
    Time complexity: O(N)
    Space complexity: O(N), the worst-case for space complexity in BFS occurs where most of the elements are in a
    single layer, for example, a flat list such as [1, 2, 3, 4, 5] as all of the elements must be put on the queue at
    the same time. Therefore, this approach also has a worst-case space complexity of O(N).
    """
    queue = deque(nested_list)
    depth, res = 1, 0
    while queue:
        n = len(queue)
        for _ in range(n):
            element = queue.popleft()
            if element.isInteger():
                res += element.getInteger() * depth
            else:
                queue.extend(element.getList())
        depth += 1
    return res
