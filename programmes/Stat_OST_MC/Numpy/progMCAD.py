#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Code permettant d'évaluer,la statistique des composantes cartésiennes du champ
rayonné par une sphère de rayon R_eut dotée de n dipoles de Hertz disposés
aléatoirement à sa surface en fonction de ses dimensions électriques et de sa
complexité. La statitistique est évaluée à partir de N mesures. M objets
quelconques sont simulés.

Auteur: Emmanuel Amador (emmanuel.amador@edf.fr)

"""

from __future__ import division
from numpy import *
from numpy.random import *
from pylab import *
from pylab import rcParams
from scipy.stats import *
import os
from champE import champElointain

c = 299792458.0
ka=logspace(-1,2,50)#linspace(0.1,20,200) #valeurs de $ka$ désirées
R_eut=1. #Rayon de l'objet sphérique en m
f=ka*c/2/pi/R_eut

R = 1000 #distance en m du point de mesure

N=100 #nombre de points pour estimer le champ rayonné
M=100 #nombre de simus de Monte Carlo 

#Matrices des champs, $E_\theta$ et $E_\phi$ et $E_r$

n_dipole=arange(1,5) #nombre de dipole $n$

ADth=zeros((len(f),len(n_dipole),M))
ADph=zeros((len(f),len(n_dipole),M))
resth=zeros((len(f),len(n_dipole),M))
resph=zeros((len(f),len(n_dipole),M))

for n in n_dipole:
    #on tire aléatoirement les coordonnées sphériques des points de mesure
    phi=2*pi*rand(N) 
    theta=arccos(2*rand(N)-1)
    print('%3d dipole(s)' %(n))
    for j in range(0,M): #boucle sur les M objets
        print('%3d/%3d' %(j+1,M))
        #création de l'objet rayonnant
        theta_eut=arccos(2*rand(n,1)-1) 
        phi_eut=2*pi*rand(n,1)
        x=R_eut*cos(phi_eut)*sin(theta_eut)
        y=R_eut*sin(phi_eut)*sin(theta_eut)
        z=R_eut*cos(theta_eut)
        tilt=arccos(2*rand(n,1)-1)
        azimut=2*pi*rand(n,1)
        ld=.1      
        amplitude=ones((n,1))*ld
        phas=2*pi*rand(n,1)
        #matrice des dipôles
        I=concatenate((x,y,z,tilt,azimut,amplitude,phas), axis=1)
        #Calcul du champ rayonné en espace libre
        Ethac,Ephac=champElointain(R,theta,phi,I,f)
        
        #Test d'Anderson Darling
        for i in arange(len(f)):  
            A,vc,perc=anderson(Ethac[:,i]**2,'expon')
            ADth[i,n-1,j]=A
            erreurth=perc[A<vc]/100
            if len(erreurth)==0:
                resth[i,n-1,j]=1.
            else:
                resth[i,n-1,j]=min(erreurth)
            B,vc,perc=anderson(Ephac[:,i]**2,'expon')
            ADph[i,n-1,j]=B
            erreurph=perc[B<vc]/100
            if len(erreurph)==0:
                resph[i,n-1,j]=1.
            else:
                resph[i,n-1,j]=min(erreurph)
    print (0.5*resph[:,n-1,:].mean(axis=1)+0.5*resth[:,n-1,:].mean(axis=1))
        

savez('../fig/EUTs_TestAD.npz',ADph=ADph,ADth=ADth,resph=resph,resth=resth,n_dipole=n_dipole,ka=ka)

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

fig.savefig('../fig/TestAD.pdf',bbox='tight')

