""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, return the ordering of courses you should take to
finish all courses.
There may be multiple correct orders, you just need to return one of them. If it is impossible to finish all courses,
return an empty array. """

from collections import defaultdict


# Refer to this excellent article for both soolutions: https://leetcode.com/articles/course-schedule-ii/

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


def find_order_v2(numCourses, prerequisites):
    """ BFS using node in-degree.
        The first node in the topological ordering will be the node that doesn't have any incoming edges. Essentially,
        any node that has an in-degree of 0 can start the topologically sorted order. If there are multiple such nodes,
        their relative order doesn't matter and they can appear in any order.
        We first process all the nodes/course with 0 in-degree implying no prerequisite courses required. If we remove
        all these courses from the graph, along with their outgoing edges, we can find out the courses/nodes that
        should be processed next. These would again be the nodes with 0 in-degree. We can continuously do this until
        all the courses have been accounted for.
    Time complexity: O(|V| + |E|)
    Space complexity: O(N), where N is the number of courses, since we use an intermediate queue to keep all the nodes
    with 0 in-degree
    """
    adj_list = defaultdict(list)
    in_degree = defaultdict(int)
    res = []
    for src, dest in prerequisites:
        adj_list[dest].append(src)
        in_degree[src] += 1
    zero_indegree_queue = [node for node in range(numCourses) if in_degree[node] == 0]
    while zero_indegree_queue:
        node = zero_indegree_queue.pop()
        res.append(node)
        for adj in adj_list[node]:  # Reduce in-degree for all the neighbors
            in_degree[adj] -= 1
            if in_degree[adj] == 0:  # Add neighbor to queue if in-degree becomes 0
                zero_indegree_queue.append(adj)
    return res if len(res) == numCourses else []

