"""Standard-library-only arithmetic/scheduling model; does not execute repository code."""
import json, math
from fractions import Fraction
from pathlib import Path
D=Fraction(169583,1000); fps=Fraction(30); sr=48000
n=math.ceil(D*fps); samples=math.ceil(D*sr)
frames=[Fraction(k,1)/fps for k in range(n)]
assert frames[-1]<D<=Fraction(n,1)/fps
boundaries=[Fraction(0),Fraction(17,3),Fraction(1001,30000),D]
for t in boundaries:
 k=math.ceil(t*sr)
 assert Fraction(k,sr)>=t and Fraction(k-1,sr)<t
# An old request completes after a newer one; gating must preserve the latest display.
requests=[{'epoch':2,'frame':20},{'epoch':1,'frame':10}]
shown=None
for r in requests:
 if r['epoch']==2:shown=r['frame']
assert shown==20
# Normalized interpolation cannot produce a nonflat segment between equal endpoint values.
def normalized_value(a,b,p):return a+(b-a)*p
assert all(normalized_value(1,1,p)==1 for p in [-1,0,0.5,1,2])
results={'duration_seconds':float(D),'fps':30,'video_frames':n,'last_frame_pts':float(frames[-1]),'nominal_video_end':float(Fraction(n,1)/fps),'audio_samples':samples,'number_safe_tick_hours':(2**53-1)/254016000000/3600,'all_rgba8_frames_gib':1280*720*4*n/2**30,'eight_rgba8_frames_mib':1280*720*4*8/2**20,'stereo_float32_output_mib':samples*2*4/2**20,'stereo_pcm16_output_mib':samples*2*2/2**20,'late_reply_selected_frame':shown,'checks':'passed','scope':'synthetic arithmetic and protocol model, not repository tests or actual media'}
Path(__file__).with_name('synthetic-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
