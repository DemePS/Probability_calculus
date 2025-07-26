# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:46:52 2022

@author: Deme
"""

from utils import load_structure, names_nodes
from Tree_class import *


#Tree built from scratch
T=Tree("A")
T.draw("Tree_before_weights")
print(T.get_n_parameters())
# Suppose T.get_n_parameters() returns 3
T.set_weights([0.5,0.3,0.8])
T.draw("Tree_after_weights")
T.compute_prob("DTG") 
