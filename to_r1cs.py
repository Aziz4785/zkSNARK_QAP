from flattening import *
import numpy as np
import sys


def value_of(string_,op):
    if(not isinstance(string_, str)):
        if(op=='-'):
            return -int(string_)  #we suppose the the AST parser transform the a - -6 to a + 6
        return int(string_)
    else:
        return 1

r1cs=[]
index_of={}

def generate_index_of(inputs,flat_code): #optimisation : the dictionnary index_of can also be generated during the flattening
    index_of={}
    count=1
    for input in inputs:
        index_of[input]=count
        count+=1
    index_of["~out"]=count
    count+=1
    nbr_of_dummy=count
    for gate in flat_code: #optimisation : we could also assign index to dummmy variables during the R1CS generation, although we lose lisibilty and modulability
        if(gate[1] not in index_of and isinstance(gate[1], str)):
            index_of[gate[1]]=count
            count+=1
        if(gate[2] not in index_of and isinstance(gate[2], str)):
            index_of[gate[2]]=count
            count+=1
        if(gate[3] not in index_of and isinstance(gate[3], str)):
            index_of[gate[3]]=count
            count+=1
    nbr_of_dummy=count-nbr_of_dummy
    return index_of,nbr_of_dummy


def R1CS_generation(flat_code,size_of_s,index_of): #we suppose there is no simple assignment ( dummy_var = dummy_value) in the flat_code
    r1cs=[]
    for gate in flat_code:
        a=[0]*size_of_s
        b=[0]*size_of_s
        c=[0]*size_of_s
        op=gate[0]
        res=gate[1]
        left=gate[2]
        right=gate[3]
        c[index_of[res]]=1
        if(op=='*'):
            a[index_of.get(left,0)]=value_of(left,op)
            b[index_of.get(right,0)]=value_of(right,op)
        elif(op=='+'):
            a[index_of.get(left,0)]=value_of(left,op)
            a[index_of.get(right,0)]=value_of(right,op)
            b[0]=1
        elif(op=='-'):  #we don't need division because we only need to parse : a^3 * 2b - 5  (for now)
            a[index_of.get(left,0)]=value_of(left,op)
            a[index_of.get(right,0)]=value_of(right,op)
            b[0]=1
        r1cs.append([a,b,c])
    return r1cs

def export_r1cs(flatcode,size_of_s,index_of):
    r1cs=R1CS_generation(flatcode,size_of_s,index_of)
    r1cs=np.array(r1cs)
    print(r1cs)
    r1cs_reshaped = r1cs.reshape(r1cs.shape[0], -1)
    # saving reshaped array to file.
    np.savetxt("r1cs.txt", r1cs_reshaped,fmt='%d')
    return True #return nbr of gates




