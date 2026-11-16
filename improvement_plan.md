# One improvement — registered before the after runs

Recorded November 16, 2026, after the three before trials and before running
any after trial. Diagnosis and choice are AI-assisted.

Change only training duration: **3 epochs → 6 epochs**. Keep the dataset,
labels, taxonomy, criteria, seeds (42, 7, 2024), 128-token input length,
learning rate (2e-5), batch size (16), base model, and split algorithm fixed.
The Trainer's default linear schedule consequently spans six epochs rather
than three; this is a consequence of changing duration, not a separately tuned
learning-rate setting. No selection among several attempted improvements.

The before runs misclassified 12, 9, and 10 general responses as firsthand
reports, with zero errors in the reverse direction. General-response recall
was 1/13, 4/13, and 3/13. The model leaned heavily toward the majority label.
Validation loss decreased in every epoch for every seed:

| Seed | Epoch 1 | Epoch 2 | Epoch 3 |
|---|---|---|---|
| 42 | 0.585411 | 0.544198 | 0.527667 |
| 7 | 0.612468 | 0.560381 | 0.536816 |
| 2024 | 0.590267 | 0.514101 | 0.482138 |

This supports testing insufficient optimization as a contributing cause.
It does not prove the annotations are correct or rule out ambiguous labels.
The staff check is unavailable and uses a different taxonomy; it cannot be
cited as direct evidence about this dataset's label boundary.

Most before errors are shorter than 128 tokens, so increasing input length
does not directly address the dominant observed failure. Six epochs is one
predeclared trial of longer training, not a guarantee of improvement.

Run: `.venv/bin/python run_experiments.py --phase after --epochs 6`.
Judge success by the unchanged five criteria and paired per-seed results;
report any worsening as well as gains. Test sets are reused for the course's
before/after comparison, so these are development results rather than a new,
untouched final evaluation.
