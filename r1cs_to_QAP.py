from math import remainder
import scipy
import numpy as np
from scipy.interpolate import lagrange
from numpy.polynomial import Polynomial
from to_r1cs import *
import sys
            

def generate_polynoms(r1cs):
    A_polynoms=[]
    B_polynoms=[]
    C_polynoms=[]
    polynoms=[A_polynoms,B_polynoms,C_polynoms]
    for i in range(0,3):
        AorBorC=r1cs[:,i]
        nbr_of_gates=len(AorBorC)
        for j in range(0,len(AorBorC[0])):
            jth_values_of_gates=AorBorC[:,j]
            x=np.array(range(1,nbr_of_gates+1))
            poly = lagrange(x, jth_values_of_gates)
            polynoms[i].append(poly)
    polynoms=np.array(polynoms)
    return polynoms

def generate_polynomT(s,polynoms):
    sAx=np.dot(s,polynoms[0])
    sBx=np.dot(s,polynoms[1])
    sCx=np.dot(s,polynoms[2])
    print()
    print(" **************** P R O O F**************")
    print()
    print(" s.A(x) * s.B(x) - s.C(x) = ")
    print()
    print(sAx*sBx-sCx)
    return sAx*sBx-sCx

def s_is_solution(s,polynoms,nbr_of_gates):
    sAx=np.dot(s,polynoms[0])
    sBx=np.dot(s,polynoms[1])
    sCx=np.dot(s,polynoms[2])
    roots_of_Z = np.poly(np.arange(1,nbr_of_gates+1))
    Z = np.poly1d(roots_of_Z)
    q,r=np.polydiv(sAx*sBx-sCx, Z)
    print(" s.A(x) * s.B(x) - s.C(x) / Z = ")
    print(q)
    if(r.order==0 and r.c[0]<10e-8):
        print("with no reminder")
        return True
    else:
        print("with reminder  = ")
        print(r)
        return False

def s_from_R1CS(a,b,r1cs):
    s=[0]*len(r1cs[0][0])
    s[0]=1
    s[1]=a
    s[2]=b
    for gate in r1cs:
        a=gate[0]
        b=gate[1]
        c=gate[2]
        s+=((np.dot(s,a)*np.dot(s,b))*c)
    return s


def generate_proof(r1cs_file_name,a,b):  #outpout polynomial t
    loaded_r1cs = np.loadtxt(r1cs_file_name) #herre we need to test if the file loaded correctly and check if the content of the file is correct
    size_of_s=int(loaded_r1cs.shape[1]/3)
    r1cs = loaded_r1cs.reshape(loaded_r1cs.shape[0], loaded_r1cs.shape[1] // size_of_s, size_of_s)
    s=s_from_R1CS(a,b,r1cs)
    polynoms=generate_polynoms(r1cs)
    t=generate_polynomT(s,polynoms)
    return s,polynoms,t

def verify_proof(s,polynoms,nbr_of_gates):
    print(s_is_solution(s,polynoms,nbr_of_gates))


