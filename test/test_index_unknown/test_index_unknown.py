

import unittest, os, sys
from ImageD11 import indexing
import numpy as np
"""
>>> from ImageD11.indexing import readubis, write_ubi_file
>>> from ImageD11.gv_general import *
>>> ul = readubis("1.ubi")
>>> ul
[array([[-1.31331619, -5.70257136, -2.14731979],
       [-0.52591148,  0.82984375, -6.15279178],
       [ 4.54824731,  0.40771549,  1.56440062]])]
>>> def norm(v): return v/np.sqrt(np.dot(v,v))
... 
>>> import numpy as np
>>> d1 = norm(np.array([-0.4,0.5,0.1]))
>>> d1
array([-0.6172134 ,  0.77151675,  0.15430335])
>>> a = rotation_axis(d1, 230)
>>> ul.append(np.dot(a.to_matrix(), ul[0]))
>>> d2 = norm(np.array([0.3,0.1,-0.7]))
>>> a = rotation_axis(d2, 80)
>>> ul.append(np.dot(a.to_matrix(), ul[0]))
>>> write_ubi_file( "3.ubi", ul )
"""


UBIS = [ 
    ("1.ubi", "-k 1 -o 1.ubi.new -v 0.01 -m 20 -f 0.75 -t 0.1"),
    ("1.ubi", "-k 1 -o 1.ubi.fftnew -v 1 -m 20 -f 0.75 -t 0.1 --fft"),
    ("2.ubi", "-k 2 -o 2.ubi.new -v 0.01 -m 20 -f 0.45 -t 0.1"),
    ("2.ubi", "-k 2 -o 2.ubi.fftnew -v 2 -m 40 -f 0.45 -t 0.1 -s 20 --fft"),
    ("3.ubi", "-k 3 -o 3.ubi.new -v 0.01 -m 20 -f 0.3 -t 0.1"),
    ("3.ubi", "-k 3 -o 3.ubi.fftnew -v 3 -m 40 -f 0.3 -t 0.1 -s 20 -r 0.80 --fft"),

    ]



SCRIPT = os.path.join(sys.executable+" ..","..","scripts","index_unknown.py")

def generate_hkls( n ):
    """ Makes solid hkl cube """
    lim = n/2
    r = list(range(-lim, lim+1))
    npk = len(r)
    hkls = np.zeros( (3,npk,npk,npk))
    for i in r:
        for j in r:
            for k in r:
                # print [ (l,l+lim) for l in [i,j,k]]
                hkls[:,i+lim,j+lim,k+lim] = i,j,k
    
    hkls = hkls.reshape( (3,npk*npk*npk))
    return hkls

def generate_gve( uf , nh=6):
    """ uf is a ubi filename"""
    h = generate_hkls(nh)
    g = []
    i = 0
    for u in indexing.readubis(uf):
        r = np.dot(np.linalg.inv( u ), h).T
        g.append(r)
        i += 1
    return np.array( g ).reshape( (h.shape[1]*i, 3) )

def write_gve( gvecs, name):
    f = open(name, "w")
    # Dummy cell line
    f.write("1 2 3 4 5 6 P\n")
    f.write("#  gx  gy  gz   xc  omega\n")
    for g in gvecs:
        f.write("%f  %f  %f 0 0 0 0 0\n"%tuple(g))
    f.close()


class testGve(unittest.TestCase):
    def setUp(self):
        for u, cmd in UBIS:
            write_gve(
                generate_gve(u),
                u+".gve"
                )
        
    def test1(self):
        for u, cmd in UBIS:
            assert os.path.exists(u+".gve")
            e = SCRIPT +" -g %s "%(u+".gve")+cmd
            print("\n",e)
            os.system(e)


    def tearDown(self):
        """ explicitely leave the files here for debugging """
        pass
            


if __name__ == "__main__":
    unittest.main()
