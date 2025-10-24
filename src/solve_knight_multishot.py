#!/usr/bin/env python3
import clingo
import sys

def extract_sub_visits(model):
    """Extract sub_visit(GX,GY,G) atoms from a subboard model and return sorted (G,X,Y)."""
    atoms = model.symbols(shown=True)
    visits = []
    for a in atoms:
        if a.name == 'sub_visit' and len(a.arguments) == 3:
            x = a.arguments[0].number
            y = a.arguments[1].number
            g = a.arguments[2].number
            visits.append((g, x, y))
    return sorted(visits)


def main():
    lpfile = 'knight_10x10_multishot.lp'
    sub_size = 25

    candidate_orders = [
        [(1,1),(2,1),(2,2),(1,2)],
        [(1,1),(1,2),(2,2),(2,1)],
        [(1,1),(2,1),(1,2),(2,2)],
        [(1,1),(1,2),(2,1),(2,2)],
    ]

    def try_order(order):
        fixed_squares = set()
        global_visits = []
        last_end = None

        for i,(bx,by) in enumerate(order):
            offset = i * sub_size

            prg = clingo.Control()
            prg.load(lpfile)

            part_fixed = 'fixed_cumulative'
            for (fx,fy) in fixed_squares:
                prg.add(part_fixed, [], f"fixed({fx},{fy}).")
            prg.ground([('base', []), (part_fixed, [])])

            if i > 0 and last_end is not None:
                prev_sym = clingo.Function('prev_end', [clingo.Number(last_end[0]), clingo.Number(last_end[1])])
                prg.assign_external(prev_sym, True)

            prg.ground([('subboard', [clingo.Number(bx), clingo.Number(by), clingo.Number(offset)])])

            print(f"Solving subboard {i+1} at tile ({bx},{by}) with offset {offset}...")

            # attempt many models looking for one that connects forward
            model = None
            chosen_visits = None
            max_models = 5000
            models_checked = 0

            def knight_adj(a,b):
                (x1,y1) = a; (x2,y2) = b
                dx = abs(x1-x2); dy = abs(y1-y2)
                return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

            next_squares = None
            if i < len(order)-1:
                nbx,nby = order[i+1]
                nx0 = (nbx - 1) * 5 + 1
                nx1 = nbx * 5
                ny0 = (nby - 1) * 5 + 1
                ny1 = nby * 5
                next_squares = [(x,y) for x in range(nx0,nx1+1) for y in range(ny0,ny1+1)]

            with prg.solve(yield_=True) as handle:
                for m in handle:
                    models_checked += 1
                    visits_cand = extract_sub_visits(m)
                    visits_cand = [v for v in visits_cand if v[0] >= offset+1 and v[0] <= offset+sub_size]
                    if len(visits_cand) != sub_size:
                        if models_checked >= max_models:
                            break
                        continue

                    last = max(visits_cand, key=lambda t: t[0])
                    last_coord = (last[1], last[2])

                    if next_squares is not None:
                        ok = any(knight_adj(last_coord, s) for s in next_squares)
                        if not ok:
                            if models_checked >= max_models:
                                break
                            continue

                    model = m
                    chosen_visits = visits_cand
                    break

            if model is None:
                print(f"Order failed at subboard {i+1} {(bx,by)} after {models_checked} models")
                return None

            visits = chosen_visits
            for g,x,y in visits:
                fixed_squares.add((x,y))
                global_visits.append((g,x,y))

            last = max(visits, key=lambda t: t[0])
            last_end = (last[1], last[2])
            print(f" Subboard end at {last_end} (global step {last[0]})")

        global_visits.sort()
        return global_visits

    # try candidate orders until one succeeds
    for ord_idx,ord_try in enumerate(candidate_orders):
        print(f"Trying order #{ord_idx+1}: {ord_try}")
        res = try_order(ord_try)
        if res is not None:
            print('\nSuccess with order:', ord_try)
            print('Assembled global tour (step -> x,y):')
            for g,x,y in res:
                print(f"{g} -> ({x},{y})")
            return 0

    print('All candidate orders failed. Consider relaxing subboard constraints or using a different decomposition.')
    return 1

if __name__ == '__main__':
    sys.exit(main())
