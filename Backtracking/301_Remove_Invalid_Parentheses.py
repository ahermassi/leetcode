""" Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make
the input string valid.

Return all the possible results. You may return the answer in any order. """

from collections import deque


def remove_invalid_parentheses_v1(s):
    """ Since we don't know which of the brackets can possibly be removed, we try all the options. The only condition
         is that we should be removing the minimum number of brackets to make an invalid expression, valid. If this
         condition was not present, we could potentially remove most of the brackets and come down to say 2 brackets in
         the end which form () and that would be a valid expression.

         For every bracket we have two choices:

             - Either it can be considered a part of the final expression, OR
             - It can be ignored i.e. we can delete it from our final expression.

         Such kind of problems where we have multiple options and have no strategy or metric of deciding greedily
         which option to take and try all the options and see which ones lead to an answer are perfect candidates for
         backtracking.

         The state of the recursion is defined by the index which we are currently processing in the original
         expression. Also, we have a second variable 'balance' that represents the number of left and right parentheses
         we have added to the expression till now, incremented when we add a left bracket and decremented when we add a
         closing bracket, so that a valid expression should have a balance value of 0.

            - If the current character i.e. s[index] is neither a closing nor an opening parenthesis, then we simply
               add this character to the final solution string for the current recursion.

            - However, if the current character is either of the two brackets, then we have two options: either
               discard this character by marking it an invalid character, or consider it part of the final expression.

            - When all the parentheses in the original expression have been processed, we simply check if the expression
               represented by the current path, i.e. the expression formed till now, is valid. The way we check if the
               final expression is valid is by looking at the value of the balance. If it is indeed valid, then it could
               be one of the possible solutions.

         Even though we have a valid expression, we also need to keep track of the number of removals we did to get
         this expression. This is done by another DERIVED variable called removal_count. Once recursion finishes, we
         check if the current value of removal_count is <= the least number of steps we took to form a valid
         expression till now i.e. the global minima. If this is not the case, we don't record the new expression, else
         we record it.

         One small optimization that we can do from an implementation perspective is introducing some sort of pruning
         to the algorithm. Right now we process all the parentheses and finally check if the expression we have can be
         considered or not. We have to wait till the very end to decide if the expression formed in recursion is a valid
         expression. Is there a way to cut down on the recursion paths early because they wouldn't lead to a solution?
         The optimization is based on the following idea.

         For a left bracket encountered during recursion, if we decide to consider it, then it may or may not lead to an
         invalid final expression. It may lead to an invalid expression eventually if there is no matching closing
         bracket available afterwards. But, we don't know for sure if this will happen or not.

         However, for a closing bracket, if we decide to keep it in the final expression (remember for every bracket we
         have two options, either to keep it or to remove it and recurse further) and there is no corresponding opening
         bracket to match it in the expression so far, then it will definitely lead to an invalid expression no matter
         what we do afterwards.

         Therefore, whenever we encounter a right parenthesis, we check if balance > 0 (it also means
         left parentheses > right parentheses) . If this is the case, then only we consider that right parenthesis and
         recurse further. Otherwise, we don't as we know it will make the expression invalid.

         That is why, in addition to having the index in the original string/expression which we are currently
         processing and the expression string formed si far, we also keep track of the number of left and right
         parentheses.

         !!! IMPORTANT !!!

         An important thing to note is that there are multiple ways of reaching the same solution. Suppose the optimal
         number of parentheses to be removed to make the original expression valid is K. We can remove multiple
         different sets of K brackets that will eventually give us the same final expression. But, each valid expression
         should be recorded only once. We have to take care of this in the solution by using a hash set to record the
         valid expressions.

    Time complexity: O(N * 2^N), in the worst case we have only left parentheses in the expression and for every bracket we
    have two options i.e. whether to remove it or leave it. We also need O(N) to create the output expression from the
    path.
    Space complexity: O(N), the maximum depth of recursion decides the stack space used. Since we process one character
    at a time and the base case for the recursion is when we have processed all the characters of the expression string,
    the size of the stack would be O(N).
    """

    def dfs(index, left, right, path):
        if index == n:
            if left == right:
                removal_count = len(s) - len(path)
                # If the current count of brackets removed <= current minimum, don't update the global minimum count
                if removal_count <= min_removals[0]:
                    res.add(''.join(path))
                    min_removals[0] = removal_count
            return
        c = s[index]
        if c not in '()':
            dfs(index + 1, left, right, path + [c])
        elif c == '(':
            # If the current parenthesis is an opening bracket, we consider it
            dfs(index + 1, left + 1, right, path + [c])
            # Ignore the bracket
            dfs(index + 1, left, right, path)
        else:
            if left > right:
                # If the current parenthesis is a closing bracket, we consider it only if we have more opening brackets
                dfs(index + 1, left, right + 1, path + [c])
            # Ignore the bracket
            dfs(index + 1, left, right, path)

    n, res = len(s), set()
    min_removals = [float('inf')]
    dfs(0, 0, 0, [])
    return res


def remove_invalid_parentheses_v2(s):
    """ Although the previous solution is valid, it is very inefficient because we try to remove each and every possible
         bracket from the expression and in the end we check two things:

             - Whether the expression is valid
             - Whether the total number of removed parentheses in the current state is less than the global minimum

         We cannot determine which of the parentheses are misplaced because, as the problem statement puts across, we
         can remove multiple combinations of parentheses and end up with a valid expression. This means there can be
         multiple valid expressions from a single invalid expression, and we have to find all of them.

         The one thing all these valid expressions have in common is that they will all be of the SAME LENGTH i.e. as
         compared to the original expression, all of these expressions will have the same number of characters removed.

         What if we could determine this count? What if in addition to determining the count of characters to be
         removed, we could also determine the number of left parentheses and the number of right parentheses to be
         removed from the original expression to get any valid expression? This would cut down the computations
         immensely and the runtime would plummet as a result. The reason for this is, if we knew how many left and right
         parentheses are to be removed from the original expression to get a valid expression, we would cut down on so
         many unwanted recursive calls.

         Let us look at how we can find out the number of misplaced left and right parentheses in a given expression
         first, and then we will slightly modify the original algorithm to incorporate these counts as well.

            - We process the expression one bracket at a time starting from the left.

            - Suppose we encounter an opening bracket i.e. '(', it may or may not lead to an invalid expression because
               there CAN be a matching ending bracket somewhere in the remaining part of the expression. Here, we simply
               increment the counter keeping track of left parentheses: unmatched_left += 1

            - If we encounter a closing bracket, this has two meanings: either there was no matching opening bracket for
               this bracket and in that case we have an invalid expression. This is the case when unmatched_left == 0
               i.e. when there are no unmatched left brackets available. In such case, we increment another counter,
               unmatched_right, that represents misplaced right parentheses. Or, we had some unmatched opening bracket
               available to match this closing bracket. This is the case when unmatched_left > 0. In this case, we
               decrement the left counter we had i.e. unmatched_left -= 1.

            - In the end, the values of unmatched_left and unmatched_right would tell us the number of unmatched '(' and
               ')' parentheses, respectively.

         Now that we have these two values available that tell us the total number of left and right parentheses that
         have to be removed to make the invalid expression valid, we modify the original algorithm to avoid unwanted
         recursions.

         The overall algorithm remains exactly the same as before. The changes that we will incorporate are:
         left_removals_remaining is the number of left parentheses that remain to be removed. right_removals_remaining
         represents the number of right parentheses that remain to be removed. Overall, for the final expression to be
         valid, left_removals_remaining == right_removals_remaining == 0.

         When we decide to not consider a parenthesis i.e. delete a parenthesis, be it a left or a right parentheses,
         we have to consider their corresponding remaining counts as well. This means that we can only discard a left
         parentheses if left_removals_remaining > 0 and similarly for the right one we will check for
         right_removals_remaining > 0.

         There are no changes to checks for considering a parenthesis. Only the conditions change for discarding a
         parenthesis.

         The condition for an expression being valid in the base case would now become left_removals_remaining == 0 and
         right_removals_remaining == 0. Note that we don't have to check if left == right anymore because in the case of
         a valid expression, we would have removed all the misplaced or invalid parenthesis by the time the recursion
         ends.

         The most important thing here is that we have completely gotten rid of checking if the number of parentheses
         removed is less than the current global minimum. The reason for this is that we always remove the same number of
         parentheses as defined by left_removals_remaining+right_removals_remaining at the start of recursion.

    Time complexity:  O(N * 2^N), the optimization that we have performed is simply a better form of pruning. Pruning is
    something that will vary from one test case to another. In the worst case, we can have something like '((((((((('
    and the unmatched_left = len(s) and in such case we can discard all the characters because all are misplaced. So, in
    the worst case we still have 2 options per parenthesis and that gives a complexity of O(2^N).
    Space complexity: O(N), we have to go to a maximum recursion depth of N before hitting the base case
    """

    def dfs(index, left, right, left_removals_remaining, right_removals_remaining, path):
        if index == n:
            if left_removals_remaining == right_removals_remaining == 0:
                res.add(''.join(path))
            return
        c = s[index]
        if c not in '()':
            dfs(index + 1, left, right, left_removals_remaining, right_removals_remaining, path + [c])
        elif c == '(':
            dfs(index + 1, left + 1, right, left_removals_remaining, right_removals_remaining, path + [c])
            if left_removals_remaining > 0:
                # Ignore the bracket if the count of remaining left parentheses to remove is 0
                dfs(index + 1, left, right, left_removals_remaining - 1, right_removals_remaining, path)
        else:
            if left > right:
                # If the current parenthesis is a closing bracket, we consider it only if we have more opening
                # brackets, i.e. balance > 0
                dfs(index + 1, left, right + 1, left_removals_remaining, right_removals_remaining, path + [c])
            if right_removals_remaining > 0:
                # Ignore the bracket if the count of remaining right parentheses to remove is 0
                dfs(index + 1, left, right, left_removals_remaining, right_removals_remaining - 1, path)

    n, res = len(s), set()
    left_unmatched = right_unmatched = 0
    # First, calculate the number of misplaced left and right parentheses
    for c in s:
        if c == '(':
            left_unmatched += 1
        elif c == ')':
            if left_unmatched > 0:
                # Decrement the count of unmatched left parentheses because we have found a right that CAN be a match
                left_unmatched -= 1
            else:
                # If we don't have a matching left, then this is a misplaced right, so record it.
                right_unmatched += 1
    dfs(0, 0, 0, left_unmatched, right_unmatched, [])
    return res


def remove_invalid_parentheses_v3(s):
    """ We are required to return the minimum number of invalid parentheses to remove. Let's model the problem as a
         graph:

            - node: string obtained by removing some parentheses, where the start node is the string s
            - edge (from u to v): remove a parenthesis from string u

         As a result, the problem becomes to first find the shortest distance from s to ANY valid node (say at level l),
         then find all valid nodes at level l.

         BFS guarantees the shortest path. Since the problem asks to remove the minimum number of parentheses, it is
         natural to think of BFS.

         The idea is straightforward: starting with the input string s, we generate all possible states by removing one
         '(' or ')' and check if they are valid. If we find valid strings at the current level, we add them to the final
         result list, and we are done. Otherwise, we add them to a queue and carry on to the next level.

         The one crucial observation is that once we find a valid expression, it means we have found the minimum
         number of needed removals since we are using BFS. Therefore, there is no need to search further. We just check
         all the valid expressions at that same level. In contrast, when using DFS, we need to keep track of the global
         minimum number of removals.

    Time complexity: O(2^N), at the first level there's only one string which is the input string s, let's say of
    length N. To check whether it's valid, we need O(N) time. At the second level, we remove one '(' or ')' from the
    first level, so there are C(N, N-1) new strings, each of them has N-1 characters, and for each string we need to
    check whether it's valid, thus the total time complexity at this level is (N-1) x C(N, N-1). Come to the third
    level, total time complexity is (N-2) x C(N, N-2), and so on and so forth. Finally, we have the formula
    T(N) = N x C(N, N) + (N-1) x C(N, N-1) + ... + 1 x C(N, 1) = N x 2^(N-1)
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
        if valid_expression_found:
            # This ensures once we've found a valid parentheses' expression, we don't do any further BFS using items
            # pending in the queue since any further BFS would only yield strings of smaller length, hence more
            # parentheses removals. However, the items already in queue need to be processed since there could be other
            # valid expressions of the same length. Once we have a string of length k that is valid, each of the strings
            # in the next level of length of k-1 is definitely invalid (we need to remove one or more parentheses to
            # make it valid).
            continue
        for i, c in enumerate(expression):
            if c not in '()':
                continue
            sub_expression = expression[:i] + expression[i + 1:]
            if sub_expression not in visited:
                queue.append(sub_expression)
                visited.add(sub_expression)
    return res
