# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 08:19:30 2013


"""
from __future__ import division
from numpy import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D



rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True
rcParams['legend.fontsize'] = 'medium'
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})

Zissou_map =   {'red':  ((0., 60./255, 60./255),
                         (0.25, 120./255, 120./255),
                         (0.5, 235./255, 235./255),
                         (0.75, 225./255, 225./255),
                         (1,  242./255, 242./255)),
               'green':  ((0.,  154./255, 154./255),
                         (0.25, 183./255, 183./255),
                         (0.5,  204./255, 204./255),
                         (0.75,  175./255, 175./255),
                         (1, 35./255, 35./255)),
               'blue':  ((0., 178./255, 178./255),
                         (0.25, 197./255, 197./255),
                         (0.5, 42./255, 42./255),
                         (0.75, 0./255, 0./255),
                         (1, 0./255, 0./255))}

Zissou_cmap = matplotlib.colors.LinearSegmentedColormap('Zissou_colormap',Zissou_map,4096)



def traitement(filename):
    a=genfromtxt(filename,skiprows=2,usecols=(2,3,4,5,6))
    Eth=reshape(a[:,1],(360,181))
    Eph=reshape(a[:,3],(360,181))
    P=Eth**2+Eph**2
    D=reshape(a[:,0],(360,181))
    return P,D,Eth,Eph
    

P800,D800,Eth800,Eph800=traitement('F800MHZ.txt')
P2000,D2000,Eth2000,Eph2000=traitement('F2GHZ.txt')
P4000,D4000,Eth4000,Eph4000=traitement('F4GHZ.txt')

f=array([800e6,2e9,4e9])

Eth=zeros((360,181,3))
Eth[:,:,0]=Eth800
Eth[:,:,1]=Eth2000
Eth[:,:,2]=Eth4000

Eph=zeros((360,181,3))
Eph[:,:,0]=Eph800
Eph[:,:,1]=Eph2000
Eph[:,:,2]=Eph4000

P=zeros((360,181,3))
P[:,:,0]=P800
P[:,:,1]=P2000
P[:,:,2]=P4000


D=zeros((360,181,36))
D[:,:,0]=D800
D[:,:,1]=D2000
D[:,:,2]=D4000


phi=linspace(1,360,360)*pi/180
theta=linspace(0,180,181)*pi/180

for u in range(0,len(f)):
    #D=(P[:,:,u]).max()/(P[:,:,u]).mean() #calcul de la directivité $D_{\max}$
    fig = figure(figsize=(12, 12), dpi=50)
    ax = fig.add_subplot(111, projection='3d', frame_on=False)
    ax._axis3don = False
    R = D[:,:,u]/(D[:,:,u]).max()
    x = R  * outer(cos(phi), sin(theta))
    y = R  * outer(sin(phi), sin(theta))
    z = R  * outer(ones_like(phi), cos(theta))
    ax.azim=-80
    ax.plot_surface(x, y, z,  rstride=1, cstride=1, facecolors=Zissou_cmap(R),\
        linewidth=1,shade=True,antialiased=False)
    max_radius = 0.7
    print('f= %2.1f MHz, Directivité = %2.1f' %(f[u]/1e6,D[:,:,u].max()))
    for axis in 'xyz':
        getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))
    fname = 'Pka_%s_%2.1f' %(f[u]/1e6,D[:,:,u].max())
    print 'Saving frame', fname
    fig.savefig(fname+'.png',bbox='tight')
    #fig.savefig(fname+'.svg',bbox='tight')
    #fig.savefig(fname+'.pdf',bbox='tight')
    close()
