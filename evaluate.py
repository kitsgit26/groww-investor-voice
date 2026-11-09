import argparse
from pathlib import Path

import pandas as pd

# Pre-declared demonstration thresholds. These are not production-readiness
# criteria and must be recalibrated with a larger, representative dataset.
MIN_MICRO_F1 = 0.80
MIN_EXACT_MATCH = 0.70

THEMES = [
    "Performance uncertainty",
    "Operational understanding",
    "Investment knowledge",
    "Financial flexibility",
    "External guidance seeking",
]


def parse_labels(value):
    """Parse pipe-delimited multi-label values into a set."""
    if pd.isna(value) or not str(value).strip():
        return set()
    return {item.strip() for item in str(value).split("|") if item.strip()}


def calculate_metrics(merged):
    """Calculate per-theme, micro, macro and exact-match metrics."""
    per_theme = []

    for theme in THEMES:
        tp = fp = fn = 0
        support = 0
        predicted_count = 0

        for _, row in merged.iterrows():
            actual = parse_labels(row["reference_themes"])
            predicted = parse_labels(row["predicted_themes"])

            support += int(theme in actual)
            predicted_count += int(theme in predicted)
            tp += int(theme in actual and theme in predicted)
            fp += int(theme not in actual and theme in predicted)
            fn += int(theme in actual and theme not in predicted)

        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )

        per_theme.append({
            "theme": theme,
            "support": support,
            "predicted_count": predicted_count,
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
        })

    tp_total = sum(row["true_positives"] for row in per_theme)
    fp_total = sum(row["false_positives"] for row in per_theme)
    fn_total = sum(row["false_negatives"] for row in per_theme)

    micro_precision = (
        tp_total / (tp_total + fp_total) if tp_total + fp_total else 0.0
    )
    micro_recall = (
        tp_total / (tp_total + fn_total) if tp_total + fn_total else 0.0
    )
    micro_f1 = (
        2 * micro_precision * micro_recall
        / (micro_precision + micro_recall)
        if micro_precision + micro_recall
        else 0.0
    )

    # Macro F1 averages classes with at least one actual or predicted example.
    # Classes with no actual and no predicted examples are unassessed, not zero.
    assessed_f1 = [
        row["f1"]
        for row in per_theme
        if row["support"] > 0 or row["predicted_count"] > 0
    ]
    macro_f1 = (
        sum(assessed_f1) / len(assessed_f1) if assessed_f1 else 0.0
    )

    exact_matches = sum(
        parse_labels(row["reference_themes"])
        == parse_labels(row["predicted_themes"])
        for _, row in merged.iterrows()
    )
    exact_match = exact_matches / len(merged)

    summary = {
        "records_evaluated": len(merged),
        "micro_precision": micro_precision,
        "micro_recall": micro_recall,
        "micro_f1": micro_f1,
        "macro_f1": macro_f1,
        "exact_match_accuracy": exact_match,
    }
    return pd.DataFrame(per_theme), summary


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate multi-label investor feedback classification."
    )
    parser.add_argument("--gold", default="golden_set.csv")
    parser.add_argument("--predictions", default="predictions.csv")
    parser.add_argument("--output", default="evaluation_report.csv")
    args = parser.parse_args()

    gold_path = Path(args.gold)
    predictions_path = Path(args.predictions)

    if not gold_path.exists():
        parser.error(f"Golden dataset not found: {gold_path}")
    if not predictions_path.exists():
        parser.error(f"Predictions file not found: {predictions_path}")

    gold = pd.read_csv(gold_path)
    predictions = pd.read_csv(predictions_path)

    required_gold = {"record_id", "reference_themes", "label_status"}
    required_predictions = {"record_id", "predicted_themes"}

    if not required_gold.issubset(gold.columns):
        parser.error(f"Golden dataset must contain: {sorted(required_gold)}")
    if not required_predictions.issubset(predictions.columns):
        parser.error(
            f"Predictions must contain: {sorted(required_predictions)}"
        )
    if gold.empty:
        parser.error("Golden dataset is empty.")
    if gold["record_id"].isna().any() or predictions["record_id"].isna().any():
        parser.error("Record IDs cannot be blank.")
    if not gold["record_id"].is_unique:
        parser.error("Duplicate record IDs in golden dataset.")
    if not predictions["record_id"].is_unique:
        parser.error("Duplicate record IDs in predictions.")
    if gold["reference_themes"].isna().any():
        parser.error("Reference labels cannot be blank; use an explicit label.")

    allowed = set(THEMES)
    for _, row in gold.iterrows():
        labels = parse_labels(row["reference_themes"])
        if not labels or not labels.issubset(allowed):
            parser.error(f"Invalid or empty reference labels for {row['record_id']}.")

    for _, row in predictions.iterrows():
        labels = parse_labels(row["predicted_themes"])
        if not labels.issubset(allowed):
            parser.error(f"Unknown predicted theme for {row['record_id']}.")

    if set(predictions["record_id"]) != set(gold["record_id"]):
        missing = sorted(set(gold["record_id"]) - set(predictions["record_id"]))
        extra = sorted(set(predictions["record_id"]) - set(gold["record_id"]))
        parser.error(
            "Prediction IDs must exactly match golden IDs. "
            f"Missing: {missing}; extra: {extra}"
        )

    merged = gold[["record_id", "reference_themes"]].merge(
        predictions[["record_id", "predicted_themes"]],
        on="record_id",
        how="inner",
        validate="one_to_one",
    )

    per_theme, summary = calculate_metrics(merged)

    print("\nGROWW INVESTOR VOICE — MULTI-LABEL EVALUATION")
    print("-" * 58)
    print(per_theme.to_string(index=False))
    print("\nOVERALL METRICS")
    for metric, value in summary.items():
        if metric == "records_evaluated":
            print(f"{metric}: {value}")
        else:
            print(f"{metric}: {value:.3f}")

    passed = (
        summary["micro_f1"] >= MIN_MICRO_F1
        and summary["exact_match_accuracy"] >= MIN_EXACT_MATCH
    )
    print("\nEVALUATION GATE")
    print("PASS - demonstration thresholds met." if passed else
          "FAIL - use safe fallback and review predictions.")

    print("\nINTERPRETATION")
    print(
        "Macro F1 averages themes with at least one reference or predicted "
        "example. Themes with neither are unassessed and excluded."
    )
    print(
        "These metrics measure theme-label agreement only. They do not "
        "measure evidence groundedness, factual accuracy, safety, or "
        "production readiness."
    )
    print(
        "The current R01-R10 dataset is illustrative practice data, not "
        "verified public investor feedback or interview data."
    )
    print("Human review remains mandatory.")

    output_path = Path(args.output)
    per_theme.to_csv(output_path, index=False)
    print(f"\nSaved per-theme metrics to: {output_path}")


if __name__ == "__main__":
    main()
