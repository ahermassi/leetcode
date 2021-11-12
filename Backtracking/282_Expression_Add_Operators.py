""" Given a string num that contains only digits and an integer target, return all possibilities to insert the binary
operators '+', '-', and/or '*' between the digits of num so that the resultant expression evaluates to the target value.

Note that operands in the returned expressions should not contain leading zeros. """


def addOperators(num, target):
    """ Since the question explicitly states that we are given binary operators, this means that each of the operators
        would require two operands. We can consider each of our digits as an operand. This means that between every
        pair of digits we can have any of the three operators i.e. +, - or *.

        If we've looked at the question's statement and the examples that are given in the question, we would realize
        that there is an example where the digits are "105" and the target value is 5. For this particular example,
        there are two expressions given to us and they are 1*0+5 and 10-5.

        The second expression is something that we need to look out for before getting to solve this question because
        this complicates things a bit. It would have been an easier question to solve if we just had to consider those
        expressions that simply had digits as operands. But, in this question, we can have all sorts of digits getting
        together and forming a bigger number that becomes a part of the expression.

        So this means that although the number of operators are defined for us i.e. 3 different binary operators,
        the number of operands is not really well defined. This is a big portion of the original problem that we need
        to address in our solution.

        Since we are asked to find out all of the valid expressions whose value equals the given target and we don't
        really know what specific operator between two operands would eventually give us a valid expression, we try out
        all of the options. This means once we have defined what the operands are for our given expression, we would
        have three possible choices of operators between each consecutive pair of operands.

        Since we are required to return all of the valid expressions that evaluate to a given target value, we have to
        try all possible partitions of the given string thereby considering all of the possible operands that can be
        formed from the digits.

        There is a very simple way of incorporating this into our algorithm. Right now, at every point in the
        algorithm, we have three different choices corresponding to the three different operators. The way we
        incorporate these partitions is by considering a 4th operator as well which simply moves one step forward and
        extends the current operand by one digit.

        Essentially, going from 12 --> 123 is a NO OP operand in our implementation.

        Now we have 4 different recursion paths in our algorithm and we have to try out all of them to see which ones
        lead to a potential solution. This try-out-everything hints at a backtracking solution and that is exactly what
        we are going to look at here.

        The recursive call will have an index which represents the current digit we're looking at in the original nums
        string, and also the expression string built till now.

        At every step, we have exactly 4 different recursive calls. The NO OP call simply extends the current
        operand by the current digit and moves ahead. Rest of the recursive calls correspond to +, -, and *.
        We keep on building the expression like this and eventually, the entire nums string would be processed.
        At that time, we check if the expression we built till now is a valid expression or not and we record it if it
        is a valid one.

        The algorithm now looks pretty straightforward. However, the implementation is something that needs more
        thought and there are some things that we need to address before actually looking at the implementation.

        When we are done building an expression out of all of the digits in our original string i.e. the base case,
        then we check if the expression is a valid expression or not. Right ? How do we actually check if an expression
        is a valid one or not if all we have is a string representing the expression and not the integer value for the
        same?

        Well, one way to go about this is to write a custom eval function that takes in a string and returns the value
        of that expression. If we do that, we will get a TLE.

        Can't we keep track of the expression's value on the fly? Well yes. That's the idea we will go with.

        Instead of just keeping track of what the expression string is, we will also keep track of its value along the
        way so that when the recursion hits the base case, we can check in O(1) time if the expression's value equals
        the target value or not.

        The implementation would have been straightforward had it just been + and - operators involved. This is
        because both of these operators have an equal precedence. That means that we can continue to evaluate the
        expression on the fly without any problems.

        But, this approach is bound to fail because the * operator takes precedence over + and -. The * operator would
        require the actual PREVIOUS operand in our expression rather than the current value of the expression, if the
        expression is 10 + 2 * 4, the * operator needs 2 rather than 12 (10 + 2) to get us the correct value of 18.

        How to handle this?

        The idea springs from the discussion above. We simply need to keep track of the last operand in our expression
        and how it modified the expression's value overall so that when we consider the * operator, we can reverse the
        effects of the previous operand and consider it for multiplication.

        For example, if we have a sequence of 12345 and we have proceeded to 1 + 2 + 3, now the eval is 6. If we want
        to add a * between 3 and 4, we would take 3 as the digit to be multiplied, so we want to take it out from the
        existing eval. We have 1 + 2 + 3 * 4 and the eval now is (1 + 2 + 3) - 3 + (3 * 4).

    Time complexity: O(4^N), at every step along the way we consider exactly 4 different choices or 4 different
    recursive paths. The base case is when the value of index reaches N i.e. the length of the nums string
    Space complexity: O(N), the space used up by the recursion stack
    """

    def dfs(index, path, cur_eval, prev_operand):
        # prev_operand can be seen as "last contributed value to current eval cur_eval"
        if index == n:
            if cur_eval == target:
                res.append(path)
            return
        # Start from first index of current position in num string, try all possible lengths of num
        for i in range(index, n):
            # Avoid cases where we have 1 + 05 or 1 * 05 since 05 won't be a valid operand. If current position is 0,
            # we can only use it as a single digit number: 0
            if i > index and num[index] == '0':
                break
            cur_operand = int(num[index:i + 1])
            # Index 0 should be considered individually since it does not have any operand before current operand.
            # We need two operands for an operator and an operator can't be apply on a single operand
            if prev_operand is None:
                dfs(i + 1, path + str(cur_operand), cur_operand, cur_operand)
            else:
                dfs(i + 1, path + '+' + str(cur_operand), cur_eval + cur_operand, cur_operand)
                dfs(i + 1, path + '-' + str(cur_operand), cur_eval - cur_operand, -cur_operand)
                dfs(i + 1, path + '*' + str(cur_operand), cur_eval - prev_operand + prev_operand * cur_operand,
                    prev_operand * cur_operand)

    n, res = len(num), []
    dfs(0, '', 0, None)
    return res
