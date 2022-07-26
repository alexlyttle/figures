#!/usr/bin/env python

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--highlight', type=str, nargs='+', default=[],
                    help="isotopes to highlight, e.g. C12, Fe56")
parser.add_argument('--xticks', type=int, nargs='+', default=None,
                    help="place xticks only at these points")
parser.add_argument('--logx', action='store_true',
                    help="make x-axis logarithmic")
parser.add_argument('--logy', action='store_true',
                    help="make y-axis logarithmic")
args = parser.parse_args()

import numpy as np
from matplotlib import pyplot as pl

if args.logx:
    if args.logy:
        plotter = pl.loglog
    else:
        plotter = pl.semilogx
else:
    if args.logy:
        plotter = pl.semilogy
    else:
        plotter = pl.plot

url = 'https://www-nds.iaea.org/amdc/ame2016/mass16.txt'
filename = 'data/mass16.txt'
delimiter = (1,3,5,5,5,4,4,14,11,11,9,3,11,9,4,13,11)
dtype = [('cc','|S1'), ('NZ',int), ('N',int), ('Z',int),
         ('A',int), ('symbol', '|S4'), ('O', '|S4'),
         ('excess',float), ('e_excess',float), ('B',float),
         ('e_B',float)]
# format    :  a1,i3,i5,i5,i5,1x,a3,a4,1x,f13.5,f11.5,f11.3,f9.3,1x,a2,f11.3,f9.3,1x,i3,1x,f12.5,f11.5
#              cc NZ  N  Z  A    el  o     mass  unc binding unc     B  beta  unc    atomic_mass   unc

try:
    data = np.genfromtxt(filename, dtype=dtype, delimiter=delimiter, skip_header=39)
except IOError:
    try:
        from urllib2 import Request, urlopen
        req = Request(url, headers={'User-Agent' : "Magic Browser"})
    except ImportError:
        from urllib.request import Request, urlopen
        req = Request(url, headers={'User-Agent' : "Magic Browser"})

    response = urlopen(req)
    with open(filename, 'wb') as f:
        f.write(response.read())

    response.close()

    data = np.genfromtxt(filename, dtype=dtype, delimiter=delimiter, skip_header=39)

plotter(data['Z'][1:], data['B'][1:]/1e3, 'ko', ms=6, alpha=0.5) # 1st element is the neutron

# create a dict of symbol -> Z
symbols, I = np.unique(data['symbol'], return_index=True)
Zs = {symbol.decode().strip(): Z for symbol, Z in zip(symbols, data['Z'][I])}

for h in args.highlight:
    symbol, A = '', ''
    for c in h:
        if c.isalpha():
            symbol += c
        else:
            A += c
    A = int(A)

    row = data[(data['A']==A)&(data['Z']==Zs[symbol])]
    plotter(row['Z'], row['B']/1e3, 'o')

if args.xticks:
    pl.xticks(args.xticks, ['%i' % tick for tick in args.xticks]);

pl.xlabel('atomic number')
pl.ylabel('binding energy per nucleon (MeV)')
pl.show()
