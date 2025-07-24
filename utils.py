# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 09:33:06 2022

@author: Deme
"""
import pickle
import numpy  as np

def weights_path(path):
    weights=[node.weight for node in path]
    return weights

def names_nodes(path):
    f=lambda A: A.name
    F=np.vectorize(f)
    return F(path)

def load_structure(file_name):
    with open(file_name, "rb") as infile:
        Tree = pickle.load(infile)
        return Tree

def to_string(weight):
    if weight==None:
        return ""
    return str(round(weight,4))

def ordinal(n):
    if n==1:
        return "1st"
    if n==2:
        return "2nd"
    if n==3:
        return "3rd"
    return str(n)+"th"

