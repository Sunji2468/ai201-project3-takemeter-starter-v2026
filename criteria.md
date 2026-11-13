# Acceptance criteria — TakeMeter

Drafted on November 13, 2026, before any training run or model results.

The classifier uses `firsthand_report` and `general_response`. All model
performance criteria below use only each run's held-out test partition from
the notebook's stratified 70/15/15 split. Compare unrounded values. In unit 6,
criteria 1, 2, and 5 must each pass for all three seeds: 42, 7, and 2024; an
average across seeds is not sufficient. Missing evidence means not evaluated,
not a pass. No criterion has been evaluated yet.

## 1. Overall test accuracy is at least 0.75

**Target:** `accuracy >= 0.75` on each seed's held-out test set.

**Why this target:** Distinguishing a concrete firsthand report from a general
response should be useful at three correct predictions out of four. Combined
with criterion 3's 65% class cap, this demands at least a ten-percentage-point
improvement over the majority share in the full dataset; report the actual
majority baseline on each test split separately because its share can differ.

**How to check:** Read `accuracy` in `results.json` for the first run and in
each entry of `results_three_seeds_before.json` for the three-seed evaluation.

## 2. Both labels have test F1 of at least 0.65

**Target:** `per_label.firsthand_report.f1 >= 0.65` and
`per_label.general_response.f1 >= 0.65` on each seed's held-out test set.

**Why this target:** High overall accuracy is not useful if the model misses
most general responses or treats every “I think” statement as experience.
A 0.65 floor requires useful precision and recall for both categories while
allowing some mistakes on mixed experience-and-opinion comments in a small
held-out set.

**How to check:** Read both labels' `f1` fields from the saved results and
report their test support alongside the scores. A missing label score does
not satisfy this criterion.

## 3. Neither label exceeds 65% of the final dataset

**Target:** In the single, fully labeled `labels.csv`, each label's count
divided by the total row count must be at most `0.65` (and hence at least
`0.35` with two labels).

**Why this target:** The first reviewed batch has 15 firsthand reports and
5 general responses, so collecting only similar comments could create a
majority-class shortcut. The 65% target is stricter than the assignment's
70% cap and preserves a substantial minority class; at 234 total examples,
each class would need at least 82 rows. The 20-row batch does not establish
the distribution of the remaining comments.

**How to check:** Count the final labels before the notebook splits the
file. Missing or unknown labels must be resolved before calculating shares.
Do not relabel comments merely to meet the target; collect more genuine
examples of the thinner class if needed. The separate assignment requirement
of at least 200 total examples still applies.

## 4. Independent staff-set annotation agreement is at least 80%

**Target:** The student's unaided labels match the staff labels on at least
`24 of 30` staff-set posts (`0.80` agreement), using `data/staff_taxonomy.md`.

**Why this target:** Four matches in five would show that the student can
apply an explicit taxonomy consistently, while allowing disagreement on
ambiguous posts. This uses the course's separate staff taxonomy and measures
rule application; it does not directly establish agreement on the custom
Ask HN taxonomy or count as the project's 20 cold annotations.

**How to check:** Label all 30 staff posts without seeing staff answers or
AI-proposed labels, then run `agreement.py` when staff answers are supplied.
Report exact matches divided by 30 and discuss every disagreement. Previously
AI-labeled comments cannot substitute for this independent exercise.

## 5. The most confident third achieves at least 80% test accuracy

**Target:** `confidence.accuracy_most_confident_third >= 0.80` on each seed's
held-out test set, with `confidence.n_per_third >= 10`.

**Why this target:** If confidence is to help prioritize human review, the
model's most confident predictions should be more reliable than the minimum
75% overall target. Requiring at least ten examples prevents declaring success
from just one or two confident guesses, although this remains a small sample
and does not establish that probabilities are calibrated.

**How to check:** Use the notebook's existing confidence report. It ranks
predictions by maximum softmax probability and evaluates the highest-ranked
`floor(n_test / 3)` examples. Use its recorded ranking and group size, without
changing the group after seeing results. Also report the least-confident
third's accuracy for context; no numerical gap is required by this target.

---

After training begins, preserve these original targets. If a criterion proves
unmeasurable, append a dated revision and explanation instead of deleting the
original. Do not lower a target simply because the model missed it.
