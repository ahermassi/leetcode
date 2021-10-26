""" A valid number can be split up into these components (in order):

A decimal number or an integer.
(Optional) An 'e' or 'E', followed by an integer.

A decimal number can be split up into these components (in order):

- (Optional) A sign character (either '+' or '-').
- One of the following formats:
    - One or more digits, followed by a dot '.'.
    - One or more digits, followed by a dot '.', followed by one or more digits.
    - A dot '.', followed by one or more digits.

An integer can be split up into these components (in order):

- (Optional) A sign character (either '+' or '-').
- One or more digits.

For example, all the following are valid numbers: ["2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3", "3e+7",
"+6e-1", "53.5e93", "-123.456e789"], while the following are not valid numbers: ["abc", "1a", "1e", "e3", "99e2.5",
"--6", "-+3", "95a54e53"].

Given a string s, return true if s is a valid number. """


def is_number(s):
    """ The problem statement outlines a very specific set of rules. Let's put all possible characters into groups,
        and then create a set of rules for each group. Then, we can iterate through the input and evaluate if the
        characters are following the rules or not.

        What are all of the possible character groups, and what can we say about them? Reading through the problem
        statement very carefully, we can ascertain:

        Digits (one of ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]): Both decimal numbers and integers must
        contain at least one digit.

        A sign ("+" or "-"): Sign characters are optional for both decimal numbers and integers, but if one is present,
        it will always be the first character. Note that this means that a sign character can also appear immediately
        after an exponent.

        An exponent ("e" or "E"): Exponents are also optional, but if the string contains one then it must be after a
        decimal number or an integer. Furthermore, an integer must follow the exponent.

        A dot ("."): A decimal number should only contain one dot. Integers cannot contain dots.

        Anything else: There will never be anything else in a valid number.

        From these facts, we can logically determine a set of rules to follow in our algorithm.

        Digits: First of all, there must always be at least one digit in the input for it to form a valid number.
        Let's use a variable seen_digit to indicate whether we have seen a digit yet.

        Signs: If a sign is present, it must be the first character in a decimal number or integer. In a valid number,
        there are two possible locations for these signs - at the front of the number, or right after an exponent
        ("e" or "E") e.g., -63e+7. Therefore, if we see a sign, and it is not the first character of the input, and
        does not come immediately after an exponent ("e" or "E"), then we know the number is not valid.

        Exponents ("e" or "E"): There cannot be more than one exponent in a valid number, so we will use a variable
        seen_exponent to indicate whether we have already seen an exponent. An exponent must appear after a decimal
        number or an integer. This means if we see an exponent, we must have already seen a digit.

        Dots: There cannot be more than one dot in a valid number, since only integers are allowed after an exponent,
        so there cannot be more than one decimal number. We will use a variable seen_dot to indicate whether we have
        seen a dot. If we see a dot appear after an exponent, the number is not valid, because integers cannot have
        dots.

        Anything else: Seeing anything else instantly invalidates the input.

        Now that we have laid out the rules, let's iterate over the input. For each character, determine what group it
        belongs to, and verify that it follows the rules.

        Declare 3 variables seen_digit, seen_exponent, and seen_dot. Set all of them to false.
        Iterate over the input.
        If the character is a digit, set seen_digit = true.
        If the character is a sign, check if it is either the first character of the input, or if the character before
        it is an exponent. If not, return false.
        If the character is an exponent, first check if we have already seen an exponent or if we have not yet seen a
        digit. If either is true, then return false. Otherwise, set seen_exponent = true, and seen_digit = false. We
        need to reset seen_digit because after an exponent we must construct a new integer.
        If the character is a dot, first check if we have already seen either a dot or an exponent. If so, return
        false. Otherwise, set seen_dot = true.
        If the character is anything else, return false.
        At the end, return seen_digit. This is one reason why we have to reset seen_digit after seeing an exponent.
        Otherwise, an input like "21e" would be incorrectly judged as valid.

        Summary of the rules:

        We can only see "." if we didn't see "e" or "E" or "."
        We can only see "e" or "E" if we didn't see "e" or "E" but we did see a number. We reset digits flag
        We can only see "+" and "-" in the beginning or after an "e" or "E"
        Any other character breaks the validation
        At the and it is only valid if there was at least 1 digit

    Time complexity: O(N), where N is the length of s
    Space complexity: O(1)
    """

    seen_digit = seen_exponent = seen_dot = False
    for i, c in enumerate(s):
        if c.isdigit():
            seen_digit = True
        elif c in '+-':
            if i > 0 and s[i - 1] not in 'eE':  # Sign can appear in the middle only when "e" or "E" appears before
                return False
        elif c in 'eE':
            # "e" and "E" cannot appear twice and digits must be in front of them
            if seen_exponent or not seen_digit:
                return False
            seen_exponent = True
            seen_digit = False  # If there's an exponent, there HAS to be a number following it
        elif c == '.':
            # "." cannot appear twice and it cannot appear after "e" or "E"
            if seen_dot or seen_exponent:
                return False
            seen_dot = True
        else:
            return False
    return seen_digit  # Making sure there is at least a digit in s and/or at least a digit followed an exponent


# There is a second solution that uses Deterministic Finite Automaton. If interested, look here:
# https://leetcode.com/problems/valid-number/discuss/23728/A-simple-solution-in-Python-based-on-DFA
# https://leetcode.com/problems/valid-number/discuss/360781/Python-with-state-machine-36ms
