"""Check saved metrics against predictions, original texts, and paired splits."""
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

ROOT = Path(__file__).resolve().parent
LABELS = ["firsthand_report", "general_response"]


def read_json(path):
    return json.loads((ROOT / path).read_text())


def read_csv(path):
    with (ROOT / path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-6, abs_tol=1e-7), (actual, expected)


def main():
    source = {r["id"]: r for r in read_csv("data/hn_unlabeled.csv")}
    rows = read_csv("labels.csv")
    assert len(rows) == len(source) == 234
    assert len({r["text"] for r in rows}) == 234
    assert all(r["text"] == source[r["id"]]["text"] for r in rows)
    assert set(r["label"] for r in rows) == set(LABELS)
    labeled = {r["id"]: r for r in rows}
    for original in read_json("data/reviewed_annotations_batch1.json"):
        assert labeled[original["id"]]["label"] == original["label"]
    digest = hashlib.sha256((ROOT / "labels.csv").read_bytes()).hexdigest()
    before = read_json("results_three_seeds_before.json")
    after = read_json("results_three_seeds_after.json")
    for phase, results in (("before", before), ("after", after)):
        assert [r["seed"] for r in results] == [42, 7, 2024]
        for result in results:
            seed = result["seed"]
            assert result["dataset_sha256"] == digest
            predictions = read_json(f"runs/predictions_{phase}_{seed}.json")
            test = read_csv(f"runs/test_split_seed_{seed}.csv")
            assert [r["id"] for r in predictions] == [r["id"] for r in test]
            assert len(predictions) == result["n_test"] == 36
            gold = [r["true_label"] for r in predictions]
            predicted = [r["predicted_label"] for r in predictions]
            for row in predictions:
                assert row["text"] == labeled[row["id"]]["text"]
                assert row["true_label"] == labeled[row["id"]]["label"]
            close(result["accuracy"], accuracy_score(gold, predicted))
            precision, recall, f1, support = precision_recall_fscore_support(
                gold, predicted, labels=LABELS, zero_division=0)
            for i, label in enumerate(LABELS):
                for metric, values in (("precision", precision), ("recall", recall),
                                       ("f1", f1), ("support", support)):
                    close(result["per_label"][label][metric], values[i])
                for guess in LABELS:
                    assert result["confusion"][label][guess] == sum(
                        g == label and p == guess for g, p in zip(gold, predicted))
            close(result["f1_macro"], float(f1.mean()))
            confidence = np.array([r["confidence"] for r in predictions])
            correct = np.array(gold) == np.array(predicted)
            ranked = np.argsort(confidence)
            third = len(predictions) // 3
            assert result["confidence"]["n_per_third"] == third == 12
            close(result["confidence"]["accuracy_most_confident_third"], correct[ranked[-third:]].mean())
            close(result["confidence"]["accuracy_least_confident_third"], correct[ranked[:third]].mean())
    for pre, post in zip(before, after):
        for key in ("seed", "dataset_sha256", "learning_rate", "batch_size", "max_length", "base_model",
                    "n_train", "n_validation", "n_test", "device", "torch_version", "transformers_version"):
            assert pre[key] == post[key], key
        assert pre["epochs"] == 3 and post["epochs"] == 6
    assert read_json("results.json") == before[0]
    assert read_csv("test_split.csv") == read_csv("runs/test_split_seed_42.csv")
    baseline = read_json("baseline_results.json")
    assert baseline["held_out"] and baseline["used_definitions"] and baseline["n"] == 36
    test = read_csv("test_split.csv")
    assert [r["text"] for r in baseline["predictions"]] == [r["text"] for r in test]
    assert [r["gold"] for r in baseline["predictions"]] == [r["label"] for r in test]
    from baseline import score
    recalculated = score([r["gold"] for r in baseline["predictions"]],
                         [r["predicted"] for r in baseline["predictions"]], LABELS)
    close(recalculated["accuracy"], baseline["scores"]["accuracy"])
    close(recalculated["f1_macro"], baseline["scores"]["f1_macro"])
    for label in LABELS:
        for metric in ("precision", "recall", "f1", "support"):
            close(recalculated["per_label"][label][metric], baseline["scores"]["per_label"][label][metric])
    staff = read_csv("my_staff_labels.csv")
    posts = read_csv("data/staff_posts.csv")
    assert len(staff) == len(posts) == 30
    assert [r["text"] for r in staff] == [r["text"] for r in posts]
    key_rows = read_csv("data/staff_labels.csv")
    key = {r["id"]: r["label"] for r in key_rows}
    assert len(key) == len(key_rows) == 30
    assert set(key) == {r["id"] for r in posts}
    assert all(r["label"] in {"analysis", "hot_take", "reaction"} for r in staff + key_rows)
    disagreements = [{"text": post["text"], "staff": key[post["id"]], "mine": mine["label"]}
                     for post, mine in zip(posts, staff) if key[post["id"]] != mine["label"]]
    agreement = read_json("agreement_results.json")
    assert agreement["compared"] == 30 and agreement["staff_posts_not_in_mine"] == 0
    assert agreement["agreed"] == 30 - len(disagreements)
    assert agreement["disagreements"] == disagreements
    close(agreement["agreement_rate"], agreement["agreed"] / 30)
    provenance = read_json("data/ai_staff_annotations.json")
    assert provenance["unaided_student_work"] is False
    assert provenance["labels_sha256"] == hashlib.sha256((ROOT / "my_staff_labels.csv").read_bytes()).hexdigest()
    adjudications = read_json("data/agreement_adjudications.json")["adjudications"]
    assert len(adjudications) == len(disagreements)
    assert {r["text"] for r in adjudications} == {r["text"] for r in disagreements}
    for decision in adjudications:
        assert decision["category"] in {"a", "b", "c"} and decision["reason"] and decision["call"]
    print("PASS: 234 original texts and 20 reviewed labels preserved.")
    print("PASS: six trials' scores, matrices, supports, and confidence thirds recomputed.")
    print("PASS: before/after data, seeds, test posts, and settings match; only epochs changed.")
    print("PASS: baseline and original trained model use the same 36 posts.")
    print("Dataset:", dict(Counter(r["label"] for r in rows)))
    print(f"PASS: AI-to-staff agreement recomputed: {agreement['agreed']}/30; all disagreements adjudicated.")
    print("LIMITATION: AI-assisted labels do not establish the unaided-student criterion.")


if __name__ == "__main__":
    main()
