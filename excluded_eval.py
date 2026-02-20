import json
import statistics
from scipy.stats import spearmanr

# ===== HARDCODED FILE PATHS =====
PREDICTIONS_FILE = "C:/Users/suuser/Desktop/semeval26-05-scripts/predictions/final_pred/predictions.jsonl"
GOLD_FILE = "C:/Users/suuser/Desktop/semeval26-05-scripts/data/test.json"


def get_standard_deviation(l):
    return statistics.stdev(l)


def get_average(l):
    return sum(l) / len(l)


def is_within_standard_deviation(prediction, labels):
    avg = get_average(labels)
    stdev = get_standard_deviation(labels)

    # Within avg ± std
    if (avg - stdev) < prediction < (avg + stdev):
        return True

    # Or within absolute distance < 1
    if abs(avg - prediction) < 1:
        return True

    return False


def load_predictions(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def evaluate():
    # Load data
    with open(GOLD_FILE, "r", encoding="utf-8") as f:
        gold_data = json.load(f)

    predictions = load_predictions(PREDICTIONS_FILE)

    gold_list = []
    pred_list = []

    correct = 0
    wrong = 0
    skipped_zero_std = 0

    for entry in predictions:
        sid = str(entry["id"])

        if sid not in gold_data:
            continue

        labels = gold_data[sid]["choices"]
        stdev = get_standard_deviation(labels)

        # Skip stddev == 0 samples
        if stdev == 0:
            skipped_zero_std += 1
            continue

        avg = get_average(labels)
        pred = entry["prediction"]

        gold_list.append(avg)
        pred_list.append(pred)

        if is_within_standard_deviation(pred, labels):
            correct += 1
        else:
            wrong += 1

    # Compute metrics
    spearman_corr, spearman_p = spearmanr(pred_list, gold_list)
    accuracy = correct / (correct + wrong)

    print("======================================")
    print("Evaluation (excluding stddev == 0)")
    print("======================================")
    print(f"Used samples: {len(gold_list)}")
    print(f"Skipped stddev==0: {skipped_zero_std}")
    print("--------------------------------------")
    print(f"Spearman Correlation: {spearman_corr}")
    print(f"Spearman p-Value:     {spearman_p}")
    print(f"Accuracy:             {accuracy} ({correct}/{correct+wrong})")


if __name__ == "__main__":
    evaluate()
