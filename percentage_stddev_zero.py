import json

IN_PATH = r"C:\Users\suuser\Desktop\semeval26-05-scripts\out_of_std_entries.json"
OUT_PATH = r"C:\Users\suuser\Desktop\semeval26-05-scripts\out_of_std_entries_filtered.json"

# For stddev==0, keep only if abs(pred-avg) < TOL
TOL = 1.0

def filter_zero_std_entries(in_path=IN_PATH, out_path=OUT_PATH, tol=TOL, save=True):
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    zero_std_total = 0
    zero_std_kept = 0

    filtered = {}

    for k, entry in data.items():
        avg = float(entry.get("average"))
        std = float(entry.get("stdev"))
        pred = float(entry.get("prediction"))

        if std == 0.0:
            zero_std_total += 1
            # Keep only if prediction is close to avg (e.g., avg=5, pred=4 -> keep)
            if abs(pred - avg) < tol:
                zero_std_kept += 1
                filtered[k] = entry
            # else: drop (e.g., avg=5, pred=1 -> drop)
        else:
            # For non-zero std, keep everything as-is (this file is already "out of std")
            filtered[k] = entry

    # Stats
    zero_std_pct_in_file = (zero_std_total / total * 100) if total else 0.0
    zero_std_kept_pct_of_zero = (zero_std_kept / zero_std_total * 100) if zero_std_total else 0.0
    zero_std_kept_pct_of_total = (zero_std_kept / total * 100) if total else 0.0

    print("======================================")
    print(f"Total entries in out_of_std_entries: {total}")
    print(f"stddev==0 entries: {zero_std_total} ({zero_std_pct_in_file:.2f}%)")
    print(f"stddev==0 kept (|pred-avg| < {tol}): {zero_std_kept} "
          f"({zero_std_kept_pct_of_zero:.2f}% of stddev==0; {zero_std_kept_pct_of_total:.2f}% of total)")
    print(f"Filtered total entries: {len(filtered)}")
    print("======================================")

    if save:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(filtered, f, indent=4, ensure_ascii=False)
        print("Saved filtered JSON to:")
        print(out_path)

    return filtered


if __name__ == "__main__":
    filter_zero_std_entries()
