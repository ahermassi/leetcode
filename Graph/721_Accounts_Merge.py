""" Given a list of accounts where each element accounts[i] is a list of strings, where the first element
accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.

Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common
email to both accounts. Note that even if two accounts have the same name, they may belong to different people as
people could have the same name. A person can have any number of accounts initially, but all of their accounts
definitely have the same name.

After merging the accounts, return the accounts in the following format: the first element of each account is the name,
and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order. """

from collections import defaultdict
import unittest2 as unittest


def accounts_merge_v1(accounts):
    """ The goal is, for each person, to identify all the emails that belong to that person. Therefore, every time we
         find two accounts with an email in common, we merge the two accounts into one.

         Whenever we must work with a set of elements (emails) that are connected (belong to the same user), we should
         always consider visualizing the input as a graph. In this problem, converting the input into a graph will
         facilitate the process of "merging" two accounts.

         We can see that the set of emails of each account form a single group belonging to a person. If we visualize
         these as a graph, we can think of them as various connected components of a graph. More specifically, the
         emails belonging to a person form the node of a connected component and all these connected components make up
         the whole graph.

         Each email from one account will have an edge with one another email of the same account. But if an email is
         found in multiple accounts, they will have edge with other emails from all these multiple accounts as well,
         effectively merging them into one connected component.

         Therefore, for every pair of emails in the same account, draw an edge between those emails. The problem is
         about enumerating the connected components of this graph.

         Suppose an account has K emails, and we want to connect these emails. We can create an acyclic graph using K−1
         edges. Recall that K−1 is the minimum number of edges required to connect K nodes. So we connect emails in an
         account in a "star" manner with the first email as the central node of the star and all other emails as the
         leaves.

         The beauty of connecting the emails in each account in this manner is that after connecting an email to a
         second account, that email will have one edge going to an email in the first account and one edge going to an
         email in the second account. Thereby automatically merging the two accounts.

         !!! IMPORTANT !!!
         We only need to connect each email of an account to the first email of that account and vice versa because that
         will construct the same set of connected components for the vertices, even though the graph isn't truly
         complete.

         Note that we can also connect every email at index i with the email at index i+1.

         After iterating over each account and connecting the emails as described above, we will have one or more
         connected components. Each connected component represents one person, and the nodes in the connected component
         are the person's emails. Now the task is to explore each connected component to find all the emails that belong
         to each person.

         Since a DFS is guaranteed to explore every node in a connected component, we perform a DFS on each connected
         component (person) to find all the connected emails.

        Start with each account, take an email from that account (let's say 1st email) and traverse over the component
        of that email. Each email traversed belongs to the person of this account (since they form a connected
        component). We can use DFS for traversing the component. We sort the list of emails found in this traversal and
        add it to the final list of merged accounts along with the person name at the beginning.
        We also mark each of these email as seen so we don't iterate over them again and form a duplicate.

        An example is attached as .img file.

        Example: suppose we have three accounts, we can connect them like this in order to use DFS, where numbers
        represent email addresses:
            {Name, 1, 2, 3} => Name -- 1 -- 2 -- 3
            {Name, 2, 4, 5} => Name -- 2 -- 4 -- 5 (node 2 is common)
            {Name, 6, 7, 8} => Name -- 6 -- 7 -- 8

    Time complexity: O(NK logNK), where N is the number of accounts and K is the maximum length of an account. In the
    worst case, all the emails will end up belonging to a single person. The total number of emails will be NK, and we
    need to sort these emails. DFS traversal will take NK operations as no email will be traversed more than once.
    Space complexity: O(NK), building the adjacency list takes O(NK) space. In the end, visited will contain
    all the emails hence it will use O(NK) space. Also, the call stack for DFS will use O(NK) space in the worst case.
    """

    def dfs(vertex):
        # Each vertex/node is an email address
        component.append(vertex)
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor)

    graph = defaultdict(list)
    for account in accounts:
        name, first_email = account[0], account[1]
        n = len(account)
        for i in range(2, n):
            graph[account[i]].append(first_email)
            graph[first_email].append(account[i])
    res = []
    visited = set()
    for account in accounts:
        name = account[0]
        n = len(account)
        for i in range(1, n):
            email = account[i]
            if email not in visited:
                # This vertex hasn't been explored yet. visited set ensures that DFS gets called for every component and
                # NOT on every node.
                component = []
                # Collect the vertices/emails that belong to the same connected component
                dfs(email)
                res.append([name] + sorted(component))
    return res


# Similar to https://leetcode.com/problems/accounts-merge/discuss/109161/Python-Simple-DFS-with-explanation!!!
# 4th comment
def accounts_merge_v2(accounts):
    """ We assign an ID to each account owner based on its index in the list of accounts.

         Next, build a graph that maps an email to a list of account owners, which can be used to track which email is
         linked to which account.

         After that, we perform a DFS on each account in accounts list and look up the graph to tell us which accounts
         are linked to that particular account via common emails. This will make sure we visit each account only once.
         This is a recursive process, and we should collect all the emails that we encounter along the way.

         Lastly, sort the collected emails and add it to final result.

         Example:
            [
                ["John", "johnsmith@mail.com", "john00@mail.com"], # Account 0
                ["John", "johnnybravo@mail.com"], # Account 1
                ["John", "johnsmith@mail.com", "john_newyork@mail.com"],  # Account 2
                ["Mary", "mary@mail.com"] # Account 3
            ]
            graph:
            {
                "johnsmith@mail.com": [0, 2],
                "john00@mail.com": [0],
                "johnnybravo@mail.com": [1],
                "john_newyork@mail.com": [2],
                "mary@mail.com": [3]
            }

    Time complexity: O(NK logNK)
    Space complexity: O(NK)
    """

    def dfs(index):
        # Collect the emails associated with the current index ID and recursively collect the other emails that are
        # shared with the rest of ids that exist in graph[email]
        visited.add(index)
        account = accounts[index]
        n = len(account)
        for j in range(1, n):
            email = account[j]
            component.add(email)
            for neighbor in graph[email]:
                # Navigate to the different account ids to which this email is associated and collect the rest of email
                # addresses
                if neighbor not in visited:
                    dfs(neighbor)

    visited, res = set(), []
    graph = defaultdict(list)
    for i, account in enumerate(accounts):
        n = len(account)
        for j in range(1, n):
            email = account[j]
            # email:[list of account ids it's associated with]
            graph[email].append(i)
    for i, account in enumerate(accounts):
        if i not in visited:
            name = account[0]
            component = set()
            dfs(i)
            res.append([name] + sorted(component))
    return res


class Test(unittest.TestCase):
    data = [([['John', 'johnsmith@mail.com', 'john00@mail.com'], ['John', 'johnnybravo@mail.com'],
              ['John', 'johnsmith@mail.com', 'john_newyork@mail.com'], ['Mary', 'mary@mail.com']],
             [['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com'],  
              ['John', 'johnnybravo@mail.com'], ['Mary', 'mary@mail.com']])]

    def test_accounts_merge(self):
        for test_accounts, result in self.data:
            self.assertEqual(result, accounts_merge_v1(test_accounts))
            self.assertEqual(result, accounts_merge_v2(test_accounts))


if __name__ == '__main__':
    unittest.main()