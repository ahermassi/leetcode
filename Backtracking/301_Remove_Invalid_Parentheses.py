""" Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make
the input string valid.

Return all the possible results. You may return the answer in any order. """

from collections import deque


def remove_invalid_parentheses_v1(s):
    """ Since we don't know which of the brackets can possibly be removed, we try out all the options!
        For every bracket we have two choices:
            - Either it can be considered a part of the final expression, OR
            - It can be ignored i.e. we can delete it from our final expression.
        Such kind of problems where we have multiple options and we have no strategy or metric of deciding greedily
        which option to take and we try out all of the options and see which ones lead to an answer are perfect
        candidates for the programming paradigm, Backtracking.

        The state of the recursion is defined by the index which we are currently processing in the original
        expression. Also, we have a second variable 'balance' that represents the number of left and right parentheses
        we have added to our expression till now, incremented when we add a left bracket and decremented when we add a
        closing bracket, so that a valid expression should have a balance value of 0.

        If the current character i.e. s[index] is neither a closing or an opening parenthesis, then we simply add this
        character to our final solution string for the current recursion.
        However, if the current character is either of the two brackets i.e. s[index] == '(' or s[index] == ')', then
        we have two options: We can either discard this character by marking it an invalid character, or we can
        consider this bracket to be a part of the final expression.

        When all of the parentheses in the original expression have been processed, we simply check if the expression
        represented by 'path' i.e. the expression formed till now is valid. The way we check if the final expression
        is valid is by looking at the value of 'balance'. For an expression to be valid balance == 0. If it is indeed
        valid, then it could be one of our possible solutions.

        Even though we have a valid expression, we also need to keep track of the number of removals we did to get
        this expression. This is done by another DERIVED variable called 'removal_count'. Once recursion finishes, we
        check if the current value of 'removal_count' is <= the least number of steps we took to form a valid
        expression till now i.e. the global minima. If this is not the case, we don't record the new expression, else
        we record it.

        One small optimization that we can do from an implementation perspective is introducing some sort of pruning
        to our algorithm. Right now we simply go till the very end i.e. process all of the parentheses and when we are
        done processing all of them, we check if the expression we have can be considered or not. We have to wait till
        the very end to decide if the expression formed in recursion is a valid expression. Is there a way for us to
        cutoff some of the recursion paths early on because they wouldn't lead to a solution? The answer to this is Yes!
        The optimization is based on the following idea.

        For a left bracket encountered during recursion, if we decide to consider it, then it may or may not lead to an
        invalid final expression. It may lead to an invalid expression eventually if there are no matching closing
        bracket available afterwards. But, we don't know for sure if this will happen or not.

        However, for a closing bracket, if we decide to keep it as a part of our final expression (remember for every
        bracket we have two options, either to keep it or to remove it and recurse further) and there is no
        corresponding opening bracket to match it in the expression till now, then it will definitely lead to an
        invalid expression no matter what we do afterwards.

        That is why, whenever we encounter a right parenthesis, we check if balance > 0 (it also means
        left_parentheses > right_parentheses) . If this is the case, then only we consider that right parenthesis and
        recurse further. Otherwise, we don't as we know it will make the expression invalid. This simple optimization
        saves a lot of runtime.
    Time complexity: O(2^N), since in the worst case we will have only left parentheses in the expression and for every
    bracket we will have two options i.e. whether to remove it or consider it
    Space complexity: O(N), the maximum depth of recursion decides the stack space used. Since we process one character
    at a time and the base case for the recursion is when we have processed all of the characters of the expression
    string, the size of the stack would be O(N)
    """

    def dfs(index, balance, path):
        if index == n:
            if balance == 0:
                removal_count = len(s) - len(path)
                # If the current count of brackets removed <= current minimum, ignore update the current minimum count
                if removal_count <= min_removals[0]:
                    res.add(path)
                    min_removals[0] = removal_count
                    return
            return
        c = s[index]
        if c not in '()':
            dfs(index + 1, balance, path + c)
        elif c == '(':
            dfs(index + 1, balance + 1, path + c)  # If the current parenthesis is an opening bracket, we consider it,
            # increment the balance, and  move forward
            dfs(index + 1, balance, path)  # Ignore the bracket
        else:
            # If the current parenthesis is a closing bracket, we consider it only if we have more number of opening
            # brackets, i.e. balance > 0
            if balance > 0:
                dfs(index + 1, balance - 1, path + c)
            dfs(index + 1, balance, path)

    n, res = len(s), set()
    min_removals = [float('inf')]
    dfs(0, 0, '')
    return res if res else [""]


def remove_invalid_parentheses_v2(s):
    """ Although the previous solution does get accepted, it is very inefficient because we try removing each and every
        possible parentheses from the expression and in the end we check two things:
            - Whether the expression is valid or not
            - Whether the total number of removed parentheses removed in the current recursion is less than the global
              minimum till now or not.
        We cannot determine which of the parentheses are misplaced because, as the problem statement puts across, we
        can remove multiple combinations of parentheses and end up with a valid expression. This means there can be
        multiple valid expressions from a single invalid expression and we have to find all of them.

        The one thing all these valid expressions have in common is that they will all be of the same length i.e. as
        compared to the original expression, all of these expressions will have the same number of characters removed.

        What if we could determine this count? What if in addition to determining this count of characters to be
        removed, we could also determine the number of left parentheses and number of right parentheses to be removed
        from the original expression to get any valid expression? This would cut down the computations immensely and
        the runtime would plummet as a result. The reason for this is, if we knew how many left and right parentheses
        are to be removed from the original expression to get a valid expression, we would cut down on so many unwanted
        recursive calls.

        Imagine the original expression to be 1000 characters long with only 3 misplaced '(' parentheses and
        2 misplaced ')' parentheses. In the previous solution, we would end up trying to remove each one of left and
        right parentheses and try to reach a valid expression in the end whereas we should only be trying out
        removing 3 '(' brackets and 2 ')' brackets. This is the exact number of '(' and ')' that have to be removed to
        get a valid expression. No more, no less.

        Let us look at how we can find out the number of misplaced left and right parentheses in a given expression
        first and then we will slightly modify our original algorithm to incorporate these counts as well.

        We process the expression one bracket at a time starting from the left.

        Suppose we encounter an opening bracket i.e. '(', it may or may not lead to an invalid expression because there CAN be a matching ending bracket
        somewhere in the remaining part of the expression. Here, we simply increment the counter keeping track of left
        parentheses till now. unmatched_left += 1

        If we encounter a closing bracket, this has two meanings: Either there was no matching opening bracket for
        this closing bracket and in that case we have an invalid expression. This is the case when unmatched_left == 0
        i.e. when there are no unmatched left brackets available. In such case, we increment another counter say
        unmatched_right += 1 to represent misplaced right parentheses. Or, we had some unmatched opening bracket
        available to match this closing bracket. This is the case when unmatched_left > 0. In this case, we simply
        decrement the left counter we had i.e. unmatched_left -= 1

        Continue processing the string until all parentheses have been processed. In the end, the values of
        'unmatched_left' and 'unmatched_right' would tell us the number of unmatched '(' and ')' parentheses,
        respectively.

        Now that we have these two values available that tell us the total number of left and right parentheses that
        have to be removed to make the invalid expression valid, we will modify our original algorithm to avoid
        unwanted recursions.

        The overall algorithm remains exactly the same as before. The changes that we will incorporate are:
        'left_removals_remaining' is the number of left parentheses that remain to be removed.
        'right_removals_remaining' represents the number of right parentheses that remain to be removed.
        Overall, for the final expression to be valid, left_removals_remaining == 0 and right_removals_remaining == 0.

        When we decide to not consider a parenthesis i.e. delete a parenthesis, be it a left or a right parentheses,
        we have to consider their corresponding remaining counts as well. This means that we can only discard a left
        parentheses if left_removals_remaining > 0 and similarly for the right one we will check for
        right_removals_remaining > 0.

        There are no changes to checks for considering a parenthesis. Only the conditions change for discarding a
        parenthesis.

        The condition for an expression being valid in the base case would now become left_removals_remaining == 0 and
        right_removals_remaining == 0. Note that we don't have to check if balance == 0 anymore because in the case of
        a valid expression, we would have removed all the misplaced or invalid parenthesis by the time the recursion
        ends.

        The most important thing here is that we have completely gotten rid of checking if the number of parentheses
        removed is lesser than the current minimum. The reason for this is that we always remove the same number of
        parentheses as defined by (left_removals_remaining + right_removals_remaining) at the start of recursion.
    Time complexity:  O(2^N), the optimization that we have performed is simply a better form of pruning. Pruning here
    is something that will vary from one test case to another. In the worst case, we can have something like '((((((((('
    and the unmatched_left = len(s) and in such a case we can discard all of the characters because all are misplaced.
    So, in the worst case we still have 2 options per parenthesis and that gives us a complexity of O(2^N).
    Space complexity: O(N), we have to go to a maximum recursion depth of N before hitting the base case
    """

    def dfs(index, balance, left_removals_remaining, right_removals_remaining, path):
        if index == n:
            if left_removals_remaining == right_removals_remaining == 0:
                res[path] = 1  # This is how we avoid duplicates without using a set
                return
            return
        c = s[index]
        if c not in '()':
            dfs(index + 1, balance, left_removals_remaining, right_removals_remaining, path + c)
        elif c == '(':
            dfs(index + 1, balance + 1, left_removals_remaining, right_removals_remaining, path + c)
            if left_removals_remaining > 0:  # We don't recurse if the remaining count for the parenthesis is 0
                dfs(index + 1, balance, left_removals_remaining - 1, right_removals_remaining, path)
        else:
            if balance > 0:  # If the current parenthesis is a closing bracket, we consider it only if we have more
                # number of opening brackets, i.e. balance > 0
                dfs(index + 1, balance - 1, left_removals_remaining, right_removals_remaining, path + c)
            if right_removals_remaining > 0:  # We don't recurse if the remaining count for the parenthesis is 0
                dfs(index + 1, balance, left_removals_remaining, right_removals_remaining - 1, path)

    n, res = len(s), {}
    unmatched_left = unmatched_right = 0
    # First, we find out the number of misplaced left and right parentheses
    for c in s:
        if c == '(':
            unmatched_left += 1
        elif c == ')':
            if not unmatched_left:  # If we don't have a matching left, then this is a misplaced right, record it.
                unmatched_right += 1
            else:
                # Decrement count of left parentheses because we have found a right which CAN be a matching for a left
                unmatched_left -= 1
    dfs(0, 0, unmatched_left, unmatched_right, '')
    return list(res.keys())


def remove_invalid_parentheses_v3(s):
    """ We are required to return the minimum number of invalid parentheses to remove. Let's model the problem as a
        graph:
            node: String obtained by removing parenthesis (The start node is `s`)
            edge (from u to v): Remove a parentheses from u
        As a result, the problem becomes to get the shortest distance from s to a valid node (assuming at level l) in
        the first place, then get all valid nodes at level l.
        BFS guarantees shortest path. Since the problem asks to remove minimum parenthesis, it is natural to think of
        BFS.

        The idea is straightforward: With the input string s, we generate all possible states by removing one '(' or
        ')' and check if they are valid; if we find valid strings at the current level, we add them to the final result
        list and we are done. Otherwise, we add them to a queue and carry on to the next level.

        The one crucial observation is that once we find a valid expression, it means we have found the minimum
        removals since we are using BFS. Therefore, there is no need to search further. We just check all the valid
        expressions  at that level. If we were using DFS, we would need to keep track of the minimum removals.
    Time complexity: O(2^N), on the first level there's only one string which is the input string s, let's say of
    length n. To check whether it's valid, we need O(n) time. On the second level, we remove one '(' or ')' from the
    first level, so there are C(n, n-1) new strings, each of them has (n - 1) characters, and for each string we need
    to check whether it's valid or not, thus the total time complexity on this level is (n-1) x C(n, n-1). Come to the
    third level, total time complexity is (n-2) x C(n, n-2), so on and so forth. Finally we have this formula:
    T(n) = n x C(n, n) + (n-1) x C(n, n-1) + ... + 1 x C(n, 1) = n x 2^(n-1)
    Space complexity: O(N)
    """

    def is_valid(s):
        balance = 0
        for c in s:
            if c == '(':
                balance += 1
            elif c == ')':
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    queue = deque([s])
    visited, res = set(), []
    valid_expression_found = False
    while queue:
        expression = queue.popleft()
        if is_valid(expression):
            res.append(expression)
            valid_expression_found = True
        if valid_expression_found:  # This ensures once we've found a valid parentheses pattern, we don't do any
            # further BFS using items pending in the queue since any further BFS would only yield strings of smaller
            # length. However, the items already in queue need to be processed since there could be other solutions of
            # the same length. Once we have a string of length k that is valid, all those strings in the next level
            # which have a length of (k - 1) are definitely not valid (we need to remove a pair to make it valid again).
            continue
        n = len(expression)
        for i in range(n):
            if expression[i] not in '()':
                continue
            sub_expression = expression[:i] + expression[i + 1:]
            if sub_expression not in visited:
                queue.append(sub_expression)
                visited.add(sub_expression)
    return res
