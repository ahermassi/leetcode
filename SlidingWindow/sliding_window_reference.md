# Sliding Window — Pattern Reference

## Core Question

For a contiguous range, identify:

1. **What state represents the current window?**
   - sum, product, frequencies, distinct count, zeros, etc.
2. **What makes the window valid or invalid?**
3. **Why can `left` and `right` move only forward?**
   - usually some monotonic property
4. **When do we evaluate the answer?**
   - after restoring validity?
   - while shrinking a valid window?
   - once the fixed-size window is complete?

---

## 1. Fixed-Size Sliding Window

Use when every candidate window must have exactly `k` elements.

### Template

```python
left = right = 0

while right < n:
    # add nums[right]

    if right - left + 1 > k:
        # remove nums[left]
        left += 1

    if right - left + 1 == k:
        # evaluate window

    right += 1
```

Often, when the outgoing element is deterministic, use the simpler rolling form:

```python
# add nums[right]
# remove nums[right - k]
```

### Useful alternate shape

For some fixed-size frequency problems:

```text
preload k - 1
-> add right
-> evaluate size-k window
-> remove left
-> repeat
```

This is only an implementation style, not a separate pattern.

---

## 2. Variable-Size — Longest Valid Window

Use when the goal is the **largest** contiguous window satisfying a condition.

### Template

```python
left = 0
res = 0

for right in range(n):
    # add right to window state

    while window_is_invalid:
        # remove left from window state
        left += 1

    res = max(res, right - left + 1)
```

### Mental model

```text
expand right
-> while INVALID:
       shrink left
-> window is valid
-> update maximum
```

### Invariant

After the shrinking loop:

```text
[left, right] is valid
```

---

## 3. Variable-Size — Minimum Valid Window

Use when the goal is the **smallest** contiguous window satisfying a condition.

### Template

```python
left = 0
res = float("inf")

for right in range(n):
    # add right to window state

    while window_is_valid:
        res = min(res, right - left + 1)

        # remove left from window state
        left += 1
```

### Mental model

```text
expand right until valid
-> while VALID:
       record answer
       shrink left
-> once invalid, expand again
```

### Key contrast

```text
Longest Valid:
    while INVALID:
        shrink
    evaluate

Minimum Valid:
    while VALID:
        evaluate
        shrink
```

---

## 4. Count Valid Subarrays Ending at `right`

Use when the goal is to **count** valid subarrays rather than optimize one window.

After restoring a valid window, ask:

> If `[left, right]` is valid, are all suffixes ending at `right` also valid?

If yes:

```python
res += right - left + 1
```

because the valid suffixes are:

```text
[left ... right]
[left+1 ... right]
...
[right]
```

### Template

```python
left = 0
res = 0

for right in range(n):
    # add right

    while window_is_invalid:
        # remove left
        left += 1

    res += right - left + 1
```

### Requirement

Validity must be **suffix-closed**:

> Removing elements from the left cannot make a valid window invalid.

Typical reasons:
- non-negative sum with an upper bound
- positive product with an upper bound
- at most `k` distinct values

---

## 5. Exact K via AtMost

Directly counting an exact condition is often awkward.

If the property is discrete and nested:

```text
exactly(K)
=
atMost(K) - atMost(K - 1)
```

### Why

```text
atMost(K)     -> 0, 1, 2, ..., K
atMost(K - 1) -> 0, 1, 2, ..., K - 1
difference    -> exactly K
```

### Template

```python
def at_most(limit):
    left = 0
    res = 0

    for right in range(n):
        # add right

        while window_exceeds(limit):
            # remove left
            left += 1

        res += right - left + 1

    return res

answer = at_most(k) - at_most(k - 1)
```

### Prerequisites

Use this when:

1. `atMost(K - 1)` is a subset of `atMost(K)`.
2. The measured property is discrete/integer-like.
3. `atMost(...)` itself can be maintained with a monotonic sliding window.

Do **not** blindly use it when the underlying `atMost` condition is not sliding-window friendly.

---

## 6. Frequency-State Patterns

### A. Two frequency maps

```python
counter = Counter(target)
window = Counter(...)
```

Validity comes from comparing required vs current frequencies.

---

### B. Incremental match count

If only a few frequencies change per step, avoid rechecking the whole state.

Maintain:

```python
matches
```

as the number of satisfied frequency equalities.

General idea:

```text
local state changed
-> update only that character's contribution
-> do not recompute the whole predicate
```

This is a general optimization pattern, not just sliding window.

---

### C. Deficit / Surplus Counter

Mutate the target counter itself.

Interpretation:

```text
counter[c] > 0  -> still needed
counter[c] == 0 -> exactly satisfied
counter[c] < 0  -> surplus
```

Useful when you want one structure to encode:

```text
target requirements - current window contents
```

---

## 7. Monotonicity: Why Sliding Window Works

Always ask what happens when pointers move.

Examples:

### Non-negative sum

```text
expand right -> sum cannot decrease
shrink left  -> sum cannot increase
```

### Positive product

```text
expand right -> product cannot decrease
shrink left  -> product cannot increase
```

### Distinct count

```text
remove from left -> distinct count cannot increase
```

If this predictable one-directional behavior disappears, ordinary sliding window may fail.

---

## 8. When Sliding Window Is Suspicious

Be careful when:

- negative numbers break sum monotonicity
- shrinking can unexpectedly increase the property you are tracking
- expanding can unexpectedly decrease it
- the condition depends on non-contiguous choices
- exact conditions are not suffix-closed
- you find yourself needing to move `left` backward

For exact subarray sums with negative numbers, prefix sums are often a better direction.

---

## 9. Common Bugs

### Window length

With inclusive boundaries:

```python
right - left + 1
```

---

### Fixed-size final window not evaluated

Be explicit about the lifecycle:

```text
build full window -> evaluate -> slide
```

or:

```text
preload k - 1 -> add -> evaluate -> remove
```

---

### Zero-count keys

If:

```python
len(counter)
```

represents the number of distinct values, delete keys whose count becomes zero.

---

### Repeated slicing

Avoid repeatedly doing:

```python
s[left:right + 1]
```

inside an O(N) loop.

Track boundaries/length and slice once at the end.

---

### Impossible thresholds

If the shrink loop can never restore validity, check the math before adding pointer guards.

Examples:

```text
positive products with k <= 1
non-negative sums with target < 0
```

Handle impossible cases upfront.

---

## 10. Five-Second Recall

```text
FIXED SIZE
    add / remove to keep size k
    evaluate

LONGEST VALID
    expand
    while INVALID:
        shrink
    update max

MINIMUM VALID
    expand
    while VALID:
        update min
        shrink

COUNT VALID SUBARRAYS
    expand
    while INVALID:
        shrink
    add right - left + 1

EXACT K
    atMost(K) - atMost(K - 1)
```

And always ask:

> **What is the invariant, and why do the pointers never need to move backward?**
