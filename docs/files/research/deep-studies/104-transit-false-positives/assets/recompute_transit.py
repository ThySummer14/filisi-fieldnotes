"""Synthetic geometry and dilution examples; no observational data fitted."""
import json,math
F1,F2,x2=98,2,4
before=F2*x2/(F1+F2);after=(F2*.5)*x2/(F1+F2*.5)
out={'depth':.01,'radius_ratio_uniform_full_overlap':math.sqrt(.01),'central_transit_total_h':3,'central_flat_h':3*.9/1.1,'each_ingress_min':(3-3*.9/1.1)/2*60,'diluted_depth':1/(98+2),'centroid_before_px':before,'centroid_after_px':after,'shift_px':after-before,'fainter_background_depth':.1/(98+.2)}
assert abs(out['diluted_depth']-.01)<1e-12
print(json.dumps(out,indent=2))
