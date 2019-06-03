"""
You're given strings J representing the types of stones that are jewels, and S representing the stones you have.
Each character in S is a type of stone you have.  You want to know how many of the stones you have are also jewels.

The letters in J are guaranteed distinct, and all characters in J and S are letters. Letters are case sensitive,
so "a" is considered a different type of stone from "A".

Submitted to Leetcode by Anouer Hermassi
"""


def num_jewels_in_stones(j: str, s: str) -> int:

    valid_stones = [stone for stone in s if stone in j]
    return len(valid_stones)


if __name__ == '__main__':
    J = "aA"
    S = "aAAbbbb"
    print(num_jewels_in_stones(J, S))

    J = "z"
    S = "ZZ"
    print(num_jewels_in_stones(J, S))

"""
Runtime: 32 ms, faster than 97.41% of Python3 online submissions for Jewels and Stones.
Memory Usage: 12.9 MB, less than 99.39% of Python3 online submissions for Jewels and Stones.
"""
