import agenticlib, subprocess as _s, sys, time as _t, pathlib as _p, random as _r

_O  = _p.Path(__file__).with_name("orb.py")
_W  = lambda *c: open(".orch","a").write(f"{_t.time():.0f}|{' '.join(map(str,c))}\n")
_N  = lambda: int(sys.argv[1]) if len(sys.argv)>1 else 3
_S  = lambda n: [_s.Popen([sys.executable,_O,str(i)]) for i in range(n)]
_K  = lambda ps: [_ for p in ps if p.poll() is None for _ in [p.terminate()]]

if __name__=="__main__":
    P=_S(_N()); _W("boot",len(P))
    try:
        while any(p.poll() is None for p in P):
            _t.sleep(_r.randint(5,9))
            if _r.random()<.12:
                P.append(_s.Popen([sys.executable,_O,"*"]))
                _W("spur",len(P))
    except KeyboardInterrupt:
        _K(P); _W("halt")
