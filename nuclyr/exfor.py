from selenium import webdriver
import pandas as pd
from os import path
import time

def entryXpath(sect, tt):
    if tt == 0:
        return '//*[contains(@id, "sect'+str(sect)+'x")]/tt/a[@class="e4link" and @title="Interpreted EXFOR: X4-iTree..."]'
    if tt != 1:
        return '//*[contains(@id, "sect'+str(sect)+'x")]/tt['+str(tt)+']/a[@class="e4link" and @title="Interpreted EXFOR: X4-iTree..."]'

def getEXFOR_SIG(Target, Reaction, output="./data/", web_driver="Edge", driver_loc="./edgedriver_win64_83.0.478.37/msedgedriver.exe", verbosity=0):
    print(type(Target))
    print(type(Reaction))
    print(Target)
    print(Reaction)
    t0 = time.time()
    num = len(Target)*len(Reaction)
    print("Number of reactions: ", num)
    i = 1
    done = False

    for target in Target:
        for reaction in Reaction:
            done = False
            print()
            print("Target: ", target)
            print("Reaction: ", reaction)
            
            
            print()
            t = time.time() - t0
            avgtime = t / i
            print("Elapsed time    : ", t, " s")
            print("Avg time        : ", avgtime, " s")
            timeLeft=avgtime*num-t
            if timeLeft >= 0:
                print("Approx time left: ", timeLeft, " s")
            else:
                print("Approx time left: ", 0, " s")
            print()
            i+=1

            if path.exists(output+target+"("+reaction+")_000.csv"):
                print()
                print("File already exists!!!")
                done = True
                continue

            while done is False:
                            
                if web_driver=="Edge":
                    driver = webdriver.Edge(driver_loc)

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
                    print("No data available!")
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

                            df["link"]=driver.current_url

                            #finding header
                            header = driver.find_element_by_xpath('html/body/div[4]/ul/li/ul/li/div[2]/span').text
                            print()
                            print("Header: ", header)
                            df["Header"] = header

                            #define reaction
                            x = reaction.upper()
                            print("Reaction: ", x)
                            df["Reaction"] = x

                            #getting data string

                            try:
                                data = driver.find_element_by_xpath('//span[contains(text(), "'+x+'")]').text
                                print("Data: ", data)
                                df["Data"] = data

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
                                    print(e)

                            #print(df)
                            #print(legend)
                            filename="./data/"+target+"("+reaction+")_"+str(j).zfill(3)+".csv"
                            df.to_csv(filename)
                            i+=1
                            time.sleep(.1)
                            driver.back()
                            time.sleep(.1)

                        except Exception as e:
                            if verbosity:
                                print(e)
                            continue
                        
                print(target+"("+reaction+") Done!!!")
                driver.quit()
                done = True
                continue