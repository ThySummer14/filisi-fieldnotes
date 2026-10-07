#!/usr/bin/env python3
"""Exact teaching arithmetic; no genetic or personal data are used.
Run: python3 recompute_ancient_dna.py
Probabilities and initial counts are invented for the explanation, not estimates.
"""
from fractions import Fraction
import json

def filtered(ancient, modern, tpr=Fraction(3,10), fpr=Fraction(1,100)):
    a, m = ancient*tpr, modern*fpr
    return {'initial_ancient':ancient,'initial_modern':modern,
            'expected_retained_ancient':float(a),'expected_retained_modern':float(m),
            'expected_purity':float(a/(a+m)),
            'ancient_recall':float(tpr),'modern_false_positive_rate':float(fpr)}

out={'scope':'Invented teaching expectations, not measured fragments or fitted PMD probabilities',
     'mixtures':[filtered(100,900),filtered(900,100)],
     'reported_table1_sample_a':{'source':'Rohland et al. 2015 Table 1, extract a',
       'untreated_percent':[32.74,24.19],'partial_udg_percent':[10.92,0.46],
       'positions':['terminal','penultimate'],'not_all_sample_average':True}}
assert out['mixtures'][0]['expected_retained_ancient']==30
assert out['mixtures'][0]['expected_retained_modern']==9
assert abs(out['mixtures'][0]['expected_purity']-10/13)<1e-12
assert abs(out['mixtures'][1]['expected_purity']-270/271)<1e-12
print(json.dumps(out,ensure_ascii=False,indent=2))
