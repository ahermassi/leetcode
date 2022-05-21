""" Given a 2D board and a list of words from the dictionary, find all words in the board.
Each word must be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally
or vertically neighboring. The same letter cell may not be used more than once in a word. """

from collections import defaultdict

# Video explanation: https://www.youtube.com/watch?v=asbcE9mZz_U


class TrieNodeV1:
    def __init__(self):
        self.children = defaultdict(TrieNodeV1)
        self.end_of_word = False


def find_words_v1(board, words):
    """ Intuitively, in order to cross out all potential words, the overall strategy would be to iterate the cells one
        by one, and from each cell we walk along its neighbors in four potential directions to find matched words.
        While wandering around the board, we would stop the exploration when we know it would not lead to the discovery
        of new words.

        However, during the backtracking process, we would encounter more often the need to tell if there exists any
        word in the dictionary that contains a certain prefix, rather than if an entire string exists as a word in the
        dictionary.

        The capability of finding a matching prefix is where the Trie data structure shines, compared to the hashset.
        Not only can a Trie tell the membership of a word, but also it can instantly find the words that share a given
        prefix.

        If we know that there does not exist any match in the dictionary for a given prefix, then we would not need
        to further explore certain direction. This would greatly reduce the exploration space, therefore improve the
        performance of the backtracking algorithm.

        The overall workflow of the algorithm is intuitive, and it consists of a loop over each cell in the board and a
        recursive function call starting from that cell. Here is the skeleton of the algorithm.

            - We build a Trie out of the words in the dictionary, which would be used later for prefix matching.

            - Starting from each cell, we start the backtracking exploration (i.e. search(cell)), if there exists any
              word in the dictionary, i.e. in the trie, that starts with the letter in the cell.

            - During the recursive function call search(cell), we explore the neighbor cells around the current cell
              for the next recursive call search(neighborCell). At each call, we check if the sequence of letters that
              we traversed so far matches any word in the dictionary with the help of the trie that we built.
              If a match is found, we add the word to the result list and remove it from the trie to avoid duplicate
              results.

        This last pruning idea is motivated by the fact that the time complexity of the overall algorithm sort of
        depends on the size of the trie. For a leaf node in the trie, once we traverse it (i.e. find a matched word), we
        would no longer need to traverse it again. Therefore, we could prune it out from the trie.

        Use a 'one time search' trie. As a side benefit, we do not need to check if there is any duplicates in
        the result set. As a result, we could simply use a list instead of set to keep the results, which could speed
        up the solution a bit.

        Bottom line:

                        We use a trie so that we can exit the backtracking early when the current path is not a prefix
                        of any word in the trie.

        This is what the board looks like after each visit (words = ['oath', 'pea', 'eat', 'rain']):
        o | a | a | n |
        e | t | a | e  |
        i | h | k | r  |
        i | f | l   | v  |

        # | a | a | n |
        e | t | a | e  |
        i | h | k | r  |
        i | f | l   | v  |

        # | # | a | n |
        e | t | a | e  |
        i | h | k | r  |
        i | f | l   | v  |

        # | # | a | n |
        e | # | a | e |
        i | h | k | r  |
        i | f | l   | v |

        # | # | a | n |
        e | # | a | e |
        i | # | k | r  |
        i | f | l   | v |

        o | a | a | n |
        # | t | a | e  |
        i | h | k | r  |
        i | f | l   | v |

        o | a | a | n |
        e | t | a | # |
        i | h | k | r |
        i | f | l | v |

        o | a | a | n |
        e | t | # | # |
        i | h | k | r |
        i | f | l | v |

        o | a | a | n |
        e | # | # | # |
        i | h | k | r |
        i | f | l | v |

        o | a | a | n |
        e | t | a | e |
        i | h | k | # |
        i | f | l | v |

    Time complexity: O(N * M * 4 * (3^L)), where N * M is the number of cells in the board and L is the maximum length
    of words. It is tricky to calculate the exact number of steps that a backtracking algorithm would perform.
    We provide an upper bound of steps for the worst scenario for this problem. The algorithm loops over all the cells
    in the board, therefore we have N * M as a factor in the complexity formula. It then boils down to the maximum
    number of steps we would need for each starting cell.
    Assume the maximum length of word is L, starting from a cell, initially we would have at most 4 directions to
    explore. Assume each direction is valid (i.e. worst case), so during the following exploration we have at most 3
    neighbor cells (excluding the cell where we come from) to explore. As a result, we would traverse at most 4 * (3^L)
    cells during the backtracking exploration.
    Space complexity: O(C), where C is the total number of letters in the dictionary of words. In the worst case where
    there is no overlapping of prefixes among the words, the trie would have as many nodes as the letters of all words.
    """

    def addWord(word, root):
        for c in word:
            root = root.children[c]
        root.end_of_word = True

    def search(i, j, node, word):
        if not 0 <= i < n or not 0 <= j < m or board[i][j] not in node.children:
            return
        c = board[i][j]
        node = node.children[c]
        word += c
        if node.end_of_word:  # Check if we found a match of word
            res.append(word)
            node.end_of_word = False  # Remove the matched word to avoid duplicates. Since we already completed that
            # word and added it to the result array, we don't want to get duplicates of that word, so we set the flag
            # to False. Example: words = ['aaa','aaab']. After matching 'aaa', when we search for 'aaab' we will add
            # 'aaa' again if we don't set its flag to False.
        board[i][j] = '#'  # Before the exploration, mark the cell as visited
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            search(x, y, node, word)
        board[i][j] = c  # End of exploration, so we restore the cell

    trie = TrieNodeV1()
    n, m, res = len(board), len(board[0]), []
    for word in words:
        node = trie
        addWord(word, node)
    for i in range(n):
        for j in range(m):
            search(i, j, trie, '')
    return res


class TrieNodeV2:
    def __init__(self):
        self.children = dict()
        self.word = None


def find_words_v2(board, words):
    """ One optimization is to keep words in the Trie. Doing so could improve the performance of the algorithm a bit.
        One benefit is that we would not need to pass the prefix as the parameter in the search() call, and this could
        speed up a bit the recursive call.
    """

    def addWord(word, root):
        for c in word:
            if c not in root.children:
                root.children[c] = TrieNodeV2()
            root = root.children[c]
        root.word = word

    def search(i, j, root):
        if not 0 <= i < n or not 0 <= j < m or board[i][j] not in root.children:
            return
        c = board[i][j]
        board[i][j] = '#'
        root = root.children[c]
        if root.word:  # Check if we find a match of word
            res.append(root.word)
            root.word = None  # Remove the matched word to avoid duplicates
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            search(x, y, root)
        board[i][j] = c

    root = TrieNodeV2()
    n, m, res = len(board), len(board[0]), []
    for word in words:
        node = root
        addWord(word, node)
    for i in range(n):
        for j in range(m):
            search(i, j, root)
    return res


def find_words_v3(board, words):
    """ A nicer way of defining the trie: dictionary of dictionaries.
        Example: word = 'test', trie = {'t': {
                                              'e': {
                                                    's': {
                                                          't': {
                                                                '$': '$'
                                                                }
                                                         }
                                                   }
                                             }
                                       }
    """

    def addWord(word, trie):
        for c in word:
            if c not in trie:
                trie[c] = {}
            trie = trie[c]
        trie['$'] = '$'

    def search(i, j, word, root):
        if not 0 <= i < n or not 0 <= j < m or board[i][j] not in root:
            return
        c = board[i][j]
        board[i][j] = '#'
        root = root[c]
        if '$' in root:
            res.append(word + c)
            del root['$']
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            search(x, y, word + c, root)
        board[i][j] = c

    root = {}
    n, m, res = len(board), len(board[0]), []
    for word in words:
        trie = root
        addWord(word, trie)
    for i in range(n):
        for j in range(m):
            search(i, j, '', root)
    return res