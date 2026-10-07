"""Exhaustive [5,2] evaluation-code examples over F7. No QR-library benchmark."""
from itertools import product,combinations
import json
codes={(a,b):tuple((a+b*x)%7 for x in range(5)) for a,b in product(range(7),repeat=2)}
def dist(a,b): return sum(x!=y for x,y in zip(a,b))
def nearest(y):
 ds={m:dist(c,y) for m,c in codes.items()};d=min(ds.values());return d,[m for m,x in ds.items() if x==d]
minimum=min(dist(a,b) for a,b in combinations(codes.values(),2)); assert minimum==4
single=0
for m,c in codes.items():
 for i in range(5):
  for v in range(7):
   if c[i]==v:continue
   y=list(c);y[i]=v;d,near=nearest(y);assert d==1 and near==[m];single+=1
erasures=0
for m,c in codes.items():
 for keep in combinations(range(5),2):
  candidates=[a for a,cc in codes.items() if all(cc[i]==c[i] for i in keep)]
  assert candidates==[m];erasures+=1
mixed=0
for m,c in codes.items():
 for erase in range(5):
  for error in range(5):
   if erase==error: continue
   for v in range(7):
    if v==c[error]: continue
    y=list(c);y[error]=v
    ds={msg:sum(cc[i]!=y[i] for i in range(5) if i!=erase) for msg,cc in codes.items()}
    best=min(ds.values()); near=[msg for msg,d in ds.items() if d==best]
    assert best==1 and near==[m];mixed+=1
ambiguous=(2,6,3,4,0);d,near=nearest(ambiguous);assert (2,3) in near and (2,4) in near and d==2
print(json.dumps({'minimum_distance':minimum,'single_error_cases_passed':single,'three_erasure_cases_passed':erasures,'one_error_one_erasure_cases_passed':mixed,'original':codes[(2,3)],'competing':codes[(2,4)],'ambiguous_received':ambiguous,'nearest_distance':d,'nearest_messages':near},indent=2))
