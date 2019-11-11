""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, is it possible for you to finish all courses? """

from collections import defaultdict, deque
import unittest2 as unittest


def can_finish_dfs(numCourses, prerequisites):
    """ This is a direct application of topological sort. Note that this type of sort can only be applied on Directed
        Graphs. A Directed Acyclic Graph fails to yield a topological sort because of the presence of a cycle. This
        property is the intuition of this questions's algorithm.
        If node v has not been visited, then mark it as 0.
        If node v is being visited, then mark it as -1. If we find a vertex marked as -1 in DFS, then their is a ring.
        If node v has been visited, then mark it as 1. If a vertex was marked as 1, then no ring contains v or its
        successors.
        -1 means this node is part of the current trip. If you see it again, it's a cycle. 1 means a DFS has been done
        starting from this node, and no cycle was found. if you hit this, going down this path won't find any cycles.
    Time complexity: O(|V| + |E|), where V is the number of vertices and E is the number of edges
    Space complexity: O(|V| + |E|)
    """
    def dfs(i):
        if visited[i] == -1:  # If ith node is marked as being visited, then a cycle is found
            return False
        if visited[i] == 1:   # If it is done visited, then do not visit again
            return True
        visited[i] = -1  # Mark as being visited during current recursion
        for neighbor in graph[i]:  # Visit all the neighbours
            if not dfs(neighbor):
                return False
        visited[i] = 1  # After visiting all the neighbours, mark it as done visited
        return True

    graph = defaultdict(list)
    for i, j in prerequisites:  # Create graph
        graph[i].append(j)
    visited = [0] * numCourses
    for i in range(numCourses):  # Visit each node
        if not dfs(i):
            return False
    return True


def can_finish_bfs(numCourses, prerequisites):
    """ Same as above but in BFS fashion. This is called Kahn's algorithm
        A better way to understand this algorithm is to draw the graph and remove edges each time the in-degree of a
        node is reduced, and remember to always start exploring from the nodes that have NO incoming edges (in-degree=0)
    Time complexity: O(|V| + |E|)
    Space complexity: O(|V| + |E|)
    """
    graph = [[] for _ in range(numCourses)]
    indegree = [0, ] * numCourses
    for i, j in prerequisites:  # Create graph, better be seen as is_prerequisite_of graph: graph[j] = i means j is a
        # prerequisite of i
        graph[j].append(i)
        indegree[i] += 1  # Recording the number of prerequisites each course i has
    queue = deque(v for v in range(numCourses) if indegree[v] == 0)  # Iterate the indegree map and find the node that
    # has 0 indegree, which maps to 0 prerequisites. If none is found, then there must be a cycle.
    n = len(queue)  # n is initialized to len(queue) because the queue contains the courses that have 0 prerequisites
    # so they can be finished without any pre-processing
    while queue and n != numCourses:  # adding n != numCourses to terminate loop earlier
        v = queue.popleft()
        for neighbor in graph[v]:  # Iterate through the courses that have 'v' as prerequisite
            indegree[neighbor] -= 1  # This is equivalent to removing the edge neighbor -> v, which in other words
            # means taking course 'v' and 'v' is no longer in the list of prerequisite of 'neighbor'
            if indegree[neighbor] == 0:  # We've taken all the prerequisites of course 'neighbor' ..
                n += 1  # .. so one more course has been finished
                queue.append(neighbor)  # Now explore the courses that have 'neighbor' as prerequisite
    return n == numCourses


class Test(unittest.TestCase):
    data = [(2, [[1, 0]], True), (2, [[1, 0], [0, 1]], False)]

    def test_can_finish(self):
        for test_num_courses, test_prerequisites, result in self.data:
            self.assertEqual(result, can_finish_dfs(test_num_courses, test_prerequisites))
            self.assertEqual(result, can_finish_bfs(test_num_courses, test_prerequisites))


if __name__ == '__main__':
    unittest.main()
