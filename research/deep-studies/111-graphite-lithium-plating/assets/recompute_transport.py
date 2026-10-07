#!/usr/bin/env python3
"""Original mass-conserving two-compartment transport illustration.
No physical battery fit, operating parameters, or charging instructions.
Time and inventory units are arbitrary. Stops when surface compartment reaches 1.
Does NOT simulate lithium plating, electrode potentials, nucleation, SEI or graphite phases.
"""
from math import exp,isclose
from pathlib import Path
import json
P=Path(__file__).resolve().parent
v=.2;q=.5
# v: surface region capacity fraction; q: added inventory per arbitrary time.
def state(t,k):
 mean=q*t;delta=q*(1-v)/k*(1-exp(-k/(v*(1-v))*t))
 return mean+(1-v)*delta,mean-v*delta,mean
rows=[];series={}
for k,label in [(.2,'内部转移慢'),(2.,'内部转移快')]:
 lo,hi=0.,1/q
 for _ in range(70):
  mid=(lo+hi)/2
  if state(mid,k)[0]>1:hi=mid
  else:lo=mid
 t=(lo+hi)/2;s,b,m=state(t,k)
 assert isclose(s,1,abs_tol=1e-12)
 assert isclose(v*s+(1-v)*b,m,abs_tol=1e-12)
 assert 0<=b<1
 # Independent explicit Euler check, rather than only evaluating analytic formula.
 n=100000;dt=t/n;ss=bb=0.
 for _ in range(n):
  transfer=k*(ss-bb);ss+=(q-transfer)/v*dt;bb+=transfer/(1-v)*dt
 assert abs(ss-s)<1e-5 and abs(bb-b)<1e-5
 rows.append(dict(label=label,k=k,surface_full_time_arbitrary=t,surface_occupancy=s,bulk_occupancy=b,mean_occupancy=m,euler_surface=ss,euler_bulk=bb))
 series[label]=[state(t*i/100,k) for i in range(101)]
result=dict(scope='Mass-transport toy, not an electrochemical model or plating prediction',surface_capacity_fraction=v,interior_capacity_fraction=1-v,inflow_per_arbitrary_time=q,cases=rows,warning='The endpoint means this toy surface compartment is full; it is not a predicted lithium-plating threshold.')
(P/'transport-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
# Show both compartments and their weighted means without presenting them as lab measurements.
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="620" viewBox="0 0 1120 620" role="img" aria-label="两区运输教学模型：表层只有总容量的20%；表层达到模型上限时，整片平均仍可能较低"><rect width="1120" height="620" fill="#faf8f2"/><g font-family="Noto Sans CJK SC,sans-serif" fill="#263e48"><text x="38" y="44" font-size="26">表层先达到上限，不等于整体已经装满</text><text x="38" y="79" font-size="17">原创两区模型：表层占总容量20%，内部占80%；只改变两区间的转移速度</text>']
for i,row in enumerate(rows):
 y=135+i*205;fill=row['bulk_occupancy'];mean=row['mean_occupancy']
 s += [f'<text x="40" y="{y}" font-size="21">{row["label"]}</text>',f'<rect x="210" y="{y-22}" width="150" height="125" fill="#cd834a"/><text x="285" y="{y+26}" font-size="18" text-anchor="middle">表层</text><text x="285" y="{y+62}" font-size="24" text-anchor="middle">100%</text>',f'<rect x="380" y="{y-22}" width="600" height="125" fill="#e8eeeb" stroke="#9bacac"/><rect x="380" y="{y-22+125*(1-fill):.2f}" width="600" height="{125*fill:.2f}" fill="#acd7d5"/><text x="680" y="{y+26}" font-size="18" text-anchor="middle">内部</text><text x="680" y="{y+62}" font-size="24" text-anchor="middle">{fill*100:.1f}%</text>',f'<text x="210" y="{y+141}" font-size="19">整体平均 = 20% × 100% + 80% × {fill*100:.1f}% = {mean*100:.1f}%</text>']
s+=['<text x="38" y="565" font-size="17">面积表示各区容量，填色高度表示占用率。两行分别画到自己的表层达到100%的时刻。</text>','<text x="38" y="598" font-size="16" fill="#61747c">这不是电池实测，也不把“表层100%”当通用析锂阈值；实际反应还受电位、成核与相变等影响。</text></g></svg>']
(P/'surface-before-average.svg').write_text(''.join(s));print(json.dumps(result,ensure_ascii=False,indent=2))
