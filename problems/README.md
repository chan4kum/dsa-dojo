# problems/

One file per topic: `<topic>.py` holds the first problems of the topic, `<topic>_more*.py` hold later batches.
Every problem is a self-contained block - prompt, tests, three hints, explanation, a brute-force solution and the
optimised one - so you can read a problem top to bottom without jumping to another file.

The header of every file lists what each key means. To add a problem, copy any block, change it, then run
`python dsa.py selftest && python tools/fuzz_diff.py`.
