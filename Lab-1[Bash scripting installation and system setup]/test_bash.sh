#!/bin/bash
# Run your Python file on every file starting with "test" in current directory

PYTHON_EXE="python3"
SCRIPT="test_python.py"

# Loop through files starting with "test"
for file in test*; do
    if [ -f "$file" ]; then
        echo ">>> Running on $file"
        $PYTHON_EXE $SCRIPT "$file"
        echo "-----------------------------"

                # Save summary for later
        first_line=$(head -n 1 "$file" | cut -c1-20)
        summaries+="---- Summary ----"$'\n'
        summaries+="File executed: $file"$'\n'
        summaries+="First line: $first_line"$'\n'
        summaries+="-----------------------------"$'\n\n'
    fi
done

echo "$summaries"