""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, return the ordering of courses you should take to
finish all courses.
There may be multiple correct orders, you just need to return one of them. If it is impossible to finish all courses,
return an empty array. """

from collections import defaultdict, deque


# Refer to this excellent article for both solutions: https://leetcode.com/articles/course-schedule-ii/

def find_order_v1(numCourses, prerequisites):
    """ DFS approach. Same logic as 207-Course Schedule.
        The way DFS would work is that we would consider all possible paths stemming from A before finishing up the
        recursion for A and moving onto other nodes. All the nodes in the paths stemming from the node A would have A
        as an ancestor. The way this fits in our problem is, all the courses in the paths stemming from the course A
        would have A as a prerequisite.
        Now we know how to get all the courses that have a particular course as a prerequisite. If a valid ordering of
        courses is possible, the course A would come before all the other set of courses that have it as a prerequisite.
        This idea for solving the problem can be explored using depth first search.
        visited[node] == -1: the node is encountered again while his children are being examined. This indicates a
        cycle.
        visited[node] == 1: this node's children have been examined in an earlier call and no cycle was detected.
        Move on.
    Time complexity: O(|V| + |E|), where V is the number of vertices and E is the number of edges
    Space complexity: O(|V| + |E|)
    """

    def dfs(node):
        if visited[node] == -1:  # Don't recurse further if we found a cycle already
            return False
        if visited[node] == 1:
            return True
        visited[node] = -1  # Start the recursion
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        res.append(node)
        visited[node] = 1
        return True

    graph = [[] for _ in range(numCourses)]  # Create the adjacency list representation of the graph
    visited = [0] * numCourses
    for src, dest in prerequisites:
        graph[src].append(dest)
    res = []
    for node in range(numCourses):
        if not dfs(node):  # If a cycle exists, no topological ordering exists and therefore it will be impossible to
            # take all courses.
            return []
    return res


def find_order_v2(numCourses, prerequisites):
    """ BFS using node in-degree. Very similar to 207- Course Schedule. This is called Kahn's algorithm for topological
        sorting.
        The first node in the topological ordering will be the node that doesn't have any incoming edges. Essentially,
        any node that has an in-degree of 0 can start the topologically sorted order. If there are multiple such nodes,
        their relative order doesn't matter and they can appear in any order.
        We first process all the nodes/courses with 0 in-degree implying no prerequisite courses required. If we remove
        all these courses from the graph, along with their outgoing edges, we can find out the courses/nodes that
        should be processed next. These would again be the nodes with 0 in-degree. We can continuously do this until
        all the courses have been accounted for.
    Time complexity: O(|V| + |E|)
    Space complexity: O(N), where N is the number of courses, since we use an intermediate queue to keep all the nodes
    with 0 in-degree
    """
    graph, indegree = defaultdict(list), [0] * numCourses
    for src, dest in prerequisites:
        graph[dest].append(src)  # Create graph, better seen as is_prerequisite_of graph: graph[dest] = src means dest
        # is a prerequisite of src
        indegree[src] += 1  # Recording the number of prerequisites each course 'src' has
    queue = deque(course for course in range(numCourses) if indegree[course] == 0)  # Iterate the in-degree list and
    # find the nodes that have 0 in-degree, which maps to 0 prerequisites. If none is found, then there must be a cycle
    # and a topological ordering is not possible.
    res = []
    while queue:
        course = queue.popleft()
        res.append(course)
        for neighbor in graph[course]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return res if len(res) == numCourses else []


