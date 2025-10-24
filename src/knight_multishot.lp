% Board size
#const n = 10.

% Board
square(1..n, 1..n).
subsquare_ul(1..n/2, 1..n/2).
subsquare_ur(n/2+1..n, 1..n/2).
subsquare_ll(1..n/2, n/2+1..n).
subsquare_lr(n/2+1..n, n/2+1..n).

% Knight moves
move(X1,Y1,X2,Y2) :- square_ul(X1,Y1), square_ul(X2,Y2), 1 = |X1-X2|, 2 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square_ul(X1,Y1), square_ul(X2,Y2), 2 = |X1-X2|, 1 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square_ur(X1,Y1), square_ur(X2,Y2), 1 = |X1-X2|, 2 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square_ur(X1,Y1), square_ur(X2,Y2), 2 = |X1-X2|, 1 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square_ll(X1,Y1), square_ll(X2,Y2), 1 = |X1-X2|, 2 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square_ll(X1,Y1), square_ll(X2,Y2), 2 = |X1-X2|, 1 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square_lr(X1,Y1), square_lr(X2,Y2), 1 = |X1-X2|, 2 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square_lr(X1,Y1), square_lr(X2,Y2), 2 = |X1-X2|, 1 = |Y1-Y2|.

% Steps
step(1..n*n).
substep(1..(n*n)/4).

% fixed positions
visit(5,4,1).
visit(4,5,25).
visit(6,4,26).
visit(7,5,50).
visit(6,7,51).
visit(7,6,75).
visit(5,7,76).
visit(4,6,100).

% For each step > 1, the knight must move from the previous square to a new square via a legal knight move.
% The choice rule ensures exactly one move is made at each step.
{ visit(X2,Y2,Z2) : visit(X1,Y1,Z1), move(X1,Y1,X2,Y2), Z2 = Z1 + 1 } = 1 :- step(Z2), Z2 > 1.
:- square(X,Y), not visit(X,Y,_).

% Constraint: no square may be visited more than once.
:- visit(X,Y,Z1), visit(X,Y,Z2), Z1 != Z2.


#show visit/3.
