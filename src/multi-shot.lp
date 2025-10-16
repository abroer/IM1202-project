a(1).
#program acid(k).
b(k).
c(X,k) :- a(X).
#program base.
a(2).
#script(python)
from clingo import Number
def main(prg):
  prg.ground([("acid",[Number(42)])])
  prg.solve()
#end.