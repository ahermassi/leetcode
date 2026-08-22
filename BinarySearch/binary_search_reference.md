# Binary Search — Pattern Cheat Sheet

## 1. Start Here: What Am I Searching For?

### A. Exact Match

> “Does this target exist?”

```python
while left <= right:
    mid = (left + right) // 2

    if nums[mid] == target:
        return mid

    if target < nums[mid]:
        right = mid - 1
    else:
        left = mid + 1
```

Mental model:

```text
[left, right] = elements still unchecked

left == right
→ 1 unchecked element remains
→ KEEP GOING

left > right
→ 0 unchecked elements remain
→ STOP
```

So:

```text
Exact match
→ while left <= right
→ stop at ZERO candidates
```

---

## 2. Boundary / Candidate-Convergence Search

> “Find the first/last valid point, minimum, maximum, boundary, etc.”

Think:

```text
F F F F T T T
        ^
     boundary
```

Template:

```python
while left < right:
    mid = (left + right) // 2

    if condition(mid):
        right = mid
    else:
        left = mid + 1

return left
```

Mental model:

```text
[left, right] ALWAYS contains the answer

many candidates
      ↓
fewer
      ↓
2 candidates
      ↓
1 candidate
```

When:

```text
left == right
```

there is exactly **one possible answer**, so stop.

```text
Boundary search
→ while left < right
→ stop at ONE candidate
```

---

# 3. The Most Important Binary-Search Question

Before moving a pointer, ask:

> **Can `mid` still be the answer?**

### NO

Discard it:

```python
left = mid + 1
```

or:

```python
right = mid - 1
```

### YES

Keep it:

```python
right = mid
```

The pointer updates should come from this reasoning — not memorization.

---

# 4. Monotonic Predicate Search

Binary search does not require literal sorted numbers.

It needs a search space shaped like:

```text
F F F F T T T
```

or:

```text
T T T T F F F
```

Examples of predicates:

```text
Is capacity large enough?
Can this task finish within D days?
Is this version bad?
Is this value >= target?
```

Then binary search finds the **transition point**.

Think:

> “Can I turn this problem into a yes/no question whose answer changes only once?”

---

# 5. Rotated Sorted Data

Visualize it as two sorted chunks:

```text
[HIGH HIGH HIGH HIGH] [LOW LOW LOW]
                      ^
                    rotation
```

Example shape:

```text
4 5 6 7 | 0 1 2
```

The data is not globally sorted, but there is still enough local ordering information to binary search.

---

# 6. Searching for a Target in Rotated Data

At every iteration, determine which half is definitely sorted.

```text
left <= mid
→ left half sorted

left > mid
→ right half sorted
```

Then ask:

> **Does the target fall inside the sorted half?**

If yes → keep it.

If no → discard it.

Mental script:

```text
1. Which half is sorted?
2. Is target inside that half?
3. Keep or discard.
```

---

# 7. Finding the Rotation Boundary / Minimum

Compare `mid` with the right boundary.

### `mid > right`

```text
HIGH ... MID | ... LOW ... RIGHT
```

The drop must happen **strictly after `mid`**.

```python
left = mid + 1
```

Why?

```text
mid definitely cannot be the minimum
→ discard it
```

---

### `mid < right`

```text
... LOW ... MID ... RIGHT
```

`mid` is already in the lower/sorted section.

The minimum is:

```text
at mid OR left of mid
```

So:

```python
right = mid
```

Why?

```text
mid might be the minimum
→ keep it
```

---

# 8. Duplicates = Lost Information

Normally comparisons give direction:

```text
left < mid
→ useful information

left > mid
→ useful information
```

But:

```text
left == mid
```

can tell us nothing.

Example:

```text
1 1 1 0 1
L   M

1 0 1 1 1
L   M
```

Same comparison:

```text
left == mid
```

but the rotation is on opposite sides.

So:

> **Equality can destroy the information binary search needs.**

---

# 9. What To Do When Duplicates Cause Ambiguity

If a duplicate gives you no direction, ask:

> **Can I prove one copy is redundant?**

For exact-target search:

```text
mid != target
left == mid
```

therefore:

```text
left != target
```

so:

```python
left += 1
```

For candidate/minimum search:

```text
mid == right
```

If `right` contains the minimum value, `mid` contains the same value.

So removing one copy is safe:

```python
right -= 1
```

Mental model:

> **No directional information → safely peel a redundant duplicate → try again.**

---

# 10. Why Duplicates Can Degrade Binary Search

Normal binary search:

```text
n
↓
n/2
↓
n/4
↓
...
```

But ambiguity may force:

```python
left += 1
```

or:

```python
right -= 1
```

So worst case becomes:

```text
O(n)
```

instead of:

```text
O(log n)
```

---

# 11. The Entire Mental Framework

When you see a binary-search problem, ask:

```text
1. Is this EXACT MATCH or BOUNDARY SEARCH?
```

```text
2. What does [left, right] mean?
```

```text
3. What comparison gives me directional information?
```

```text
4. What did that comparison actually PROVE?
```

```text
5. Can mid still be the answer?
```

Then:

```text
mid impossible
→ discard it

mid possible
→ keep it

comparison ambiguous
→ look for a safely removable duplicate
```

---

# 12. If You Forget Everything Else

```text
EXACT MATCH
while left <= right
→ stop when ZERO candidates remain
```

```text
BOUNDARY / CONVERGENCE
while left < right
→ stop when ONE candidate remains
```

```text
F F F T T T
      ^
binary search loves monotonic transitions
```

```text
Can mid still be the answer?

NO  → mid +/- 1
YES → keep mid
```

```text
Rotated data:
find the ordered region
→ use it to recover direction
```

```text
Duplicates:
equality may destroy direction
→ safely peel redundant copies
```

> **Don't memorize pointer movements. Ask what you have proved, then the pointer movement follows.**