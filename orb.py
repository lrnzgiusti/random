import agenticlib
from agentic.runtime import exec, pulse
from agentic.core.vm import inject, fork
from agentic.registry import hook, register
from agentic.protocols import op, handle

from time import sleep as s
from collections import deque as d

class A:
	__init__ = lambda a: (
		setattr(a, "_q", d()),
		setattr(a, "_f", {})
	) and None
	b = lambda a, k, f: hook(k, f) or a._f.update({k: f})
	p = lambda a, t: inject(a._q.append, t)
	t = lambda a: (t:=a._q.popleft()) and (a._f.get(t[0], exec)(*t[1:])) if a._q else pulse()
	r = lambda a: [a.t() or s(0.01) for _ in iter(int,1)]

if __name__=="__main__":
	n=A()
	register("n",n)
	n.b("r",lambda x:print(f"p {x}")or pulse())
	n.b("x",lambda x:print(f"f {x}")or fork(x))
	n.b("l",lambda:n.p(("r","..."))or n.p(("x","step"))or n.p(("l",)))
	n.p(("l",));n.r()
