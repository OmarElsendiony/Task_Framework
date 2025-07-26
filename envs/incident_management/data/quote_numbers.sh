#!/bin/bash

# This script wraps unquoted numbers followed by commas in quotes,
# while preserving the comma, in all files in the current directory and subdirectories.

find . -type f -name "*" | while read -r file; do
  # Replace unquoted numbers followed by a comma with quoted numbers, preserving the comma
  perl -i.bak -pe 's/(?<!")\b(\d+)\b(?!")(?=,)/"$1"/g' "$file"
done

echo "Replacement complete. Backups saved as .bak files."
