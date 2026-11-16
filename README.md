# TakeMeter — Ask HN firsthand reports

**Status, November 16, 2026:** Model evaluation and the staff comparison are complete:
a baseline, three before/after trials, and **29/30 (96.67%)** agreement with staff.
The one disagreement is adjudicated below.

This continues the existing repository and preserves its original criteria/history.
Unit 5 training had not been completed in the pulled version; the dataset and initial
training were completed on November 16 before the Unit 6 comparison. No earlier
training or results are claimed. The first seed-42 trial also supplies the initial
`results.json` and `test_split.csv`; it is not counted as an extra independent trial.

## What This Does

TakeMeter classifies whole top-level comments from public Ask HN discussions as
`firsthand_report` or `general_response`. It asks whether the writer describes a
concrete personal experience, even if the rest of the comment is advice or opinion.
It does not assess whether the comment is true, useful, or well written. The model measurements score agreement with the working dataset's annotations.

## Label Taxonomy

**Taxonomy:** The two labels below distinguish personal reports from general
responses. The first 20 annotations have been reviewed and confirmed.

### `firsthand_report`

**Definition:** The writer reports a concrete event, action, observation, or ongoing practice they personally experienced, including a specific tool they actually use or work they actually perform.

**Example 1:** [Original comment](https://news.ycombinator.com/item?id=50481224)

> Same. An hour ago, had 10 minutes of auth failures before it resolved. Just happened again with all my claude cli agents halting for auth.
>
> https://status.claude.com/history (https://status.claude.com/history)

**Example 2:** [Original comment](https://news.ycombinator.com/item?id=50405770)

> I was in a very different situation. Microsoft decided to stop supporting Skype, which we had been using for 15 or so years. We moved to Matrix.

### `general_response`

**Definition:** The comment contains no concrete firsthand report by its writer and instead offers an opinion, explanation, recommendation, question, prediction, or reaction.

**Example 1:** [Original comment](https://news.ycombinator.com/item?id=50481259)

> I value human work more than AI - especially if that book is fiction rather than some technical documentation.

**Example 2:** [Original comment](https://news.ycombinator.com/item?id=50426119)

> Everything after C++14 is useless bloat that actively makes the language worse and more convoluted.

### The hardest boundary

**Which two labels:** `firsthand_report` and `general_response`.

**Decision rule:** Read only the comment text. If the writer describes at
least one concrete firsthand event or practice, choose `firsthand_report`,
even when the rest is advice or opinion. Otherwise choose `general_response`.
“I think,” “I prefer,” hypothetical plans, and rhetorical questions alone do
not establish experience. A quoted story from another writer does not count
as the current writer’s experience. A clearly implied first-person account
(such as “Same. An hour ago, had 10 minutes of auth failures”) does count.
Do not infer an experience solely from the thread title.

**Borderline example:** [This comment](https://news.ycombinator.com/item?id=50480367)
recommends a model and then describes using it in an RPG. Under the priority
rule, its label is `firsthand_report`.

**Why two labels:** Advice frequently accompanies personal accounts, so
“advice” would overlap with experience. These two labels instead measure
whether a response contains firsthand experience; they do not grade truth,
usefulness, or writing quality. Eight synthetic boundary tests are recorded
in [taxonomy_stress_test.md](taxonomy_stress_test.md).

## The Dataset

The original collection contains **234 unique comments from 16 threads** in
`data/hn_unlabeled.csv`. Text and source IDs were preserved exactly in `labels.csv`;
there are no duplicate texts or blank labels. The 40-comment reading sample and
source provenance remain in `data/reading_sample.md` and the original collection.

| Label | Count | Share |
|---|---|---|
| firsthand_report | 147 | 62.8205% |
| general_response | 87 | 37.1795% |
| **Total** | **234** | **100%** |

**Annotation workflow:** The first 20 labels were confirmed on November 13, and the
remaining 214 were completed on November 16 using the unchanged taxonomy. Each row's
`note` records a reason and provenance. Detailed decisions are retained in
`data/ai_annotations.json` and `data/ai_annotation_decisions.tsv`. No comments were
relabeled to meet a balance target, and no data changed between before and after.

**Three hard cases:**

- [Comment 50485546](https://news.ycombinator.com/item?id=50485546): The opening firsthand statement belongs to a quoted writer. The current writer offers an opinion, so the label is `general_response`.
- [Comment 50480367](https://news.ycombinator.com/item?id=50480367): Advice comes first, but the author then says they use the model in an RPG. The concrete-use priority rule makes this `firsthand_report`.
- [Comment 50389705](https://news.ycombinator.com/item?id=50389705): A terminal concept and a collective historical “we” do not establish that this writer built or uses it. Under the text-only rule it is `general_response`; the project-discussion title cannot supply the missing experience.

## The Training Run

The original targets were committed before these runs in `criteria.md`; none were
revised. The notebook now uses the two established Ask HN labels and the baseline
uses their exact README definitions in `label_definitions.txt`.

| Setting | Before | After |
|---|---|---|
| Base model | distilbert-base-uncased | same |
| Epochs | 3 | **6** |
| Learning rate | 0.00002 | same |
| Batch size | 16 | same |
| Maximum tokens | 128 | same |
| Seeds | 42, 7, 2024 | same |
| Split | stratified 70/15/15 | identical posts per seed |
| Device | Apple Silicon GPU (MPS) | same |
| Python / PyTorch / Transformers | 3.12.12 / 2.15.0 / 4.57.6 | same |

Each seed has **163 training, 35 validation, and 36 test posts**. Each test partition
contains **23 firsthand reports and 13 general responses**, so its majority-label
baseline is 23/36 = 0.638889. The most-confident third contains 12 posts in each trial.
The three seeds are different random partitions, not three disjoint test datasets.
Splitting is at comment level; comments from the same discussion can occur in
training and test, so these results do not establish performance on unseen threads.

`run_experiments.py` executes the notebook's setup, training, and evaluation functions.
It saves each trial immediately, plus per-post predictions and training histories in
`runs/`. Before/after splits and the SHA-256 of `labels.csv` are checked. The notebook's
section 6 is now set to `RUN_LABEL = "after"` and six epochs, with an overwrite guard.
The environment check passed 9 checks with no failures. Its sandboxed device probe
reported CPU; the actual training processes ran with GPU access and recorded `mps`.
The baseline cache warning in that earlier check predates the successful download.

## Baseline vs. Trained

**Prediction recorded before either model ran:** I predict fine-tuning
will outperform the zero-shot baseline on firsthand reports mixed with advice,
because the training labels consistently prioritize concrete experience.

The baseline is `facebook/bart-large-mnli`, run with the two full definitions and no
examples. `baseline.py --trained results.json` scored **all 36 posts in
`test_split.csv`**, exactly the original seed-42 held-out set. There was no random
fallback or cap. The after column uses that same seed-42 test set. A bare-label-names
baseline was not run.

| Measure | Baseline | Trained before | Before − baseline | Trained after | After − baseline |
|---|---|---|---|---|---|
| Overall accuracy | 0.666667 | 0.666667 | +0.000000 | 0.888889 | +0.222222 |
| Macro F1 | 0.467980 | 0.467980 | -0.000000 | 0.869091 | +0.401111 |
| F1 — firsthand_report | 0.793103 | 0.793103 | +0.000000 | 0.920000 | +0.126897 |
| F1 — general_response | 0.142857 | 0.142857 | -0.000000 | 0.818182 | +0.675325 |

The original trained model added no measured accuracy or F1 advantage on this split;
34/36 individual predictions match the baseline. The pre-run expectation was not
supported by the original model's aggregate result, and no separately scored
mixed-advice subgroup was preregistered. The six-epoch model improves seed-42 accuracy
by 22.22 percentage points over both. This is a one-split baseline comparison, not
proof that it beats the baseline over all seeds. Baseline runtime was not timed under
controlled conditions, so no numerical speed claim is made.

## Run Log — Before

Values are shown to six decimals; verdicts use the unrounded saved values. A performance
target must hold in **every** trial. Criterion 2 shows the lower of the two label F1s.
Criteria 3 and 4 measure the full dataset and annotator, respectively: they are not
three independent model-trial measures. Criterion 3's same measurement is repeated
across columns to retain the required five-row format. Missing evidence is not a pass.

| Criterion | Original target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.75 | 0.666667 | 0.750000 | 0.722222 | MISSED |
| 2. Both labels’ F1 (minimum shown) | ≥ 0.65 | 0.142857 | 0.470588 | 0.375000 | MISSED |
| 3. Largest full-dataset label share | ≤ 0.65 | 0.628205 | 0.628205 | 0.628205 | MET |
| 4. Independent staff agreement | ≥ 24/30 | Not evaluated | Not evaluated | Not evaluated | NOT EVALUATED |
| 5. Most-confident-third accuracy | ≥ 0.80; n ≥ 10 | 0.916667 (n=12) | 1.000000 (n=12) | 1.000000 (n=12) | MET |

### Per-label results before

| Seed | Label | Precision | Recall | F1 | Test support |
|---|---|---|---|---|---|
| 42 | firsthand_report | 0.657143 | 1.000000 | 0.793103 | 23 |
| 42 | general_response | 1.000000 | 0.076923 | 0.142857 | 13 |
| 7 | firsthand_report | 0.718750 | 1.000000 | 0.836364 | 23 |
| 7 | general_response | 1.000000 | 0.307692 | 0.470588 | 13 |
| 2024 | firsthand_report | 0.696970 | 1.000000 | 0.821429 | 23 |
| 2024 | general_response | 1.000000 | 0.230769 | 0.375000 | 13 |

### Confusion matrix — before, seed 42

Rows are dataset labels; columns are predictions.

| true \ predicted | firsthand_report | general_response |
|---|---|---|
| **firsthand_report** | 23 | 0 |
| **general_response** | 12 | 1 |

The biggest off-diagonal cell is **12 general responses called firsthand reports**,
versus **0** in the reverse direction. The model predicted firsthand report on 35 of
36 posts. Seed 7 makes 9 general-to-firsthand errors and seed 2024 makes 10, also with
zero reverse errors. Accuracy spans 0.666667–0.750000, an **8.33-point spread**. That is
below the course's approximate ten-point warning, but one changed answer moves a
36-post accuracy by 2.78 points, so this remains a small-sample estimate.

## Verdicts and Diagnoses

| Criterion | Before | After | Decision and evidence |
|---|---|---|---|
| 1. Accuracy ≥ 0.75 | MISSED | MET | Before seeds 42 and 2024 fall short; all after seeds pass. |
| 2. Both F1 ≥ 0.65 | MISSED | MET | Before general-response F1 fails in every seed; all six after label scores pass. |
| 3. No label above 65% | MET | MET | Largest share is 147/234 = 62.8205%; dataset unchanged. |
| 4. Independent agreement ≥ 24/30 | NOT EVALUATED | NOT EVALUATED | Agreement is 29/30; the original independence condition was not measured (see How I Used AI). |
| 5. Confident-third accuracy ≥ 0.80, n ≥ 10 | MET | MET | Every trial reaches at least 11/12, and each third has 12 posts. |

**Criterion 1 miss — majority-label bias and insufficient training are supported
contributors.** All 31 before errors across the three trials are general responses
called firsthand reports (these are trial errors, not necessarily 31 unique posts).
The majority label comprises 62.82% of the dataset. Validation loss declines through
epoch 3 in all seeds, suggesting training has not exhausted useful signal. Longer
training with unchanged data fixes many errors, supporting an optimization contribution;
it does not prove annotation consistency or that more epochs always help.

**Criterion 2 miss — the general-response boundary was not learned adequately.**
Its before recall is only 1/13, 4/13, and 3/13; F1 is 0.142857, 0.470588, and 0.375000.
There are 87 general-response examples overall and 13 in each test set, so the label
is neither absent nor represented by only one or two test posts. Moderate imbalance,
a small corpus, and a subtle boundary are plausible contributors. Preference-only
sentences and concrete use accounts can share first-person wording. The unchanged-data
improvement materially raises general-response F1, but uncertain annotations still
limit the interpretation.

**Agreement evidence now available, with a scope limit.** The staff
comparison yields 29/30, with one `analysis` / `hot_take` disagreement about whether
a statistic carries an argument. This highlights a boundary-interpretation issue,
but it does not demonstrate inconsistent student labeling. The staff taxonomy differs
from the Ask HN taxonomy, so this disagreement cannot directly explain the classifier's
`general_response` / `firsthand_report` errors. The comparison was completed after
both sets of model trials and was not the basis for choosing the epoch improvement.
The original criterion 4 is preserved; its interpretation is explained in How I Used AI.

## Agreement Report

**Agreement: 29 / 30 = 96.6667%.** All 30 texts matched exactly; none were
missing or extra. `agreement_results.json` contains the script's actual output.

The supplied key is saved as `data/staff_labels.csv`. All 30 labels and reasons were
saved and committed in `f2643f0` **before reading or comparing the key**.
`data/ai_staff_annotations.json` contains the original reasons and label-file hash.
The labels were not changed after comparison. `runs/agreement.log` records the
successful run; the earlier missing-key log is retained as historical evidence.

### Disagreement 1 — sp_014

> Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem.

**Staff label:** `hot_take`. **Submitted label:** `analysis`.

**Case for staff:** Rule 1 excludes statistics that decorate a conclusion. “Obviously,”
“the whole story,” and “the sport has a problem” express a sweeping judgment that a
single time trend cannot substantiate. This resembles the taxonomy's hot-take example
about shoes ruining racing and a 3% improvement.

**Case for the submitted label:** This post explicitly links a measured change to the timing
of the rule change and uses “so” to draw a conclusion. Removing the statistic and
timing removes the offered causal premise. Rule 1's analysis example also infers a
shoe effect from changes in times and rules. The taxonomy requires an argument backed
by a fact; it does not explicitly require that the causal inference be sound or
appropriately qualified. Poorly supported analysis is therefore a defensible reading.

**Adjudication:** Retain `analysis` as a defensible alternative, while recording the
staff disagreement unchanged. The statistic performs an explicit inferential role;
the argument's overconfidence does not by itself make the statistic decorative.
Staff's reading is also reasonable given the normative ending and the close hot-take
example. This is an interpretation disagreement, not a verified error in the answer key.
Rule 4 does not clearly resolve it because the premise and conclusion form one short
sentence; counting words cannot establish whether the premise is load-bearing.

**Pile: (c), ambiguous rule with a defensible reading.** Counts: (a) 0, (b) 0, (c) 1.
A future clarification could explain when an overstated conclusion makes otherwise
explicit evidence “decoration.” No taxonomy was changed for this experiment.

**What the pattern tells us:** There is one disagreement, insufficient to establish a
systematic annotation problem. It concerns evidence-versus-rhetoric under the staff
rules, not the model's personal-experience boundary. The 29/30 rate exceeds the
numerical 24/30 target; the original criterion's independence condition is discussed
in How I Used AI.


## The Improvement

**Only change: 3 → 6 training epochs.** `improvement_plan.md` records the choice and
validation-loss evidence before the after runs. Training length changes the duration
of the default linear learning-rate schedule; its initial rate and all other settings
remain fixed. Dataset, taxonomy, criteria, and exact per-seed partitions are unchanged.
Only this one improvement was attempted. Most original errors fit within 128 tokens,
so longer input length was not chosen as the intervention.

### Run Log — After

| Criterion | Original target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.75 | 0.888889 | 0.861111 | 0.916667 | MET |
| 2. Both labels’ F1 (minimum shown) | ≥ 0.65 | 0.818182 | 0.814815 | 0.880000 | MET |
| 3. Largest full-dataset label share | ≤ 0.65 | 0.628205 | 0.628205 | 0.628205 | MET |
| 4. Independent staff agreement | ≥ 24/30 | Not evaluated | Not evaluated | Not evaluated | NOT EVALUATED |
| 5. Most-confident-third accuracy | ≥ 0.80; n ≥ 10 | 1.000000 (n=12) | 1.000000 (n=12) | 0.916667 (n=12) | MET |

### Paired before/after comparison

| Seed | Before accuracy | After accuracy | Change (percentage points) | Before minimum F1 | After minimum F1 |
|---|---|---|---|---|---|
| 42 | 0.666667 | 0.888889 | +22.22 | 0.142857 | 0.818182 |
| 7 | 0.750000 | 0.861111 | +11.11 | 0.470588 | 0.814815 |
| 2024 | 0.722222 | 0.916667 | +19.44 | 0.375000 | 0.880000 |

Mean accuracy rises from **0.712963 to
0.888889**. Every seed improves, by 22.22,
11.11, and 19.44 percentage points, respectively. Means describe the change; they do
not replace the all-seeds requirement. Criteria 1 and 2 change from MISSED to MET.
The improvement therefore helped on these measured partitions. The after accuracy
spread is **5.56 points**.

### Per-label results after

| Seed | Label | Precision | Recall | F1 | Test support |
|---|---|---|---|---|---|
| 42 | firsthand_report | 0.851852 | 1.000000 | 0.920000 | 23 |
| 42 | general_response | 1.000000 | 0.692308 | 0.818182 | 13 |
| 7 | firsthand_report | 0.909091 | 0.869565 | 0.888889 | 23 |
| 7 | general_response | 0.785714 | 0.846154 | 0.814815 | 13 |
| 2024 | firsthand_report | 0.916667 | 0.956522 | 0.936170 | 23 |
| 2024 | general_response | 0.916667 | 0.846154 | 0.880000 | 13 |

### Confusion matrices after

**Seed 42**

| true \ predicted | firsthand_report | general_response |
|---|---|---|
| **firsthand_report** | 23 | 0 |
| **general_response** | 4 | 9 |

**Seed 7**

| true \ predicted | firsthand_report | general_response |
|---|---|---|
| **firsthand_report** | 20 | 3 |
| **general_response** | 2 | 11 |

**Seed 2024**

| true \ predicted | firsthand_report | general_response |
|---|---|---|
| **firsthand_report** | 22 | 1 |
| **general_response** | 2 | 11 |

Across trials, general-to-firsthand errors fall from 31 to 8, while
firsthand-to-general errors rise from 0 to 4. The gain has a tradeoff: firsthand recall
falls from 1.0 to 0.869565 in seed 7 and 0.956522 in seed 2024. For example, seed 7 now
misses the real RPG-use account in comment 50480367, and seed 2024 misses the short
Outlook-use account in comment 50482151. These are residual errors, despite all measured
model criteria passing.

### Confidence criterion

This check was already criterion 5 before training; it is not a newly claimed stretch
goal. No additional stretch feature was preregistered in this session.

| Phase | Seed | Most confident third | Least confident third | n per third |
|---|---|---|---|---|
| Before | 42 | 0.916667 | 0.166667 | 12 |
| Before | 7 | 1.000000 | 0.500000 | 12 |
| Before | 2024 | 1.000000 | 0.333333 | 12 |
| After | 42 | 1.000000 | 0.833333 | 12 |
| After | 7 | 1.000000 | 0.666667 | 12 |
| After | 2024 | 0.916667 | 0.916667 | 12 |

Confident thirds are more accurate than unsure thirds in all before trials and two
after trials. In after seed 2024, both thirds are 11/12, so confidence does not separate
them on that partition. It still meets the original criterion, which requires no gap.
This small ranking check does not establish probability calibration or guarantee that
an individual confident prediction is right.

## What's Still Broken

All measured model criteria pass after the improvement. The staff comparison and
adjudication are complete; criterion 4's independence condition remains unmeasured.
The original targets have not been lowered or rewritten.

The remaining annotations should receive independent review in a future data revision;
labels were frozen for this experiment. Short implied-first-person statements,
preference-only comments, quoted speech, and project descriptions remain difficult.
A future evaluation should also hold out entire discussion threads and use a new final
test set. No such changes were mixed into this one-improvement comparison. Because
this test set informed the improvement choice, the after results are development
measurements rather than performance on a fresh untouched final test.

**Intended labels versus learned behavior:** The taxonomy asks for concrete firsthand
experience, but the before matrix shows the model largely treating general responses
as firsthand reports. Longer training reduces that confusion, yet the after matrices
still contain errors in both directions, showing that the model has not fully learned
the distinction between personal wording and concrete experience.

## How I Used AI

Codex helped with the taxonomy and criteria, proposed the first 20 labels that the
student confirmed, completed the remaining 214 annotations, ran the local training
and baseline, verified results, selected the epoch-count improvement, and drafted
the report. It also labeled the 30 staff posts before reading the answer key and
wrote the disagreement adjudication. Scores come from actual saved predictions and
comparisons. Attribution is consolidated here rather than repeated beside each result.

The 29/30 staff agreement exceeds the numerical target, but original criterion 4
specifies unaided student labeling. That condition was not measured, so its verdict
remains NOT EVALUATED rather than claiming independent human work. The original
criterion is preserved in `criteria.md`.

## Reproduce and Verify

```bash
source .venv/bin/activate
python test.py
python verify_evidence.py
```

The completed commands were:

```bash
python run_experiments.py --phase before
HF_HOME="$PWD/.cache/huggingface" python baseline.py --trained results.json
python run_experiments.py --phase after --epochs 6
python agreement.py
```

Use a separate working copy and archive existing result files before intentionally
repeating training; the runner refuses to overwrite completed three-seed evidence.
Model downloads are cached under `.cache/huggingface` (ignored by Git), and exact
installed package versions are in `runs/requirements_lock.txt`. `RUNNING.md` retains
the starter's setup instructions. The saved verification report checks text integrity,
all six trials' accuracy/F1/matrices/confidence thirds, identical paired splits/settings,
the baseline's exact test-post match, and all 30 staff matches plus adjudication coverage.

## Submission Status

- [x] Original `criteria.md` preserved with five unchanged targets.
- [x] 234-row labeled dataset and documented annotation provenance.
- [x] `results.json` and `test_split.csv` from actual initial training.
- [x] `baseline_results.json` on the same held-out posts.
- [x] `results_three_seeds_before.json` and `results_three_seeds_after.json`.
- [x] Five-row before/after logs, typed matrices, verdicts, and diagnoses.
- [x] One predeclared improvement, measured on identical seed partitions.
- [x] All 30 staff texts labeled in `my_staff_labels.csv`.
- [x] Staff key supplied; `agreement_results.json` generated (29/30).
- [x] Every disagreement has a rule-grounded adjudication.
- [ ] Criterion 4’s original independence condition remains unmeasured; see How I Used AI.

The repository URL remains:
https://github.com/Sunji2468/ai201-project3-takemeter-starter-v2026
