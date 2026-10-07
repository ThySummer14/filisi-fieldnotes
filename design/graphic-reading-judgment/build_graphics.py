from pathlib import Path
import html,json,math
import subprocess
D=Path(__file__).parent; A=D/'assets'
font='Noto Sans CJK SC'; ink='#172B35'; paper='#FFFFFF'; orange='#A74618'; muted='#526670'
def t(x,y,txt,size=28,color=ink,weight=400):return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(txt)}</text>'
def rect(x,y,w,h,c,stroke='none'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{stroke}"/>'
def line(x1,y1,x2,y2,c=ink,width=3,dash=''):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{width}" stroke-dasharray="{dash}"/>'
def save(n,body,w=1400,h=820):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+rect(0,0,w,h,paper)+body+'</svg>'
 (A/f'{n}.svg').write_text(s);subprocess.run(['inkscape',str(A/f'{n}.svg'),'--export-type=png',f'--export-filename={A}/{n}.png'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
# All information retained; same words on both sides.
body=t(40,48,'A  各组争夺注意',28)+t(740,48,'B  主题与行动分层',28)
for x in [40,740]:body+=rect(x,78,620,695,'#F6F2E9')
texts=['夜间地图工作坊','用线条画出熟悉街道的另一种走法','10月24日  19:00—21:00','北馆二层','零基础可参加','10月22日前登记参加']
ys=[180,275,370,465,560,655]
for y,txt in zip(ys,texts):body+=t(70,y,txt,34 if len(txt)<15 else 26,orange,700)
for y,txt,sz,co,we in [(175,texts[0],49,ink,700),(248,texts[1],27,ink,400),(455,texts[2],30,ink,600),(508,texts[3],30,ink,400),(315,texts[4],26,muted,400),(676,texts[5],31,'#FFFFFF',600)]:
 if y==676:body+=rect(770,623,548,84,orange)
 body+=t(790 if y==676 else 770,y,txt,sz,co,we)
save('01-hierarchy',body)
# grid
b=t(40,45,'四栏是组织单位  内容可以跨栏',30)
x0,y0,cw,g=100,95,282,24
for i in range(4):b+=rect(x0+i*(cw+g),y0,cw,650,'#F0F5F6')+t(x0+i*(cw+g)+10,735,str(i+1),22,muted)
b+=rect(110,120,1178,115,'#DAE7EB')+t(135,196,'夜间地图工作坊',55,ink,700)
b+=rect(110,270,566,292,'#FFFFFF','#9CB5BF')+t(135,323,'说明文字跨两栏',32,ink,600)
for y,s in [(382,'用线条画出熟悉街道的'),(430,'另一种走法。'),(503,'零基础可参加')]:b+=t(135,y,s,29)
b+=rect(722,270,566,292,'#E8DACA')+t(755,425,'原创路线图跨两栏',34)
b+=t(110,625,'10月24日  19:00—21:00',32)+t(722,625,'北馆二层',32)
b+=t(110,682,'10月22日前登记参加',31,orange,600)
save('02-grid',b)
# intentional punctuation mistakes, clearly labelled
b=t(40,48,'A  刻意构造的断行问题',28)+t(740,48,'B  保留语义与标点关系',28)
for x in [40,740]:b+=rect(x,85,620,680,'#F6F2E9')
for y,s in [(175,'夜间地'),(246,'图工作坊')]:b+=t(80,y,s,52,ink,700)
for y,s in [(175,'夜间地图'),(246,'工作坊')]:b+=t(780,y,s,52,ink,700)
for x,lines in [(80,['沿着熟悉的街道行走','，重新画出夜晚的地图','。零基础也可以参加。']),(780,['沿着熟悉的街道行走，','重新画出夜晚的地图。','零基础也可以参加。'])]:
 for j,s in enumerate(lines):b+=t(x,414+j*60,s,34)
b+=t(80,676,'“地图”拆开  句末标点落到行首',26,orange)+t(780,676,'先按意思断行  再调整尺寸',26,muted)
save('03-type',b)
# image-text
b=t(40,48,'A  插图与文字分开',28)+t(740,48,'B  路线参与文字组织',28)
for x in [40,740]:b+=rect(x,85,620,680,'#F6F2E9')
for pts in [[(100,170),(450,170),(450,280),(220,280),(220,375)],[(780,205),(1230,205),(1230,450),(1050,450),(1050,570)]]:
 b+='<polyline points="'+' '.join(f'{x},{y}'for x,y in pts)+f'" fill="none" stroke="{orange}" stroke-width="12"/>'
 for x,y in [pts[0],pts[-1]]:b+=f'<circle cx="{x}" cy="{y}" r="15" fill="{orange}"/>'
for x,y in [(85,515),(780,350)]:b+=t(x,y,'夜间地图',60,ink,700)+t(x,y+72,'工作坊',60,ink,700)
for x in [85,780]:b+=t(x,675,'10月24日  19:00—21:00',29)+t(x,725,'北馆二层  ·  零基础可参加',27)
save('04-image-text',b)
# color
b=t(40,48,'A  低对比度示例',28)+t(740,48,'B  重要文字使用深色',28)
for x in [40,740]:b+=rect(x,85,620,680,'#FFFFFF','#CED7DA')
for x,co,button in [(80,'#A8AFB2','#E9AA86'),(780,ink,orange)]:
 b+=t(x,198,'夜间地图工作坊',47,co,700)+t(x,305,'10月24日  19:00—21:00',31,co)+t(x,365,'北馆二层  ·  零基础可参加',28,co)
 b+=rect(x,470,540,100,button)+t(x+28,533,'10月22日前登记参加',31,'#FFFFFF',600)
 b+=t(x,690,'色彩气质可以保留  信息需要辨认',25,muted)
save('05-color',b)
# adaptation abstract blocks with real, complete key content.
b=t(35,48,'同一信息按媒介重排',30)
for x,y,w,h,c in [(40,90,420,660,'#F6F2E9'),(495,90,430,430,'#F6F2E9'),(970,90,390,660,'#F6F2E9')]:b+=rect(x,y,w,h,c)
b+=t(68,151,'竖版海报',25,muted)+t(68,220,'夜间地图',48,ink,700)+t(68,280,'工作坊',48,ink,700)
b+=t(68,352,'用线条画出熟悉街道的',25)+t(68,393,'另一种走法',25)+t(68,478,'10月24日',31)+t(68,523,'19:00—21:00',31)+t(68,571,'北馆二层',28)+t(68,620,'零基础可参加',25)+t(68,694,'10月22日前登记参加',26,orange,600)
b+=t(520,151,'方形预览',25,muted)+t(520,225,'夜间地图',48,ink,700)+t(520,285,'工作坊',48,ink,700)+t(520,361,'地图绘制  ·  零基础',28)+t(520,428,'10月24日',37,orange,700)+t(504,573,'配套可读说明补充完整细节',25)+t(504,620,'不把整张海报等比缩小',25)
b+=t(995,151,'窄屏详情',25,muted)+t(995,217,'夜间地图',43,ink,700)+t(995,271,'工作坊',43,ink,700)+t(995,336,'用线条画出熟悉街道的',23)+t(995,374,'另一种走法',23)+t(995,443,'10月24日',28)+t(995,485,'19:00—21:00',28)+t(995,527,'北馆二层',27)+t(995,574,'零基础可参加',24)
b+=rect(990,627,345,70,orange)+t(1003,673,'10月22日前登记参加',26,'#FFFFFF',600)
save('06-adaptation',b)
def luminance(h):
 a=[int(h[i:i+2],16)/255 for i in (1,3,5)];a=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in a];return sum(v*w for v,w in zip(a,[.2126,.7152,.0722]))
def cr(a,b):
 x,y=sorted([luminance(a),luminance(b)]);return (y+.05)/(x+.05)
colors=[('#A8AFB2','#FFFFFF'),('#FFFFFF','#E9AA86'),('#172B35','#FFFFFF'),('#FFFFFF','#A74618')]
data=[dict(foreground=a,background=b,ratio=cr(a,b),normal_text_AA=cr(a,b)>=4.5)for a,b in colors]
(D/'contrast-calculations.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(data)
