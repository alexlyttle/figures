#!/usr/bin/env python

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-X', type=str, default='0.7',
                    help="string for X (default='0.7')")
parser.add_argument('-Z', type=str, default='0.02',
                    help="string for Z (default='0.02')")
args = parser.parse_args()

key = 'z%s_x%s' % (args.Z, args.X)

import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import RectBivariateSpline as RBS
import os

with open('%s/data/kap_data/gs98_%s.data' % (os.environ['MESA_DIR'], key),'r') as f:
    lines = f.readlines()

opac1 = np.loadtxt(lines[7:])[:,1:].T
logT1 = np.loadtxt(lines[7:])[:,0]
logR1 = np.loadtxt(lines[5:6])

with open('%s/data/kap_data/lowT_fa05_gs98_%s.data' % (os.environ['MESA_DIR'], key),'r') as f:
    lines = f.readlines()

opac2 = np.loadtxt(lines[7:])[:,1:].T
logT2 = np.loadtxt(lines[7:])[:,0]
logR2 = np.loadtxt(lines[5:6])

Rmin = min(np.min(logR1), np.min(logR2))
Rmax = max(np.max(logR1), np.max(logR2))
Tmin = min(np.min(logT1), np.min(logT2))
Tmax = max(np.max(logT1), np.max(logT2))

i1 = np.where(logT1>=4.)[0][0]
i2 = np.where(logT2<4.)[0][-1]

interpolator1 = RBS(logR1, logT1, opac1)
interpolator2 = RBS(logR2, logT2, opac2)

for rho in np.arange(-10.,0.1,2.):
    T = np.linspace(Tmin, Tmax, 200)
    R = rho - 3.*T + 18.
    T = T[(R>Rmin)&(R<Rmax)]
    R = R[(R>Rmin)&(R<Rmax)]

    # c = np.hstack((interpolator2(R[:i2],T[:i2]), interpolator1(R[i1:],T[i1:])))
    c = [interpolator2(Ri,Ti) for (Ri,Ti) in zip(R,T) if Ti<4.] + \
        [interpolator1(Ri,Ti) for (Ri,Ti) in zip(R,T) if Ti>=4.]
    c = np.squeeze(c)
    pl.plot(T, c, '-', color=pl.cm.viridis((rho+10)/10))
    # pl.loglog(10**T, 10**c, '-', color=pl.cm.viridis((rho+10)/10*0.9))

pl.xlabel(r'$\log_{10}(T/\mathrm{K})$')
pl.ylabel(r'$\log_{10}(\kappa_\mathrm{R}/(\mathrm{cm}^2/\mathrm{g}))$')
# pl.xlabel('temperature (K)')
# pl.ylabel('Rosseland mean opacity (cm²/g)')
pl.show()
