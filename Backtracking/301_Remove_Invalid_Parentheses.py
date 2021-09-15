""" Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make
the input string valid.

Return all the possible results. You may return the answer in any order. """


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
