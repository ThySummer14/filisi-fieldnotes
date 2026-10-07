"""Spherical weak-field teaching model and 1-D clock-bias examples, not a GPS receiver."""
from math import sqrt
from pathlib import Path
import json
c=299792458.0;GM=3.986004418e14;R=6378137.0;r=26560000.0;day=86400.
v=sqrt(GM/r)
grav=GM*(1/R-1/r)/c**2
motion=-v*v/(2*c*c)
F=-4.442807633e-10;e=.01
amp=abs(F*e*sqrt(r))
L=20000000.;x=8000000.;b=0.
def solve(sL,sR):
 pL=x+b-c*sL;pR=L-x+b-c*sR
 xhat=(pL-pR+L)/2;bhat=(pL+pR-L)/2
 return dict(satellite_clock_errors_s=[sL,sR],pseudoranges_m=[pL,pR],x_estimate_m=xhat,position_error_m=xhat-x,receiver_clock_estimate_s=bhat/c)
out=dict(model='spherical Earth, stationary ground reference, circular satellite orbit; no geoid/rotation/oblateness',parameters=dict(c_m_s=c,GM_m3_s2=GM,ground_radius_m=R,orbital_radius_m=r),orbital_speed_m_s=v,gravitational_gain_us_day=grav*day*1e6,motion_loss_us_day=motion*day*1e6,net_gain_us_day=(grav+motion)*day*1e6,classic_adjustment_us_day=4.4647e-10*day*1e6,classic_nominal_MHz=10.23*(1-4.4647e-10),eccentric_example=dict(a_m=r,e=e,correction_peak_ns=amp*1e9,equivalent_range_peak_m=amp*c),chou_height_change=dict(h_m=.33,fractional_prediction=9.8*.33/c**2),one_dimensional_examples=[solve(0,0),solve(1e-6,1e-6),solve(1e-6,0)])
assert abs(out['one_dimensional_examples'][1]['position_error_m'])<1e-7
assert abs(out['one_dimensional_examples'][2]['position_error_m']+c*1e-6/2)<1e-7
assert 38<out['net_gain_us_day']<39
p=Path(__file__).resolve().parent/'gps-results.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
