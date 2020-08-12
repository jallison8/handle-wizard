#Handle Wizard setup for Windows

import os
import shutil


def check_exiftool():
    print("To set up Handle Wizard, I'm going to copy ExifTool to your C: drive...")
    exiflocal = os.path.join("C:\\","exiftool")
    if not os.path.exists(exiflocal):
        os.mkdir(exiflocal)
        move()
    else:
        if os.path.isfile("C:\\exiftool\\exiftool.exe"):
            print("Handle Wizard is ready!")
        else:
            move()

def move():
    cwd = os.getcwd()
    path = os.path.join(cwd, "exiftool\\exiftool.exe")
    if os.path.isfile(path):
        print("Copying ExifTool to C: Drive...")
        shutil.copy2(path, "C:\\exiftool")
        print("Handle Wizard is ready!")
    else:
        print("ExifTool is not in your Current Working Directory. Please run this Setup from the directory where you downloaded Handle Wizard.")
    input("Enter To Exit")

check_exiftool()