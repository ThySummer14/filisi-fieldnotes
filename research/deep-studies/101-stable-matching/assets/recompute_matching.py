"""Deterministic teaching example, standard library only; not real admissions data."""
from itertools import permutations
import json
S={'甲':['X','Y','Z'],'乙':['Y','X','Z'],'丙':['X','Y','Z']}
L={'X':['乙','甲','丙'],'Y':['甲','乙','丙'],'Z':['甲','乙','丙']}
def da(p,q):
 nxt={a:0 for a in p}; held={}; waiting=list(p); trace=[]
 while waiting:
  a=waiting.pop(0); b=p[a][nxt[a]]; nxt[a]+=1; old=held.get(b)
  if old is None or q[b].index(a)<q[b].index(old):
   held[b]=a
   if old is not None: waiting.append(old)
  else: waiting.append(a)
  trace.append({'proposal':[a,b],'held':held.copy()})
 return {a:b for b,a in held.items()},trace
def blocks(m):
 inv={v:k for k,v in m.items()}
 return [(a,b) for a in S for b in L if m[a]!=b and S[a].index(b)<S[a].index(m[a]) and L[b].index(a)<L[b].index(inv[b])]
allm=[dict(zip(S,perm)) for perm in permutations(L)]
lie={**L,'X':['乙','丙','甲']}
out={'all_matchings':[{'matching':m,'blocking_pairs':blocks(m)} for m in allm], 'student_proposing':da(S,L),'lab_proposing':da(L,S),'X_misreport':da(S,lie)}
assert len([m for m in allm if not blocks(m)])==2
assert da(S,L)[0]=={'甲':'X','乙':'Y','丙':'Z'}
assert da(S,lie)[0]=={'乙':'X','甲':'Y','丙':'Z'}
print(json.dumps(out,ensure_ascii=False,indent=2))
