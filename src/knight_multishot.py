from clingo import Control, Number

def extract_positions(model):
    return sorted([(s.arguments[0].number, s.arguments[1].number, s.arguments[2].number)
                   for s in model.symbols(shown=True) if s.name == "pos"])

def unique_cells(positions):
    return set((x,y) for (x,y,_) in positions)

def main():
    prg = Control()
    prg.load("knight.lp")

    # ground base
    prg.ground([("base", [])])
    # match n with the const in knight.lp
    n = 5
    max_steps = n * n - 1

    # initial solve (time 0 already grounded)
    print("Initial solve (time 0):")
    with prg.solve(yield_=True) as handle:
        for m in handle:
            pos = extract_positions(m)
            print("visited:", unique_cells(pos))

    # incrementally add steps
    for t in range(1, max_steps + 1):
        prg.ground([("step", [Number(t)])])
        print(f"\nSolve after step {t}:")
        with prg.solve(yield_=True) as handle:
            found = False
            print(handle)
            for m in handle:
                print(m)
                found = True
                pos = extract_positions(m)
                visited = unique_cells(pos)
                print(f"visited {len(visited)}/{n*n}")
                if len(visited) == n * n:
                    print("Full tour found. Positions (x,y,time):")
                    for p in pos:
                        print(p)
                    return
            if not found:
                print("No solution at this depth (partial search failed).")
                return

if __name__ == "__main__":
    main()