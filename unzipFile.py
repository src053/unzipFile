# This script will take look for any .7zip files in a specified location (remoter or local) and copy to a specified directory 
# then unzip the file for a specified amount of time before cleaning it out

#import python libraries
import subprocess, os, optparse, sys, time, shutil
import datetime
import os.path
import re

#import pip libraries

#Create global var
ONEHOUR = 3600


def checkFolderExist(folderPath, hostDirName):
	searchFor = str.split(hostDirName, '.')
	storeFileNumber = []
	print 'search for: ', searchFor
	for dirName, subdirList, fileList in os.walk(folderPath):
		for subDir in subdirList:
			print 'Checking subdir: ', subDir
			matchDirName= str.split(subDir, '.')
			print 'Dir name after spliting on dot', matchDirName
			if searchFor[0] == matchDirName[0]:
				#print 'found a directory of the same name'
				#return [True, matchDirName[2][-2:]]
				print 'There is a MATCH'
				storeFileNumber.append(int(matchDirName[len(matchDirName) - 1][-2:]))
				print storeFileNumber
	if sum(storeFileNumber) > 0:
		storeFileNumber.sort()
		highestFolderNumber = storeFileNumber.pop()
		return [True, highestFolderNumber]
	else:
		return [False, 0]


def createHostNameFolder(folderPath, z7Name):
	"""this function will create the hostname directory for source 7z file to be copied too"""
	#create a variable for temporary hostname file
	tempHostNameDir = folderPath + "\\tempHostNameDir"
	#check if the tempHostNameDir folder exists
	if not os.path.exists(tempHostNameDir):
		#Make the temporary directory
		os.mkdir(tempHostNameDir)
		print 'CREATED', tempHostNameDir
		#call the unzip function to unzip the hostname.txt file to the temp HostNameDir
		unzip(folderPath, tempHostNameDir, False)

		hostFileName = tempHostNameDir + "\\hostname.txt"
		#Read in the name of the hostname
		with open(hostFileName, 'r') as f:
			hostDirName = f.read()
		#create destination folder
		#if not os.path.exists(os.path.join(folderPath, hostDirName + "00")):

	folderExists, folderNumber = checkFolderExist(folderPath, hostDirName) #run the checkFolderExist function and create variables with the output
	#print 'folder Exists {0}, folder number {1}'.format(folderExists, folderNumber)
	if not folderExists:
		#call the unzip function to unzip the whole directory into the permanent folder
		unzip(os.path.join(folderPath, z7Name), os.path.join(folderPath, hostDirName + "01"), True)

	else:
		folderNumber = int(folderNumber)
		if folderNumber < 9:
			folderNumber += 1
			changeToString = "0" + str(folderNumber)
			hostDirName = hostDirName + changeToString
			unzip(os.path.join(folderPath, z7Name), os.path.join(folderPath, hostDirName), True)
		else:
			folderNumber += 1
			changeToString = str(folderNumber)
			hostDirName = hostDirName + changeToString
			unzip(os.path.join(folderPath, z7Name), os.path.join(folderPath, hostDirName), True)	
	#remove the tempHostNameDir that was created
	shutil.rmtree(tempHostNameDir)
	os.remove(os.path.join(folderPath, z7Name))		

def moveFile(destinationPath, srcName):
	""" Used to move the file to a destination """
	print 'The destination path is {0} the file to be copied is {1}'.format(destinationPath, srcName)
	#Copy source file to destination path
	shutil.copy2(srcName, destinationPath)

def crawl(folderPath, destinationPath, hoursOld):
	"""This function will be used to crawl the source path and do a logic check on files within the crawl.  The criteria to pass is two fold:
	1) It must be a 7zip file
	2) It must be newer then the hoursOld number """
	#set the ONEHOUR var as the global
	global ONEHOUR
	#Regular expression to find 7zip files .*\.7z$
	extenMatch = re.compile('.*\.7z$')
	machineName = re.compile('hostname.txt')

	#create the hourse old in EPOCH time
	hoursOld = time.time() - (ONEHOUR * hoursOld)

	#check the value of hoursOld for sanity
	#datetime.datetime.fromtimestamp(1347517370).strftime('%Y-%m-%d %H:%M:%S')
	#print the current epoch time in human readable format
	#print '\nepoch time = {0} minus hours old = {1}\n'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M.%S'), datetime.datetime.fromtimestamp(hoursOld).strftime('%Y-%m-%d %H:%M.%S'))

	# Set the directory you want to start from
	#rootDir = folderPath
	#hoursAgo = time.time() - (ONEHOUR * 2)
	#Print the hours ago variable in human readable format
	print 'Hours ago is : %s' % datetime.datetime.fromtimestamp(hoursOld).strftime('%Y-%m-%d %H:%M.%S')
	#start the os.walk loop for the source path
	for dirName, subdirList, fileList in os.walk(folderPath):
	    print'\nFound directory: %s' % dirName #print the directory name
	    #iterate over each file in the file list
	    for fname in fileList:
	    	fnameStats = os.stat(os.path.join(dirName, fname)) #pull the file stats from the files in the directory
	    	fnameAge=fnameStats.st_mtime #create a variable with the age of the file
	    	#check if the file age is older than the time that was provided
	    	if fnameAge > hoursOld:
	    		# print 'the file is %s old' % fnameAge 
	      		#test the regex and move 7zip file if it passes	      		
	      		if extenMatch.match(fname): #another possible way to match is with simple string function fname.endswith(".7z")
	      			moveFile(destinationPath, os.path.join(dirName, fname)) #Move the file to the destination location
	      			createHostNameFolder(destinationPath, fname) #create the final spot to unzip the files to

	      		else:
	      			print 'file %s is not a 7zip file' % fname #keep record of files that are not 7zfiles

def unzip(folderPath, destinationPath, hostInfo):
	""" This function will call the 7z exe and unzip a compressed file"""
	#create a variable with the 7z.exe path
	exeLocation = "c:\\program files\\7-zip\\7z.exe"
	#call the subprocess
	#check if the machineInfo is already provided
	if hostInfo:
		print 'HOSTINFO =', hostInfo #print out the status of hostInfo True or False
		print 'FOLDERPATH =', folderPath #print out the destination path
		subprocess.call(exeLocation + " x " + folderPath + " -o" + destinationPath) #this will call the 7z.exe and extract the entire content
	else:
		print 'HOSTINFO =', hostInfo #print out the status of hostInfo True or False
		print 'FOLDERPATH =', folderPath #print out the destination path
		subprocess.call(exeLocation + " e " + folderPath + " -o" + destinationPath + " hostname.txt -r") #this will call the 7z.exe and extract only the hostname.txt

if __name__ == "__main__":

	#Create variables from the optparser

	#create variable from optparse object
	parser = optparse.OptionParser(usage= '%prog -s <Source Folder Path> -d <Destination Folder Path> -t <hours back>') #Create the parser var plus provide some usage guidelins

	#add source folder path option
	parser.add_option('-s', '--path', 
	                  dest="folder_path",
	                  help="Provide the path of the folder you would like to scan"
	                  )

	#add destination folder path option
	parser.add_option('-d', '--dest', 
	                  dest="destination_path",
	                  default= os.getcwd(),
	                  help="Provide the path of the folder you would like to send the matching files too Default is current working directory"
	                  )

	#add hours back options
	parser.add_option('-t', '--time', 
	                  dest="hours_back",
	                  default=8,
	                  help="How many hours back you would like to scan"
	                  )
	#send the options to options var and send any over flow into remainder
	options, remainder = parser.parse_args()

	folderPath =  options.folder_path #create a var with the folderPath of directory to scan
	destinationPath = options.destination_path #the location you would like the matching files to go to
	hoursOld = int(options.hours_back) #create a var with the int of hours back to scan

	if folderPath == None:
		print parser.usage #Print usage from when we created the parser var with the OptionParser class
		exit(0)


	print 'Path to scan    :', folderPath
	print 'Destination location: ', destinationPath
	print 'Hours back to scan :', hoursOld

	#test that the input path is valid
	if os.path.exists(folderPath) and os.path.exists(destinationPath):
		#send the input variables to the crawl function
		crawl(folderPath, destinationPath, hoursOld)
	#If the source path fails the path validation then print a warning with the parser usage
	else:
		print 'source path does not exist please verify the input path'
		print parser.usage
		exit(0) #exit the script
