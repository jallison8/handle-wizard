# "Handle Wizard" by Justin Allison 
An EDL generator for cutting VFX shots delivered with consistent frame handles.

IMPORTANT NOTES
______________________________________________________________________

The software is presented as open source for free and without warranty.

This software is designed to be built upon by the post-production community and incorporated into specific workflows (see Use Cases) but has not been tested in a professional production environment.

Some limitations exist (see Known Issues) which might be prohibitive for professional post-production workflows. This project will benefit greatly from community support and development! 

It is best practice to run "Handle Wizard" from the command-line.

Windows Users: "Handle Wizard" relies on ExifTool being run from C:\exiftool\exiftool.exe on Windows. Running the setup file will copy ExifTool to this folder path (or this can be done manually).

Mac Users: Before running "Handle Wizard", you will need to install the ExifTool DMG included in the download package.


OVERVIEW
____________________________________________________________

"Handle Wizard" is a command-line tool that outputs an EDL to the user's desktop based on user input. Each video file in the selected directory will be automatically added to the EDL with the correct in and outpoints based on the number of frame handles the user inputs. Each clip is assigned a number based on the order in which the clip appears in the directory. The clip is added to the EDL's timeline at the record timecode hour mark which corresponds to the clip number. For example, the 1st clip in the directory will be cut in at 01:00:00:00 and the 15th clip in the directory will be cut in at 15:00:00:00. "Handle Wizard" expects all the files in the selected directory to be the same frame rate and contain the same number of frame handles.


DOCUMENTATION
____________________________________________________________

"Handle Wizard" is written in Python 3 and uses ExifTool by Phil Harvey to extract source timecode from media.

The Python wrapper PyExifTool is used to launch ExifTool from within the Python script and get the Start Timecode tag from ExifTool's output.

The Python library Timecode is then used to make timecode calculations that will be output into the EDL.

ExifTool can be downloaded directly here: https://exiftool.org/ 

PyExifTool can be installed with pip install PyExifTool. Documentation is available here: https://smarnach.github.io/pyexiftool/ 

Timecode can be installed with pip install timecode. Documentation is available here: https://pypi.org/project/timecode/ 

Upon launch, "Handle Wizard" asks the user for the path to the VFX shots, the number of frame handles they contain, the project frame rate, and the sequence name.
If the user selects a frame rate of 29.97fps or 59.94fps, "Handle Wizard" will generate an EDL with Drop Frame Timecode. Otherwise, the EDL will be generated with Non-Drop Frame Timecode.

"Handle Wizard" extracts the start timecode and duration of each video file and calculates the end timecode by adding the start timecode to the duration. The Source Timecode In is calculated by adding the number of frame handles to the start timecode. The Source Timecode Out is calculated by subtracting the number of frame handles from the end timecode. These timecodes are then output to handleWizard.edl on the user's desktop.


USE CASES
____________________________________________________________

An Assistant Editor working in Avid Media Composer on an episode of scripted television is delivered a batch of work-in-progress VFX shots from a vendor that need to be cut into the current timeline and reviewed by the showrunner. All of the shots delivered have 16 frame handles. Typically, the AE would have to manually add inpoints and outpoints to each shot before cutting them in. With "Handle Wizard", he or she is able to run the script, open handleWizard.edl in Media Composer, decompose the EDL, and then cut the decomposed clips (which now begin and end at the correct timecodes) into the episode.

An On-line Editor working in DaVinci Resolve on a feature film is delivered a batch of final VFX shots from a vendor for Reel 4. No EDL has been given by the film's AE (or there is reason to believe the EDL given is not accurate). All of the shots delivered have 12 frame handles. Typically, the on-line editor would have to manually add inpoints and outpoints to each shot before cutting them into the hero project. With "Handle Wizard", he or she is able to run the script and open handleWizard.edl in Resolve. He or she could either match frame to each clip, thereby loading the shot into the source monitor with the correct in and outpoints, or copy and paste each clip from the EDL timeline to the Reel 4 timeline.


KNOWN ISSUES
____________________________________________________________

When dragging and dropping folders into the Mac Terminal, an extra space after the directory name is sometimes added. Remove this space before continuing or the script will fail.

Multiple codecs and file formats are supported, however Apple ProRes QuickTimes are most reliable for extracting accurate source timecode.

DNXHD and DNXHR codecs are not supported. ExifTool is unable to read the source timecode of these files.

MXF files are not supported. A bug in ExifTool 12.01 incorrectly reports the start timecode of these files.

Only video files are supported. ExifTool cannot extract metadata from image sequences. As a workaround, a user could transcode image sequences to Apple ProRes QuickTimes, run the script on the QuickTimes, and then import the EDL with the original image sequences.

"Handle Wizard" is only available on Mac and Windows systems. It has not yet been developed for Linux systems. It is possible that the Mac version will work on some Linux distributions, but this has not been tested.



