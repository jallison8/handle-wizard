
# "Handle Wizard" by Justin Allison
# This software is provided free and open source without warranty. 

# Version 1.0 (Windows)

import os
import exiftool
import time
import timecode
from sys import exit

dropFrame = False

def wizard():
    global dropFrame
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    print("Welcome to Handle Wizard!\nThis script will generate an EDL of all the shots in your directory with new start and end timecodes based on the number of frame handles.")
    time.sleep(1)
    if os.path.isfile('desktop\\handleWizard.edl'): #Check if Handle Wizard EDL file exists
        print("You already have handleWizard.edl on your desktop. This script will overwrite that file. Do you want to continue? y/n")
        choice = input(">>> ")
        if choice == 'y' or choice == 'yes':
            os.remove('desktop\\handleWizard.edl') #Deletes old EDL
            edl = open('desktop\\handleWizard.edl','w+') #Creates new EDL
            edl.close()
            print("Continuing...")
            time.sleep(1)
        else:
            print("Exiting Handle Wizard...")
            time.sleep(1)
            exit()
    else:
        edl = open('desktop\\handleWizard.edl','w+') #Creates new EDL
        edl.close()
    print("Drag and drop folder or enter path")
    dir = input(">>> ")
    if len(dir) > 0:
        fps = input("""Select Frame Rate:
A. 23.98
B. 24
C. 25
D. 29.97
E. 30
F. 50
G. 59.94
H. 60
>>> """)
        if len(fps) > 0 and fps.isalpha():
            fps = fps.lower()
        if fps == 'a':
            fps = "23.98"
        elif fps == 'b':
            fps = "24"
        elif fps == 'c':
            fps = "25"
        elif fps == 'd':
            fps = "29.97"
            dropFrame = True
        elif fps == 'e':
            fps = "30"
        elif fps == 'f':
            fps = "50"
        elif fps == 'g':
            fps = "59.94"
            dropFrame = True
        elif fps == 'h':
            fps = "60"
        else:
            print("Type the letter for the correct frame rate.")
            time.sleep(1)
            wizard()
        handles = input("Number of frame handles: ")
        handles = timecode.Timecode(fps, str("00:00:00:" + handles)) #Convert frame handles to SMPTE Timecode
        clip_num = 0
        print ("Working on it...")
        for subdir, dirs, files in os.walk(dir):
            for file in files:
                clip = (dir + ("\\") + str(file))
                clip_num += 1 
                with exiftool.ExifTool('C:\\exiftool\\exiftool.exe') as et: #Generates new Source In and Outs                    
                    startTC = et.get_tag('StartTimecodeTimeValue', clip) #get Start TC                    
                    duration = et.get_tag('Duration', clip) #get Duration
                    startTC = timecode.Timecode(fps, str(startTC)) #Converts Start TC to be readable by Timecode library
                    duration = ('00:00:' + str(duration)) #Converts duration from seconds to HH:MM:SS.ss for Timecode library
                    duration = timecode.Timecode(fps, str(duration)) #Converts duration from HH:MM:SS.ss to HH:MM:SS:FF
                    endTC = startTC + duration #Calculates End TC by adding the converted Start TC to the Duration TC using Timecode library
                    newStartTC = startTC + (handles - 1)
                    newEndTC = endTC - (handles)
                    
                    #Generate Record TC's for EDL
                    
                    if clip_num == 1: 
                        recTCIN = timecode.Timecode(fps, '01:00:00:00')
                    else:
                        recTCIN = ("0" + str(clip_num) + ":00:00:00")
                        recTCIN = timecode.Timecode(fps, str(recTCIN))
                    recTCOUT = (recTCIN + duration) - ((handles * 2) - 1)                

                    #Export to EDL
                    
                    edl = open('desktop\\handleWizard.edl', 'r+')
                    new_lines = ("00000" + str(clip_num) + "  " + file + " V     C        " + str(newStartTC) + " " + str(newEndTC) + " " + str(recTCIN) + " " + str(recTCOUT) + "\n* FROM CLIP NAME: " + file + "\n* SOURCE FILE: " + file + "\n")
                    with open('desktop\\handleWizard.edl', 'a') as edl:
                        edl.write("\n")
                        edl.write(new_lines)
                        edl.close()
                            
        title_edl()        
                           
    else:
        print("Enter folder path")

def title_edl():
    print("Name your sequence")
    seq = input(">>> ")
    edl = open('desktop\\handleWizard.edl', 'r+')
    header = edl.readlines()
    if dropFrame:
        header[0] = "TITLE:   " + seq + "\nFCM: DROP FRAME\n\n"
    else:
        header[0] = "TITLE:   " + seq + "\nFCM: NON-DROP FRAME\n\n"
    with open('desktop\\handleWizard.edl', 'w') as edl:
        edl.write("\n")
        edl.writelines(header)
        edl.close()
    print("Your EDL is on your desktop!")
    exit()        
        

wizard()
