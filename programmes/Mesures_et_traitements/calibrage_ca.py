# -*- coding: utf-8 -*-
"""
Created on Fri Nov 02 07:56:07 2012
Pilotage CA, pour réaliser un étalonnage
@author: Emmanuel Amador emmanuel.amador@edf.fr
"""

from __future__ import division
import time
from numpy import *
import visa
import os

#Chargement des classes du matériel employé
#from Brasseur import * #classe du brasseur de la CRBM... 
from Sondedechamp import * #classe générique des sondes de champ contiendra tous les modèles
from Generateur import * #classe générique des générateurs contiendra tous les modèles
from Wattmetre import *   #classe générique des wattmètres contiendra tous les modèles

###############################################
########## Paramètres de l'essai ##############
###############################################

#Préfixe des fichiers #########################
##JJ-MM-AAAA_HHhMM
timestamp=time.localtime()
nom=str(timestamp[0])+'-'+str(timestamp[1])+'-'+str(timestamp[2])+'_'+str(timestamp[3])\
    +'h'+str(timestamp[4])#'Nom_de_l\'essai'
t0=time.clock()
os.mkdir('resultats/'+nom)
os.chdir('resultats/'+nom)

#Fréquences####################################
f0=800e6 #fréquence de départ
f1=2000e6 #dernière fréquence

#---->fréquences uniformément réparties
Nf=61 #nombre de fréquence
f=linspace(f0,f1,Nf) #liste des fréquences testées

P=0 #PNiveau injecté testé en dBm 

print '_______________\nInitialisations\n'
###############################################
###### Initialiation des instruments

print '\nInitialisation du generateur:'
gene=RS_SMF100A()
gene.reset()
gene.arret() #RF OFF
gene.setPower(P)
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
Puissance=zeros(len(f)) #Matrice de la mesure de la puissance dans la chambre 
Champ=zeros((len(f),3)) #Matrice de la mesure de champ dans la chambre 


Mesure=zeros((1,6))
#boucle sur les frequences
for j in range(0,len(f)):
    gene.setFreq(f[j])
    gene.setPower(P)
    gene.marche()
    time.sleep(0.5)
    Puissance[j]=wmetre.getPowA(f[j])
    Champ[j,:]=sonde.getChamp()
    Mesure=vstack((Mesure,array([f[j],P,Puissance[j],Champ[j,0],Champ[j,1],Champ[j,2]])))
    print 'f = %2.2f MHz, Ex= %2.2f, Ey= %2.2f, Ez= %2.2f, Et= %2.2f V/m' \
        %(f[j]/1e6,Champ[j,0],Champ[j,1],Champ[j,2],sqrt(sum(Champ[j,:]**2)))
    gene.arret()
# Sauvegarde des mesures à chaque pas du mat #
fname = nom + '_alpha.txt' 
#Format du fichier:
print 'Sauvegarde des mesures...'
savetxt(fname,Mesure[1:,:])
print 'OK'

gene.reset()  #RAZ du géné
t1=time.clock() #pour la durée de la mesure

##Sauvegarde en binaire dans un fichier numpy
##tableaux à 4 dimensions, Angle x fréquence x puissance x données
print '\n\nSauvegarde au format numpy zip (npz)'
fnamez = nom + '.npz'
savez(nom,P=P,f=f,Puissance=Puissance,Champ=Champ)

#calcul de alpha
os.chdir('..')
os.chdir('..')
alphaz=Champ[:,2]/sqrt(10**(P/10)/1000)

savetxt('alpha.txt',alphaz)

