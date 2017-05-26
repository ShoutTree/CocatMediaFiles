import os,sys

# dateToConcat = "2017-01-01"
LIST_FILE_NAME = "temp_mylist.txt"
FILE_EXT = ".mp4"

def generateListFile(dir):

	f_list_file = open(LIST_FILE_NAME, "w+")

	for i in range(0, 24):
		hour = "%02d" % i
		hourStr = str(hour)
		hourFolderPath = dir + "/" + hourStr
		if os.path.isdir(hourFolderPath):
			for j in range(0, 59):
				minute = "%02d" % j
				minuteStr = str(minute)
				minuteFilePath = hourFolderPath + "/" + minuteStr + FILE_EXT
				if os.path.exists(minuteFilePath):
					try:
						f_minuteFile = open(minuteFilePath)
						f_list_file.write("file " + "\'" + minuteFilePath + "\'" + "\n")
						f_minuteFile.close()

					except IOError, e:
						print 'file cannot open: ' + minuteFilePath
						print sys.stderr, "Failed to open 'noexists' : %s" % e

	f_list_file.close()

def concatMediaFiles(dataStr):
	commandStr = "ffmpeg -f concat -safe 0 -i " + LIST_FILE_NAME +  " -c copy " + dateToConcat + FILE_EXT
	print 'commandStr : ' + commandStr
	os.system(commandStr)

# -------------- main, call from bat or shell script --------------
if __name__ == '__main__':
	if len(sys.argv) >= 2:

		dataRootPath = sys.argv[1]
		for dateToConcat in os.listdir(dataRootPath):
			dateFolderPath = dataRootPath + "/" + dateToConcat
			generateListFile(dateFolderPath)
			concatMediaFiles(dateToConcat)
			break
