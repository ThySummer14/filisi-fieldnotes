"""1-D Gaussian photon model; no microscope data, pixelation, background or drift fit."""
from random import Random
from statistics import mean,stdev
from math import sqrt,exp
from pathlib import Path
import json
rng=Random(20261008);sigma=120.;trials=400
rows=[]
for n in [100,400,1600]:
 estimates=[sum(rng.gauss(0,sigma) for _ in range(n))/n for t in range(trials)]
 expected=sigma/sqrt(n);observed=stdev(estimates)
 assert abs(observed/expected-1)<.15
 rows.append(dict(photons=n,expected_sd_nm=expected,empirical_sd_nm=observed,trials=trials))
def g(x,mu,s):return exp(-.5*((x-mu)/s)**2)
xgrid=[i*.25 for i in range(-720,721)]
wide=[g(x,-20,120)+g(x,20,120) for x in xgrid]
assert xgrid[wide.index(max(wide))]==0
# Repeated estimates can have excellent precision around a wrong center.
mixed=[(sum(rng.gauss(-20,sigma) for _ in range(800))+sum(rng.gauss(20,sigma) for _ in range(800)))/1600 for t in range(trials)]
out=dict(seed=20261008,sigma_nm=sigma,independent_single_emitter_trials=rows,two_equal_emitters_nm=[-20,20],combined_single_center=dict(expected_nm=0,empirical_mean_nm=mean(mixed),empirical_sd_nm=stdev(mixed)),systematic_shift_example_nm=20,live_cell_frame_math=dict(raw_frames=7500,exposure_ms=40,total_s=300,reconstructions=[dict(final_frames=n,raw_frames_per_group=7500//n,seconds_per_reconstruction=300/n) for n in [5,10,20]]))
a=Path(__file__).resolve().parent;(a/'localization-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
X=lambda x:110+(x+180)/360*740
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="980" height="535" viewBox="0 0 980 535" role="img" aria-label="同时发光的两分子形成宽单峰；轮流发光定位后重建为两个窄位置分布"><rect width="980" height="535" fill="#faf8f2"/><g font-family="Noto Sans CJK SC, sans-serif" fill="#213d49"><text x="38" y="40" font-size="24">光斑仍然宽，记录中心的任务变了</text><text x="38" y="71" font-size="17">原创一维模型：真实分子在−20与+20纳米；每个光斑的标准差σ=120纳米</text>']
for y0,height,mode,label in [(238,115,'wide','两者同帧发光：总光斑只有一个峰，中心落在0'),(446,115,'narrow','分别定位后重建：每个位置的不确定度设为3纳米')]:
 vals=wide if mode=='wide' else [g(x,-20,3)+g(x,20,3) for x in xgrid];mx=max(vals);pts=' '.join(f'{X(x):.2f},{y0-height*v/mx:.2f}' for x,v in zip(xgrid,vals));parts.append(f'<text x="38" y="{y0-height-19}" font-size="19">{label}</text><path d="M110 {y0} H850" stroke="#687e86"/><polyline points="{pts}" fill="none" stroke="'+('#287f87' if mode=='wide' else '#ab5d36')+'" stroke-width="3"/>')
 for x in [-20,20]:parts.append(f'<path d="M{X(x)} {y0+1} v12" stroke="#7560a6" stroke-width="2"/>')
 for x in [-180,-90,0,90,180]:parts.append(f'<text x="{X(x)}" y="{y0+32}" font-size="14" text-anchor="middle">{x}</text>')
parts.append('<text x="900" y="478" font-size="15">纳米</text><text x="38" y="518" font-size="16" fill="#617275">下图是定位结果的表达，镜头的点扩散函数并没有变窄。非仪器测量或性能基准。</text></g></svg>');(a/'localization-concept.svg').write_text(''.join(parts));print(json.dumps(out,ensure_ascii=False,indent=2))
