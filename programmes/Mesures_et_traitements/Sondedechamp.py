# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 13:23:16 2012
Classe de contrôle des sondes de champ
@author: emmanuel.amador@edf.fr
"""

from visa import *
from numpy import *
import time


class DARE_CTR1002A():
    """ Classe de type pyVISA pour la mesure de champ avec l'interface DARE
    """
    def __init__(self):
        self.ctrl = instrument("ASRL3::INSTR",timeout=1,baud_rate=57600,term_chars="\n")

    def reset(self):
        self.ctrl.time_out=1
        s=self.ctrl.ask("*IDN?")
        if (s=='D.A.R.E!! RadiCentre2 version 1.2.38'):
            print 'IDN OK'
        s=self.ctrl.ask("P1:C2")
        if (s==':C'):
            print 'Liaison OK'
        s=self.ctrl.ask("P1:AEEE") #????????
        if (s==':A'):
            print 'Trois Axes OK'
        s=self.ctrl.ask("P1:R4")
        if (s==':R4'):
            print 'Calibre OK'
        s=self.ctrl.ask("P1:Filter_1")
        if (s==':F'):
            print 'Pas de lissage'

    def zero(self):
        self.ctrl.time_out=0.05
        """ fais le Zero de la mesure éteindre toutes les sources avant !"""
        self.ctrl.write("P1:ZERO")
        time.sleep(5)
        s=self.ctrl.read()        
        if (s==':Z'):
            print('Zero OK')
        
    def getChamp(self):
        """ Mesure des troix axes"""
        s=(self.ctrl.ask("P1:D3"))
        ch=(((s[2:len(s)-2]).split(';')))
        return array([eval(ch[0]),eval(ch[1]),eval(ch[2])])
        

class DARE_CTR1001S():
    """ Classe de type pyVISA pour la mesure de champ avec l'interface DARE
    Args:
        * portname (str): nom du port
        * baudrate (int): vitesse du port série (1)
        * term_chars    : charactères de fin de ligne
    """
    def __init__(self):
        self.ctrl = instrument("ASRL1::INSTR",baud_rate=9600,data_bits=7,parity=odd_parity)
        self.ctrl.parity=odd_parity

    def reset(self):
        self.ctrl.time_out=1
        s=self.ctrl.ask("*IDN?")
        if (s=='D.A.R.E!! RadiCentre2 version 1.2.38'):
            print 'IDN OK'
        s=self.ctrl.ask("C2")
        if (s==':C'):
            print 'Liaison OK'
        s=self.ctrl.ask("AEEE") #????????
        if (s==':A'):
            print 'Trois Axes OK'
        s=self.ctrl.ask("R4")
        if (s==':R4'):
            print 'Calibre OK'
        s=self.ctrl.ask("Filter_1")
        if (s==':F'):
            print 'Pas de lissage'

    def zero(self):
        self.ctrl.time_out=0.05
        """ fais le Zero de la mesure éteindre toutes les sources avant !"""
        self.ctrl.write("ZERO")
        time.sleep(5)
        s=self.ctrl.read()        
        if (s==':Z'):
            print('Zero OK')
        
    def getChamp(self):
        """ Mesure des troix axes"""
        s=(self.ctrl.ask("D3"))
        ch=(((s[2:len(s)-2]).split(';')))
        return array([eval(ch[0]),eval(ch[1]),eval(ch[2])])
