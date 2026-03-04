import json

# Load the JSON file
with open('out_of_std_entries.json', 'r') as f:
    data = json.load(f)

print(f"Verifying {len(data)} entries in out_of_std_entries.json...\n")

# Verify each entry
all_correct = True
errors = []

for key, entry in data.items():
    prediction = entry['prediction']
    average = entry['average']
    stdev = entry['stdev']
    lower_bound = entry['lower_bound']
    upper_bound = entry['upper_bound']
    
    # Calculate expected bounds
    expected_lower = average - stdev
    expected_upper = average + stdev
    
    # Check if prediction is outside bounds
    is_outside = prediction < lower_bound or prediction > upper_bound
    
    # Check if bounds match expected
    bounds_match = abs(lower_bound - expected_lower) < 0.0001 and abs(upper_bound - expected_upper) < 0.0001
    
    if not is_outside:
        errors.append(f"Entry {key}: Prediction {prediction} is WITHIN bounds [{lower_bound}, {upper_bound}]")
        all_correct = False
    
    if not bounds_match:
        errors.append(f"Entry {key}: Bounds mismatch. Expected [{expected_lower}, {expected_upper}], got [{lower_bound}, {upper_bound}]")
        all_correct = False

if all_correct:
    print("[OK] All entries verified successfully!")
    print(f"  - All {len(data)} entries have predictions outside the bounds (average +/- stddev)")
    print(f"  - All bounds are correctly calculated")
else:
    print("[ERROR] Errors found:")
    for error in errors:
        print(f"  - {error}")

# Also show some examples
print("\n" + "="*80)
print("Sample entries:")
print("="*80)
for i, (key, entry) in enumerate(list(data.items())[:5]):
    prediction = entry['prediction']
    average = entry['average']
    stdev = entry['stdev']
    lower_bound = entry['lower_bound']
    upper_bound = entry['upper_bound']
    
    print(f"\nEntry {key}:")
    print(f"  Average: {average}, StdDev: {stdev}")
    print(f"  Bounds: [{lower_bound}, {upper_bound}]")
    print(f"  Prediction: {prediction}")
    print(f"  Status: {'OUTSIDE bounds' if prediction < lower_bound or prediction > upper_bound else 'WITHIN bounds'}")
