from clingo import Control, Number

def extract_positions(model):
    return sorted([(s.arguments[0].number, s.arguments[1].number, s.arguments[2].number)
                   for s in model.symbols(shown=True) if s.name == "pos"])

def unique_cells(positions):
    return set((x,y) for (x,y,_) in positions)

def print_solve_statistics(res, ctrl=None):
    """
    Print solver statistics if available, otherwise show fallback info.
    `res` is the clingo SolveResult returned by `handle.get()`.
    `ctrl` is the clingo Control object (optional).
    """
    # Prefer SolveResult.statistics if present
    if hasattr(res, "statistics"):
        try:
            print(res.statistics)
            return
        except Exception:
            pass

    # Avoid using hasattr(ctrl, "statistics") because the property access can raise.
    if ctrl is not None:
        try:
            stats = getattr(ctrl, "statistics")
        except RuntimeError:
            # statistics not yet available from Control
            print("Control.statistics not (yet) available.")
        except Exception:
            pass
        else:
            print(stats)
            return

    # fallback: show available attributes and string form
    print("SolveResult has no 'statistics' attribute on this clingo build or stats unavailable.")
    attrs = [a for a in dir(res) if not a.startswith("_")]
    print("Available SolveResult attributes:", attrs)
    print("SolveResult string representation:")
    print(res)

# Example usage inside your solve loop:
# with prg.solve(yield_=True) as handle:
#     res = handle.get()
#     print_solve_statistics(res, prg)
#     for m in handle:
#         ...
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
            for m in handle:
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

    prg = Control()
    prg.load("knight.lp")
    prg.ground([("base", [])])
    prg.ground([("step", [Number(25)])])
    res = prg.solve()
    print(res)

if __name__ == "__main__":
    main()