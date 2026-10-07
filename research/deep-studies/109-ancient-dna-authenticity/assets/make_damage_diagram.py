#!/usr/bin/env python3
"""Draw original SVG: published table values above, invented teaching counts below."""
from pathlib import Path
from html import escape
P=Path(__file__).resolve().parent
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="730" viewBox="0 0 1080 730">','<rect width="1080" height="730" fill="#fcfbf7"/>','<style>text{font-family:"Noto Sans CJK SC",sans-serif;fill:#24353b}.title{font-size:27px;font-weight:700}.sub{font-size:19px}.small{font-size:16px}</style>']
def t(x,y,a,cls='sub',anchor='start'):
 s.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(a)}</text>')
def rect(x,y,w,h,color):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{color}"/>')
t(40,43,'酶处理改变读数；同一筛选规则也不保证同一纯度','title')
t(40,80,'上：Rohland 等（2015）表 1 的同一提取物 a，按报告数据重绘','sub')
t(40,109,'不是八份样本平均；原表没有此处可用的误差条。','small')
t(40,134,'比例按两端相应的参考C/G位点统计；不是全部片段的比例，也不是古DNA纯度。','small')
rect(645,92,18,18,'#5d7889');t(672,108,'未处理','small');rect(815,92,18,18,'#d07e49');t(842,108,'部分 UDG','small')
for yi,label,vals in [(150,'最末端',[32.74,10.92]),(243,'向内第二个位置',[24.19,.46])]:
 t(210,yi+32,label,anchor='end')
 for k,v in enumerate(vals):
  y=yi+k*34;rect(250,y,v*17,24,['#5d7889','#d07e49'][k]);t(260+v*17,y+19,f'{v:.2f}%','small')
for val in [0,10,20,30,40]:
 x=250+val*17;s.append(f'<line x1="{x}" y1="320" x2="{x}" y2="326" stroke="#617078"/>');t(x,348,str(val),'small','middle')
s.append('<line x1="250" y1="320" x2="930" y2="320" stroke="#617078"/>');t(930,375,'相应末端位置的损伤率（%）','small','end')
s.append('<line x1="40" y1="400" x2="1040" y2="400" stroke="#c9cec9"/>')
t(40,439,'下：教学设定，古老片段通过 30%，现代片段误通过 1%','sub')
t(40,470,'显示按设定比例计算的期望数量，不是测序实测数据。','small')
for y,left,right,purity in [(505,'100 古老 + 900 现代','30 古老 + 9 现代','纯度 76.9%'),(605,'900 古老 + 100 现代','270 古老 + 1 现代','纯度 99.63%')]:
 rect(40,y,350,60,'#edf0ec');t(215,y+38,left,anchor='middle')
 t(435,y+38,'→','title','middle');rect(480,y,350,60,'#e0ebe6');t(655,y+38,right,anchor='middle');t(1025,y+38,purity,'sub','end')
t(40,711,'同样的通过率，起始混合比例不同，留下来的组成就不同。','small')
s.append('</svg>');(P/'damage-and-filter.svg').write_text('\n'.join(s),encoding='utf8')
