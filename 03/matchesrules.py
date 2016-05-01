# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""
#matchrules.py V. 150423

def take_0_poss(zustand):
    # test ob ueberhauot schon so viele zuege gemacht wurden:
    if len(zustand)>1:  # zustand besteht aus noch da und pfad -> koennen nicht 4 auf einmal gezogen werden, also it nur 0 drin, wenn 0 gezogen wurden.
        if (zustand[-1] != "0" and zustand[-2] != "0"):
            return True
        else:
            return False
    else:
        return True  # zustand besteht aus noch da und pfad, wenn zustand nur aus noch_da besteht, wurde nichts gezogen -> man darf 0 ziehen.
        
def take_1_poss(zustand):
    # kann immer gezogen werden!
    return True
    
def take_2_poss(zustand):
    if int(zustand[0]) > 2:
        return True
    else:
        return False