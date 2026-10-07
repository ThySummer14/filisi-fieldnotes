"""Three explicit teaching models; Python 3 standard library only.
Run: python3 recompute_xylem.py
No tree-growth prediction or reanalysis of experimental raw data.
"""
from fractions import Fraction
from pathlib import Path
import json

rho_kg_m3 = 1000.0
g_m_s2 = 9.81
height_m = 100.0
surface_tension_N_m = 0.072
radii_m = [20e-6, 100e-9]
gravity_Pa = rho_kg_m3 * g_m_s2 * height_m
capillary = []
for radius in radii_m:
    pressure = 2 * surface_tension_N_m / radius
    capillary.append({'hemisphere_radius_m': radius, 'delta_P_Pa': pressure,
                      'delta_P_MPa': pressure / 1e6,
                      'static_equivalent_height_m': pressure / (rho_kg_m3 * g_m_s2)})
radius_ratios = [1, 1, 1, 1, 2]
weights = [r ** 4 for r in radius_ratios]
total = sum(weights)
loss_large = Fraction(weights[-1], total)
loss_small_four = Fraction(sum(weights[:-1]), total)
assert loss_large == Fraction(4, 5)
assert loss_small_four == Fraction(1, 5)
assert abs(gravity_Pa - 981000) < 1e-8
assert abs(capillary[0]['delta_P_Pa'] - 7200) < 1e-8
assert abs(capillary[1]['delta_P_MPa'] - 1.44) < 1e-12
result = {
 'scope': 'Gravity, ideal hemispherical meniscus, and five parallel equal-length Poiseuille tubes',
 'assumptions': ['Water density=1000 kg/m3; g=9.81 m/s2',
  'Surface tension=0.072 N/m; complete wetting and hemispherical meniscus',
  'Capillary result balances static gravity only, without viscous losses',
  'Five tubes have common pressure difference, length and viscosity',
  'Laminar flow in circular tubes; no pit or network resistance',
  'No actual leaf pore radius, tree height limit or drought threshold inferred'],
 'gravity': {'height_m': height_m, 'delta_P_Pa': gravity_Pa,
             'delta_P_MPa': gravity_Pa / 1e6,
             'pressure_drop_MPa_per_m': rho_kg_m3 * g_m_s2 / 1e6},
 'capillary': capillary,
 'gauge_to_absolute_example': {'atmospheric_MPa': .101, 'gauge_MPa': -1,
                             'absolute_MPa': -1 + .101},
 'five_tubes': {'radius_ratios': radius_ratios, 'conductance_weights': weights,
  'total_weight': total,
  'one_large_lost': {'count_loss_fraction': '1/5', 'conductance_loss_fraction': str(loss_large),
                     'conductance_loss_percent': float(loss_large * 100)},
  'four_small_lost': {'count_loss_fraction': '4/5', 'conductance_loss_fraction': str(loss_small_four),
                     'conductance_loss_percent': float(loss_small_four * 100)}},
 'published_comparison_not_recomputed': {
  'source': 'Choat et al. 2016 Table I, DOI 10.1104/pp.15.00732; signs converted from -MPa column heading',
  'P50_MPa': {'Quercus_robur': {'microCT': -4.16, 'Cavitron': -1.38, 'static_centrifuge': -.47},
              'Populus_tremula_x_alba': {'microCT': -1.81, 'Cavitron': -1.83},
              'Pinus_pinaster': {'microCT': -3.27, 'Cavitron': -3.50}},
  'note': 'Reported means only; no raw observations fitted; CT endpoint inferred from conduit geometry'}
}
Path(__file__).with_name('xylem-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'gravity_MPa': gravity_Pa / 1e6, 'capillary_heights_m': [x['static_equivalent_height_m'] for x in capillary], 'capacity_loss_large_percent': float(loss_large*100)}, ensure_ascii=False))
