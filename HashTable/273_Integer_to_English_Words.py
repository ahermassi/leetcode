""" Convert a non-negative integer num to its English words representation. """


def number_to_words_v1(num):
    """ Let's simplify the problem by representing it as a set of simple sub-problems.

        We could split the initial integer 1234567890 into groups containing no more than three digits: 1.234.567.890.
        That results in the following representation: "1 Billion 234 Million 567 Thousand 890" and reduces the initial
        problem to how to convert a 3-digit integer to an English word.

        We could further split 234: "2 Hundred 34" resulting into two sub-problems : Convert a 1-digit integer and
        convert a 2-digit integer. The first one is trivial. The second one could be reduced to the first one for all
        2-digit integers except the ones from 10 to 19 which should be considered separately.


    Time complexity: O(log10 N), intuitively the output is proportional to the number of digits in the input
    Space complexity: O(1)
    """

    def decompose(num):
        if num < 20:
            res = less_than_20[num]
        elif num < 100:
            res = tens[num // 10] + ' ' + decompose(num % 10)
        else:
            res = less_than_20[num // 100] + ' Hundred ' + decompose(num % 100)
        return res.rstrip()

    less_than_20 = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven',
                    'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    thousands = ['', ' Thousand', ' Million', ' Billion']
    if not num:
        return 'Zero'
    group = 0
    words = []
    while num:
        if num % 1000:
            words.append(decompose(num % 1000) + thousands[group])
        num //= 1000
        group += 1
    # We need to reverse 'words' because we're processing the groups of 3-digit integers from right to left
    return ' '.join(words[::-1]).rstrip()


def number_to_words_v2(num):
    """ We can also convert the number to English words without splitting it into chunks of 3 digits.
    Time complexity: O(log10 N), intuitively the output is proportional to the number of digits in the input
    Space complexity: O(1)
    """

    def decompose(num):
        if num < 20:
            res = less_than_20[num]
        elif num < 100:
            res = tens[num // 10] + ' ' + decompose(num % 10)
        elif num < THOUSAND:
            res = less_than_20[num // 100] + ' Hundred ' + decompose(num % 100)
        elif num < MILLION:
            res = decompose(num // THOUSAND) + ' Thousand ' + decompose(num % THOUSAND)
        elif num < BILLION:
            res = decompose(num // MILLION) + ' Million ' + decompose(num % MILLION)
        else:
            res = decompose(num // BILLION) + ' Billion ' + decompose(num % BILLION)
        return res.rstrip()

    less_than_20 = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven',
                    'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    THOUSAND, MILLION, BILLION = 1000, 1000000, 1000000000
    if not num:
        return 'Zero'
    return decompose(num)
