"""Independent numerical oracle and fixture checks for Experiment 008.

These are math and presence checks, NOT human comprehension experiments.
"""
from pathlib import Path
import math
import unittest

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT / 'experiments/008-atemporal-invariant/index.html'

class AtemporalInvariantCalibration(unittest.TestCase):
    def test_html_has_manipulation_and_reveal_controls(self):
        s=HTML.read_text(encoding='utf8')
        for marker in ['id="x"','id="y"','id="reveal"','id="hide"','window.__triangleState','dragging=false']:
            self.assertIn(marker,s)

    def test_independent_euclidean_angle_invariant(self):
        A=(87,335);B=(477,335)
        def angle(p,q,r):
            u=(p[0]-q[0],p[1]-q[1]);v=(r[0]-q[0],r[1]-q[1])
            cos=(u[0]*v[0]+u[1]*v[1])/(math.hypot(*u)*math.hypot(*v))
            return math.acos(max(-1,min(1,cos)))
        for x in [155,180,270,330,430]:
            for y in [70,135,250,270]:
                C=(x,y)
                degrees=sum([angle(C,A,B),angle(A,B,C),angle(A,C,B)])*180/math.pi
                self.assertAlmostEqual(degrees,180,places=9)

if __name__=='__main__':
    unittest.main()
