# Lab 5 — Refactoring Report: TennisGame1 (Python)

**Repository:** https://github.com/Kwenpicasso/tennis-refactoring-lab5
**File refactored:** `python/tennis1.py` (`TennisGame1`)
**Language:** Python · **Test runner:** pytest

## 1. Code Smells Identified

**a) Long Method** — `score()` (originally lines 14–46)
A single method handled three unrelated game states (tied score, advantage/win,
regular play) inside a three-level nested `if/elif/else` plus a `for` loop.
Any change to one scoring state required reading and understanding all of them,
raising the risk of accidentally breaking another branch.

**b) Duplicated Code** — point→name mapping inside `score()` (lines 18–22 and 40–44)
The mapping from points to tennis terms (`Love`, `Fifteen`, `Thirty`, `Forty`)
was hardcoded in two separate dict literals. Renaming a term or adding a new
score name would require editing both copies — easy to forget one and produce
inconsistent output.

**c) Obscure loop and temporary variable** — regular-score branch (lines 34–44)
`for i in range(1, 3)` iterated "twice" to format two players' scores, using
`temp_score` and an `if i == 1` check to decide which player's points to read.
The reader must mentally execute the loop to discover it simply produces
`"<p1 name>-<p2 name>"`.

**d) (Noted, intentionally not fixed) Magic literal** — `won_point()` (line 9)
`player_name == "player1"` compares against a hardcoded string instead of
`self.player1_name`, so points would be misattributed for differently named
players. This is a latent defect, but correcting it would change externally
observable behavior, so per the lab constraints it was left unchanged and
documented here instead.

## 2. Refactoring Performed

**Technique 1 — Extract Method.** The three branches of `score()` were moved
into `_equal_score()`, `_endgame_score()`, and `_regular_score()`. Chosen
because the method's only real problem was length/structure — each branch was
already self-contained, making extraction safe and mechanical.

Before:
```python
def score(self):
    result = ""
    temp_score = 0
    if self.p1points == self.p2points:
        result = {0: "Love-All", 1: "Fifteen-All", 2: "Thirty-All"}.get(self.p1points, "Deuce")
    elif self.p1points >= 4 or self.p2points >= 4:
        ...  # nested advantage/win if-chain
    else:
        for i in range(1, 3):
            ...  # temp_score loop
    return result
```

After:
```python
def score(self):
    if self.p1points == self.p2points:
        return self._equal_score()
    if self.p1points >= 4 or self.p2points >= 4:
        return self._endgame_score()
    return self._regular_score()
```

`score()` now reads as a dispatcher: the *order of checks* (the actual business
rule) is visible at a glance, and each state's details live in a named method.

**Technique 2 — Extract Constant / Consolidate duplicated lookup.** The two
hardcoded dicts were replaced by one module-level constant
`SCORE_NAMES = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}`.
`_equal_score()` derives `"-All"` names from it; `_regular_score()` indexes it
directly. Chosen to eliminate the duplication smell — score names now have a
single source of truth.

**Technique 3 — Replace Loop with direct expression.** The `range(1, 3)` loop,
`temp_score`, and string concatenation were replaced by:
```python
def _regular_score(self):
    return f"{SCORE_NAMES[self.p1points]}-{SCORE_NAMES[self.p2points]}"
```
One line now states exactly what the branch computes; the loop's iteration
trick and the throwaway variable are gone.

## 3. Behavior Preservation

The provided test suite was used as the safety net. Command used throughout:

```
cd python && .venv/bin/python -m pytest tests
```

- **Baseline (before any change):** 231 passed, 0 failed
- **After each of the three refactoring commits:** 231 passed, 0 failed

The suite covers all 33 score combinations for `TennisGame1` (Love-All through
Deuce, Advantage, and Win scenarios, up to 16–14). Changes were applied in
small increments — one refactoring per commit (`d815369`, `36de4c6`, `4568cb6`)
with a full test run between each — so any regression would have been isolated
immediately. No scoring rules were altered and no functionality was added.
Note: passing tests give strong evidence of behavior preservation for the
tested inputs but do not prove it for every possible input.

## 4. Reflection

The main difficulty was resisting the urge to "fix" `won_point()`'s hardcoded
player name, since the lab forbids changing observable behavior — distinguishing
a *smell* from a *bug* took care. The incremental commit-and-test rhythm kept
each step low-risk. For an agile team, the refactored structure means future
scoring changes (e.g., tiebreak rules or new score names) now have one obvious
place to be made, shortening iteration time and reducing review effort.
