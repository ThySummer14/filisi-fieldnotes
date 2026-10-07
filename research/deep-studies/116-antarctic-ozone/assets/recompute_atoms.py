"""Integer atom bookkeeping only; no rate, yield, field-data or laboratory simulation.
Run with Python 3 using only its standard library.
"""
import json
from collections import Counter
from pathlib import Path

COMPOSITION = {
    'Cl': {'Cl': 1}, 'O3': {'O': 3}, 'O2': {'O': 2},
    'ClO': {'Cl': 1, 'O': 1}, 'ClOOCl': {'Cl': 2, 'O': 2},
    'ClOO': {'Cl': 1, 'O': 2}, 'HCl': {'H': 1, 'Cl': 1},
    'ClONO2': {'Cl': 1, 'N': 1, 'O': 3}, 'Cl2': {'Cl': 2},
    'HNO3': {'H': 1, 'N': 1, 'O': 3},
}

def atoms(species):
    total = Counter()
    for name, number in species.items():
        for element, count in COMPOSITION[name].items():
            total[element] += number * count
    return dict(sorted(total.items()))

reactions = [
    ('surface activation', {'HCl': 1, 'ClONO2': 1}, {'Cl2': 1, 'HNO3': 1}),
    ('precursor photolysis', {'Cl2': 1}, {'Cl': 2}),
    ('ozone consumption, twice', {'Cl': 2, 'O3': 2}, {'ClO': 2, 'O2': 2}),
    ('dimer formation', {'ClO': 2}, {'ClOOCl': 1}),
    ('dimer photolysis', {'ClOOCl': 1}, {'Cl': 1, 'ClOO': 1}),
    ('intermediate decomposition', {'ClOO': 1}, {'Cl': 1, 'O2': 1}),
]
checks = []
for label, left, right in reactions:
    assert atoms(left) == atoms(right), label
    checks.append({'step': label, 'reactants': left, 'products': right,
                   'atoms_each_side': atoms(left), 'balanced': True})
net = Counter()
for label, left, right in reactions[2:]:
    for name, count in right.items(): net[name] += count
    for name, count in left.items(): net[name] -= count
net = dict(sorted((name, count) for name, count in net.items() if count))
assert net == {'O2': 3, 'O3': -2}
stages = [
    {'Cl': 2, 'O3': 2},
    {'ClO': 2, 'O2': 2},
    {'ClOOCl': 1, 'O2': 2},
    {'Cl': 2, 'O2': 3},
]
assert all(atoms(stage) == {'Cl': 2, 'O': 6} for stage in stages)
cycles = 100
result = {
    'model': 'Exact stoichiometric bookkeeping for one idealized ClO dimer cycle',
    'not_a_claim_about': ['reaction rate', 'actual cycle count', 'atmospheric loss fraction'],
    'omitted_from_atom_count': ['Photons carry energy, not atoms',
                                'M is the unchanged third-body collision partner'],
    'reaction_checks': checks,
    'diagram_states': [{'species': s, 'atoms': atoms(s)} for s in stages],
    'net_molecule_change_per_completed_cycle': net,
    'illustration': {'completed_cycles_assumed': cycles, 'O3_consumed': cycles * 2,
                     'O2_produced': cycles * 3, 'Cl_atoms_recycled': 2},
}
path = Path(__file__).with_name('atom-balance-results.json')
path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result['illustration'], ensure_ascii=False))
