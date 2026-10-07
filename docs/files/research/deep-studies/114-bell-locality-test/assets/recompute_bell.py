#!/usr/bin/env python3
"""Recompute CHSH teaching examples with Python 3 standard library only.
No network access. Usage: python3 recompute_bell.py [optional-output-json]
All experimental counts are manually transcribed from Hensen 2015 Fig. 4a;
this is a check of published aggregates, not a raw-timestamp reanalysis.
"""
from itertools import product
from collections import Counter
from fractions import Fraction
from math import comb, sqrt, fsum
from pathlib import Path
import json
import sys

SETTINGS = [(0, 0), (0, 1), (1, 0), (1, 1)]
strategies = []
for answers in product((0, 1), repeat=4):
    a0, a1, b0, b1 = answers
    a, b = (a0, a1), (b0, b1)
    wins = [int((a[u] ^ b[v]) == u * v) for u, v in SETTINGS]
    strategies.append({'A0': a0, 'A1': a1, 'B0': b0, 'B1': b1,
                       'wins_00_01_10_11': wins, 'wins_of_four': sum(wins)})
assert len(strategies) == 16
assert Counter(s['wins_of_four'] for s in strategies) == {1: 8, 3: 8}

# Same-sign and opposite-sign output counts, in setting order 00,01,10,11.
COUNTS = [(46, 7), (63, 16), (46, 16), (10, 41)]
correlations = [Fraction(same-opp, same+opp) for same,opp in COUNTS]
s = correlations[0] + correlations[1] + correlations[2] - correlations[3]
n = sum(same+opp for same,opp in COUNTS)
k = sum(COUNTS[i][0] if i < 3 else COUNTS[i][1] for i in range(4))
assert (n,k) == (245,196)
se = sqrt(fsum((1-float(e)**2)/sum(c) for e,c in zip(correlations,COUNTS)))
i_value = 8 * (Fraction(k,n)-Fraction(1,2))

def binomial_upper_tail(n,k,p):
    return fsum(comb(n,j)*p**j*(1-p)**(n-j) for j in range(k,n+1))

tau = 1.08e-5
# Hensen 2015 Supplementary Information, equations (7)-(8).
xi_original = .75 + 3*(tau + tau*tau)
# Elkouss & Wehner arXiv:1510.07233v3, Lemma 1, sharper later bound.
xi_later = .75 + tau - tau*tau

# Ideal quantum joint probabilities: E=+1/sqrt(2) in first 3 settings,
# E=-1/sqrt(2) in setting 11; each local marginal is exactly one-half.
quantum = []
for u,v in SETTINGS:
    e = (1 if (u,v)!=(1,1) else -1)/sqrt(2)
    joint = [{'A':a,'B':b,'probability':(1+a*b*e)/4}
             for a,b in product((-1,1),repeat=2)]
    assert abs(fsum(x['probability'] for x in joint)-1)<1e-12
    for answer in (-1,1):
        assert abs(fsum(x['probability'] for x in joint if x['A']==answer)-.5)<1e-12
        assert abs(fsum(x['probability'] for x in joint if x['B']==answer)-.5)<1e-12
    quantum.append({'settings':[u,v],'E':e,'joint':joint,
                    'A_plus_marginal':.5,'B_plus_marginal':.5})

out = {
 'description':'Original teaching computations and verification of published aggregate counts',
 'settings_order':['00','01','10','11'],
 'classical_strategies':strategies,
 'classical_score_histogram':dict(sorted(Counter(s['wins_of_four'] for s in strategies).items())),
 'classical_uniform_input_win_probability_bound':.75,
 'published_aggregate_source':'https://arxiv.org/pdf/1508.05949 (page 6, Fig. 4a)',
 'hensen_2015': {
  'same_opposite_counts':COUNTS,'setting_totals':[sum(c) for c in COUNTS],
  'correlations':[float(e) for e in correlations],
  'S_exact':str(s),'S':float(s),'conventional_standard_error':se,
  'n':n,'wins':k,'win_fraction':k/n,'I':float(i_value),
  'perfect_inputs_tail':binomial_upper_tail(n,k,.75),
  'tau':tau,'xi_original_2015':xi_original,
  'original_2015_tail_bound':binomial_upper_tail(n,k,xi_original),
  'xi_later_sharper_bound':xi_later,
  'later_sharper_tail_bound':binomial_upper_tail(n,k,xi_later),
  'note':'All tail values round to 0.039 at three decimal places; original and later bounds are not interchangeable derivations.'
 },
 'ideal_quantum':{'S':2*sqrt(2),'uniform_input_win_probability':(2+sqrt(2))/4,'settings':quantum},
 'timing_simplified':{'distance_m':1280,'c_m_s':299792458,
  'light_travel_us':1280/299792458*1e6,
  'basis_choice_to_readout_start_us':.480,'readout_duration_us':3.7,
  'total_us':4.18,'nominal_margin_ns':(1280/299792458*1e6-4.18)*1e3,
  'note':'Diagram uses synchronized start times as an explicitly simplified reconstruction, not raw event timestamps; reported distance is rounded.'},
 'limitations':['No individual raw experimental time tags were downloaded or reprocessed.',
  'Binomial tails are applicable as proven bounds for history-dependent local models under the stated setting-independence/predictability and sample-size conditions.',
  'No stopping-rule audit or independent device calibration is claimed.']
}
p = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('bell-results.json')
p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'strategies':len(strategies),'histogram':out['classical_score_histogram'],
                 'S':float(s),'standard_error':se,'wins':k,'n':n,
                 'original_p_bound':out['hensen_2015']['original_2015_tail_bound']},ensure_ascii=False))

# Original SVG figures. Raster PNGs in this package are exports of these SVGs.
# The numerical recomputation and SVG generation require only the standard library.
from html import escape
D = Path(__file__).parent

def text_svg(x,y,t,size=22,fill='#17333d',anchor='start',weight='400'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(t))}</text>'

def svg_start(w,h,title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>',
            '<rect width="100%" height="100%" fill="#f7f4ee"/>',
            '<g font-family="Noto Sans CJK SC, sans-serif">']

v=svg_start(1060,1180,'CHSH全部16种确定策略，每种赢一题或三题')
v += [text_svg(52,65,'16种纸条，最多赢四题中的三题',32,weight='700'),
      text_svg(52,108,'左侧：预先写好的四个答案   右侧：分别遇到四种设置时的输赢',20)]
xs=[92,172,252,332,485,605,725,845,976]
for x,t in zip(xs,['A₀','A₁','B₀','B₁','00','01','10','11','赢几题']):
    v.append(text_svg(x,175,t,24,anchor='middle',weight='700'))
v.append(text_svg(665,140,'设置组合',18,anchor='middle'))
for j,s in enumerate(strategies):
    yy=198+j*51
    bg='#ffffff' if j%2==0 else '#ece9e2'
    v.append(f'<rect x="52" y="{yy}" width="962" height="50" rx="5" fill="{bg}"/>')
    for x,k0 in zip(xs[:4],['A0','A1','B0','B1']): v.append(text_svg(x,yy+34,s[k0],24,anchor='middle'))
    for x,w in zip(xs[4:8],s['wins_00_01_10_11']):
        color='#176a61' if w else '#b45438'
        v.append(f'<rect x="{x-30}" y="{yy+7}" width="60" height="36" rx="6" fill="{color}"/>')
        v.append(text_svg(x,yy+33,'赢' if w else '输',22,'#ffffff','middle'))
    v.append(text_svg(xs[-1],yy+34,s['wins_of_four'],24,anchor='middle',weight='700'))
v += [text_svg(52,1060,'8种赢三题，8种赢一题。均匀抽题时，任何混合策略的胜率都不超过75%。',21),
      text_svg(52,1102,'每轮只问一种设置；这张表是枚举全部可能的局域确定策略。',20),
      text_svg(52,1141,'原创计算与绘图；标准库脚本 recompute_bell.py 可重新生成。',18,fill='#51656a'),'</g></svg>']
(D/'chsh-sixteen-strategies.svg').write_text('\n'.join(v),encoding='utf-8')

v=svg_start(1180,900,'1280米间距下的选设置、读出及真空光速传播时间预算')
v += [text_svg(50,60,'读出结束时，对面的光速消息还没赶到',32,weight='700'),
      text_svg(50,103,'简化重画甲乙时间预算：两端起点对齐；不包含C站，不是原始事件时间戳。',21)]
xa,xb,y0,scale=220,860,690,110
Y=lambda t:y0-scale*t
light=out['timing_simplified']['light_travel_us']
for t in range(6):
    yy=Y(t)
    v.append(f'<line x1="170" y1="{yy}" x2="880" y2="{yy}" stroke="#d8dfde" stroke-width="1"/>')
    v.append(text_svg(148,yy+7,str(t),20,anchor='end'))
v.append(text_svg(80,140,'时间',21));v.append(text_svg(80,168,'微秒',18))
v.append(f'<line x1="170" y1="{Y(5)}" x2="170" y2="{y0}" stroke="#48616b" stroke-width="2"/>')
v.append(f'<line x1="170" y1="{y0}" x2="880" y2="{y0}" stroke="#48616b" stroke-width="2"/>')
for x,lab in [(xa,'甲：0米'),(xb,'乙：1280米')]:
    v.append(f'<line x1="{x}" y1="{Y(5)}" x2="{x}" y2="{y0}" stroke="#bbceca" stroke-width="2"/>')
    v.append(f'<line x1="{x}" y1="{Y(.48)}" x2="{x}" y2="{y0}" stroke="#d18932" stroke-width="15"/>')
    v.append(f'<line x1="{x}" y1="{Y(4.18)}" x2="{x}" y2="{Y(.48)}" stroke="#176a61" stroke-width="15"/>')
    v.append(f'<circle cx="{x}" cy="{Y(4.18)}" r="6" fill="#17333d"/>')
    v.append(text_svg(x,732,lab,23,anchor='middle',weight='700'))
for a,b in [(xa,xb),(xb,xa)]:
    v.append(f'<line x1="{a}" y1="{y0}" x2="{b}" y2="{Y(light)}" stroke="#ab623d" stroke-width="3" stroke-dasharray="8 6"/>')
    v.append(f'<circle cx="{b}" cy="{Y(light)}" r="5" fill="#ab623d"/>')
v += [text_svg(535,401,'光速信号',21,'#8e4b2a','middle'),
      text_svg(270,450,'读出：3.7微秒',21,'#176a61'),
      text_svg(340,663,'选设置、切换及旋转：0.48微秒',19,'#8b5a1f')]
v.append(f'<polyline points="{xb},{Y(light)} 897,190 915,190" fill="none" stroke="#ab623d" stroke-width="1.5"/>')
v.append(text_svg(925,185,'光到达',19,'#8e4b2a'));v.append(text_svg(925,213,'≈4.270微秒',20,'#8e4b2a'))
v.append(f'<polyline points="{xb},{Y(4.18)} 897,275 915,275" fill="none" stroke="#176a61" stroke-width="1.5"/>')
v.append(text_svg(925,270,'读出结束',19,'#176a61'));v.append(text_svg(925,298,'4.180微秒',20,'#176a61'))
v += [text_svg(925,353,'差约90纳秒',21,weight='700'),
      text_svg(50,804,'横纵坐标均线性。斜线斜率来自真空光速299,792,458米/秒。',21),
      text_svg(50,844,'数据：Hensen等（2015）图2及正文；距离为论文取整值，不以本图另作时序校准。',19),'</g></svg>']
(D/'chsh-spacetime.svg').write_text('\n'.join(v),encoding='utf-8')
