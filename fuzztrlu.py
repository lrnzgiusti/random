# state: {'cap':int, 'm':{(t,i):v}, 'l':[keys LRU-old..new], 't':[keys sorted], 'i':int_seq}
from time import time as _t
new  = lambda cap=128: {'cap': cap, 'm': {}, 'l': [], 't': [], 'i': 0}

# helpers
upd      = lambda s, **kw: (lambda d={**s, **kw}: d)()
touch    = lambda l, k: (lambda nl=[x for x in l if x != k]: nl + [k])()   # <-- called
remove1  = lambda a, x: (lambda i=(a.index(x) if (x in a) else None): (a[:i]+a[i+1:] if i is not None else a))()  # <-- called

# right-bisect
bs_right = None
bs_right = lambda a, k, lo=0, hi=None: (
    (lambda H=(len(a) if hi is None else hi):
        (lo if lo==H else
         (lambda mid=(lo+H)//2:
             (bs_right(a,k,mid+1,H) if a[mid] <= k else bs_right(a,k,lo,mid))
         )())
    )()
)

ins      = lambda a, k: (lambda i=bs_right(a, k): a[:i] + [k] + a[i:])()   # <-- called
mkkey    = lambda s, t: (lambda ts=(float(s['i']+1) if t is None else float(t)): (ts, s['i']+1))()  # <-- called

evict1   = lambda s: (
    (lambda k=s['l'][0]:
        upd(s,
            m=dict((kk,v) for kk,v in s['m'].items() if kk != k),
            l=s['l'][1:],
            t=remove1(s['t'], k)
        )
    )()
)

trim     = None
trim     = lambda s: (s if len(s['m']) <= s['cap'] else trim(evict1(s)))

# API
a = lambda s, v: (
    (lambda k_i=mkkey(s, float(_t())):
        (lambda k=k_i[0:2]:
            trim(
                upd(s,
                    m={**s['m'], k: v},
                    l=touch(s['l'], k),
                    t=ins(s['t'], k),
                    i=k[1]
                )
            )
        )()
    )()
)

g = lambda s: (
    (lambda idx=bs_right(s['t'], (float(_t()), 10**18)) - 1:
        ((s, None) if idx < 0 else
         (lambda k=s['t'][idx]:
             (upd(s, l=touch(s['l'], k)), (k[0], s['m'][k]))
         )()
        )
    )()
)

# help
keys    = lambda s: [k[0] for k in s['t']]
newest  = lambda s: (None if not s['t'] else (lambda k=s['t'][-1]: (k[0], s['m'][k]))())
oldest  = lambda s: (None if not s['t'] else (lambda k=s['t'][0] : (k[0], s['m'][k]))())
length  = lambda s: len(s['m'])

# demo
if __name__ == "__main__":
    s = new(3)
    s  = a(s,  "a")
    s  = a(s, "b")
    s  = a(s, "c")
    print("[I] len=", length(s), " newest=", newest(s))
    s, out = g(s); print("[Q] g(t0+2.5) =>", out)   # touches b
    s  = a(s,"d")                                    # evicts a
    print("[I] after add d, len=", length(s), " keys=", keys(s))
    s, out = g(s);  print("[Q] g(t0+10)  =>", out)
    s, out = g(s); print("[Q] g(t0+1.0) =>", out)
    print(); print(s)
