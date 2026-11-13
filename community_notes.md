# Community exploration — Ask HN

Status: AI-assisted preparation; the student's own reading and observations
are still pending. This is not a claim that the student completed the reading.

## Community and scope

Hacker News, restricted to top-level comments in public Ask HN discussions.
Each whole comment is one example. The classifier will see only comment text,
not the thread title, author, score, or source URL.

Sources are collected using the [official public API](https://github.com/HackerNews/API).
`data/hn_unlabeled.csv` preserves comment IDs, source links, thread IDs, collection
timestamps, and original HTML. Its label and note columns are intentionally blank.
`data/reading_sample.md` contains 40 comments spread across the collected threads.

## Three candidate distinctions observed by Codex

These are observations from the sample, not finalized labels:

1. **Firsthand experience versus general claims.** Sample 2 reports the
   writer's authentication failures; sample 23 predicts where people will
   move online without reporting a personal event.
2. **Concrete supporting examples versus bare assertions.** Sample 24 explains
   robot safety with appliance interlocks; sample 17 asserts a preference
   for human-written books without developing supporting evidence.
3. **Actionable advice versus descriptions or reactions.** Sample 40 gives
   specific suggestions for running a private messaging service; sample 20
   is a short service-status response.

## Boundary to examine

Experience and advice often appear together. Sample 11 reports the writer's
experience moving people to Signal and uses it to recommend a messaging
strategy. A taxonomy must specify which feature takes priority. Merely using
"I think" should not count as reporting an experience.

## Collection limitations

- This is a convenience sample of active Ask HN discussions, not a random
  sample of all Hacker News comments.
- Only top-level comments are collected, with a cap of 60 per thread in API
  display order. Deleted, dead, empty, and duplicate texts are excluded.
- HTML is converted to readable text, paragraph breaks are preserved, and
  full link destinations are appended. Comments are not shortened.
- Some comments require thread context. Identify such cases during review;
  do not silently rewrite a comment to make it self-contained.
- Comments from the same discussion can share wording and subject matter.
  The starter's random row split can put related comments in different
  partitions; this limits claims about performance on new discussions.

## Next steps requiring the student's work

1. Read the 40-comment sample and record your own three observations below.
2. Choose two to four labels and settle the hardest boundary. AI can help
   stress-test the definitions with eight synthetic examples kept outside
   the real dataset.
3. Write five numeric acceptance criteria and reasons in `criteria.md`
   before training. AI can critique whether they are measurable.
4. Label 20 previously unlabeled examples unaided, then mark those rows
   `cold`. After that, AI can pre-label the remainder for your full review.

## Student observations

1. Pending.
2. Pending.
3. Pending.
