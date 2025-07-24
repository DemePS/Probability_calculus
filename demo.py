# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:46:52 2022

@author: Deme
"""

from utils import load_structure, names_nodes
from Tree_class import *

#Loaded tree
T1=load_structure("ABC_tree")
T1.n_parameters
#T1.draw("ART_before_weights")
T1.set_weights([0.5,0.3,0.8])
#T1.draw("ART_after_weights")
a=T1.compute_prob("DTG")
b=T1.compute_prob("EFV")
c=T1.compute_prob("EFV/r")
for ART in ["DTG","EFV","EFV/r"]:
    print(ART,":")
    T1.print_pathes(ART)
    print("\n")

"""
#Tree built from scratch
T2=Tree("A")
T2.save_structure("tree_tuto")
T2.n_parameters
#T2.draw("ART_before_weights")
T2.set_weights([0.5,0.3,0.8])
#T2.draw("ART_after_weights")
T2.ART_LeafNodes["DTG"][0].name
T2.ART_LeafNodes["DTG"][0].compute_prob()
"""
T3=Tree("EFV_as_ART2")
T3.draw("EFV_as_ART2_tree")
T3.get_n_parameters()
n=T3.get_n_parameters()
L=[i/20 for i in range(1,n+1)]
T3.set_weights(L)
T3.save_structure("EFV_as_ART2_tree")
T3.reset_weights()
type(T3.get_LeafNodes_names("EFV"))
names_nodes(T3.left.child_nodes)