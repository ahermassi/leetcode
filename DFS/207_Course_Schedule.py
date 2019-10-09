""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, is it possible for you to finish all courses? """

import collections

import unittest2 as unittest


def can_finish_dfs(numCourses, prerequisites):
    """ This is a direct application of topological sort. Note that this type of sort can only be applied on Directed
        Graphs. a Directed Acyclic Graph fails to yield a topological sort because of the presence of a cycle. This
        property is the intuition of this questions's algorithm.
        If node v has not been visited, then mark it as 0.
        If node v is being visited, then mark it as -1. If we find a vertex marked as -1 in DFS, then their is a ring.
        If node v has been visited, then mark it as 1. If a vertex was marked as 1, then no ring contains v or its
        successors.
        -1 means this node is part of the current trip. If you see it again, it's a cycle. 1 means a dfs has been done
        starting from this node, and no cycle was found. if you hit this, going down this path won't find any cycles.
    Time complexity: O(|V| + |E|), where V is the number of vertices and E is the number of edges
    Space complexity: O(|V| + |E|)
    """
    graph = [[] for _ in range(numCourses)]
    visited = [0 for _ in range(numCourses)]
    # Create graph
    for x, y in prerequisites:
        graph[x].append(y)

    def dfs(i):
        if visited[i] == -1:  # If ith node is marked as being visited, then a cycle is found
            return False
        if visited[i] == 1:  # If it is done visited, then do not visit again
            return True
        visited[i] = -1  # Mark as being visited during current recursion
        for j in graph[i]:  # Visit all the neighbours
            if not dfs(j):
                return False
        visited[i] = 1  # After visiting all the neighbours, mark it as done visited
        return True

    # Visit each node
    for i in range(numCourses):
        if not dfs(i):
            return False
    return True


def can_finish_bfs(numCourses, prerequisites):
    """ Same as above but in BFS fashion.
    Time complexity: O(|V| + |E|)
    Space complexity: O(|V| + |E|)
    """
    graph = [[] for _ in range(numCourses)]
    indegree = [0, ] * numCourses
    for to_, from_ in prerequisites:
        graph[from_].append(to_)
        indegree[to_] += 1
    queue = collections.deque(v for v in range(numCourses) if indegree[v] == 0)  # Iterate the inDegree map, find the
    # Node has 0 inDegree. (If none, there must be a circle)
    n = len(queue)
    while queue and n != numCourses:  # adding n != numCourses to terminate loop earlier
        v = queue.popleft()
        for to_ in graph[v]:
            indegree[to_] -= 1
            if indegree[to_] == 0:
                n += 1
                queue.append(to_)
    return n == numCourses


class Test(unittest.TestCase):
    data = [(2, [[1, 0]], True), (2, [[1, 0], [0, 1]], False)]

    def test_can_finish(self):
        for test_num_courses, test_prerequisites, result in self.data:
            self.assertEqual(result, can_finish_dfs(test_num_courses, test_prerequisites))
            self.assertEqual(result, can_finish_bfs(test_num_courses, test_prerequisites))


if __name__ == '__main__':
    unittest.main()
