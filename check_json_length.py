import json

# Load the JSON file
with open('out_of_std_entries.json', 'r') as f:
    data = json.load(f)

# Get the length
length = len(data)

print(f"Length of out_of_std_entries.json: {length} entries")

# Also check the filtered file
with open('out_of_std_entries_filtered.json', 'r') as f:
    data_filtered = json.load(f)

length_filtered = len(data_filtered)

print(f"Length of out_of_std_entries_filtered.json: {length_filtered} entries")

print(f"\nDifference: {length - length_filtered} entries (entries with std=0)")
