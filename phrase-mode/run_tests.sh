#!/usr/bin/env bash

FLAG=0
for i in `seq 7`; do
    TESTFILE="./tests/test${i}.txt"
    OUTFILE="./tests/test${i}.txt.out"
    EXPECTEDFILE="./tests/test${i}.txt.expected"

    python3 parse.py $TESTFILE > $OUTFILE

    if ! cmp -s "$OUTFILE" "$EXPECTEDFILE"; then
        FLAG=1
	      echo "Test failed: ${TESTFILE}"
    fi

    rm $OUTFILE
done

if [[ $FLAG != 1 ]]; then
    echo "Test passed"
fi
