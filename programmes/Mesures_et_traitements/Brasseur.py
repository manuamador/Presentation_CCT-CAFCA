# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 17:18:33 2012
Classe Brasseur
@author: emmanuel.amador@edf.fr
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 13:23:16 2012

@author: Administrateur
"""
import minimalmodbus
import time
from numpy import *

class Brasseur(minimalmodbus.Instrument):
    """ Classe de type Instrument pour le brasseur de la CRBM des Renardières.
    Args:
        * portname (str): nom du port
        *slaveaddress (int): adresse de l'escloave RTU (1)
    """
    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self,portname,slaveaddress)
        self.serial.baudrate = 9600
        self.serial.bytesize = 8
        self.serial.stopbits = 1
        self.serial.timeout = 0.05
    
    def reset(self):
        """ retoune à la position 0"""
        self.write_long(57766,0)
        posmesuree=self.read_long(58144,3)     
        while posmesuree != 0:
            posmesuree=self.read_long(58144,3)            
            time.sleep(.5)
        print 'Reset OK' 
    
    def getPosition(self):
        """ retourne la position du brasseur"""
        return self.read_long(58144,3)
    
    def setPosition(self,position):
        """ déplacement vers l'angle donné +/- angle en degrès"""
        self.write_long(57766,position*10,signed=True)      
        posmesuree=nan
        while posmesuree != position*10:
            posmesuree=self.read_long(58144,3)            
            time.sleep(.1)
