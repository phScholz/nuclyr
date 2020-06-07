from selenium import webdriver
import pandas as pd
from os import path
import os
import time
import json
import sys
import nuclyr.config as cf

def entryXpath(sect, tt):
    if tt == 0:
        return '//*[contains(@id, "sect'+str(sect)+'x")]/tt/a[@class="e4link" and @title="Interpreted EXFOR: X4-iTree..."]'
    if tt != 1:
        return '//*[contains(@id, "sect'+str(sect)+'x")]/tt['+str(tt)+']/a[@class="e4link" and @title="Interpreted EXFOR: X4-iTree..."]'

def checkOutputDir(outputDir):
    if path.exists(outputDir):
        return True
    else:
        try:
            os.mkdir(outputDir)
        except Exception as e:
            print(e)
            return False

def checkHeader(df):
    header_list = list(df)

    en_gev = False
    en_mev = False
    en_kev = False
    data_b = False
    data_mb = False

    if ("EN", "GEV") in header_list:
        en_gev = True

    if ("EN", "MEV") in header_list:
        en_mev = True
    
    if ("EN", "KEV") in header_list:
        en_kev = True

    if ("DATA", "B") in header_list:
        data_b = True

    if ("DATA", "MB") in header_list:
        data_mb = True

    return en_gev, en_mev, en_kev, data_mb, data_b

def getSIG(Target, Reaction, output=cf.Get("output"), outputDir=cf.Get("outputDir"), web_driver=cf.Get("webdriver"), driver_loc=cf.Get("driver_loc"), verbosity=0):
    if output:
        checkOutputDir(outputDir)
    
    TargetList=[]
    ReactionList=[]
    Data=[]
    Legends=[]
    
    if type(Target) is not list:
        TargetList.append(Target)
    else:
        TargetList=Target
    
    if type(Reaction) is not list:
        ReactionList.append(Reaction)
    else:
        ReactionList=Reaction

    t0 = time.time()
    num = len(TargetList)*len(ReactionList)
    print("[nuclyr|exfor] Total number of reactions: ", num)
    i = 1
    done = False

    for target in TargetList:
        for reaction in ReactionList:
            done = False
            print()
            print("[nuclyr|exfor] Target: ", target)
            print("[nuclyr|exfor] Reaction: ", reaction)
            
            
            print()
            t = time.time() - t0
            avgtime = t / i
            print("[nuclyr|exfor] Elapsed time    : ", t, " s")
            print("[nuclyr|exfor] Avg time        : ", avgtime, " s")
            timeLeft=avgtime*num-t
            if timeLeft >= 0:
                print("[nuclyr|exfor] Approx time left: ", timeLeft, " s")
            else:
                print("[nuclyr|exfor] Approx time left: ", 0, " s")
            print()
            i+=1

            if path.exists(outputDir+target+"("+reaction+")_000.csv"):
                print()
                print("[nuclyr|exfor] File already exists!!!")
                done = True
                continue
                
            driver_loc = cf.Get("driver_loc")

            while done is False:
                            
                if web_driver=="Edge":
                    print("[nuclyr|exfor] Using 'Edge' as webdriver...")
                    print("[nuclyr|exfor] Webdriver location: ", driver_loc)
                    driver = webdriver.Edge(driver_loc)
                
                if web_driver=="Chrome":
                    print("[nuclyr|exfor] Using 'Chrome' as webdriver...")
                    print("[nuclyr|exfor] Webdriver location: ", driver_loc)
                    driver = webdriver.Chrome(driver_loc)

                try:
                    driver.get("https://www-nds.iaea.org/exfor/exfor.htm")

                except Exception as e:
                    if verbosity:
                        print(e)
                    done = False
                    continue

                submit = "/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input[1]"
                reset = "/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input[2]"
                tar = "/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[3]/td[3]/input"
                reac = "/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[5]/td[3]/input"
                chkTarget = "/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/input"
                chkReaction = "/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[5]/td[2]/input"
                quantity = "/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[7]/td[3]/input"
                chkQuantity = "/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[7]/td[2]/input"

                driver.find_element_by_xpath(tar).send_keys(target)
                driver.find_element_by_xpath(reac).send_keys(reaction)
                driver.find_element_by_xpath(quantity).send_keys("CS")
                driver.find_element_by_xpath(submit).click()


                sect_element = driver.find_elements_by_xpath('//*[contains(@id, "sect")]')
                entries_element = driver.find_elements_by_xpath('//*[contains(@id, "sect")]/tt[*]')
                num_sect=len(sect_element)
                #print("Number of entries: ", num_sect)

                if num_sect == 0:
                    print()
                    print("[nuclyr|exfor] No data available!")
                    driver.quit()
                    done = True
                    continue

                j = 0
                for sect in range(num_sect-1):
                    entries_element = driver.find_elements_by_xpath('//*[contains(@id, "sect'+str(sect)+'x")]/tt[*]')
                    num_tt=len(entries_element)
                    #print("Number of sub-entries: ", num_tt)
                    for tt in range(num_tt+1):
                        #print("Current: ",tt)
                        try:
                            #print(entryXpath(sect,tt))
                            driver.find_element_by_xpath(entryXpath(sect,tt)).click()
                            time.sleep(.1)
                            #print(driver.current_url)

                            html = driver.page_source

                            #Getting data tables using pandas.read_html and select the last table

                            tables = pd.read_html(html, header=[0,1])
                            df = tables[-1]
                            legend = tables[-2]

                            # checking if the data is in a proper form
                            en_gev, en_mev, en_kev, data_mb, data_b = checkHeader(df)

                            if en_gev and not en_mev:
                                df[("EN","MEV")] = df[("EN","GEV")]*1e3
                                en_mev = True
                            
                            if en_kev and not en_mev:
                                df[("EN","MEV")] = df[("EN","KEV")]/1e3
                                en_mev = True

                            if en_mev and not en_kev:
                                df[("EN","KEV")] = df[("EN","MEV")]*1e3
                                en_kev = True
                            
                            if data_b and not data_mb:
                                df[("DATA","MB")] = df[("DATA","B")]*1e3
                                data_mb = True
                            
                            if data_mb and not data_b:
                                df[("DATA","B")] = df[("DATA","MB")]/1e3
                                data_b = True

                            if verbosity:
                                print(df.head())

                            df[("Link","")]=driver.current_url
                            df[("Target","")] = target

                            #finding header
                            header = driver.find_element_by_xpath('html/body/div[4]/ul/li/ul/li/div[2]/span').text
                            print()
                            print("[nuclyr|exfor] Header: ", header)
                            df[("Header","")] = header

                            #define reaction
                            x = reaction.upper()
                            print("[nuclyr|exfor] Reaction: ", x)
                            df[("Reaction","")] = x

                            #getting data string
                            try:
                                data = driver.find_element_by_xpath('//span[contains(text(), "'+x+'")]').text
                                df[("Quantity","")] = data
                                print("[nuclyr|exfor] Quantity: ", data)

                                good=True

                                if ",SIG," or ",SIG)" in data:
                                    good=True
                                else:
                                    good=False                         

                                if "-M," in data:
                                    good=False

                                if "-G," in data:
                                    good=False

                                if not good:
                                    print("Not good.")
                                    continue
                                
                            except Exception as e:
                                if verbosity:
                                    print("[nuclyr|exfor] Quantity scraping didn't work.")
                                    print(e)

                            if output:
                                filename=outputDir+target+"("+reaction+")_"+str(j).zfill(3)+".csv"
                                df.to_csv(filename)

                            i+=1

                            if en_mev and en_kev and data_mb and data_b:
                                Data.append(df[[("EN","MEV"),("EN","KEV"),("DATA","B"),("DATA","MB"),("Target",""),("Reaction",""),("Quantity",""),("Header",""),("Link","")]])
                                Legends.append(legend)
                            else:
                                print("[nuclyr|exfor] Data was not added.")

                            time.sleep(.1)
                            driver.back()
                            time.sleep(.1)

                        except Exception as e:
                            if verbosity:
                                print(e)
                            continue

                print() 
                print("[nuclyr|exfor] "+target+"("+reaction+") Done!!!")
                driver.quit()
                done = True
                continue
            
    return Data, Legends