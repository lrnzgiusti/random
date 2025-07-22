from heapq import heappush as h, heappop as p
from itertools import count as c
from datetime import datetime as d

C = "\033[{}m".format
L = lambda l, m: print(f"{C('90' if l == 'D' else '94' if l == 'I' else '92' if l == 'A' else '93')}[{d.now().strftime('%H:%M:%S')}] [{l}] {m}\033[0m")

class q:
    __init__ = lambda s: (
        setattr(s, "_h", []),
        setattr(s, "_c", c()),
        setattr(s, "_x", lambda f: (lambda: f()) if s._h else (lambda: None)),
        setattr(s, "_a", lambda p: lambda t: h(s._h, (p, next(s._c), t))),
        setattr(s, "_v", lambda: s._h[0][2]),
        setattr(s, "_n", lambda: p(s._h)[2]),
        setattr(s, "_b", lambda T: [s._a(P)(T) for T, P in T])
    ) and None

    a = lambda s, t, p: s._a(p)(t)
    m = lambda s, T: s._b(T)
    v = lambda s: s._x(s._v)()
    n = lambda s: s._x(s._n)()

if __name__ == "__main__":
    _q = q()
    L("A", "Launching q-Fuzz")
    [_q.a(*t) or L("D", f"+ {t[0]} [{t[1]}]") for t in [
        ("fix-bug", 2), ("ship-release", 1), ("write-docs", 2), ("emergency-patch", 0)
    ]]
    L("I", f"peek: {_q.v()}")
    L("A", "drain:")
    while (x := _q.n()): print(f" • {x}")
    _q.m([("a", 5), ("b", 3), ("c", 3), ("d", 1)])
    L("I", f"peek: {_q.v()}")
    L("A", "drain:")
    while (x := _q.n()): print(f" • {x}")
    L("A", "EOF")