#program base.
% Global board size
#const n = 10.
#const sub = 5.

% Global squares
square(1..n,1..n).
step(1..n*n).

% Knight moves on the global board
move(X1,Y1,X2,Y2) :- square(X1,Y1), square(X2,Y2), 1 = |X1-X2|, 2 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square(X1,Y1), square(X2,Y2), 2 = |X1-X2|, 1 = |Y1-Y2|.

% Presence of a previous subboard's endpoint (optional)
% prev_end(X,Y) can be added to the base dynamically from the Python driver.
#external prev_end(X,Y) : square(X,Y).

#show visit/3.

#program subboard(bx,by,offset).
% bx,by are 1-based indices of the subboard in a 2x2 tiling (values 1..2)
% offset is the global step offset for this subboard (number of already visited squares)

% Local coordinates inside a subboard: lx,ly in 1..sub
local_lx(1..sub).
local_ly(1..sub).

% Generate the global squares that belong to this subboard
local_square(XG,YG) :- local_lx(LX), local_ly(LY), XG = (bx - 1) * sub + LX, YG = (by - 1) * sub + LY.

% Subboard internal steps (1..sub*sub), and map to global steps G = offset + S
substep(1..sub*sub).
global_step(G) :- substep(S), G = offset + S.

% Exactly one sub_visit per global step inside this subboard: choose one local square for each global step
{ sub_visit(XG,YG,G) : local_square(XG,YG) } = 1 :- global_step(G).

% Each local square must be visited at least once (within the subboard)
:- local_square(XG,YG), not sub_visit(XG,YG,_).
% No square visited more than once within the subboard
:- sub_visit(X,Y,Z1), sub_visit(X,Y,Z2), Z1 != Z2.

% Do not allow visiting squares that were fixed by previous subboards
:- fixed(X,Y), local_square(X,Y), sub_visit(X,Y,_).

% Moves must be legal between consecutive global steps inside the subboard
:- sub_visit(X1,Y1,G1), sub_visit(X2,Y2,G2), G2 = G1 + 1, not move(X1,Y1,X2,Y2).

% If a prev_end is provided, require that the first step of this subboard (offset+1) is reachable from it.
has_prev_end :- prev_end(_, _).
reachable_from_prev(X,Y) :- prev_end(PX,PY), move(PX,PY,X,Y).
:- has_prev_end, sub_visit(X,Y,Gfirst), Gfirst = offset + 1, not reachable_from_prev(X,Y).

% The subboard program defines sub_visit atoms for its range; the driver converts them to global visit/3 facts.
#show sub_visit/3.
