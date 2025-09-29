import os
from collections import Counter

base_path = "week_11"  # change to your root directory

numbers = []

for root, dirs, files in os.walk(base_path):
    for name in dirs:
        parts = name.split("-")
        if len(parts) >= 3:  # make sure there's a number in between
            num = parts[2]   # the number between dashes
            if num.isdigit():
                numbers.append(int(num))

# Count occurrences
counts = dict(Counter(numbers))

print(counts)
