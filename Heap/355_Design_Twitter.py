""" Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to
see the 10 most recent tweets in the user's news feed.

Implement the Twitter class:

Twitter() Initializes your twitter object.
void postTweet(int user_id, int tweet_id) Composes a new tweet with ID tweet_id by the user user_id.
Each call to this function will be made with a unique tweet_id.
List<Integer> getNewsFeed(int user_id) Retrieves the 10 most recent tweet IDs in the user's news feed.
Each item in the news feed must be posted by users who the user followed or by the user themselves.
Tweets must be ordered from most recent to least recent.
void follow(int follower_id, int followee_id) The user with ID follower_id started following the user with ID followee_id.
void unfollow(int follower_id, int followee_id) The user with ID follower_id started unfollowing the user with ID followee_id.
 """
from collections import defaultdict
from heapq import heappush, heappop


class Twitter:
    """  Use a hash map to track the tweets for each user. When we need to generate news feed, merge the
        news feeds for all the followees in a min heap of size 10 which will allow us to retrieve the 10 most
        recent tweets.
    """

    def __init__(self):
        self.followers = defaultdict(set)
        self.tweets = defaultdict(list)
        self.timestamp = 1

    def postTweet(self, user_id, tweet_id):
        """ Time complexity: O(1) """
        self.tweets[user_id].append((self.timestamp, tweet_id))
        self.timestamp += 1

    def getNewsFeed(self, user_id):
        """ Time complexity: O(#followees * #tweets) """
        followees = self.followers[user_id]
        followees.add(user_id)   # Add myself to the list of my followees
        heap, res = [], []
        for followee in followees:  # O(#followees)
            for timestamp, tweet_id in self.tweets[followee]:  # O(#tweets))
                heappush(heap, (timestamp, tweet_id))  # O(log10) ~= O(1)
                if len(heap) > 10:
                    heappop(heap)
        while heap:
            res.append(heappop(heap)[1])
        return res[::-1]

    def follow(self, follower_id, followee_id):
        """ Time complexity: O(1) """
        self.followers[follower_id].add(followee_id)

    def unfollow(self, follower_id, followee_id):
        """ Time complexity: O(1) """
        if followee_id in self.followers[follower_id]:
            self.followers[follower_id].remove(followee_id)