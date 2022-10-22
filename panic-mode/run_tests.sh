#!/usr/bin/env bash

FLAG=0
for TESTFILE in "$@"; do
    OUTFILE="${TESTFILE}.out"
    EXPECTEDFILE="${TESTFILE}.expected"
    python3 parse.py $TESTFILE
    if ! cmp -s "$OUTFILE" "$EXPECTEDFILE"; then
        FLAG=1
	echo "Test failed: ${TESTFILE}"	
    fi
    rm $OUTFILE    
done
if [[ $FLAG != 1 ]]; then
    echo "Test passed"
fi
