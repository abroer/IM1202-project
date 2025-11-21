#program base.
% Global board size
#const n = 10.

#program base.
% Board
square(1..n, 1..n).

% Knight moves
move(X1,Y1,X2,Y2) :- square(X1,Y1), square(X2,Y2), 1 = |X1-X2|, 2 = |Y1-Y2|.
move(X1,Y1,X2,Y2) :- square(X1,Y1), square(X2,Y2), 2 = |X1-X2|, 1 = |Y1-Y2|.


% For each step > 1, the knight must move from the previous square to a new square via a legal knight move.
% The choice rule ensures exactly one move is made at each step.
{ visit(X2,Y2,Z2) : visit(X1,Y1,Z1), move(X1,Y1,X2,Y2), Z2 = Z1 + 1 } = 1 :- step(Z2), Z2 > 1.

% Constraint: no square may be visited more than once.
:- visit(X,Y,Z1), visit(X,Y,Z2), Z1 != Z2.
:- square(X,Y), not visit(X,Y,_).

#program sub_knight(x0, y0, size, start_x, start_y, end_x, end_y).
% define the subboard
sub_square(X,Y) :- square(X,Y), X >= x0, X < x0 + size, Y >= y0, Y < y0 + size.

% Steps
step(1..size*size).

% Initial position at step 1 and end position at step size*size
visit(start_x, start_y, 1).
visit(end_x, end_y, size*size).



#show visit/3.
