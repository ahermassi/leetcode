""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, is it possible for you to finish all courses? """

from collections import defaultdict, deque
import unittest2 as unittest


def can_finish_dfs(num_courses, prerequisites):
    """ This is a direct application of topological sort. Note that this type of sort can only be applied on Directed
        Acyclic Graphs (DAG). A Directed cyclic graph fails to yield a topological sort because of the presence of a
        cycle. This property is the intuition of this questions's algorithm.
        Recall that DFS maintains a color for each vertex. Initially, all vertices are white (0). When a vertex is
        first discovered, it is colored gray (-1). When DFS finishes processing a vertex, that vertex is colored black
        (1). As soon as we discover an edge from a gray vertex back to a gray vertex, a cycle exists and we can stop.
        If node course has not been visited, then mark it as 0.
        If node course is being visited, then mark it as -1. If we find a vertex marked as -1 during DFS, then this
        vertex is part of a cycle.
        If node course has been visited, then mark it as 1. If a vertex was marked as 1, then no cycle contains course
        or its successors.
        -1 means this node is part of the current trip. If you see it again, it's a cycle. 1 means a DFS has been done
        starting from this node, and no cycle was found. if we hit this, going down this path won't find any cycles.
        In summary, a cycle exists if and only if DFS discovers an edge from a gray (-1) vertex to a gray vertex.
    Time complexity: O(|V| + |E|), where V is the number of vertices and E is the number of edges. We iterate over all
    vertices, and spend a constant amount of time per edge
    Space complexity: O(|V|), which is the maximum stack depth. If we go deeper than |V| calls, some vertex must
    repeat, implying a cycle in the graph, which leads to early termination.
    """
    def dfs(i):
        if visited[i] == -1:  # If ith node is marked as being visited, then a cycle is found
            return False
        if visited[i] == 1:   # If it is done visiting, then do not visit again
            return True
        visited[i] = -1  # Mark as being visited during current recursion
        for neighbor in graph[i]:  # Visit all the neighbours
            if not dfs(neighbor):
                return False
        visited[i] = 1  # After visiting all the neighbours, mark it as done visiting
        return True

    graph = defaultdict(list)
    for course, prereq in prerequisites:  # Create graph
        graph[course].append(prereq)
    visited = [0] * num_courses
    for i in range(num_courses):  # Visit each node.  Since the graph may not be strongly connected, we must examine
        # each vertex and run DFS from it if it has not already been explored
        if not dfs(i):
            return False
    return True


def can_finish_bfs(numCourses, prerequisites):
    """ Same as above but in BFS fashion. This is called Kahn's algorithm for topological sorting.
        A better way to understand this algorithm is to draw the graph and remove edges each time the in-degree of a
        node is reduced, and remember to always start exploring from the nodes that have NO incoming edges (in-degree=0)
    Time complexity: O(|V| + |E|)
    Space complexity: O(|V| + |E|)
    """
    graph = defaultdict(list)
    indegree = [0] * numCourses
    for course, prereq in prerequisites:  # Create graph, better be seen as is_prerequisite_of graph:
        # graph[prerq] = course means prereq is a prerequisite of course
        graph[prereq].append(course)
        indegree[course] += 1  # Recording the number of prerequisites each course i has
    queue = deque(course for course in range(numCourses) if indegree[course] == 0)  # Iterate over the indegrees list
    # and find the node that has 0 indegree, which maps to 0 prerequisites. If none is found, then there must be a
    # cycle.
    n = len(queue)  # n is initialized to len(queue) because the queue contains the courses that have 0 prerequisites
    # so they can be finished without any pre-processing
    while queue and n != numCourses:  # adding n != numCourses to terminate loop earlier
        course = queue.popleft()
        for neighbor in graph[course]:  # Iterate through the courses that have 'course' as prerequisite
            indegree[neighbor] -= 1  # This is equivalent to removing the edge neighbor -> course, which in other words
            # means taking course 'course' and 'course' is no longer in the list of prerequisite of 'neighbor'
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
