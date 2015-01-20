# -*- coding: utf-8 -*-
"""
Created on Wed Aug 07 11:42:12 2013

@author: e68972
"""

from __future__ import division
from pylab import *
import matplotlib.pyplot  as pyplot
from numpy import *



res=load('../fig/EUTs_TestAD.npz')
resth=res['resth']
resph=res['resph']
ADph=res['ADph']
ADth=res['ADth']
n_dipole=res['n_dipole']
ka=res['ka']


fig = figure(num=1)
fig.add_subplot(1,1,1)
im=pyplot.contourf(n_dipole,ka,1-(0.5*resth.mean(axis=2)+0.5*resph.mean(axis=2)),(0,0.5,0.75,0.85,0.90,0.95,0.99))
pyplot.yscale('log')
ylim(0.1,100)
grid()
title(u'Probabilité d\'observer une distribution de Rayleigh')
cbar1=colorbar(im)
cbar1.set_label(r'$p$')
xlabel(r'$n$')
ylabel(r'$ka$')

fig.savefig('../fig/TestADb.pdf',bbox='tight')

