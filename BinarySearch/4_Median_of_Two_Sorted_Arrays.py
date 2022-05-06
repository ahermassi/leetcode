""" Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)). """

# Video explanation: https://www.youtube.com/watch?v=q6IEA26hvXc


def find_median_sorted_arrays(nums1, nums2):
    """ This problem is notoriously hard to implement due to all the corner cases. Most implementations consider
        odd-length and even-length arrays as two different cases and treat them separately. As a matter of fact, with a
        little mind twist, these two cases can be combined as one, leading to a very simple solution where (almost) no
        special treatment is needed.

        First, let's see the concept of median in a slightly unconventional way. That is:

                    If we cut a sorted array to two halves of EQUAL LENGTHS, then median is:
                    AVERAGE OF Max(lower_half) and Min(upper_half)
                    i.e. the two numbers immediately next to the cut

        For example, for [2, 3, 5, 7], we make the cut between 3 and 5: [2, 3 / 5, 7], then median = (3+5)/2.
        For [2, 3, 4, 5, 6], we make the cut right through 4 like this: [2, 3, (4/4) 5, 7]. Since we split 4 into two
        halves, we say now both the lower and upper sub-arrays contain 4. This notion also leads to the correct answer:
        median = (4 + 4) / 2 = 4.

        For convenience, let's use L to represent the number exactly at the cut, and R the right counterpart.
        In [2, 3, 5, 7], for instance, we have L = 3 and R = 5, respectively.
        We observe the indices of L and R have the following relationship with the length of the array N:

            N        Index of L / R
            1               0 / 0
            2               0 / 1
            3               1 / 1
            4               1 / 2
            5               2 / 2
            6               2 / 3
            7               3 / 3
            8               3 / 4

        It is not hard to conclude that index of L = (N-1)/2, and R is at N/2. Thus, the median can be represented as:
                (L + R)/2 = (nums[(N-1)/2] + nums[N/2])/2

        Therefore, we need to find a cut that divides the two arrays each into two halves such that:

                Any number in the two left halves <= any number in the two right halves

        Now how do we decide if this cut is the cut we want?

        Let L1 and L2 be the largest numbers on the left halves, respectively, and R1 and R2 are the smallest numbers on the right halves.
        Notice that L1 and R1 are adjacent, and L2 and R2 are adjacent (the two arrays are sorted).
        To decide if we have a correct cut, we need:

                L1 <= R1 && L1 <= R2 && L2 <= R1 && L2 <= R2

        This makes sure that any number in lower halves <= any number in upper halves. As a matter of fact, since
        L1 <= R1 and L2 <= R2 are naturally guaranteed because the two arrays are sorted, we only need to make sure that:

                L1 <= R2 and L2 <= R1

        Now, we can use simple binary search on the shortest array (for convenience, let's assume it's nums1) to locate
        the correct cut index. The reason is that on the shorter array, all positions are possible cut locations for
        median, but on the longer array, the positions that are too far left or right are simply impossible for a
        legitimate cut. For instance, nums1 = [1], nums2 = [2 3 4 5 6 7 8]. Clearly the cut between 2 and 3 is
        impossible because the shorter array does not have that many elements to balance out the [3 4 5 6 7 8] part if
        we make the cut this way.

            - If L1 > R2, it means there are too many large numbers in the left half of nums1, then we must move the
               cut to the left and drop the larger numbers to the right at nums1 since they can't contribute towards the
               median.
            - If L2 > R1, then there are too many large numbers in the left half of nums2, and we must move the cut to
               the right to include larger numbers of nums1
            - Otherwise, this cut is the right one, and the medium can be computed as (max(L1, L2) + min(R1, R2)) / 2

        The only edge case is when a cut falls on the first or the last position. To solve this problem, we can imagine
        that both arrays actually have two extra elements, INT_MIN at A[-1] and INT_MAX at A[N]. These additions don't
        change the result, but make the implementation easier: If any L falls out of the left boundary of the array,
        then L = INT_MIN, and if any R falls out of the right boundary, then R = INT_MAX.

        Key points:

        We want to make two cuts, separating nums1 into [. . . . L1 | R1 . . . ] and nums2 into [. . . .L2 | R2 . . . ],
        respectively, so that [. . . . L1] + [. . . . L2] has equal number of elements as [R1 . . . ] + [R2 . . . ].
        Our goal is to find such cutting positions that give us the median values.

        Cutting on a gap is simple. Cutting on a number means both left half and right half get the number.

        With two arrays, a valid cutting position that gives the median can be ANY cutting position of the shorter
        array. This is not true for the longer array. Therefore, we always cut the shorter array, and then calculate the
        cutting position of longer array directly. We want to make nums1 always points to the shorter array for
        convenience.

        Using binary search, If L1 > R2, we know current cutting position is incorrect. A valid cutting position for
        median should be on the left half of nums1.
        If L2 > R1, we know current cutting position is incorrect. A valid cutting position for median should be on the
        right half of nums1.

    Time complexity: O(log(min(n, m))
    Space complexity: O(1)
    """
    if len(nums2) < len(nums1):
        return find_median_sorted_arrays(nums2, nums1)
    n, m = len(nums1), len(nums2)
    size = n + m
    half = size // 2
    left, right = 0, n - 1
    while True:
        nums1_cut = (left + right) // 2
        nums2_cut = half - nums1_cut - 2

        nums1_left = nums1[nums1_cut] if nums1_cut >= 0 else float('-inf')
        nums1_right = nums1[nums1_cut + 1] if nums1_cut < n - 1 else float('inf')

        nums2_left = nums2[nums2_cut] if nums2_cut >= 0 else float('-inf')
        nums2_right = nums2[nums2_cut + 1] if nums2_cut < m - 1 else float('inf')

        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            break
        if nums1_left > nums2_right:
            right = nums1_cut - 1
        elif nums2_left > nums1_right:
            left = nums1_cut + 1

    left_max = max(nums1_left, nums2_left)
    right_min = min(nums1_right, nums2_right)
    return (left_max + right_min) / 2 if size % 2 == 0 else right_min
