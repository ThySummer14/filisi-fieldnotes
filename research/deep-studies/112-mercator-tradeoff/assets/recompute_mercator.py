#!/usr/bin/env python3
"""Original spherical geometry teaching examples. Standard library only.
No geographic boundary dataset and no route planning. Sphere R=6371 km,
normal Mercator with equator scale=1, longitude relative to central meridian.
"""
from math import sin,cos,tan,atan,acos,atan2,log,exp,pi,sqrt,degrees,radians,isclose
from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=6371.
def my(phi):return log(tan(pi/4+phi/2))
rows=[]
for d in [0,30,60,80]:
 k=1/cos(radians(d));rows.append(dict(latitude_degrees=d,local_length_scale=k,local_area_scale=k*k))
phi=radians(60);l1,l2=radians(-60),radians(60)
u=(cos(phi)*cos(l1),cos(phi)*sin(l1),sin(phi));v=(cos(phi)*cos(l2),cos(phi)*sin(l2),sin(phi))
theta=acos(sum(a*b for a,b in zip(u,v)));gc=R*theta;rh=R*cos(phi)*(l2-l1)
path=[]
for i in range(201):
 t=i/200.;a=sin((1-t)*theta)/sin(theta);b=sin(t*theta)/sin(theta);w=[a*u[j]+b*v[j] for j in range(3)];lat=atan2(w[2],sqrt(w[0]**2+w[1]**2));lon=atan2(w[1],w[0]);path.append((degrees(lon),degrees(lat)))
start_bearing=degrees(atan2(sin(l2-l1)*cos(phi),cos(phi)*sin(phi)-sin(phi)*cos(phi)*cos(l2-l1)))
cut=degrees(2*atan(exp(pi))-pi/2)
assert isclose(rows[2]['local_area_scale'],4,rel_tol=1e-12)
assert gc<rh
# Finite-difference derivative verifies equal E-W/N-S local magnification.
dphi=1e-7;fd=(my(phi+dphi)-my(phi-dphi))/(2*dphi)
assert isclose(fd,1/cos(phi),rel_tol=1e-8)
result=dict(sphere_radius_km=R,equator_scale=1,local_distortion=rows,small_true_NE_vector=dict(true_bearing_degrees=45,plate_carree_bearing_at_60N=degrees(atan2(2,1)),mercator_bearing_at_60N=45),routes=dict(endpoints_lat_lon=[[60,-60],[60,60]],rhumb_km=rh,great_circle_km=gc,difference_km=rh-gc,shorter_percent=(rh-gc)/rh*100,maximum_great_circle_latitude=max(p[1] for p in path),initial_great_circle_bearing_degrees=start_bearing),square_web_mercator_cutoff_degrees=cut,finite_difference_y_derivative_at_60N=fd,notes=['Pure spherical teaching calculations; not a navigational plan.','Local area scale is not an entire country area multiplier.','Spherical Mercator is distinct from ellipsoidal Mercator and Web Mercator on ellipsoidal coordinates.'])
(P/'mercator-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
# Local same-ground-size square comparison.
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="480" viewBox="0 0 1120 480" role="img" aria-label="三个实地同样大小的小方块，在赤道、60度和80度纬度处按墨卡托局部尺度放大"><rect width="1120" height="480" fill="#faf8f2"/><g font-family="Noto Sans CJK SC,sans-serif" fill="#263f48"><text x="38" y="43" font-size="26">同样大小的一小块地，搬到高纬后画得多大</text><text x="38" y="77" font-size="17">球面近似，赤道尺度设为1；方块代表实地相等且足够小的面积，不是同样经纬跨度</text>']
for cx,d in [(180,0),(490,60),(870,80)]:
 k=1/cos(radians(d));w=40*k
 s+=[f'<rect x="{cx-w/2:.2f}" y="{335-w:.2f}" width="{w:.2f}" height="{w:.2f}" fill="#bcdedc" stroke="#287e84" stroke-width="2"/>',f'<text x="{cx}" y="372" font-size="21" text-anchor="middle">纬度 {d}°</text>',f'<text x="{cx}" y="405" font-size="18" text-anchor="middle">边长 ×{k:.2f}　面积 ×{k*k:.2f}</text>']
s+=['<text x="38" y="457" font-size="17" fill="#62767c">60°处横向、纵向都放大2倍，面积便是4倍。尺度沿纬度连续改变，不能直接套给整片大陆。</text></g></svg>'];(P/'mercator-scale.svg').write_text(''.join(s))
# Both spherical routes displayed in the same normal Mercator coordinates.
px_per_radian=880/radians(160)
x=lambda lon:110+radians(lon+80)*px_per_radian
y=lambda lat:125+(my(radians(80))-my(radians(lat)))*px_per_radian
plot_bottom=y(50)
assert isclose((x(1)-x(0))/radians(1),px_per_radian,rel_tol=1e-12)
assert isclose((y(50)-y(80))/(my(radians(80))-my(radians(50))),px_per_radian,rel_tol=1e-12)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="750" viewBox="0 0 1120 750" role="img" aria-label="同一对北纬60度端点：墨卡托图上恒向线是直线，而更短的大圆弧弯向高纬"><rect width="1120" height="750" fill="#faf8f2"/><g font-family="Noto Sans CJK SC,sans-serif" fill="#263f48"><text x="38" y="43" font-size="26">图上的直线，未必是球面上的短路</text><text x="38" y="77" font-size="18">两点均在北纬60°，经度相差120°；只比较理想球面几何，不考虑陆地、风与海流</text>']
for lat in [50,60,70,75,80]:s+=[f'<path d="M110 {y(lat):.2f} H990" stroke="#d6ddda"/><text x="92" y="{y(lat)+5:.2f}" text-anchor="end" font-size="16">{lat}°N</text>']
for lon in [-80,-60,-40,-20,0,20,40,60,80]:s+=[f'<path d="M{x(lon):.2f} 125 V{plot_bottom:.2f}" stroke="#d6ddda"/><text x="{x(lon):.2f}" y="{plot_bottom+29:.2f}" text-anchor="middle" font-size="16">{abs(lon)}°'+('W' if lon<0 else 'E' if lon>0 else '')+'</text>']
s+=[f'<path d="M{x(-60)} {y(60)} H{x(60)}" stroke="#b3703d" stroke-width="4"/>', '<polyline points="'+' '.join(f'{x(lon):.2f},{y(lat):.2f}' for lon,lat in path)+'" fill="none" stroke="#167d84" stroke-width="4"/>']
for lon in [-60,60]:s+=[f'<circle cx="{x(lon)}" cy="{y(60)}" r="6" fill="#273e47"/>']
s+=[f'<text x="550" y="{y(73.8979)-20}" font-size="18" text-anchor="middle" fill="#176c72">大圆弧约{gc:.1f}公里；最高约73.90°N</text>',f'<text x="550" y="{y(60)+31}" font-size="18" text-anchor="middle" fill="#965f32">沿60°纬线向东：恒向线约{rh:.1f}公里</text>',f'<text x="38" y="{plot_bottom+78:.2f}" font-size="18">恒向线始终朝真北以东90°。大圆弧的真方位角沿途变化，初始约33.69°。</text>',f'<text x="38" y="{plot_bottom+116:.2f}" font-size="17" fill="#62767c">本例大圆弧短约{rh-gc:.1f}公里。高纬处图面比例更大，不能把图上尺量长度当实际里程。</text></g></svg>']
(P/'rhumb-and-great-circle.svg').write_text(''.join(s));print(json.dumps(result,ensure_ascii=False,indent=2))
