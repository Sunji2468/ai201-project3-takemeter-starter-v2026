# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter will classify whole top-level comments from public Ask HN discussions
on Hacker News. A two-label draft distinguishes firsthand reports from general responses;
no model has been trained yet. See [community_notes.md](community_notes.md)
for candidate distinctions and [the reading sample](data/reading_sample.md)
for 40 real comments with source links.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

**AI-assisted taxonomy draft:** These definitions and example assignments were
prepared by Codex. Student review is pending. Twenty proposed labels are now recorded separately in `data/ai_annotations_batch1.json`; student review is pending.

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
rule, its proposed label is `firsthand_report`. This is an AI-proposed example,
not a student cold annotation.

**Why two labels:** Advice frequently accompanies personal accounts, so
“advice” would overlap with experience. These two labels instead measure
whether a response contains firsthand experience; they do not grade truth,
usefulness, or writing quality. Eight synthetic boundary tests are recorded
in [taxonomy_stress_test.md](taxonomy_stress_test.md).

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Public Ask HN discussions, collected through
the official Hacker News API. The current pool contains 234 unique comments
from 19 threads in `data/hn_unlabeled.csv`, with original HTML and provenance.
This is an unlabeled collection, not the final `labels.csv` submission.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

**Counts per label:**

| Label | Count | Share |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
| **Total** |  | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**2.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**3.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Setup status (November 13, 2026):** The local `.venv` uses Python 3.12.12
with the project requirements and `ipykernel` installed. The environment
check passed all nine checks with no failures; the baseline model has not
been downloaded yet. `pip check` found no broken requirements. The notebook's
first setup cell executed successfully. Apple Silicon GPU (`mps`) availability
and a tensor operation were verified outside the restricted execution sandbox.
Training has not started; the actual run's device and metrics will be recorded
after the dataset and acceptance criteria are ready.

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Help setting up my GitHub fork locally.
- *What came back:* Codex connected the workspace to my fork, created a
  Python 3.12 virtual environment, installed the dependencies and notebook
  kernel, and verified the environment and GPU access.
- *What I changed:* No manual changes so far. Codex used the installed Python
  3.12 interpreter because the default Python 3.9 was below the course's
  supported range.

**Moment 2**

- *What I asked for:* Continue the project and choose a public community.
- *What came back:* Codex chose Ask HN, collected public comments with source
  links, prepared a 40-comment reading sample, and documented three candidate
  distinctions after reading the sample.
- *What I changed:* Pending my reading and taxonomy decisions.

**Pre-labelling disclosure:** At my request, Codex pre-labeled the 20 comments
originally prepared as a cold batch. These are AI annotations, not unaided
annotations, and human review is pending. The proposed labels and reasons
are in [ai_annotation.md](ai_annotation.md) and `data/ai_annotations_batch1.json`.
The original 234-comment collection remains unchanged. No cold annotations
have been completed; the other 214 comments have no proposed labels yet.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
