# -*- coding: utf-8 -*-
"""
Created on Fri Nov 02 07:56:07 2012
Pilotage CRBM, mesures de champ et puissance
@author: Emmanuel Amador emmanuel.amador@edf.fr
"""

from __future__ import division
import time
from numpy import *
import visa
import os

#Chargement des classes du matériel employé
from Brasseur import * #classe du brasseur de la CRBM
from Sondedechamp import * #classe générique des sondes de champ contiendra tous les modèles
from Generateur import * #classe générique des générateurs contiendra tous les modèles
from Wattmetre import *   #classe générique des wattmètres contiendra tous les modèles

###############################################
########## Paramètres de l'essai ##############
###############################################

#Préfixe des fichiers #########################
##JJ-MM-AAAA_HHhMM
timestamp=time.localtime()
nom=str(timestamp[0])+'-'+str(timestamp[1])+'-'+str(timestamp[2])+'_'+str(timestamp[3])+\
    'h'+str(timestamp[4])#'Nom_de_l\'essai'
t0=time.clock()
nom="calibrage_rapide_0.8-2"


if (os.path.isdir('resultats/'+nom)==False):
    os.mkdir('resultats/'+nom)

os.chdir('resultats/'+nom)

#Fréquences####################################
f0=800e6 #fréquence de départ
f1=2000e6 #dernière fréquence

#---->fréquences uniformément réparties
Nf=61 #nombre de fréquence
f=linspace(f0,f1,Nf) #liste des fréquences testées

#Brasseur######################################  
N=150 # nombre de positions du brasseur
Angles=linspace(360/N,360,N) #liste des positions en degré


P=-30 #Niveau injecté testé en dBm (unn calibrage de la chambre permettra de\
        # donner directement le niveau dansd la chambre)

print '_______________\nInitialisations\n'
###############################################
###### Initialiation des instruments ##########
###############################################
print '\nInitialisation du brasseur:'
brasseur=Brasseur('/com2',1)
print 'Retour a la position 0...'
brasseur.reset()

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
Puissance=zeros((len(Angles),len(f))) #Matrice de la mesure de la puissance dans la chambre 
Champ=zeros((len(Angles),len(f),3)) #Matrice de la mesure de champ dans la chambre 

gene.setFreq(f0)
gene.setPower(-30)
gene.marche()
while (wmetre.getPowA(f0)<-20):
    raw_input("!!Allumer l'ampli et appuyer sur n'importe quelle touche pour continuer...")
gene.arret()

print '10 secondes d\'attente'
time.sleep(10) #pour que l'ampli soit bien relancé

#boucle sur les frequences
for i in range(0,len(Angles)):
    brasseur.setPosition(int(Angles[i]))
    time.sleep(5)
    print 'N = %3d' %(i+1)
    for j in range(0,len(f)):
        gene.setFreq(f[j])
        gene.setPower(P)
        gene.marche()
        time.sleep(0.5)
        Puissance[j]=wmetre.getPowA(f[j])
        Champ[i,j,:]=sonde.getChamp()
        print 'f = %2.2f MHz, Ex= %2.2f, Ey= %2.2f, Ez= %2.2f, Et= %2.2f V/m' \
            %(f[j]/1e6,Champ[i,j,0],Champ[i,j,1],Champ[i,j,2],sqrt(sum(Champ[i,j,:]**2)))
        gene.arret()

gene.reset()  #RAZ du géné
t1=time.clock() #pour la durée de la mesure

##Sauvegarde en binaire dans un fichier numpy
##tableaux à 4 dimensions, Angle x fréquence x puissance x données
print '\n\nSauvegarde au format numpy zip (npz)'
fnamez = nom + '.npz'
savez(nom,P=P,f=f,Puissance=Puissance,Champ=Champ)

alphax=mean(Champ[:,:,0],axis=0)/sqrt(10**(P/10)/1000)
alphay=mean(Champ[:,:,1],axis=0)/sqrt(10**(P/10)/1000)
alphaz=mean(Champ[:,:,2],axis=0)/sqrt(10**(P/10)/1000)

alpha=vstack((alphax,alphay,alphaz)).mean(axis=0)
savetxt('alpha0.8-2_CRBM.txt',alpha)


