#const n = 5. % size of the chessboard n x n
cell(X,Y) :- X = 1..n, Y = 1..n.

% generate knight moves (8 offsets)
% needs refactoring to 2 rules
knight(X,Y,U,V) :- cell(X,Y), U = X+1, V = Y+2, cell(U,V).
knight(X,Y,U,V) :- cell(X,Y), U = X+2, V = Y+1, cell(U,V).
knight(X,Y,U,V) :- cell(X,Y), U = X-1, V = Y+2, cell(U,V).
knight(X,Y,U,V) :- cell(X,Y), U = X-2, V = Y+1, cell(U,V).
knight(X,Y,U,V) :- cell(X,Y), U = X+1, V = Y-2, cell(U,V).
knight(X,Y,U,V) :- cell(X,Y), U = X+2, V = Y-1, cell(U,V).
knight(X,Y,U,V) :- cell(X,Y), U = X-1, V = Y-2, cell(U,V).
knight(X,Y,U,V) :- cell(X,Y), U = X-2, V = Y-1, cell(U,V).

#program base.
#const start_x = 1.
#const start_y = 1.

% starting position at time 0
pos(start_x, start_y, 0).

% forbid visiting the same cell at two different times
:- pos(X,Y,T1), pos(X,Y,T2), T1 != T2.

#show pos/3.

#program step(k).
% Choose exactly one reachable position at time k based on time k-1
1 { pos(U,V,k) : knight(X,Y,U,V), pos(X,Y,k-1) } 1.
