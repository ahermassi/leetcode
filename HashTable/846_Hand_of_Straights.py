""" Alice has some number of cards, and she wants to rearrange the cards into groups so that each group is of size
groupSize, and consists of groupSize consecutive cards.

Given an integer array hand where hand[i] is the value written on the ith card and an integer groupSize, return true if
she can rearrange the cards, or false otherwise. """

from collections import Counter


def isNStraightHand( hand, group_size):
    """ We can use a greedy approach. Sort the input array and start with the smallest number 'start' that has a nonzero
         frequency and check if the numbers from start to (start + k) exist. If they do, we then keep removing them from
         the numbers we have, and if there is a case where it's not possible then we return false.

            - Count the number of different cards counter in a map 'counter'
            - Loop from the smallest card number 'start' that has a nonzero frequency
            - Try to find 'group_size' cards with consecutive values starting from 'start' card

    Time complexity: O(N logN + N), where N is the total number of cards. We sort the input array, which costs O(N logN),
    then we try to build a group of cards of size group_size which we can do N times in the worst case of group_size=1.
    Space complexity: O(N), for sort and frequency map
    """
    if len(hand) % group_size:
        return False
    n = len(hand)
    hand.sort()
    counter = Counter(hand)
    while counter:
        i = 0
        while i < n and hand[i] not in counter:
            i += 1
        cur_hand = hand[i]
        for _ in range(group_size):
            if cur_hand not in counter:
                return False
            counter[cur_hand] -= 1
            if counter[cur_hand] == 0:
                del counter[cur_hand]
            cur_hand += 1
    return True
