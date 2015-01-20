# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 10:45:00 2013
Classe du générateur de signaux
@author: emmanuel.amador@edf.fr
"""

from visa import instrument

class RS_SMF100A():
    def __init__(self,address=28):
        self.ctrl = instrument("GPIB::%s" %address)
        self.powmax=15 #pour les amplis MilMega/M2S
    
    def reset(self):
        """ RESET """
        self.ctrl.write("*RST;*WAI")
        self.ctrl.write("*ESE 1;*SRE 32;OUTP1 OFF")
        self.ctrl.write("PULM:SOUR INT;:PULM:STAT OFF")
        print 'OK'
        return True
    
    def arret(self):
        """ RF OFF """
        return self.ctrl.write("*CLS;OUTP1 OFF")
    
    def marche(self):
        """ RF ON """
        return self.ctrl.write("*CLS;OUTP1 ON")
    
    def setPower(self,value):
        """ fixe le niveau de sortie"""
        if value>self.powmax:
            print '!!!!!!!\n!!! Puissance trop grande !!!\n!!!!!!!!!'
            self.ctrl.write("*CLS;POW %s dbm" %powmax)
        else:
            self.ctrl.write("*CLS;POW %s dbm" %value)
        
    def setFreq(self,value):
        """ fixe la fréquence de sortie"""
        s='"*CLS;FREQ '+str(int(value))+' HZ"'
        return self.ctrl.write("*CLS;FREQ %s HZ" %value)
