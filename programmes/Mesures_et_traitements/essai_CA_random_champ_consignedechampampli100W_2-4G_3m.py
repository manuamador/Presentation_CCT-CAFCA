
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 02 07:56:07 2012
Pilotage chambre anéchoique, mesures de champ et puissance
@author: emmanuel.amador@edf.fr
"""

from __future__ import division
import time
from numpy import *
import visa
import os
from numpy import random

#Chargement des classes du matériel employé
from Sondedechamp import * #classe générique des sondes de champ contiendra tous les modèles
from Generateur import * #classe générique des générateurs contiendra tous les modèles
from Wattmetre import *   #classe générique des wattmètres contiendra tous les modèles

###############################################
########## Paramètres de l'essai ##############
###############################################

#fichier de calibrage
alpha=loadtxt('alpha2-4.txt')


#Préfixe des fichiers #########################
##JJ-MM-AAAA_HHhMM
timestamp=time.localtime()
date=str(timestamp[0])+'-'+str(timestamp[1])+'-'+str(timestamp[2])+'_'+\
    str(timestamp[3])+'h'+str(timestamp[4])#'Nom_de_l\'essai'
t0=time.clock()
nom="essai_random_2-4"

os.chdir('resultats/'+nom)

#Fréquences####################################
f0=2000e6 #fréquence de départ
f1=4000e6 #dernière fréquence

#---->fréquences uniformément réparties
Nf=41 #nombre de fréquence
f=linspace(f0,f1,Nf) #liste des fréquences testées


#Positions testées######################################  
N=30 # nombre de positions du mat

Angles=loadtxt('Angles2-4.txt') #angles tirés aléatoirement
polar=loadtxt('Polar2-4.txt') #polarisations

#Niveaux de consigne ##################################

E=empty(8)
for i in range(0,len(E)):
    E[i]=1.8**i

Pconsigne=zeros((len(E),len(f)))

for i in range(0,len(E)):
    Pconsigne[i,:]=10*log10((E[i]/alpha)**2*1000)


print '_______________\nInitialisations\n'
###############################################
###### Initialiation des instruments ##########
###############################################

print '\nInitialisation du generateur:'
gene=RS_SMF100A()
gene.reset()
gene.arret() #RF OFF
gene.setPower(Pconsigne[0,0])
gene.setFreq(f0)

print '\nInitialisation des sondes de champ DARE:'
print 'DARE_CTR1001S'
sonde=DARE_CTR1001S()
sonde.reset()
print 'Zeroing...'
sonde.zero()

##print '\nInitialisation du Wattmetre:'
wmetre=RS_NRVD()
wmetre.reset()

print '_______\nMesures\n'
###############################################
################# Mesure ######################
###############################################

Champconsigne=zeros((len(Angles),len(f),len(E))) #Mesure de la puissance injectée 
PuissanceB=zeros((len(Angles),len(f),len(E))) #Mesure de la puissance dans la chambre 
Champ=zeros((len(Angles),len(f),len(E),3)) #Mesure de champ dans la chambre

for i in range(0,len(Angles)): #boucle sur les positions du mat
    Mesure=zeros((1,8))
    #brasseur.setPosition(int(Angles[i]))
    if (polar[i]==0):
        polarisation="Polarisation V"
    else:
        polarisation="Polarisation H"
    print 'Placer l\'EUT selon l\'angle = %2.2f, %s\n' %(Angles[i],polarisation)
    raw_input(" Allumer l'ampli et appuyer sur n'importe quelle touche pour continuer...")
    gene.setFreq(f0)
    gene.setPower(-30)
    gene.marche()
    while (wmetre.getPowA(f0)<-20):
        raw_input("Allumer l'ampli et appuyer sur n'importe quelle touche pour continuer...")
    gene.arret()
    time.sleep(10) #pour que l'ampli soit bien relancé
    for k in range(0,len(E)):
        print 'Champ consigne = %2.2f V/m' %(E[k])
        #boucle sur les frequences
        for j in range(0,len(f)):
            gene.setFreq(f[j])
            gene.setPower(Pconsigne[k,j])
            gene.marche()
            time.sleep(0.2)
            Champconsigne[i,j,k]=E[k]#wmetre.getPowA(f[j])
            PuissanceB[i,j,k]=wmetre.getPowA(f[j])
            Champ[i,j,k,:]=sonde.getChamp()
            #Champ2[i,j,k,:]=sonde2.getChamp()
            Mesure=vstack((Mesure,array([Angles[i],f[j],E[k],Champconsigne[i,j,k],\
                PuissanceB[i,j,k],Champ[i,j,k,0],Champ[i,j,k,1],Champ[i,j,k,2]])))
            print 'f = %2.2f MHz, Ex= %2.2f, Ey= %2.2f, Ez= %2.2f, Et= %2.2f V/m'\
                %(f[j]/1e6,Champ[i,j,k,0],Champ[i,j,k,1],Champ[i,j,k,2],\
                sqrt(sum(Champ[i,j,k,:]**2)))
            gene.arret()
        gene.arret()
    gene.arret()
    # Sauvegarde des mesures à chaque pas du mat #
    fname = nom + '_Pos_%03d.txt'%(i+1) #1 fichier par position de brasseur
    #Format du fichier:
    print 'Sauvegarde des mesures pour la position %3d/%3d...' %(i+1,N)
    savetxt(fname,Mesure[1:,:])
    fnamez = nom +'_'+str(i+1)+'.npz'
    savez(nom,Angles=Angles,Polar=polar,f=f,\
        Champconsigne=Champconsigne,PuissanceB=PuissanceB,Champ=Champ)
    print 'OK'


gene.reset()  #RAZ du géné
t1=time.clock() #pour la durée de la mesure

##Sauvegarde en binaire dans un fichier numpy
##tableaux à 4 dimensions, Angle x fréquence x puissance x données
print '\n\nSauvegarde au format numpy zip (npz)'
fnamez = nom + '.npz'
savez(nom,Angles=Angles,Polar=polar,f=f,Champconsigne=Champconsigne,\
    PuissanceB=PuissanceB,Champ=Champ)

#Résumé de la mesure à réaliser
elapsed=t1-t0
minutes, secondes = divmod(elapsed, 60)
heures, minutes = divmod(minutes, 60)

fichier_resume = open('./resume_'+nom+'.txt', 'w')
fichier_resume.write('----------------------------------------------------\n')
fichier_resume.write('---------------- Résumé de la mesure ---------------\n')
fichier_resume.write('----------------  '+str(timestamp[2])+'.'+str(timestamp[1])+'.'\
    +str(timestamp[0])+' à '+str(timestamp[3])+':'+str(timestamp[4])+'  ---------------\n')
fichier_resume.write('----------------------------------------------------\n\n')
fichier_resume.write('Durée de la mesure:\t\t'+str(int(heures))+' heure(s) '+\
    str(int(minutes))+' minute(s) '+str(int(secondes))+' seconde(s)'+'\n')
fichier_resume.write('Fréquence de départ:\t\t'+str(f0/1e6)+'\tMHz\n')
fichier_resume.write('Fréquence de fin:\t\t'+str(f1/1e6)+'\tMHz\n')
fichier_resume.write('Champ consigne min.:\t'+str(E.min())+'\tV/m\n')
fichier_resume.write('Champ consigne max.:\t'+str(E.max())+'\tV/m\n')
fichier_resume.write('Nombre d\'angles:\t'+str(int(N))+'\n')
fichier_resume.close()
