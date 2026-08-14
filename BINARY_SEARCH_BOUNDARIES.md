# Binary Search Loop Conditions — Cheat Sheet

## 1. `while left <= right` → Exact-Match Search

Use when asking:

> **Does this target exist?**

Example:

```python
while left <= right:
    mid = (left + right) // 2

    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
```

### Meaning of `[left, right]`

These are all the elements we **still need to inspect**.

If:

```text
left = 3
right = 3
```

there is still **one unchecked element**, so we must run another iteration.

We stop only when:

```text
left > right
```

because then:

```text
0 candidates remain
```

### Mental model

```text
while left <= right
→ search until ZERO candidates remain
→ exact-match search
```

---

# 2. `while left < right` → Boundary Search

Use when asking:

> **Which index is the boundary?**

Classic conceptual shape:

```text
F F F F T T T
        ^
     first T
```

Example:

```python
while left < right:
    mid = (left + right) // 2

    if condition(mid):
        right = mid
    else:
        left = mid + 1

return left
```

### Meaning of `[left, right]`

The interval contains the **answer**.

We're not trying to inspect every element.

We're repeatedly shrinking:

```text
many possible answers
↓
fewer possible answers
↓
2 possible answers
↓
1 possible answer
```

If:

```text
left = 7
right = 7
```

there is exactly **one candidate left**.

Therefore it must be the answer.

No additional iteration is needed.

### Mental model

```text
while left < right
→ shrink until ONE candidate remains
→ boundary search
```

---

# The Key Difference

## Exact match

```text
left == right
```

means:

> There's still one element I haven't checked.

So **keep going**.

```python
while left <= right:
```

---

## Boundary search

```text
left == right
```

means:

> I've narrowed the possible answer down to exactly one index.

So **stop**.

```python
while left < right:
```

---

# Why Boundary Search Often Uses `right = mid`

Suppose:

```text
F F F T T
      M
```

If `mid` satisfies the condition, `mid` might actually be the **first ****`T`**.

So:

```python
right = mid
```

We **keep ****`mid`**** as a candidate**.

Do NOT do:

```python
right = mid - 1
```

because that could throw away the answer.

On the other hand, if `mid` is definitely **not** the answer:

```text
F F F T T
    M
```

then we can discard it:

```python
left = mid + 1
```

---

# Pointer-Update Rule

Ask:

> **Can ****`mid`**** still be the answer?**

If **NO**:

```python
left = mid + 1
# or
right = mid - 1
```

Discard `mid`.

If **YES**:

```python
right = mid
```

Keep `mid`.

---

# The Two Rules to Remember

```text
while left <= right
→ ZERO candidates remaining ends the search
→ exact match
```

```text
while left < right
→ ONE candidate remaining ends the search
→ boundary search
```

And:

> **Whether you use ****`mid`****, ****`mid + 1`****, or ****`mid - 1`**** depends on whether ****`mid`**** can still be the answer.**
