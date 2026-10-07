"""Synthetic closed-system and single-Pb-loss illustration; Ga units."""
from math import log,exp
from pathlib import Path
import json
base=Path(__file__).resolve().parent
l8=log(2)/4.468;l5=log(2)/.7038
point=lambda t:(exp(l8*t)-1,exp(l5*t)-1)
a,b=point(1),point(.2);rows=[]
for f in [1,.75,.5,.25,0]:
 x,y=[f*u+(1-f)*v for u,v in zip(a,b)]
 rows.append(dict(old_Pb_retained=f,x=x,y=y,t238_Ga=log(1+x)/l8,t235_Ga=log(1+y)/l5))
assert abs(rows[0]['t238_Ga']-1)<1e-12 and abs(rows[-1]['t235_Ga']-.2)<1e-12
(base/'zircon-recomputed.json').write_text(json.dumps({'half_life_Ga':[4.468,.7038],'assumptions':['no initial daughter','U retained','single instantaneous equal-fraction Pb loss at 0.2 Ga','formed at 1 Ga','closed after loss'],'rows':rows},indent=2))
X=lambda x:80+x/.21*640;Y=lambda y:430-y/2.3*350
curve=' '.join(f'{X(x):.2f},{Y(y):.2f}' for x,y in [point(i/100) for i in range(121)])
s=['<svg xmlns="http://www.w3.org/2000/svg" width="820" height="530" viewBox="0 0 820 530"><rect width="820" height="530" fill="#fffdf7"/><g font-family="Noto Sans CJK SC, sans-serif" fill="#263445"><text x="80" y="38" font-size="24">两只钟，一次假想的失铅事件</text><text x="80" y="62" font-size="14">教学模型：不是实测样品；未画测量误差椭圆</text><path d="M80 80 V430 H730" fill="none" stroke="#263445"/>']
for x in [0,.05,.1,.15,.2]:s.append(f'<text x="{X(x)-12}" y="453" font-size="12">{x}</text>')
for y in [0,.5,1,1.5,2]:s.append(f'<text x="48" y="{Y(y)+4}" font-size="12">{y}</text>')
s.append(f'<polyline points="{curve}" fill="none" stroke="#236ca4" stroke-width="3"/><line x1="{X(a[0])}" y1="{Y(a[1])}" x2="{X(b[0])}" y2="{Y(b[1])}" stroke="#b76c2c" stroke-width="3"/>')
for r in rows:s.append(f'<circle cx="{X(r["x"])}" cy="{Y(r["y"])}" r="5" fill="#b76c2c"/><text x="{X(r["x"])+10}" y="{Y(r["y"])-5}" font-size="13">{int(r["old_Pb_retained"]*100)}%</text>')
s.append('<text x="285" y="485" font-size="16">206Pb* / 238U</text><text transform="translate(24 325) rotate(-90)" font-size="16">207Pb* / 235U</text><text x="490" y="110" font-size="14" fill="#236ca4">谐和曲线</text><text x="80" y="514" font-size="13">百分比：扰动前已形成的放射成因铅，后来保留了多少</text></g></svg>')
(base/'zircon-concordia.svg').write_text(''.join(s))
print('wrote table and original SVG')
