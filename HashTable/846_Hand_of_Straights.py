""" Alice has some number of cards, and she wants to rearrange the cards into groups so that each group is of size
groupSize, and consists of groupSize consecutive cards.

Given an integer array hand where hand[i] is the value written on the ith card and an integer groupSize, return true if
she can rearrange the cards, or false otherwise. """

from collections import Counter
from heapq import heappush, heappop


def isNStraightHand_v1( hand, group_size):
    """ We can use a greedy approach. Sort the input array and start with the smallest number 'start' that has
         non-zero occurrences and check if the numbers from start to (start + k) exist in the array. If they do, we then
         keep removing them from the list of numbers, and if it's not possible to enumerate the entire sequence we
         return false.

            - Create a hashmap 'counter' to count the frequency of each card in the hand

            - Loop from the smallest card value 'start' that has a non-zero frequency

            - Try to find 'group_size' cards with consecutive values starting from 'start' card

         The intuition is if we know the first number in one of the groups, we can enumerate the entire group. That is
         to say, we just need to find all starting numbers of each group, then check if all the other numbers in the
         group can be found in the given hand.

         Since there might be groups with the same starting number, each time we use a card we decrement its count, and
         once its count drops to 0 we know the number is no longer available for future use.

    Time complexity: O(N logN + N), where N is the total number of cards. We sort the input array, which costs O(N logN),
    then we try to build a group of cards of size group_size which we can do N times in the worst case of group_size=1.
    Space complexity: O(N), for sort and frequency map
    """
    if len(hand) % group_size:
        return False
    hand.sort()
    n, counter = len(hand), Counter(hand)
    for i in range(n):
        if counter[hand[i]] == 0:
            continue
        start = hand[i]
        for _ in range(group_size):
            if counter[start] == 0:
                return False
            counter[start] -= 1
            start += 1
    return True


# Video explanation: https://youtu.be/amnrMCVd2YI (slightly different implementation)
def isNStraightHand_v2( hand, group_size):
    """ Similar approach but using a min heap instead of sorting the input.

        By using a priority queue, we can poll the smallest number and remove the next (group_size - 1) consecutive
        numbers. If any of the consecutive numbers is no longer available, it implies the hand is invalid, and thus we
        return false.

        Each time we want to find a starting number, we pop the heap. If the number is no longer available, we pop again
        until we find the minimum of the remaining numbers.

    Time complexity: O(N logN + N logN) ~= O(N logN), O(NlogN ) for building the heap then we have to extract all
    numbers from the heap if the entire array can be used, which is another O(N logN).
    Example: hand = [1, 2, 3, 4, 5, 6, 7, 8, 9], group_size = 3. We pop the first 3 elements and still have 6 elements,
    and heap is not empty yet. So we pop the next 3 elements, and we still have 3 elements. Then next iteration we pop
    the remaining 3 elements. So essentially, we are visiting each element once.
    Space complexity: O(N)
    """
    counter = Counter(hand)
    heap = []
    for card in hand:
        heappush(heap, card)
    while counter:
        start = heappop(heap)
        # Find the starting number of the current group
        while start not in counter:  # Number is no longer available
            start = heappop(heap)
        for _ in range(group_size):
            if start not in counter:
                return False
            counter[start] -= 1
            if counter[start] == 0:
                del counter[start]
            start += 1
    return True
