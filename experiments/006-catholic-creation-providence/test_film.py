"""Local, deterministic checks for Film 006, not a doctrinal or comprehension guarantee."""
import json, subprocess, pathlib
from PIL import ImageChops
import render
ROOT=pathlib.Path(__file__).resolve().parent

def test_scene_contract():
 d=json.loads((ROOT/'scene-contract.json').read_text())
 assert d['tradition']=='Catholicism'
 assert len(d['represented_relations'])==4
 assert len(d['promoted_grammar_rules'])==0
 assert render.FPS==20 and render.DURATION==84

def test_chronological_caption_coverage():
 v=render.CAPTIONS
 assert v[0][0]==0 and v[-1][1]==render.DURATION
 assert all(v[i][1]==v[i+1][0] for i in range(len(v)-1))
 assert all(a<b and t for a,b,t in v)

def test_camera_continuity_and_living_world():
 assert all(0.95<=render.camera_pose(t)[2]<=1.6 for t in [0,7,15,27,40,53,62,73,83])
 for a,b in [(11.2,11.25),(28.9,28.95),(43.9,43.95)]:
  x=render.camera_pose(a);y=render.camera_pose(b)
  assert abs(x[0]-y[0])<4 and abs(x[1]-y[1])<4 and abs(x[2]-y[2])<.07
 i1,i2=render.render_at(24),render.render_at(25)
 assert ImageChops.difference(i1,i2).getbbox() is not None

def test_video_streams():
 f=ROOT/'catholic_creation_providence_mobile.mp4'\n if not f.exists(): f=ROOT/'film-preview.mp4'
 p=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_name,codec_type','-show_entries','format=duration','-of','json',str(f)],capture_output=True,text=True,check=True)
 j=json.loads(p.stdout)
 assert 83.9<float(j['format']['duration'])<84.2
 types={s['codec_type']:s['codec_name'] for s in j['streams']}
 assert types.get('video')=='h264' and types.get('audio')=='aac'

if __name__=='__main__':
 for f in [test_scene_contract,test_chronological_caption_coverage,test_camera_continuity_and_living_world,test_video_streams]:
  f();print('PASS',f.__name__)