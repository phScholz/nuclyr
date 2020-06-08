import pandas as pd
import numpy as np
import requests
import math
import io
import os

def massExcess(Z,A, model="RIPL"):
    this_dir, this_filename = os.path.split(__file__)

    df=pd.read_csv(os.path.join(this_dir,"data","ripl","mass-frdm95.dat"), skiprows=(0,1,2,3), sep=",", names=["Z","A","Element","Flag","Mexp","MErr","Mth","Emic","beta2","beta3","beta4","beta6"], header=0)

    if model == "RIPL":
        df=pd.read_csv(os.path.join(this_dir,"data","ripl","mass-frdm95.dat"), skiprows=(0,1,2,3), sep=",", names=["Z","A","Element","Flag","Mexp","MErr","Mth","Emic","beta2","beta3","beta4","beta6"], header=0)
        df[["Mexp","MErr","Mth"]]=df[["Mexp","MErr","Mth"]].replace(r'^\s*$', np.nan, regex=True)
        df[["Mexp","MErr","Mth"]]=df[["Mexp","MErr","Mth"]].astype(float)
        a = df["Mexp"].loc[(df["Z"] == Z) & (df["A"]==A)]
        b = df["MErr"].loc[(df["Z"] == Z) & (df["A"]==A)]
        c = df["Mth"].loc[(df["Z"] == Z) & (df["A"]==A)]
        d = 0
        
        if len(a.values)>0:
            if math.isnan(a.values[0]):
                return c.values[0], d
            else:
                return a.values[0], b.values[0]
        else:
            return 0,0
        

    if model == "AMDC":
        df=pd.read_csv(os.path.join(this_dir,"data","amdc","mass16.dat"),sep=",", skiprows=0, names=["1N-Z","N","Z","A","EL","O","Mexp","MErr","BE","BEErr","DECAY"], header=0)
        df[["Mexp","MErr","Mth","BE","BEErr"]]=df[["Mexp","MErr","Mth","BE","BEErr"]].replace(r'^\s*$', np.nan, regex=True)
        df[["Mexp","MErr","Mth","BE","BEErr"]]=df[["Mexp","MErr","Mth","BE","BEErr"]].astype(float)
        return df["Mexp"].loc[(df["Z"] == Z) & (df["A"]==A)].values[0]/1e3, df["MErr"].loc[(df["Z"] == Z) & (df["A"]==A)].values[0]/1e3
    

def abundance(Z,A):
    this_dir, this_filename = os.path.split(__file__)
    df=pd.read_csv(os.path.join(this_dir,"data","ripl","abundance.dat"))
    return df["abundance"].loc[(df["Z"] == Z) & (df["A"]==A)].values[0], df["uncert."].loc[(df["Z"] == Z) & (df["A"]==A)].values[0]