""" Given a string, find the length of the longest substring without repeating characters. """

import unittest2 as unittest


def length_of_longest_substring_v0(s):
    """ Brute force. Check all the substring one by one to see if it has no duplicate character.

         To check if one substring has duplicate characters, we can use a hash set. We iterate through all the characters
         in the substring and put them into the set one by one. Before putting one character, we check if the set
         already contains it.

    Time complexity: O(N^2)
    Space complexity: O(N), or O(1) if the set of characters considered is the English alphabet O(26)
    """
    n, res = len(s), 0
    for i in range(n):
        chars = {s[i]}
        j = i + 1
        while j < n and s[j] not in chars:
            chars.add(s[j])
            j += 1
        res = max(res, j - i)
    return res


def length_of_longest_substring_v1(s):
    """ Given a substring with a fixed end index in the string, maintain a hash map to record the occurrence of each
         character in the current substring. If any character occurs more than once, drop the leftmost characters until
         there are no duplicate characters.

         In the brute force approach, we repeatedly check a substring to see if it has duplicate character. But it is
         unnecessary. If a substring s(i,j) from index i to j-1 was already checked to have no duplicate characters, we
         only need to check if s[j] is already in the substring s(i,j).

        We will reuse previous computation as we iterate through the string. Suppose we know the longest duplicate-free
        substring ending at a given index right. The longest duplicate-free substring ending at index right+1 is either:

            1- The previous substring extended with the element at index right+1, if that element does not appear in
                 the longest duplicate-free substring ending at index right
            2- The substring beginning at the most recent occurrence of the element at index right+1 plus 1

        To perform this case analysis as we iterate, all we need is a hash table storing the most recent occurrence of
        each character, and the longest duplicate-free substring ending at the current index.

        The basic idea is to keep a hash map which stores the characters in string as keys and their indices as values,
        then we can skip the characters immediately when we find a repeated character.

        We use two pointers which define the max substring. Move the right pointer 'right' to scan the string, and in
        the meanwhile update the hash map. If the current character is already in the hash map, then move the left
        pointer 'left' after the last occurrence of this repeated character. The reason is that if s[right] has a
        duplicate in the range [left, right) at index j, we can skip all the elements in the range [left, j] and let
        'left' be equal to (j + 1). This is because we need to make sure our left pointer is at least past the index
        where we last saw the current duplicate character, so we move 'left' to (last_occurrence[right] + 1). We also
        need to ensure that 'left' always moves forward or just stays at its position.

        Example: s = 'fsfetwenwe'. When we process the element at index 2, the longest duplicate-free substring ending
        at index 1 is from 0 to 1. The hash table tells us that the element at index 2, namely f, appears in that
        substring, so we update the longest substring ending at index 2 to being from index 1 to 2.
        Indices 3-5 introduce fresh elements. Index 6 holds a repeated value, e, which appears within the longest
        substring ending at index 5; specifically, it appears at index 3. Therefore, the longest substring ending at
        index 6 starts at index 4.

        Example:

        index    0    1    2    3   4   5   6   7
        string   a    c    b    d   b   a   c   d
                 ^                  ^
                 |                  |
		        left               right

		last_occurrence = {a : 0, c : 1, b : 2, d: 3}
		# case 1: last_occurrence[b] = 2, current window  is s[0:4] ,
		#         b is inside current window, last_occurrence[b] = 2 > left = 0. Move left pointer to last_occurrence[b] + 1 = 3
		last_occurrence = {a : 0, c : 1, b : 4, d: 3}

        index    0    1    2    3   4   5   6   7
        string   a    c    b    d   b   a   c   d
						        ^   ^
					            |   |
				              left  right

        index    0    1    2    3   4   5   6   7
        string   a    c    b    d   b   a   c   d
					            ^       ^
					            |       |
				              left    right
		# case 2: last_occurrence[a] = 0, which means 'a' is not in current window s[3:5] , since last_occurrence[a] = 0 < left = 3
		# We can keep moving right pointer.

    Time complexity : O(N)
    Space complexity: O(N), or O(1) if the set of characters considered is the English alphabet O(26)
    """
    last_occurrence = {}
    n, res = len(s), 0
    left = right = 0  # 'left' denotes the left end of the longest substring with no repeating characters seen so far
    while right < n:  # 'right' is the right end of that string, or the right boundary of our sliding window
        if s[right] in last_occurrence:  # If this is a duplicate character
            # Slide the window past the last recorded occurrence of the duplicate character
            left = max(left, last_occurrence[s[right]] + 1)
            # The variable 'left' is used to indicate the index of first character of this substring/window. If the
            # duplicate character's index is less than 'left' itself, this means the duplicate character in the hash
            # map is no longer available at this time and is already outside the current window.
            # Consider the input:  s = 'tmsmfdut'
            # When right = s.length()-1 = 7, left = 2 after we've encountered the first repeated 'm',
            # so the current window is defined by left=2, right=7, substring='smfdut' If we update
            # left = last_occurrence['t'] + 1, then 'left' will be equal to 1 because the previous occurrence
            # of 't' is at index 0, and this will give a wrong answer. For this reason, 'left' should not be set to
            # (last_occurrence[c] + 1) as this value is less than current value of left = 2, or in simple words
            # (last_occurrence_index[c] + 1) is outside the window defined by left=2 and right=7.
            # If we have a string  like 'abba', when we encounter the second 'a', we want to mark the start of the
            # duplicate-free string from index 2 (second occurrence of 'b') which is the last known index which
            # holds uniqueness assumption, not from (last_occurrence['a'] + 1) which is 1.
        res = max(res, right - left + 1)
        last_occurrence[s[right]] = right
        right += 1
    return res


def length_of_longest_substring_v2(s):
    """ Similar idea to previous solution but uses a hash set to keep track of the characters processed so far (window).
        The only difference is that as long as the current character at 'right' pointer is duplicate, we delete from
        the head of the window by moving 'left' pointer forward one step at a time until the occurrence of the
        duplicate character is removed, then we can add the character at 'right' index to the hash set.
    Time complexity: O(N)
    Space complexity: O(N), or O(1)
    """
    n = len(s)
    prev_chars = set()  # A hash set is used to represent the current sliding window
    res = left = right = 0
    while right < n:
        c = s[right]
        while c in prev_chars:
            prev_chars.remove(s[left])
            left += 1  # Notice that only 'left' moves forward. This is running a while loop that keeps deleting
            # characters at 'left' index until we get rid of the duplicate character at 'right'
        prev_chars.add(c)
        res = max(res, right - left + 1)
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('abcabcbb', 3), ('bbbbb', 1), ('pwwkew', 3)]

    def test_length_of_longest_substring(self):
        for test_string, result in self.data:
            self.assertEqual(result, length_of_longest_substring_v0(test_string))
            self.assertEqual(result, length_of_longest_substring_v1(test_string))
            self.assertEqual(result, length_of_longest_substring_v2(test_string))


if __name__ == '__main__':
    unittest.main()
