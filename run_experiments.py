"""Execute the notebook's training functions with durable, auditable trial output.

Usage: .venv/bin/python run_experiments.py --phase before
       .venv/bin/python run_experiments.py --phase after --epochs 6
Functions are loaded from the notebook, rather than maintaining a second model.
"""
import argparse
import ast
import gc
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
os.environ.setdefault("HF_HOME", str(ROOT / ".cache" / "huggingface"))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def notebook_namespace():
    notebook = json.loads((ROOT / "takemeter.ipynb").read_text())
    namespace = {}
    # Execute setup/settings and only imports/function definitions elsewhere.
    for index in (2, 6, 10, 12, 14, 16, 21, 23):
        source = "".join(notebook["cells"][index]["source"])
        tree = ast.parse(source)
        if index not in (2, 6):
            tree.body = [node for node in tree.body if isinstance(
                node, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
        exec(compile(tree, f"takemeter.ipynb:cell{index}", "exec"), namespace)
    return namespace


def save_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, choices=["before", "after"])
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()
    output = ROOT / f"results_three_seeds_{args.phase}.json"
    if output.exists():
        raise SystemExit(f"Refusing to overwrite completed evidence: {output}")
    import pandas as pd
    import numpy as np
    import torch
    from datasets import Dataset, disable_progress_bars
    from transformers import __version__ as transformers_version
    disable_progress_bars()
    ns = notebook_namespace()
    ns["MAX_LENGTH"] = args.max_length
    ns["EPOCHS"] = args.epochs
    df = pd.read_csv(ROOT / "labels.csv", keep_default_na=False)
    problems, warnings = ns["check_dataset"](df, ns["LABELS"])
    if df["label"].eq("").any() or df["text"].duplicated().any():
        problems.append("Blank labels or duplicate text")
    if problems:
        raise SystemExit(str(problems))
    print("Dataset warnings:", warnings, flush=True)
    dataset_sha = hashlib.sha256((ROOT / "labels.csv").read_bytes()).hexdigest()
    runs = ROOT / "runs"
    runs.mkdir(exist_ok=True)
    all_results = []
    for seed in (42, 7, 2024):
        started = datetime.now(timezone.utc).isoformat()
        tr, va, te = ns["split_dataset"](df, seed)
        if args.phase == "after":
            original = pd.read_csv(runs / f"test_split_seed_{seed}.csv", keep_default_na=False)
            assert te.equals(original), "Before/after test split differs"
        else:
            te.to_csv(runs / f"test_split_seed_{seed}.csv", index=False)
        print(f"Starting {args.phase} seed {seed}, max_length {args.max_length}", flush=True)
        start = time.perf_counter()
        trainer, tokenizer = ns["train_model"](
            tr, va, ns["LABELS"], seed, ns["EPOCHS"], ns["LEARNING_RATE"],
            ns["BATCH_SIZE"], ns["BASE_MODEL"], quiet=True)
        train_seconds = time.perf_counter() - start
        start = time.perf_counter()
        result = ns["evaluate"](trainer, tokenizer, te, ns["LABELS"], seed=seed)
        eval_seconds = time.perf_counter() - start
        tokenized = Dataset.from_pandas(ns["to_ids"](te, ns["LABELS"])).map(
            lambda batch: tokenizer(batch["text"], truncation=True, padding="max_length",
                                    max_length=args.max_length), batched=True)
        prediction = trainer.predict(tokenized)
        logits = prediction.predictions
        assert np.isfinite(logits).all(), "Nonfinite predictions"
        predicted = logits.argmax(axis=-1)
        exponentials = np.exp(logits - logits.max(axis=-1, keepdims=True))
        probabilities = exponentials / exponentials.sum(axis=-1, keepdims=True)
        records = []
        for index, row in te.iterrows():
            records.append({"id": str(row["id"]), "text": row["text"],
                            "true_label": row["label"],
                            "predicted_label": ns["LABELS"][int(predicted[index])],
                            "confidence": float(probabilities[index].max()),
                            "token_count": len(tokenizer.encode(row["text"], truncation=False))})
        assert sum(r["true_label"] == r["predicted_label"] for r in records) / len(records) == result["accuracy"]
        result.update({
            "device": str(trainer.args.device), "device_name": ns["DEVICE_NAME"],
            "torch_version": torch.__version__, "transformers_version": transformers_version,
            "max_length": args.max_length, "epochs": ns["EPOCHS"],
            "learning_rate": ns["LEARNING_RATE"], "batch_size": ns["BATCH_SIZE"],
            "base_model": ns["BASE_MODEL"], "phase": args.phase,
            "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(),
            "dataset_sha256": dataset_sha, "train_seconds": train_seconds,
            "evaluation_seconds": eval_seconds,
            "n_train": len(tr), "n_validation": len(va),
            "majority_baseline_accuracy": float(te["label"].value_counts().max() / len(te)),
        })
        save_json(runs / f"predictions_{args.phase}_{seed}.json", records)
        save_json(runs / f"training_history_{args.phase}_{seed}.json", trainer.state.log_history)
        save_json(runs / f"result_{args.phase}_{seed}.json", result)
        if args.phase == "before" and seed == 42:
            save_json(ROOT / "results.json", result)
            te.to_csv(ROOT / "test_split.csv", index=False)
        all_results.append(result)
        save_json(runs / f"partial_{args.phase}.json", all_results)
        print(json.dumps(result), flush=True)
        del trainer, tokenizer, tokenized, prediction
        gc.collect()
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
    save_json(output, all_results)
    print(ns["spread_table"](all_results, ns["LABELS"]), flush=True)
    print(ns["matrix_markdown"](all_results[0]["confusion"], ns["LABELS"]), flush=True)


if __name__ == "__main__":
    main()
