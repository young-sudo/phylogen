#!/bin/bash

# fasturec doesn't overwrite results
rm fu.txt

if [ "$1" ]; then
    TREES="$1"
else
    # Default value if no parameter is provided
    TREES="trees.txt"
fi

echo "Running fasturec for file $TREES"

fasturec -G "$TREES" -Z -ea
# -G file with trees
# -Z standard heuristic
# -ea output name fu.txt
