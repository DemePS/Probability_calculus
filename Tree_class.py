# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 09:04:31 2022

@author: Deme
"""
import numpy as np
from utils import weights_path, names_nodes, to_string, ordinal
import pickle 
import graphviz 


class Node:
    def __init__(self,name,weight=None,path=[]):
        self.name=name
        self.weight=weight
        self.path=path
        self.node_id=0
        
    def set_weight(self,weight):
        self.weight=weight
        
        
class LeafNode(Node):
    def isLeafNode(self):
        return True
    
    def compute_prob(self):
        weights=weights_path(self.path)
        prob=np.prod(weights)*self.weight
        return prob
    
    def print_path_from_root(self):
        names=names_nodes(self.path)
        for name in names:
            print(name, end="--> ")
        print(self.name)
        
class ParentNode(Node):
    def __init__(self,name,right=None,left=None,weight=None,path=[]):
        super().__init__(name,weight,path)
        self.right=right
        self.left=left
        
    def isLeafNode(self):
        return False

    def isBinaryNode(self):
        return True

class MultiNode(Node):
    def __init__(self,name,child_nodes=[],weight=None,path=[]):
        super().__init__(name,weight,path)
        self.child_nodes=child_nodes

    def isBinaryNode(self):
        return False

    def isLeafNode(self):
        return False

    def get_n_childs(self):
        return len(self.child_nodes)
        
class Tree(ParentNode):
    def __init__(self,name_root,right=None,left=None,weight=None,path=[]):
        print("The name of the root node is " + name_root + ".")
        super().__init__(name_root,right,left,weight,path)
        self.n_parameters=1
        self.ART_LeafNodes={}
        self.ART_LeafNodes["DTG10"]=[]
        self.ART_LeafNodes["DTG50"]=[]
        self.ART_LeafNodes["EFV"]=[]
        self.ART_LeafNodes["LPV/r"]=[]
        self.ART_LeafNodes["NVP"]=[]

        self.build_structure()
        print("The structure of the ART tree have successfully been built." +
        " You can save it by using the save_structure(file_name) method.")
        
    def build_structure(self):
        #Constructing tree beginning from root node to leaf nodes and from right to left 
        nodes=[self] #nodes whose children are to be constructed
        which=["right","left"] #allows me to write fewer lines of codes when the node is binary
        while nodes != []:
            node=nodes.pop(0)
            path=node.path.copy()
            path.append(node)
            if node.isBinaryNode():
                self.n_parameters+=1
                child_nodes=[]
                #Constructing the 2 child nodes of the current node 
                for item in which :
                    name=input("What is the name of "  + node.name + "'s "\
                            + item + " child node? ")
                    leaf_node=int(input("Is " + name + " a leaf node ? Press 1 if so and 0 otherwise. "))
                    if leaf_node:
                        child=LeafNode(name) 
                        ART=input("Which next line antiretroviral therapy (ART)" + 
                        " does this leaf node corrrespond to (DTG10, DTG50, EFV, LPV/r or NVP) ? ")
                        self.ART_LeafNodes[ART].append(child)
                    else :
                        binary_node=int(input("Is " + name + " a binary node (2 child nodes) ? Press 1 if so and 0 otherwise. "))
                        if binary_node:
                            child=ParentNode(name)
                        else:
                            child=MultiNode(name)
                        nodes.append(child)
                    child.path=path
                    child_nodes.append(child)
                node.right=child_nodes[0]
                node.left=child_nodes[1]
            else:
                n=int(input("How many child nodes does " + node.name + " have?"))
                self.n_parameters+=n-1
                child_nodes=[]
                for i in range(1,n+1):
                    name=input("What is the name of "  + node.name + "'s "\
                            + ordinal(i) + " child (from right to left)? ")
                    leaf_node=int(input("Is " + name + " a leaf node ? Press 1 if so and 0 otherwise. "))
                    if leaf_node:
                        child=LeafNode(name) 
                        ART=input("Which next line antiretroviral therapy (ART)" +
                        " does this leaf node corrrespond to (DTG10, DTG50, EFV, LPV/r or NVP) ? ")
                        self.ART_LeafNodes[ART].append(child)
                    else :
                        binary_node=int(input("Is " + name + " a binary node (2 child nodes) ? Press 1 if so and 0 otherwise. "))
                        if binary_node:
                            child=ParentNode(name)
                        else:
                            child=MultiNode(name)
                        nodes.append(child)
                    child.path=path
                    child_nodes.append(child)
                node.child_nodes=child_nodes
                    
    def get_n_parameters(self):
        return self.n_parameters           
            
    def get_LeafNodes_names(self,ART):
        try:
            nodes=self.ART_LeafNodes[ART]
            assert len(nodes)!=0  #checks if nodes is empty
            return names_nodes(nodes)
        except KeyError:
            print("Please enter DTG10, DTG50, EFV, LPV/r or NVP. Nothing is returned.")
        except AssertionError:
            return np.array([])

    def compute_prob(self,ART):
        try :
            nodes=self.ART_LeafNodes[ART]
            assert len(nodes)!=0  #checks if nodes is empty
            f=lambda node: node.compute_prob()
            F=np.vectorize(f)
            probs=F(nodes)
            return np.sum(probs)
        except TypeError:
            print("Set the weights of the tree before computing probabilities.")
        except AssertionError:
            return 0
    
    def set_weights(self,weights_list):
        assert type(weights_list)==list, "weights_list should be a list."
        assert len(weights_list)==self.n_parameters, "weights_list does "\
        + "not have the correct length."
        weights=weights_list.copy()
        weight=weights.pop(0)
        self.set_weight(weight)
        nodes=[self]
        while  weights!= []:
            node=nodes.pop(0)
            if node.isBinaryNode():
                weight=weights.pop(0)
                node.right.set_weight(weight)
                node.left.set_weight(1-weight)
                if node.right.isLeafNode()==False:
                    nodes.append(node.right)
                if node.left.isLeafNode()==False:
                    nodes.append(node.left)
            else:
                sum_weigts=0
                for child in node.child_nodes[:-1]:
                    weight=weights.pop(0)
                    child.set_weight(weight)
                    sum_weigts+=weight
                    if node.isLeafNode()==False:
                        nodes.append(child)                   
                node.child_nodes[-1].set_weight(1-sum_weigts)
                if node.child_nodes[-1].isLeafNode()==False:
                    nodes.append(node.child_nodes[-1])
            
        
    def reset_weights(self):
        self.weight=None
        nodes=[self]
        while  nodes!= []:
            node=nodes.pop(0)
            if node.isBinaryNode():
                node.right.weight=None
                node.left.weight=None
                if node.right.isLeafNode()==False:
                    nodes.append(node.right)
                if node.left.isLeafNode()==False:
                    nodes.append(node.left)
            else:
                for child in node.child_nodes:
                    child.weight=None
                    if child.isLeafNode()==False:
                        nodes.append(child)


    def save_structure(self,file_name):
        self.reset_weights()
        with open(file_name, "wb") as outfile:
            pickle.dump(self, outfile)
            
    def draw(self,file_name= "The ART tree"):
        G=graphviz.Digraph(file_name)
        #G.attr(label=r'\n\nEntity Relation Diagram\ndrawn by NEATO')
        G.attr(label= "\n\n" + file_name)
        #G.attr(fontsize='20')
        G.node(str(self.node_id),label= self.name + "\n\n" + to_string(self.weight))
        nodes=[self]
        node_id=0
        while  nodes!= []:
            node=nodes.pop(0)
            if node.isBinaryNode():
                child_nodes=[node.left, node.right]
            else:
                child_nodes=node.child_nodes.copy()
                child_nodes.reverse()
            for child in child_nodes:
                node_id+=1
                child.node_id=node_id
                G.node(str(node_id), label=child.name)
                G.edge(str(node.node_id),str(node_id),to_string(child.weight))
                if child.isLeafNode()==False:
                    nodes.append(child)
        G.view(cleanup=True)
        
    def print_pathes(self,ART):
        try:
            nodes=self.ART_LeafNodes[ART]
            for node in nodes:
                node.print_path_from_root()
        except KeyError:
            print("Please enter DTG10, DTG50, EFV, LPV/r or NVP. Nothing is returned.")
        
        