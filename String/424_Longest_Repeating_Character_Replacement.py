""" Given a string s that consists of only uppercase English letters, you can perform at most k operations on that
string.
In one operation, you can choose any character of the string and change it to any other uppercase English character.
Find the length of the longest sub-string containing all repeating letters you can get after performing the above
operations. """

from collections import defaultdict
import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=gqXU1UyA8pk


def character_replacement_v1(s, k):
    """ Given a substring, we want to find out if it can be converted into a string with the same letters. Because
         we are allowed only k operations to do so, we would want to MINIMIZE the number of operations.

         We can divide all the characters of the string s into two groups - fixed letters and the letters that will be
         changed. Fixed letters remain unchanged. The rest of the letters would be substituted by fixed letters.
         To keep the number of substitutions minimum, the number of fixed letters must be maximum.

        Inn other words, if we want to replace the characters in a substring and make it into the longest repeating,
        then we definitely want to find the character with maximum frequency and then replace all the other characters
        with this one, hence in this way, we can minimize the number of replacements.

        Given this, we can apply the at-most-k-changes constraint and maintain a sliding window such that:

                size of window - frequency of the most frequent letter in the window <= k

        i.e. max characters to replace = size of window - frequency of the most frequent letter in the window

        So, we find the character which occurs with the maximum frequency in the string. All other characters can now
        be replaced with this character. If the count of other characters is less than or equal to k, then this
        substring fulfills the condition, and we'd call it a valid substring. The length of the longest valid substring
        would be our answer.

        IMPORTANT: Using induction, we can say that if there exists a valid substring of length L, then all of its
        substrings of lengths L-1, L-2, L-3... 2, and 1 would also be valid.

        Suppose we have identified a valid substring/window of length L-1. To find an even longer valid window, we
        should try adding the next character. This temporarily increases the size of the window to L. We check whether
        it forms a valid window or not. If not, we shift the beginning of the window to the right, which resets the
        window size back to L-1 and effectively moves the window to the right.

        We keep moving it until we reach a point where we find a valid window of size L. Now, we don't need to stop
        there. We can continue looking for a valid window of size L+1. We continue this process until the window hits
        the right edge of the string. The size of the window at the end would be our answer.

        The key takeaway here is that once we have found a valid window, we don't need to decrease its size. The window
        keeps moving toward the right. At each step, even if the window becomes invalid, we never decrease its size.
        We increase the size only when we find a valid window of larger size.

        While the window is valid, we expand it by moving the right pointer forward. As we do so, we also note the
        maximum length of the window seen so far. When the window becomes invalid, we shrink the size by moving
        the left pointer forward. Left pointer moves until the window becomes valid again. The process continues until
        the window reaches the right edge of the string and can't move any further.

        The frequency map helps us keep track of the character that appears most frequently in the window.
        Every time right pointer moves forward, we update the frequency map of the newly added character. We also update
        max_frequency if the added character's frequency is the maximum we have seen so far.

        Each time we expand right, we include a new character in the window. If the max number of characters to replace
        in the current window is bigger than k, we get an invalid window, and so we shrink the window from the left.

        !!! VERY IMPORTANT !!!

                max_frequency does NOT tell us the maximum frequency of a character in the CURRENT WINDOW.
                Rather, it tells us the maximum frequency of a character SEEN UNTIL NOW.

                max_frequency == maximum frequency of a character across all chars IN THE LAST SEEN VALID WINDOW

        We don't need to recalculate max_frequency when we increment the left pointer because if the new max
        frequency is less than whatever we have seen so far, surely our window will not be a better solution.

        We are checking window validity using (window_size - max_frequency) <= k and window_size remains constant
        after a valid window becomes invalid, as we increment left by one if invalid and right moves forward with
        every iteration. Hence, an invalid window of size L can only ever become a valid window of size L + 1 if
        max_frequency INCREASES past the max_frequency of the last seen valid window/substring.
        Since we only care about max_frequency increasing past the max_frequency of the last seen valid window, we
        don't need to care when a window is invalidated and the most frequent char was removed as it only decreases
        max_frequency. Any update to max_frequency that increases it is accurate as counter[ s[right]] is always
        updated.

        Shifting our start pointer means we have reached the limit (k), and a next/future interval must have a greater
        max_frequency to replace our current longest.

        At any given window, max_frequency will only be violated if the start index happens to be pointing at the char
        with max frequency. For example: "AABBA", left = 0, right = 4. If we shrink the window by moving the start
        pointer to the right by 1, max_frequency should be 2 instead of 3.
        BUT, keep in mind that the way we validate the window is by comparing (window_size - max_frequency) with k.
        When the situation described earlier happens, notice that the most frequent char is removed from both the
        max_frequency count AND the window_size count. In other words, "the number of chars that need to be replaced"
        becomes (window_size - 1) - (max_frequency - 1). The two -1s cancel each other out.

        Example:
        s = C A A A B C B A B B A; k = 2
                    ^          ^
                    |           |
                left=2    right=6
        counter = {'A': 2, 'B': 2, 'C: 1}, HOWEVER  max_frequency = 3 from a previous valid window.
        If we recalculate max_frequency in the current window, it will be 2 (of A or B), which actually makes the
        substring invalid, because we can't convert all 5 characters into A or B with at most k=2 replacements.
        But we've previously seen a valid window of size 5. We don't want to decrease the size of the window, and
        max_frequency helps us achive that.

    Time complexity: O(N), we access each index of the string at most two times, when it is added to the sliding window
    and when it is removed from the sliding window.
    Space complexity: O(1), the maximum number of keys in the map equals the number of unique characters in the string,
    which is the size of English alphabet
    """
    n = len(s)
    left = right = max_frequency = res = 0
    counter = defaultdict(int)
    while right < n:
        counter[ s[right]] += 1
        max_frequency = max(max_frequency, counter[s[right]])
        window_size = right - left + 1
        max_replacements = window_size - max_frequency
        if max_replacements <= k:
            res = max(res, window_size)
        else:
            counter[s[left]] -= 1
            left += 1
        right += 1
    return res


def character_replacement_v2(s, k):
    """ Same idea but we keep shrinking the window from the left AS LONG AS the max number of character replacements
        exceeds k.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(s)
    left = right = max_frequency = res = 0
    counter = defaultdict(int)
    while right < n:
        c = s[right]
        counter[c] += 1
        max_frequency = max(max_frequency, counter[c])
        while right - left +  1 - max_frequency > k:
            counter[s[left]] -= 1
            left += 1
        res = max(res, right - left + 1)
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('ABAB', 2, 4), ('AABABBA', 1, 4)]

    def test_character_replacement(self):
        for test_s, test_k, result in self.data:
            self.assertEqual(result, character_replacement_v2(test_s, test_k))


if __name__ == '__main__':
    unittest.main()