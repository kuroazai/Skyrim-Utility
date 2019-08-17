# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 15:58:50 2019

@author: KuroAzai

WIP tool that can help newbies who don't know or lack the patience to troubleshoot
their load order and also help those lazy people who don't want to keep repeating same
processes to find the culprit. 

How it works: 
    We open the plugins files and everytime the game ctds upon start up we disable n number of them
    rinse and repeat the process until you find a shortlist of the troublesome mods.
    if you have over 200+ mods it gets tedius to do that manually aswell so this
    is the rememdy i made for myself.


Requirements : 
1. Create an skse shortcut and put it in the same directory as this script.
2. Create a backup of your plugins just in case 
3. Get the file path to your plugins folder
4. change "self.path" with your own path for plugins
5. Run and observe you can adjust the wait times to suit your needs. 
"""

import psutil
import time 
import os  


class Organizer:
 
    def __init__ (self):
        #Change this to your plugins.txt 
        self.path = "Your path to your plugins"
        self.status = None
        self.file = None
        self.data = None
        self.prev_data = None
        #Change this to how many mods you are happy with the script to deactive at a time
        self.n = 10
        self.problematic = []
        
    def crash_check(self):
        print("\nChecking if application is running")
        #Load Process
        a = psutil.process_iter()
        #Check if the process exists
        for x in a:
            #If it's oldrim or vr set the name as seen within the task manager
            if "SkyrimSE.exe" in str(x) :
                #check for WerFault
                a = psutil.process_iter()
                for x in a:
                    #If it crashed close dialog box and continue
                    if "WerFault.exe" in str(x):
                        os.system("taskkill /f /im WerFault.exe")
                        self.status = False
                        return self.status                   
                self.status = True
                return self.status
            else:
                pass
        #If it's not found 
        self.status = False
        return self.status
     
    def Open_File(self): 
        print("\nLoading File")
        #open the file and move each line within the list 
        with open(self.path, 'r') as f:
            self.file = f.readlines()
        return self.file
            
    def Save_File(self):
        #Organise Structure
        savefile = ""
        for x in self.file: 
            x.rstrip()
            x.lstrip()
            savefile = savefile + x 
        print(savefile)
        #Write to file 
        with open(self.path, 'w') as f:
            print("Updating Plugins")
            f.write(str(savefile))
        
    def Run_Skyrim(self):
        print("\nRunnig Skyrim")
        #Run skyrim again ~ 
        os.system("start skse")
        #Wait n number of seconds for application to open
        time.sleep(20)
        self.crash_check()
        #Check for crash
        while self.status == False:
            time.sleep(45)
            self.crash_check()
            if self.status == True:
                print("\nRunning")
                break
            else:
                print("\nCrashed...", "\nDeactivatingPlugins")
                #deactivate N mods
                self.remove_mod()
                
                #Run Again
                os.system("start skse")
        self.crash_resolver()
                

    
    def remove_mod(self):
        #Find Active Mods
        z = "*"
        a = []
        #Find all files with * that indactes it's activated and store their name + index
        for x in self.file :
            if z in str(x):
                a.append([x,self.file.index(x)])
                        
        #get index and disable the last n values 
        c = 1
        self.problematic = []
        while self.n > 0 and len(self.file)-1 > self.n: 
            z = a[len(a)-c][0]  
            z = str(z[1:])
            self.problematic.append(z)
            #Select index then change the value
            self.file[a[len(a)-c][1]] = z
            print ("Changing Values \n", self.file[a[len(a)-c][1]], z)
            #decrement 
            self.n -= 1
            c += 1
        #Store a record of the previous data 
        self.prev_data = a
        #Update the plugins 
        self.Save_File()

    def crash_resolver(self):   
        #Once the program becomes stable 
        if self.prev_data == None:
            return "No Errors"
        else:
            return print("Potential Problematic mods \n", self.problematic)
        

a = psutil.process_iter()
for x in a:  
    if "SkyrimSE.exe" in str(x):
        print("Skyrim Already running...", "\n Close and try again well it's already working...")
        input()
        quit()
print("\nSkyrim isn't running starting application")
#Create the object
skyrim = Organizer()
#Open the file 
plugins = skyrim.Open_File()

#misc debug
print("Plugins avaliable", len(plugins))
#Test if it's running  
state = skyrim.crash_check()

if plugins != None:
    #Run the game and proceed with the test
    skyrim.Run_Skyrim()
else:
    print("Plugins Not loaded, Check Provided File path")

plugins = skyrim.file
print("Done")
input()
