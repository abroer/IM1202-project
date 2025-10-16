# python
# File: run_multi_shot.py
# This script writes `multi_shot.lp`, then performs multi-shot solving with clingo.

from clingo import Control, Number

lp = r"""
#program base.
node(a). node(b). node(c).
edge(a,b). edge(b,c).
infected(a).

#program spread(k).
step(k).
infected(Y) :- infected(X), edge(X,Y), step(k).
"""

# write the ASP file (optional; clingo can also load strings)
with open('multi_shot.lp', 'w') as f:
    f.write(lp)

prg = Control()
prg.load('multi_shot.lp')

# ground base and solve (initial state)
prg.ground([("base", [])])
print("Initial solve:")
with prg.solve(yield_=True) as handle:
    for model in handle:
        print(sorted(map(str, model.symbols(shown=True))))

# Ground and solve incrementally for steps 1 and 2
for t in range(1, 3):
    prg.ground([("spread", [Number(t)])])
    print(f"Solve after step {t}:")
    with prg.solve(yield_=True) as handle:
        for model in handle:
            print(sorted(map(str, model.symbols(shown=True))))