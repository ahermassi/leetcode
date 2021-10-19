""" We are given n different types of stickers. Each sticker has a lowercase English word on it.

You would like to spell out the given string target by cutting individual letters from your collection of stickers
and rearranging them. You can use each sticker more than once if you want, and you have infinite quantities of each
sticker.

Return the minimum number of stickers that you need to spell out target. If the task is impossible, return -1.

Note: In all test cases, all words were chosen randomly from the 1000 most common US English words, and target was
chosen as a concatenation of two random words. """

from collections import Counter, defaultdict


def min_stickers_v1(stickers, target):
    """ Backtracking.

        We start by building a frequency map of the target word. dfs() function has 3 parameters:
            - 'index': The index of the current character of 'target' being processed
            - 'stickers_used': The number of stickers used so far
            - 'chars_used': Frequency map of all the stickers' characters we have used up to the current index 'index'.

        At any point during the recursion, let 'c' be the target character at index 'index'.
        If chars_used[c] is greater than the frequency of c in target's frequency map, it means we have exhausted all
        the occurrences of 'c' needed to build 'target' and we can move on the next index.
        Otherwise, we look at all the stickers at hand, and for each sticker if it contains 'c' we can consider it as
        a candidate sticker and add its information, which is its characters and their frequencies, to 'chars_used'
        and proceed to the next index. We then delete the frequencies from 'chars_used' (backtrack).

        To avoid TLE, we only process the stickers if the number of stickers used so far plus 1 is less than the global
        minimum found so far, i.e. proceeding further COULD yield a better answer.

    Time complexity:
    Space complexity:
    """

    def dfs(index, stickers_used, chars_used):
        if index == n:
            res[0] = min(res[0], stickers_used)
            return
        c = target[index]
        if chars_used[c] >= counter[c]:  # I've had enough occurrences of 'c' to construct 'target'
            dfs(index + 1, stickers_used, chars_used)
        elif stickers_used + 1 < res[0]:
            for sticker in stickers:
                if c in sticker:
                    # If 'c' is in the sticker, we use the ENTIRE sticker, and that's how we get the minimum number of
                    # stickers needed as one sticker carries other characters along with 'c'
                    for ch in sticker:
                        chars_used[ch] += 1
                    dfs(index + 1, stickers_used + 1, chars_used)
                    for ch in sticker:
                        chars_used[ch] -= 1

    if any(c not in set(''.join(stickers)) for c in target):
        return -1
    n, res = len(target), [float('inf')]
    counter = Counter(target)
    dfs(0, 0, defaultdict(int))
    return res[0]


def min_stickers_v2(stickers, target):
    """ Top-Down Dynamic Programming.

        There are potentially a lot of overlapping sub-problems, but meanwhile we don't exactly know what those
        sub-problems are. DP with memoization works pretty well in such cases.

        The workflow is like backtracking, but with memoization. We use a substring of 'target' as the key for the
        DP array. Let dp[s] be the minimum stickers required to construct string s (-1 if impossible). Therefore:

            dp[''] = 0
            dp[s] = 1 + min({dp[reduced_s] for all stickers}), where reduced_s is a new string obtained after a
            certain sticker is applied

        This is similar to 322- Coin Change where dp(sum) = 1 + min(dp(sum - c_i) for all coins c_i).
        Reducing the substring of 'target' by applying the sticker is equivalent to subtracting the coin.

        If 'target' can be spelled out by a group of stickers, at least one of them has to contain character target[0].
        So we explicitly require next sticker to contain target[0], which significantly reduces the search space.
        If this sticker didn't contain the first character but contains the character after it and is unique, it will
        be picked in the future anyway (when next character becomes the first character). So we won't miss it due to
        this optimization.

    Time complexity:
    Space complexity:
    """

    def dfs(target):
        if target in memo:
            return memo[target]
        target_chars = Counter(target)
        res = float('inf')
        for sticker in stickers:  # Try every sticker
            if target[0] not in sticker:
                continue
            target_after_applying_sticker = target
            for c, count_in_sticker in sticker.items():  # Every sticker has the format {c1: count1, c2: count2,...}
                if c in target_chars:  # Apply the sticker on every character of 'target'
                    target_after_applying_sticker = target_after_applying_sticker.replace(c, '', count_in_sticker)
            # Find how many stickers are needed to build the rest of 'target' after this sticker was applied
            rest_of_target = dfs(target_after_applying_sticker)
            if rest_of_target != -1:
                res = min(res, 1 + rest_of_target)  # +1 to account for the current sticker
        memo[target] = res if res != float('inf') else -1
        return memo[target]

    stickers = [Counter(sticker) for sticker in stickers]
    memo = {'': 0}
    return dfs(target)
