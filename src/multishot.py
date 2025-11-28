# python
# File: run_multi_shot.py
# This script writes `multi_shot.lp`, then performs multi-shot solving with clingo.

from clingo import Control, Number

prg = Control()
prg.load('multi-shot.lp')

# ground base and solve (initial state)
prg.ground([("base", [])])
print("Initial solve:")
with prg.solve(yield_=True) as handle:
    for model in handle:
        print(sorted(map(str, model.symbols(shown=True))))

# Ground and solve incrementally for steps 1 and 2
#program sub_knight(x0, y0, size, start_x, start_y, end_x, end_y, offset).
for t in range(1, 4):
    prg.ground([("sub_knight", [Number(0), Number(0), Number(5), Number(0), Number(0), Number(4), Number(4), Number(t-1)])])
    print(f"Solve after step {t}:")
    with prg.solve(yield_=True) as handle:
        for model in handle:
            print(sorted(map(str, model.symbols(shown=True))))