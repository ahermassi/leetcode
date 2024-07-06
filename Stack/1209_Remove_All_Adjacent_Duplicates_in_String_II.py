""" You are given a string s and an integer k, a k duplicate removal consists of choosing k adjacent and equal letters
from s and removing them, causing the left and the right side of the deleted substring to concatenate together.

We repeatedly make k duplicate removals on s until we no longer can.

Return the final string after all such duplicate removals have been made. It is guaranteed that the answer is
unique. """


# Video explanation: https://youtu.be/w6LcypDgC4w
def remove_duplicates_v1(s, k):
    """ Notice that we consider groups of elements with the same value which are adjacent. If we delete them, other
        symbols will become adjacent. The stack is ideal for this purpose. When a character does not match the previous
        one, we push 1 to the stack. Otherwise, we increment the count on the top of the stack.

        So, we maintain a stack with pairs of elements: the character and its count. For each character:

            - If the current character is the same as the one before, increment the count on the top of the stack.
               Otherwise, push 1 to the stack.

            - If the count on the top of the stack equals k, erase last k characters and pop from the stack.

        Finally, build the result string using characters and counts in the stack.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack = []
    for c in s:
        if not stack or stack[-1][0] != c:
            stack.append([c, 1])
        else:
            stack[-1][1] += 1
        if stack[-1][1] == k:
            stack.pop()
    return ''.join([c * freq for c, freq in stack])


def remove_duplicates_v2(s, k):
    """ We can also use an in-place stack approach for the char array 'chars' formed from the input string, rather than
        using a separate stack.

        To do so, we use a two-pointer system in which one pointer 'left' keeps track of the end of the in-place
        "stack", while the 'right' pointer iterates over 'chars'.

        As we move 'right' through 'chars', we write to the stack 'chars' by overwriting chars[left] with chars[right].
        When we want to remove k elements from 'chars', we move 'left' back by k. Then, once we're done, we return the
        result string, which is the first part of 'chars' through 'left'.

        Example: S = 'aabbbcdddcc', k = 3 (another example in the png file):

                 i,j                                            // i, j start at 0
        S  = [ a, a, b, b, b, c, d, d, d, c, c ]    // S[j] overwrites S[i]
        stack = [ 1 ]                                    // i == 0, stack.push(1)

                    i,j                                          // i, j move up 1
        S  = [ a, a, b, b, b, c, d, d, d, c, c ]    // S[j] overwrites S[i]
        stack = [ 2 ]                                    // S[i] == S[i-1], increment top of stack

                    ->i,j                                     // i, j move up 1
        S  = [ a, a, b, b, b, c, d, d, d, c, c ]    // S[j] overwrites S[i]
        stack = [ 2, 1 ]                                // S[i] != S[i-1], stack.push(1)

                        ->i,j                                 // i, j move up 1
        S  = [ a, a, b, b, b, c, d, d, d, c, c ]    // S[j] overwrites S[i]
        stack = [ 2, 2 ]                                // S[i] == S[i-1], increment top of stack

                            ->i,j                              // i, j move up 1
        S  = [ a, a, b, b, b, c, d, d, d, c, c ]    // S[j] overwrites S[i]
        stack = [ 2, 3 ]                                // S[i] == S[i-1], increment top of stack

                     i<-------j                             // i moves back 3 steps because...
        S  = [ a, a, b--b--b, c, d, d, d, c, c ]    // ...3 b's found, so...
        stack = [ 2 ]                                       //  stack.pop()

                     ->i            ->j                          // i, j move up 1
        S  = [ a, a, c<-------c, d, d, d, c, c ]    // S[j] overwrites S[i]
        stack = [ 2, 1 ]                                     // S[i] != S[i-1], stack.push(1)

                        ->i             ->j                      // i, j move up 1
        S  = [ a, a, c, d<-------d, d, d, c, c ]    // S[j] overwrites S[i]
        stack = [ 2, 1, 1 ]                                 // S[i] != S[i-1], stack.push(1)

                            ->i                 ->j              // i, j move up 1
        S  = [ a, a, c, d, d<-------d, d, c, c ]    // S[j] overwrites S[i]
        stack = [ 2, 1, 2 ]                                 // S[i] == S[i-1], increment top of stack

                                ->i             ->j               // i, j move up 1
        S  = [ a, a, c, d, d, d<-------d, c, c ]    // S[j] overwrites S[i]
        stack = [ 2, 1, 3 ]                                 // S[i] == S[i-1], increment top of stack

                         i<--------        j             // i moves back because...
        S  = [ a, a, c, d--d--D,  ,  ,  , c, c ]    // ...3 d's found, so...
        stack = [ 2, 1 ]                                 // stack.pop()

                        ->i                             ->j           // i, j move up 1
        S  = [ a, a, c, c<----------------c, c ]    // S[j] overwrites S[i]
        stack = [ 2, 2 ]                                          // S[i] == S[i-1], increment top of stack

                            ->i                            ->j        // i, j move up 1
        S  = [ a, a, c, c, c<----------------c ]    // S[j] overwrites S[i]
        stack = [ 2, 3 ]                                         // S[i] == S[i-1], increment top of stack

                     i<--------                 j      // i moves back because...
        S  = [ a, a, c--c--c,  ,  ,  ,  ,  ,   ]     // ...3 c's found, so...
        stack = [ 2 ]                                  // stack.pop()

        S  = [ a, a ]                               // Only keep S up to i ..
        = "aa"                                      // then join to a string
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack, chars = [], list(s)  # Stack to hold the count of currently processed character and its eventual duplicates
    n = len(s)
    left = right = 0
    while right < n:
        chars[left] = chars[right]
        if left == 0 or chars[left] != chars[left - 1]:
            # For the first character and when the current and previous character are not equal, we start keeping count
            # of the current character
            stack.append(1)
        else:
            # Another occurrence of the previous character is encountered
            stack[-1] += 1
            if stack[-1] == k:
                stack.pop()
                left -= k
        left += 1
        right += 1
    return ''.join(chars[:left])

