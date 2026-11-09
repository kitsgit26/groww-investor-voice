
import argparse
import pandas as pd
from pathlib import Path

# --------------------------------
# PRE-DECLARED DEMONSTRATION GATE
# --------------------------------

MIN_MICRO_F1 = 0.80
MIN_EXACT_MATCH = 0.70

THEMES = [
    "Performance uncertainty",
    "Operational understanding",
    "Investment knowledge",
    "Financial flexibility"
]

def parse_labels(value):
    if pd.isna(value) or not str(value).strip():
        return set()

    return {
        item.strip()
        for item in str(value).split("|")
        if item.strip()
    }


def calculate_metrics(gold, predictions):

    records = []

    for theme in THEMES:
        tp = fp = fn = 0

        for _, row in gold.iterrows():
            actual = parse_labels(row["reference_themes"])
            predicted = parse_labels(row["predicted_themes"])

            if theme in actual and theme in predicted:
                tp += 1
            elif theme not in actual and theme in predicted:
                fp += 1
            elif theme in actual and theme not in predicted:
                fn += 1

        precision = tp / (tp + fp) if tp + fp else 0
        recall = tp / (tp + fn) if tp + fn else 0

        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall else 0
        )

        records.append({
            "theme": theme,
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3)
        })

    tp_total = sum(x["true_positives"] for x in records)
    fp_total = sum(x["false_positives"] for x in records)
    fn_total = sum(x["false_negatives"] for x in records)

    micro_precision = (
        tp_total / (tp_total + fp_total)
        if tp_total + fp_total else 0
    )

    micro_recall = (
        tp_total / (tp_total + fn_total)
        if tp_total + fn_total else 0
    )

    micro_f1 = (
        2 * micro_precision * micro_recall /
        (micro_precision + micro_recall)
        if micro_precision + micro_recall else 0
    )

    exact_matches = 0

    for _, row in gold.iterrows():
        actual = parse_labels(row["reference_themes"])
        predicted = parse_labels(row["predicted_themes"])

        if actual == predicted:
            exact_matches += 1

    exact_match_accuracy = exact_matches / len(gold)

    return (
        pd.DataFrame(records),
        micro_precision,
        micro_recall,
        micro_f1,
        exact_match_accuracy
    )


def main():

    parser = argparse.ArgumentParser(
        description="Evaluate multi-label investor feedback classification."
    )

    parser.add_argument(
        "--gold",
        default="golden_set.csv"
    )

    parser.add_argument(
        "--predictions",
        default="predictions.csv"
    )

    args = parser.parse_args()

    gold_path = Path(args.gold)
    predictions_path = Path(args.predictions)

    if not gold_path.exists():
        print("ERROR: golden_set.csv not found.")
        return

    gold = pd.read_csv(gold_path)

    required_gold = {
        "record_id",
        "reference_themes",
        "label_status"
    }

    if not required_gold.issubset(gold.columns):
        print("ERROR: Golden dataset has missing columns.")
        return

    if not gold["record_id"].is_unique:
        print("ERROR: Duplicate record IDs in golden dataset.")
        return

    if not predictions_path.exists():

        template = pd.DataFrame({
            "record_id": gold["record_id"],
            "predicted_themes": [""] * len(gold)
        })

        template.to_csv("predictions_template.csv", index=False)

        print("No predictions.csv found.")
        print("Created predictions_template.csv.")
        print("Add actual AI predictions before evaluation.")
        return

    predictions = pd.read_csv(predictions_path)

    required_predictions = {
        "record_id",
        "predicted_themes"
    }

    if not required_predictions.issubset(predictions.columns):
        print("ERROR: Prediction file has missing columns.")
        return

    if not predictions["record_id"].is_unique:
        print("ERROR: Duplicate prediction record IDs.")
        return

    if set(predictions["record_id"]) != set(gold["record_id"]):
        print("ERROR: Prediction IDs do not exactly match golden IDs.")
        print("Evaluation blocked to prevent misleading results.")
        return

    merged = gold.merge(
        predictions,
        on="record_id",
        how="inner"
    )

    valid_labels = set(THEMES)

    for _, row in merged.iterrows():
        actual = parse_labels(row["reference_themes"])
        predicted = parse_labels(row["predicted_themes"])

        if not actual.issubset(valid_labels):
            print("ERROR: Unknown reference theme.")
            return

        if not predicted.issubset(valid_labels):
            print("ERROR: Unknown predicted theme.")
            return

    (
        metrics,
        precision,
        recall,
        f1,
        exact_match
    ) = calculate_metrics(merged, predictions)

    print("\nGROWW INVESTOR VOICE")
    print("MULTI-LABEL EVALUATION REPORT")
    print("-" * 45)

    print(metrics.to_string(index=False))

    print("\nOVERALL METRICS")
    print(f"Micro precision: {precision:.3f}")
    print(f"Micro recall:    {recall:.3f}")
    print(f"Micro F1:        {f1:.3f}")
    print(f"Exact match:     {exact_match:.3f}")

    passed = (
        f1 >= MIN_MICRO_F1
        and exact_match >= MIN_EXACT_MATCH
    )

    print("\nEVALUATION GATE")

    if passed:
        print("PASS - Demonstration thresholds met.")
    else:
        print("FAIL - Use safe fallback and review predictions.")

    print("\nIMPORTANT:")
    print("These thresholds are provisional demonstration thresholds.")
    print("Ten illustrative records are not sufficient for production validation.")
    print("Classification metrics do not establish AI safety.")
    print("Human review remains mandatory.")

    metrics.to_csv("evaluation_report.csv", index=False)

    print("\nSaved: evaluation_report.csv")


if __name__ == "__main__":
    main()
