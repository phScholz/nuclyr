import requests
import pandas as pd
from os import path
import os
import time
import sys

class levelscheme:
    def __init__(self, Isotope):
        self.Isotope=Isotope
        self.df = self.getLevelScheme()

    def getLevelScheme(self):
        try:
            x = requests.get("https://www.nndc.bnl.gov/nudat2/getdatasetClassic.jsp?nucleus="+self.Isotope+"&unc=nds").text

        except Exception as e:
            print(e)
            

        tables = pd.read_html(x, skiprows=(0,1))

        references = tables[1]
        levels = tables[2]
        levels[["E(level) [keV]","XREF","Jpi(level)", "T1/2(level)","E(gamma) [keV]","I(gamma)", "M(gamma)", "Final level", "Spin"]] = levels[[0,1,2,3,4,5,6,7,8]]
        levels=levels[["E(level) [keV]","XREF","Jpi(level)", "T1/2(level)","E(gamma) [keV]","I(gamma)", "M(gamma)", "Final level", "Spin"]]

        return levels

    def energies(self):
        levelsTemp=self.df["E(level) [keV]"].str.split(" +",expand = True)
        levelsTemp[[0,1]]=levelsTemp[[0,1]].replace({'\?':''}, regex=True) #get rid of these stupid question marks
        #levelsTemp[[0,1]]=levelsTemp[[0,1]].replace({'(^|\s)[-+]?[0-9]{1,5}(\.[0-9]{1,5})?(\s|$)':'nan'}, regex=True) # regex matching: xxxxx.xxxxx where x are numbers
        levelsTemp[[0,1]]=levelsTemp[[0,1]].replace({'Level':'nan'}, regex=True)
        levelsTemp[[0,1]]=levelsTemp[[0,1]].replace({'None':'nan'}, regex=True)
        levelsTemp[0]=levelsTemp[0].replace({'E\(level\)\:':'nan'}, regex=True)
        levelsTemp[1]=levelsTemp[1].replace({'From':'nan'}, regex=True)
        levelsTemp[1]=levelsTemp[1].replace({'For':'nan'}, regex=True)
        levelsTemp[1]=levelsTemp[1].replace({'In':'nan'}, regex=True)
        levelsTemp[[0,1]]=levelsTemp[[0,1]].replace({" +":'nan'}, regex=True)
        levelsTemp[[0,1]]=levelsTemp[[0,1]].astype(float)
        return levelsTemp[[0,1]]
