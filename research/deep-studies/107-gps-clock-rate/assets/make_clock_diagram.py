"""Original conceptual clock-error plot. Chosen numbers are not observed GPS data."""
from math import sin,pi
from pathlib import Path
p=Path(__file__).resolve().parent
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="590" viewBox="0 0 1020 590" role="img" aria-label="钟差的常量、线性漂移、漂移叠加周期项三种假想曲线"><rect width="1020" height="590" fill="#faf8f2"/><g font-family="Noto Sans CJK SC, sans-serif" fill="#213d49"><text x="36" y="43" font-size="25">三种不同的对时任务</text><text x="36" y="77" font-size="17">假想曲线，仅说明形状；不是卫星实测，也不表示修正的具体正负号</text>']
for row,(title,sub,fn,color) in enumerate([('只差初始读数','整体平移即可对齐',lambda t:25,'#287f87'),('走速持续不同','还须改掉增长的斜率',lambda t:5+5*t,'#ab5d36'),('平均走速之外还有周期项','减去直线后，起伏仍留下',lambda t:5+5*t+18*sin(2*pi*t/12),'#7560a6')]):
 y0=216+row*158;x0=430;w=530;scale=1.2
 s.append(f'<text x="36" y="{y0-60}" font-size="22">{title}</text><text x="36" y="{y0-24}" font-size="17">{sub}</text><path d="M{x0} {y0-100} V{y0} H{x0+w}" stroke="#7b8c90" fill="none"/><text x="{x0-20}" y="{y0-111}" font-size="15">钟差</text>')
 points=' '.join(f'{x0+w*i/240:.2f},{y0-scale*fn(12*i/240):.2f}' for i in range(241));s.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')
 s.append(f'<text x="{x0+w-50}" y="{y0+23}" font-size="15">时间</text>')
s.append('</g></svg>');(p/'clock-error-components.svg').write_text(''.join(s))
