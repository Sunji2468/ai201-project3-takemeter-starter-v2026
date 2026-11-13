# Community exploration — Ask HN

Status: Community sample and taxonomy prepared; labeling is in progress.

## Community and scope

Hacker News, restricted to top-level comments in public Ask HN discussions.
Each whole comment is one example. The classifier will see only comment text,
not the thread title, author, score, or source URL.

Sources are collected using the [official public API](https://github.com/HackerNews/API).
`data/hn_unlabeled.csv` preserves comment IDs, source links, thread IDs, collection
timestamps, and original HTML. Its label and note columns are intentionally blank.
`data/reading_sample.md` contains 40 comments spread across the collected threads.

## Three distinctions observed in the sample

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

The resulting taxonomy draft is now in README.md: `firsthand_report`
versus `general_response`. This collapses advice and other non-experiential
responses into one class because advice overlaps heavily with experience.
See `taxonomy_stress_test.md` for eight synthetic boundary cases and
`annotation_review.md` for the first 20 reviewed annotations.

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

## Next steps

1. Label and review the remaining 214 comments.
2. Check label balance and document ambiguous cases.
3. Run training using the recorded acceptance targets, then save results.
