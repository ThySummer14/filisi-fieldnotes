"""Original explanatory diagram. Requires matplotlib; no external data/graphics.
No axes: layout is a mechanism/atom-inventory diagram, not measured concentrations.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

base = Path(__file__).parent
font_manager.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams.update({'font.family': ['Noto Sans CJK JP', 'DejaVu Sans'], 'svg.fonttype': 'path'})
fig, ax = plt.subplots(figsize=(14, 9.4), dpi=140)
fig.patch.set_facecolor('#f6f5f0')
ax.set_facecolor('#f6f5f0')
ax.set_xlim(0, 1400); ax.set_ylim(0, 940); ax.axis('off')
ink = '#1a3444'; muted = '#506471'; teal = '#207c8b'; ochre = '#ce752c'

def text(x, y, s, size=16, color=ink, **kw):
    return ax.text(x,y,s,ha=kw.pop('ha','left'),va='center',fontsize=size,color=color,**kw)
def box(x,y,w,h,fill,edge='none'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=16',
                               linewidth=1,edgecolor=edge,facecolor=fill))
def arrow(x1,y1,x2,y2,color=muted):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,
                                linewidth=1.8,color=color))
text(55, 890, '冬天准备，阳光使循环持续', 26, weight='bold')
text(55, 848, '机制示意；没有时间轴，也不表示实测浓度或各反应的速度', 14, muted)
box(55, 638, 690, 166, '#dcebf0')
text(80,769,'冬季：低温、颗粒表面与极涡隔离',19,weight='bold')
text(80,717,'HCl + ClONO₂ → Cl₂ + HNO₃',23)
text(80,673,'储库氯换了形态；此步没有消耗 O₃',15,muted)
arrow(761,719,845,719)
box(864,638,480,166,'#f4e6ce')
text(890,769,'阳光逐渐返回',19,weight='bold')
text(890,717,'Cl₂ + 光子 → 2Cl',23)
text(890,673,'为下方循环提供氯原子',15,muted)
text(55,584,'一轮 ClO 二聚体循环：只跟踪 2 颗 Cl 与 6 颗 O',19,weight='bold')

xs=[55,391,727,1063]
labels=['2Cl + 2O₃','2ClO + 2O₂','ClOOCl + 2O₂','2Cl + 3O₂']
for i,x in enumerate(xs):
    box(x,259,281,275,'#ffffff','#d1dce0')
    text(x+140.5,497,labels[i],19,ha='center',weight='bold')
    text(x+140.5,294,'2Cl 原子 · 6O 原子',14,muted,ha='center')

def molecule(cx,cy,elements):
    distance=33; left=cx-distance*(len(elements)-1)/2
    for j in range(len(elements)-1):
        ax.plot([left+j*distance,left+(j+1)*distance],[cy,cy],color='#718691',lw=3,zorder=1)
    for j,e in enumerate(elements):
        c=ochre if e=='Cl' else teal
        ax.add_patch(Circle((left+j*distance,cy),19,facecolor=c,edgecolor='white',lw=1.3,zorder=2))
        text(left+j*distance,cy,e,11,'white',ha='center',zorder=3)
# The arrangements group atoms by molecular formula; they are not bond-angle models.
molecule(125,425,['Cl']); molecule(266,425,['Cl'])
molecule(125,353,['O','O','O']); molecule(266,353,['O','O','O'])
molecule(478,425,['Cl','O']); molecule(584,425,['Cl','O'])
molecule(478,353,['O','O']); molecule(584,353,['O','O'])
molecule(867,425,['Cl','O','O','Cl'])
molecule(814,353,['O','O']); molecule(920,353,['O','O'])
molecule(1150,425,['Cl']); molecule(1256,425,['Cl'])
molecule(1113,353,['O','O']); molecule(1203,353,['O','O']); molecule(1293,353,['O','O'])
for j,(label,a,b) in enumerate([('耗损 O₃',336,391),('结合',672,727),('光解 / 分解',1008,1063)]):
    arrow(a+5,396,b-5,396)
    text((a+b)/2,236,label,13,muted,ha='center')
text(55,200,'图中圆点只表示原子数量与分组，不表示真实分子几何。M 为未改变的碰撞伙伴，未画出。',13,muted)
box(55,77,1290,88,'#183846')
text(82,121,'净结果：2O₃ + 光子 → 3O₂',23,'white',weight='bold')
text(830,121,'Cl 回到起点；O₃ 没有回来',17,'#e4f2f3')
text(55,38,'100 轮只是整数账示例：200 O₃ → 300 O₂；不对应任何指定时间或真实大气损耗量。',13,muted)
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
for ext in ['svg','png']:
    fig.savefig(base/f'chlorine-season-cycle.{ext}',facecolor=fig.get_facecolor())
print('Saved original SVG and PNG.')
