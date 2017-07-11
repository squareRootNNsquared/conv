###							###
###	  audioformatconverter	###
###							###
###	   copy, run, convert 	###
###							###
###		 wma,wav -> mp3		###

###
###	BUG LIST:
###
###	- Repeated operation will fail due to a directory already being present - deemed a minor issue.
###

###
### Import necessary files and scripts
###
import os
import sys
import glob
import time as t
import shutil as dop

###
### Define constants
###
scannedLayers = 10

###
### Define necessary functions
###

###
###	GenList
###
### Generate list of all file paths within chosen directory while removing " " (replacing with "_"), "'", "&"" (replacing with "[[and]]"), and {"(",")"} (replacing with {"[","]"}) from targeted directory and generated list
###
def GenList(path):
	layer = 1
	filepaths = []
	while layer < scannedLayers:
		curLayer = glob.glob("%s%s"%(path,"/*"*layer))
		for item in curLayer:
			itemFormatted = str(item)
			itemFormatted = itemFormatted.replace(" ","_")
			itemFormatted = itemFormatted.replace("'","[[sq]]")
			itemFormatted = itemFormatted.replace('"',"[[dq]]")
			itemFormatted = itemFormatted.replace("&","[[and]]")
			itemFormatted = itemFormatted.replace("(","[")
			itemFormatted = itemFormatted.replace(")","]")
			os.rename(item,itemFormatted)
		curLayer = glob.glob("%s%s"%(path,"/*"*layer))
		for item in curLayer:
			if (".wma" in item)|(".wav" in item)|(".mp3" in item):
				temp = []
				temp.append(item)
				filepaths = filepaths + temp
		layer = layer + 1
	return filepaths

###					
### Begin Routine	=	=	=	=	=	=	=	=	=	=	=	=	=	>
###					

### Obtain quality to convert to (in mp3) and directory to act upon 
bitrate = input("Please enter desired bitrate [kbps] (you may not obtain it): ")
path = input("Please drag and drop a copy of music containing directory placed near root to operate on with conversion to mp3: ")

### Generate copy of directory to operate on
dop.copytree(path,path + "__copy")
path = path + "__copy"

### Format copied directory
pathFormatted = path
pathFormatted = pathFormatted.replace(" ","_")
pathFormatted = pathFormatted.replace("'","[[sq]]")
pathFormatted = pathFormatted.replace('"',"[[dq]]")
pathFormatted = pathFormatted.replace("&","[[and]]")
pathFormatted = pathFormatted.replace("(","[")
pathFormatted = pathFormatted.replace(")","]")
os.rename(path,pathFormatted)
path = pathFormatted

### Format copied directory
filepaths = GenList(path)

### Convert all files in generated list
for filepath in filepaths:

	###	Rename file path to represent new file format
	newPath = filepath.split(".")[0] + ".mp3"
	wavPath = filepath.split(".")[0] + ".wav"

	###	Convert
	if (filepath.split(".")[1] == "wav")|(filepath.split(".")[1] == "mp3"):
		os.system('avconv -i %s -acodec libmp3lame -ab %dk %s'%(filepath,bitrate,newPath))
		os.remove(filepath)
	if (filepath.split(".")[1] == "wma"):
		os.system('avconv -i %s %s'%(filepath,wavPath))
		os.remove(filepath)
		os.system('avconv -i %s -acodec libmp3lame -ab %dk %s'%(wavPath,bitrate,newPath))
		os.remove(wavPath)

### Remain directory to denote conversion success
os.rename(path,path + "__conv")

print sys.version

###					
### End Routine	=	=	=	=	=	=	=	=	=	=	=	=	=	<
###	

### ### avconv (via Libav) notes ###
### -i 			:	input source
### -acodec		:	codec selection	
### pcm_u24be	:	PCM unsigned 24-bit big-endian

