import json


def find_out_of_std_entries(json_path, jsonl_path, output_path):
    # Load main JSON file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Load predictions JSONL file
    predictions = {}
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line.strip())
            predictions[obj["id"]] = obj["prediction"]

    out_of_range_entries = {}

    for id_, pred in predictions.items():
        if id_ not in data:
            continue

        avg = data[id_]["average"]
        std = data[id_]["stdev"]

        lower = avg - std
        upper = avg + std

        if pred < lower or pred > upper:
            # Copy full original entry
            full_entry = data[id_].copy()

            # Add prediction info
            full_entry["prediction"] = pred
            full_entry["lower_bound"] = lower
            full_entry["upper_bound"] = upper

            out_of_range_entries[id_] = full_entry

    # Save to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out_of_range_entries, f, indent=4, ensure_ascii=False)

    return out_of_range_entries


# Example usage
if __name__ == "__main__":
    json_path = "C:/Users/suuser/Desktop/semeval26-05-scripts/data/test.json"
    jsonl_path = "C:/Users/suuser/Desktop/semeval26-05-scripts/predictions/submitted/predictions.jsonl"
    output_path = "C:/Users/suuser/Desktop/semeval26-05-scripts/out_of_std_entries.json"

    results = find_out_of_std_entries(json_path, jsonl_path, output_path)

    print(f"Saved {len(results)} entries to:")
    print(output_path)
