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

class Folder:
	#used to pull all the relevant information from the folder path provided
	def __init__(self, stat):
		self.creationTime =  time.ctime(stat.st_ctime)#set the path variable to the provided string
		#self.createTime = creationTime #get the ctime of the folder

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

	#create the hourse old in EPOCH time
	hoursOld = time.time() - (ONEHOUR * hoursOld)

	#check the value of hoursOld for sanity
	#datetime.datetime.fromtimestamp(1347517370).strftime('%Y-%m-%d %H:%M:%S')
	#print the current epoch time in human readable format
	print '\nepoch time = {0} minus hours old = {1}\n'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M.%S'), datetime.datetime.fromtimestamp(hoursOld).strftime('%Y-%m-%d %H:%M.%S'))

	# Set the directory you want to start from
	#rootDir = folderPath
	#hoursAgo = time.time() - (ONEHOUR * 2)
	#Print the hours ago variable in human readable format
	print 'Hours ago is : %s' % datetime.datetime.fromtimestamp(hoursOld).strftime('%Y-%m-%d %H:%M.%S')
	#start the os.walk loop for the source path
	for dirName, subdirList, fileList in os.walk(folderPath):
	    print'\nFound directory: %s' % dirName
	    for fname in fileList:
	    	fnameStats = os.stat(os.path.join(dirName, fname))
	    	fnameAge=fnameStats.st_mtime

	    	if fnameAge > hoursOld:
	    		# print 'the file is %s old' % fnameAge 
	      		#test the regex and move 7zip file if it passes
	      		
	      		if extenMatch.match(fname): #another possible way to match is with simple string function fname.endswith(".py")
	      			moveFile(destinationPath, os.path.join(dirName, fname))
	      		else:
	      			print 'file %s is not a 7zip file' % fname

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
	if os.path.exists(folderPath):
		#send the input variables to the crawl function
		crawl(folderPath, destinationPath, hoursOld)
	#If the source path fails the path validation then print a warning with the parser usage
	else:
		print 'source path does not exist please verify the input path'
		print parser.usage
		exit(0) #exit the script
