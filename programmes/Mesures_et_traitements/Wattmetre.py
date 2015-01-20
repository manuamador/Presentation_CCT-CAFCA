# -*- coding: utf-8 -*-
"""
Created on Mon Nov 05 15:17:13 2012
Classe de contrîole du Wattmètre
@author: emmanuel.amador@edf.fr
"""

from visa import instrument

class RS_NRVD():
    """ Classe de type visa pour le wattmètre double entrée R&S.
    Args:
        * portname (str): nom du port et adresse
    """
    def __init__(self,address=20):
        self.ctrl = instrument("GPIB::%s" %address)
    
    def reset(self):
        """ RESET """
        self.ctrl.write("*RST")
        self.ctrl.write(":SENS1:POW:UNIT dBm;:CALC1:FILT:NSEL 2")
        self.ctrl.write(":SENS2:POW:UNIT dBm;:CALC2:FILT:NSEL 2")
        self.ctrl.write(":SENS1:VOLT:ATT 0;:SENS2:VOLT:ATT 0")
        self.ctrl.write("CORR:FREF:STAT ON")
        print('OK')
        return True
        
    def getPowA(self,freq):
        """ Fais la mesure sur l'entrée A"""
        self.ctrl.write("CORR:FREF %s Hz" %freq)
        s=self.ctrl.ask("INP:NSEL 1;*TRG")
        return eval(s[1:])
        
    def getPowB(self,freq):
        """ Fais la mesure sur l'entrée B"""   
        self.ctrl.write("CORR:FREF %s Hz" %freq)        
        s=self.ctrl.ask("INP:NSEL 2;*TRG")
        return eval(s[1:])
