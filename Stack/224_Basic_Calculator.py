""" Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the
result of the evaluation. s consists of digits, '+', '-', '(', ')', and ' '.

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as
eval(). """


def calculate(s):
    """ This question qualifies really well for a stack question. Since the expression might have parenthesis, we can
        use a stack to find the value for each sub-expression within a parenthesis. Essentially, we need to delay
        processing the main expression until we are done evaluating the interim sub-expressions within parenthesis,
        and to introduce this delay we use a stack.

        We push the elements of the expression one by one onto the stack until we get a closing bracket ). Then we pop
        the elements from the stack one by one and evaluate the expression on-the-go. This is done till we find the
        corresponding ( opening bracket. This kind of evaluation is very common when using the stack data structure.

        We need to understand how + and - work. + follows the associative property. For the expression A+B+C, we have
        (A+B)+C = A+(B+C). However, - does not follow this rule which is the root cause of all the problems.

        A very easy way to solve the problem of associativity for -  is to use - operator as the magnitude for the
        operand to the right of it. Once we start using - as a magnitude for the operands, we just have one operator
        left which is addition and + is associative.
        For e.g. A - B - C could be re-written as A + (-B) + (-C).
        The re-written expression would follow associativity rule.

        What we need to keep in mind is that the expressions given would be complicated, i.e. there would be
        expressions nested within other expressions. Even if we have something like (A - (B - C)) we need to associate
        the negative sign outside of B-C with the result of B-C instead of just with B.

        We can solve this problem by following the basic drill before and associating the sign with the expression to
        the right of it. However, the approach that we will instead take has a small twist to it in that we will be
        evaluating most of the expression on-the-go. This reduces the number of push and pop operations.

        Iterate the expression string one character at a time. Since we are reading the expression character by
        character, we need to be careful when we are reading digits and non-digits.

        The operands could be formed by multiple characters. A string "123" would mean a numeric 123, which could be
        formed as: 123 >> 120 + 3 >> 100 + 20 + 3. Thus, if the character read is a digit we need to form the operand
        by multiplying 10 to the previously formed continuing operand and adding the digit to it.

        Whenever we encounter an operator such as + or - we first evaluate the expression to the left and then save
        this sign for the NEXT evaluation.

        If the character is an opening parenthesis (, we just push the result calculated so far and the sign on to the
        stack (the sign is the magnitude) and start afresh as if we are calculating a new expression.

        If the character is a closing parenthesis ), we first calculate the expression to the left. The result from
        this would be the result of the expression within the set of parenthesis that just concluded. This result is
        then multiplied by the sign, if there is any on top of the stack. Remember we saved the sign on top of the
        stack when we had encountered an open parenthesis. This sign is associated with the parenthesis that started
        then, thus when the expression ends or concludes, we pop the sign and multiply it with result of the
        expression. It is then just added to the next element on top of the stack.

        It's possible that we don't have any more characters left to process but the stack is still non-empty. This
        would happen when the main expression is not enclosed by parenthesis. So, once we are done evaluating the
        entire expression, we check if the stack is non-empty. If it is, we treat the elements in it as one final
        expression and evaluate it the same way we would if we had encountered an opening bracket.

    Time complexity: O(N), where N is the length of the string. Every character will get processed exactly once
    Space complexity: O(N)
    """
    ongoing_sum, num, last_sign = 0, 0, 1  # 1 means positive, -1 means negative
    stack = []
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in '+-':
            ongoing_sum += num * last_sign  # Evaluate the expression to the left of the +/-
            last_sign = 1 if c == '+' else -1  # Save the recently encountered sign
            num = 0  # Reset operand
        elif c == '(':
            # Push the result and the sign to the stack for later
            stack.append(ongoing_sum)
            stack.append(last_sign)
            # Reset operand and result as if a new evaluation begins for the new sub-expression
            ongoing_sum, last_sign = 0, 1
        elif c == ')':
            # Evaluate the expression to the left of the closing parenthesis
            ongoing_sum += num * last_sign
            # ')' marks the end of the expression within the set of parenthesis. Its result is multiplied by the sign
            # on top of the stack, as stack.pop() is the sign before the parenthesis
            ongoing_sum *= stack.pop()
            # Add to the next operand on the top, as stack.pop() is the result calculated before this parenthesis:
            # (operand on stack) + (sign on stack * (result from parenthesis))
            ongoing_sum += stack.pop()
            num = 0  # Reset the operand
    ongoing_sum += num * last_sign
    return ongoing_sum


