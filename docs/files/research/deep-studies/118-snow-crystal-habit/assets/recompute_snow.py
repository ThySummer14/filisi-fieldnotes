#!/usr/bin/env python3
"""Standard-library-only illustrative facet calculation; no diffusion solver.

Run: python3 assets/recompute_snow.py
Writes JSON, CSV and two original SVGs beside this file. PNGs are rendered from
the SVGs separately with Inkscape; the numerical reproduction needs no packages.
All sigma values in calculations are fractions, not numbers in percent.
The -15 C coefficients are literature parameterizations juxtaposed for a
controlled thought experiment, not a newly fitted snow-crystal simulation.
"""
import csv
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
V_KIN = 208.0  # micrometres / second, -15 C
SIGMA0_BASAL = 0.02
CASES = {"broad_prism": 0.033, "narrow_prism": 0.0015}


def rates(sigma, sigma0_prism):
    ab = math.exp(-SIGMA0_BASAL / sigma)
    ap = math.exp(-sigma0_prism / sigma)
    vb, vp = ab * V_KIN * sigma, ap * V_KIN * sigma
    return {"sigma_surface_fraction": sigma, "alpha_basal": ab,
            "alpha_prism": ap, "v_basal_um_s": vb, "v_prism_um_s": vp,
            "v_basal_over_v_prism": vb / vp}


rows = []
for j in range(101):
    sigma = (0.2 + 0.01 * j) / 100
    for case, s0 in CASES.items():
        rows.append({"case": case, **rates(sigma, s0)})
examples = {name: rates(0.005, s0) for name, s0 in CASES.items()}
assert abs(examples["broad_prism"]["v_basal_over_v_prism"] - math.exp(2.6)) < 1e-10
assert abs(examples["narrow_prism"]["v_basal_over_v_prism"] - math.exp(-3.7)) < 1e-12
assert all(0 < r["alpha_basal"] <= 1 and 0 < r["alpha_prism"] <= 1 for r in rows)
result = {
    "description": "Local facet-rate thought experiment at -15 C, fixed common surface supersaturation.",
    "formula": "v = A * exp(-sigma0/sigma_surface) * v_kin * sigma_surface; A=1",
    "parameter_origins": {
        "v_kin_um_s": "Libbrecht et al. 2015 arXiv:1512.03389v2 p.4, 208 at -15 C",
        "sigma0_basal": "2015 p.10, 2 percent",
        "sigma0_prism_broad": "2015 pp.4-5 and 10, broad-facet literature value 3.3 percent",
        "sigma0_prism_narrow": "2015 p.10, thin-edge fit near 0.15 percent",
        "sigma_surface_for_example": "Chosen 0.5 percent; near 2015 p.13 thin-edge model inference, not a measured humidity imposed on both faces"
    },
    "inputs": {"T_celsius": -15, "v_kin_um_s": V_KIN, "A_basal": 1,
               "A_prism": 1, "sigma0_basal": SIGMA0_BASAL, "sigma0_prism_cases": CASES},
    "examples": examples,
    "limits": ["Common, constant surface supersaturation is an imposed simplification.",
               "No three-dimensional diffusion, latent heating, facet-width evolution, or shape integration.",
               "The broad and narrow coefficients do not describe the same surface geometry.",
               "A growth-rate ratio is not the aspect ratio of a crystal at an arbitrary finite time."],
    "experimental_comparison": [
        {"T_celsius": -15, "sigma_center_percent_approx": 4.6, "observed": "block on needle tip"},
        {"T_celsius": -15, "sigma_center_percent_approx": 7.0, "observed": "thick plate on needle tip"},
        {"T_celsius": -15, "sigma_center_percent_approx": 11.3, "observed": "thin plate on needle tip"}
    ]
}
(OUT / "snow-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
with (OUT / "snow-rates.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)


def header(w, h):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="100%" height="100%" fill="#fbfcfe"/>
<style>text{{font-family:'Noto Sans CJK SC',sans-serif;fill:#172938}} .muted{{fill:#526676}} .small{{font-size:19px}} .body{{font-size:23px}}</style>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 Z" fill="context-stroke"/></marker></defs>'''


def text(x, y, s, size=23, color="#172938", anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{s}</text>'


def arrow(x1, y1, x2, y2, color):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="4" fill="none" marker-end="url(#arrow)"/>'


# Original cross-section diagram. Each rectangle is a vertical section through
# opposite prism faces, not a claim that ice has a square basal face.
s = header(1200, 745)
s += text(55, 62, "看法向推进速度，别把大晶面当成快晶面", 32)
s += text(55, 100, "纵剖面示意：水平边对应基面，竖直边对应一对相对的棱柱面", 21)
for cx, label, w, h, which in [(320, "棱柱面向外推进快 → 薄片", 350, 60, "plate"),
                              (875, "基面向两端推进快 → 细柱", 90, 210, "column")]:
    cy = 365
    s += text(cx, 163, label, 24, anchor="middle")
    x, y = cx - w / 2, cy - h / 2
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#dfebf3"/>'
    s += f'<path d="M{x},{y}h{w} M{x},{y+h}h{w}" stroke="#a65224" stroke-width="5"/>'
    s += f'<path d="M{x},{y}v{h} M{x+w},{y}v{h}" stroke="#236c94" stroke-width="5"/>'
    vb, vp = (23, 68) if which == "plate" else (56, 24)
    s += arrow(cx, y, cx, y-vb, "#a65224") + arrow(cx, y+h, cx, y+h+vb, "#a65224")
    s += arrow(x, cy, x-vp, cy, "#236c94") + arrow(x+w, cy, x+w+vp, cy, "#236c94")
    s += text(cx, 579, "厚度 H 的增速 = 2 v基", 23, anchor="middle")
    s += text(cx, 616, "对边宽 W 的增速 = 2 v棱", 23, anchor="middle")
s += text(55, 676, "橙色：两个基面，法向沿 c 轴。蓝色：六个棱柱面，法向在横向。", 21)
s += text(55, 713, "箭头表示增长方向；长度仅作快慢示意。晶面的外露面积不等于其法向生长速度。", 19)
s += '</svg>'
(OUT / "facet-normal-growth.svg").write_text(s)

# Original quantitative plot, plotted from generated rows, not copied paper art.
s = header(1200, 800)
s += text(55, 60, "同一温度，改一项表面参数就能反转快慢", 31)
s += text(55, 103, "−15°C 说明性复算；两类面取相同的局部过饱和度；纵轴为对数刻度", 21)
x0, x1, y0, y1 = 125, 1090, 160, 595
xx = lambda pct: x0 + (pct-0.2)/1.0*(x1-x0)
yy = lambda ratio: y1 - (math.log10(ratio)+4.2)/7.2*(y1-y0)
for power in range(-4, 4):
    y = yy(10**power)
    s += f'<path d="M{x0},{y}H{x1}" stroke="#d7e0e7" stroke-width="1"/>'
    s += text(x0-15, y+7, f'{10**power:g}', 18, anchor="end")
for pct in [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]:
    x=xx(pct)
    s += f'<path d="M{x},{y1}v7" stroke="#526676"/>'
    s += text(x, y1+33, f'{pct:g}%', 19, anchor="middle")
s += f'<path d="M{x0},{y0}V{y1}H{x1}" stroke="#526676" fill="none" stroke-width="2"/>'
y_equal=yy(1)
s += f'<path d="M{x0},{y_equal}H{x1}" stroke="#80909b" stroke-dasharray="7,6" stroke-width="2"/>'
s += text(1078, y_equal-12, "1：两类面等速", 19, anchor="end")
s += f'<path d="M{xx(.5)},{y0}V{y1}" stroke="#9ca9b2" stroke-dasharray="5,6"/>'
for case, color in [("broad_prism", "#a65224"), ("narrow_prism", "#236c94")]:
    rr=[r for r in rows if r['case']==case]
    d=' '.join(('M' if i==0 else 'L')+f'{xx(r["sigma_surface_fraction"]*100):.2f},{yy(r["v_basal_over_v_prism"]):.2f}' for i,r in enumerate(rr))
    s+=f'<path d="{d}" stroke="{color}" stroke-width="4" fill="none"/>'
    val=examples[case]['v_basal_over_v_prism']
    s+=f'<circle cx="{xx(.5)}" cy="{yy(val)}" r="6" fill="{color}"/>'
s += text(145, 150, "v基 / v棱", 23)
s += text(620, 214, "宽棱柱面参数：σ₀,棱 = 3.3%", 23)
s += text(620, 248, "在 0.5% 处，v基 / v棱 = 13.46", 21)
s += text(620, 515, "窄棱柱面参数：σ₀,棱 = 0.15%", 23)
s += text(620, 549, "在 0.5% 处，v基 / v棱 = 0.0247", 21)
s += text(610, 668, "表面过饱和度 σ表面", 23, anchor="middle")
s += text(55, 718, "两条曲线均取 A = 1、σ₀,基 = 2%。参数出处：Libbrecht 等 2015，第4、10页。", 20)
s += text(55, 755, "这是局部速度对照，未解水汽扩散与放热，也没有预测最终晶体长宽比。", 20)
s += '</svg>'
(OUT / "attachment-rate-comparison.svg").write_text(s)
print(json.dumps(examples, ensure_ascii=False, indent=2))
