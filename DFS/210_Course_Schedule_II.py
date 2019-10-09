""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, return the ordering of courses you should take to
finish all courses.
There may be multiple correct orders, you just need to return one of them. If it is impossible to finish all courses,
return an empty array. """


def find_order_v1(numCourses, prerequisites):
    """ DFS approach. Same logic as 207-Course Schedule.
        visited[i] == -1: the node is encountered again while his children are being examined. This indicates a cycle.
        visited[i] == 1: this node's children have been examined in an earlier call and no cycle was detected. Move on.
    Time complexity: O(|V| + |E|), where V is the number of vertices and E is the number of edges
    Space complexity: O(|V| + |E|)
    """

    def dfs(i):
        if visited[i] == -1:  # Don't recurse further if we found a cycle already
            return False
        if visited[i] == 1:
            return True
        visited[i] = -1  # Start the recursion
        for j in graph[i]:
            if not dfs(j):
                return False
        res.append(i)
        visited[i] = 1
        return True

    graph = [[] for _ in range(numCourses)]  # Create the adjacency list representation of the graph
    visited = [0] * numCourses
    for x, y in prerequisites:
        graph[x].append(y)
    res = []
    for i in range(numCourses):
        if not dfs(i):
            return []
    return res

