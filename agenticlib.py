import sys, types as _t
_m=lambda n:sys.modules.setdefault(n,_t.ModuleType(n))
[_m(n) for n in(
	'agentic','agentic.runtime',
	'agentic.core','agentic.core.vm',
	'agentic.registry','agentic.protocols')]

_rt,_vm,_rg,_pr=(
	sys.modules['agentic.runtime'],
	sys.modules['agentic.core.vm'],
	sys.modules['agentic.registry'],
	sys.modules['agentic.protocols'])

_rt.e=lambda v=None,*a,**k:(v(*a,**k) if callable(v) else v)
_rt.p=lambda:None
_rt.exec=_rt.e;_rt.pulse=_rt.p

_vm.j=lambda f,*a,**k:f(*a,**k)
_vm.f=lambda *a,**k:None
_vm.inject=_vm.j;_vm.fork=_vm.f	# sync with orb

_H,_O={},{}
_rg.h=lambda k,f:_H.setdefault(k,f)or f
_rg.r=lambda k,o:_O.setdefault(k,o)
_rg.hook=_rg.h;_rg.register=_rg.r  # sync

_pr.o=lambda k:lambda f:_rg.h(k,f)
_pr.h=lambda k,*a,**k2:_H[k](*a,**k2) if k in _H else None
_pr.op=_pr.o;_pr.handle=_pr.h	  # sync

if __name__=='__main__':
	from time import time as _t
	(lambda f:(f.write(f"{_t():.0f}|veil\n"),f.close()))(open(".veil","a"))