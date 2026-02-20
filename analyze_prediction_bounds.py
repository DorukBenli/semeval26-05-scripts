import json
from scipy import stats

def analyze_predictions(json_file):
    """
    Analyze predictions and calculate how far off they are from the bounds.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Define distance ranges for categorization
    distance_ranges = [
        (0.0, 0.1),    # 0.0 - 0.1
        (0.1, 0.2),    # 0.1 - 0.2
        (0.2, 0.3),    # 0.2 - 0.3
        (0.3, 0.4),    # 0.3 - 0.4
        (0.4, 0.5),    # 0.4 - 0.5
        (0.5, 0.75),   # 0.5 - 0.75
        (0.75, 1.0),   # 0.75 - 1.0
        (1.0, 1.5),    # 1.0 - 1.5
        (1.5, 2.0),    # 1.5 - 2.0
        (2.0, float('inf')),  # 2.0+
    ]
    
    # Initialize counters
    within_bounds = 0
    below_bounds = 0
    above_bounds = 0
    distance_counts = {f"{low}-{high}": 0 for low, high in distance_ranges}
    distance_counts["2.0+"] = 0
    
    # Track detailed info for each entry
    entries_info = []
    
    # Collect predictions and averages for Spearman correlation
    predictions = []
    averages = []
    
    for key, entry in data.items():
        prediction = entry['prediction']
        lower_bound = entry['lower_bound']
        upper_bound = entry['upper_bound']
        average = entry['average']
        homonym = entry['homonym']
        sample_id = entry['sample_id']
        
        # Collect for Spearman correlation
        predictions.append(prediction)
        averages.append(average)
        
        # Calculate distance from bounds
        if lower_bound <= prediction <= upper_bound:
            within_bounds += 1
            distance = 0.0
        elif prediction < lower_bound:
            below_bounds += 1
            distance = lower_bound - prediction
        else:  # prediction > upper_bound
            above_bounds += 1
            distance = prediction - upper_bound
        
        # Categorize by distance
        categorized = False
        for low, high in distance_ranges:
            if low <= distance < high:
                range_key = f"{low}-{high}" if high != float('inf') else f"{low}+"
                if range_key not in distance_counts:
                    distance_counts[range_key] = 0
                distance_counts[range_key] += 1
                categorized = True
                break
        
        if not categorized:
            distance_counts["2.0+"] += 1
        
        # Store entry info
        entries_info.append({
            'key': key,
            'homonym': homonym,
            'sample_id': sample_id,
            'prediction': prediction,
            'average': average,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'distance': distance,
            'status': 'within' if distance == 0 else ('below' if prediction < lower_bound else 'above')
        })
    
    total = len(data)
    
    # Calculate Spearman correlation
    spearman_corr, spearman_pvalue = stats.spearmanr(predictions, averages)
    
    # Print summary
    print("=" * 80)
    print("PREDICTION BOUNDS ANALYSIS")
    print("=" * 80)
    print(f"\nTotal entries: {total}")
    print(f"\nSpearman Correlation (Predictions vs Average): {spearman_corr:.4f} (p-value: {spearman_pvalue:.4e})")
    print(f"\nWithin bounds: {within_bounds} ({within_bounds/total*100:.2f}%)")
    print(f"Below bounds: {below_bounds} ({below_bounds/total*100:.2f}%)")
    print(f"Above bounds: {above_bounds} ({above_bounds/total*100:.2f}%)")
    
    print("\n" + "=" * 80)
    print("DISTANCE FROM BOUNDS BREAKDOWN")
    print("=" * 80)
    print(f"\n{'Distance Range':<20} {'Count':<10} {'Percentage':<15} {'Cumulative':<15}")
    print("-" * 60)
    
    cumulative = 0
    for range_key in sorted(distance_counts.keys(), key=lambda x: float(x.split('-')[0]) if '-' in x else float(x[:-1])):
        count = distance_counts[range_key]
        percentage = count / total * 100
        cumulative += percentage
        print(f"{range_key:<20} {count:<10} {percentage:<15.2f}% {cumulative:<15.2f}%")
    
    print("\n" + "=" * 80)
    print("EXAMPLES BY DISTANCE RANGE")
    print("=" * 80)
    
    # Group entries by distance range
    entries_by_range = {}
    for entry in entries_info:
        dist = entry['distance']
        range_key = None
        for low, high in distance_ranges:
            if low <= dist < high:
                range_key = f"{low}-{high}" if high != float('inf') else f"{low}+"
                break
        if range_key is None:
            range_key = "2.0+"
        
        if range_key not in entries_by_range:
            entries_by_range[range_key] = []
        entries_by_range[range_key].append(entry)
    
    # Show examples for each range
    for range_key in sorted(entries_by_range.keys(), key=lambda x: float(x.split('-')[0]) if '-' in x else float(x[:-1])):
        entries = entries_by_range[range_key]
        print(f"\n--- Distance Range: {range_key} ({len(entries)} entries) ---")
        for entry in entries[:3]:  # Show first 3 examples
            print(f"  Sample ID: {entry['sample_id']}, Homonym: {entry['homonym']}")
            print(f"    Prediction: {entry['prediction']:.4f}, Average: {entry['average']:.4f}")
            print(f"    Bounds: [{entry['lower_bound']:.4f}, {entry['upper_bound']:.4f}]")
            print(f"    Distance: {entry['distance']:.4f} ({entry['status']})")
        if len(entries) > 3:
            print(f"  ... and {len(entries) - 3} more")
    
    return {
        'total': total,
        'within_bounds': within_bounds,
        'below_bounds': below_bounds,
        'above_bounds': above_bounds,
        'distance_counts': distance_counts,
        'entries_info': entries_info,
        'spearman_correlation': spearman_corr,
        'spearman_pvalue': spearman_pvalue
    }

if __name__ == "__main__":
    result = analyze_predictions('out_of_std_entries.json')
