#!/usr/bin/env python3
"""Original ideal-solution teaching model; Python 3 standard library only.
Assumptions: initial feed volume 1 m^3, perfect salt retention, pure product,
constant temperature/volume additivity, osmotic pressure proportional to concentration.
Not a plant simulator, seawater-property model, or equipment operating guide.
Run: python recompute_osmosis.py ; writes results and original SVG beside this file.
"""
from math import log,isclose
from pathlib import Path
import json
p=Path(__file__).resolve().parent
pi0_bar=25.0
bar_m3_to_kwh=1e5/3.6e6
rows=[]
for r in [.1,.5,.75]:
 least=pi0_bar*(-log(1-r))/r*bar_m3_to_kwh
 n=10000;step=r/n
 numeric=sum(pi0_bar/(1-(i+.5)*step)*step for i in range(n))/r*bar_m3_to_kwh
 assert isclose(least,numeric,rel_tol=1e-8)
 rows.append(dict(recovery=r,end_osmotic_bar=pi0_bar/(1-r),least_kwh_per_m3_product=least,midpoint_10000_steps=numeric))
r=.5;P=pi0_bar/(1-r)
pump=P*bar_m3_to_kwh;recovered=P*(1-r)*bar_m3_to_kwh
fixed_net=(pump-recovered)/r
no_recovery=pump/r
least_half=rows[1]['least_kwh_per_m3_product']
assert no_recovery>fixed_net>least_half>0
midpoints=[(i+.5)*.1 for i in range(5)]
pressures=[pi0_bar/(1-x) for x in midpoints]
local=[dict(A_l_m2_h_bar=a,J_l_m2_h=20,delta_pi_bar=25,delta_P_bar=25+20/a) for a in [1,3,1000000]]
result=dict(description='Original teaching calculation, not measured plant performance',assumptions=['1 m^3 initial feed','pure permeate','perfect salt retention','constant temperature','osmotic pressure proportional to concentration'],bar_m3_to_kwh=bar_m3_to_kwh,recovery_comparison=rows,local_flux_example=local,half_recovery=dict(feed_m3=1,product_m3=.5,brine_m3=.5,constant_pressure_bar=P,gross_pump_kwh=pump,ideal_brine_recovery_kwh=recovered,net_kwh=pump-recovered,without_ERD_kwh_per_m3_product=no_recovery,with_ideal_ERD_kwh_per_m3_product=fixed_net,reversible_kwh_per_m3_product=least_half),five_segment_midpoint=dict(midpoint_recovery=midpoints,pressure_bar=pressures,kwh_per_m3_product=sum(v*.1 for v in pressures)/r*bar_m3_to_kwh))
(p/'osmosis-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
# Geometric area is pressure times extracted volume (initial feed is 1 m^3).
x=lambda r:90+1060*r
y=lambda pressure:495-6.7*pressure
points=[(x(i*.5/120),y(pi0_bar/(1-i*.5/120))) for i in range(121)]
curve=' '.join(f'{a:.2f},{b:.2f}' for a,b in points)
area=f'{x(0):.2f},{y(0):.2f} '+curve+f' {x(.5):.2f},{y(0):.2f}'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="710" viewBox="0 0 1120 710" role="img" aria-label="原创理想模型：渗透压从25巴随取水升到50巴；渐增加压的最低功小于全程50巴"><rect width="1120" height="710" fill="#faf8f2"/><g font-family="Noto Sans CJK SC, sans-serif" fill="#243e48">', '<text x="40" y="42" font-size="27">后半程的水，为什么更费力</text>','<text x="40" y="76" font-size="18">原创教学模型：1立方米进水，初始渗透压25巴，最终取得0.5立方米淡水</text>']
s+=[f'<rect x="{x(0)}" y="{y(50)}" width="{x(.5)-x(0)}" height="{y(0)-y(50)}" fill="#eddfcf"/>',f'<polygon points="{area}" fill="#bcdedc"/>']
for t in [0,10,20,30,40,50]:
 s+=[f'<path d="M{x(0)} {y(t)} H{x(.5)}" stroke="#d7dddb"/><text x="74" y="{y(t)+5}" text-anchor="end" font-size="15">{t}</text>']
s+=[f'<path d="M{x(0)} {y(0)} H{x(.5)} M{x(0)} {y(0)} V{y(56)}" fill="none" stroke="#516c76"/>',f'<polyline points="{curve}" fill="none" stroke="#177d84" stroke-width="4"/>',f'<path d="M{x(0)} {y(50)} H{x(.5)}" stroke="#af7042" stroke-width="3" stroke-dasharray="8 6"/>','<text x="42" y="112" font-size="18">压力（巴）</text>','<text x="182" y="139" font-size="17" fill="#995d32">全程按末端50巴加压</text>','<text x="254" y="394" font-size="17" fill="#166971">按当时渗透压逐渐增加压力</text>']
for t in [0,.1,.2,.3,.4,.5]:
 s+=[f'<path d="M{x(t)} {y(0)} v7" stroke="#516c76"/><text x="{x(t)}" y="524" font-size="16" text-anchor="middle">{round(t*100)}%</text>']
s+=['<text x="270" y="559" font-size="18">已取出的淡水占原水比例</text>','<text x="685" y="150" font-size="21">每立方米产水的功</text>','<text x="685" y="184" font-size="16" fill="#61747c">千瓦时/立方米；所有数值来自同一模型</text>']
for yy,label,val,col in [(243,'固定压力，直接泄压',no_recovery,'#815146'),(332,'固定压力，理想回收压力能',fixed_net,'#a76a3e'),(421,'随渗透压渐增，可逆极限',least_half,'#177d84')]:
 s+=[f'<text x="685" y="{yy}" font-size="18">{label}</text><text x="685" y="{yy+36}" font-size="28" fill="{col}">{val:.3f}</text>']
s+=['<text x="40" y="606" font-size="17">蓝色面积：渐增加压所需的功。橙色多出的面积：理想回收压力后，全程高压仍多付的功。</text>','<text x="40" y="638" font-size="16" fill="#61747c">比例乘1立方米得到取水量；面积给总功，再除0.5立方米产水，得到右侧数值。</text>','<text x="40" y="675" font-size="16" fill="#61747c">固定压力比较取极限值50巴；实际持续出水须略高。未计泵损失、浓差极化及预处理等。</text>','</g></svg>']
(p/'osmotic-work.svg').write_text(''.join(s))
print(json.dumps(result,ensure_ascii=False,indent=2))
