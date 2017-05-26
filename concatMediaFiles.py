import os,sys

# dateToConcat = "2017-01-01"
LIST_FILE_NAME = "temp_mylist.txt"
ERROR_FILE_NAME = "error.txt"
FILE_EXT = ".mp4"
global f_error

def generateListFile(dir):
	global f_error
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

					t=os.popen('ffmpeg -v error -i ' + '\"' + minuteFilePath + '\"' + ' -f null - 2>&1').read()
					if (t.find('atom not found') >= 0):
						print 'file cannot open: ' + minuteFilePath
						f_error.write('file cannot open: ' + minuteFilePath + "\n")
					else:
						f_list_file.write("file " + "\'" + minuteFilePath + "\'" + "\n")

					# try:
					# 	f_minuteFile = open(minuteFilePath)
					# 	f_list_file.write("file " + "\'" + minuteFilePath + "\'" + "\n")
					# 	f_minuteFile.close()

					# except IOError, e:
					# 	print 'file cannot open: ' + minuteFilePath
					# 	print sys.stderr, "Failed to open 'noexists' : %s" % e

	f_list_file.close()

def concatMediaFiles(dataStr):
	commandStr = "ffmpeg -f concat -safe 0 -i " + LIST_FILE_NAME +  " -c copy " + dateToConcat + FILE_EXT
	print 'commandStr : ' + commandStr
	os.system(commandStr)

# -------------- main, call from bat or shell script --------------
if __name__ == '__main__':
	if len(sys.argv) >= 2:
		global f_error
		f_error = open(ERROR_FILE_NAME, "w+")

		dataRootPath = sys.argv[1]
		for dateToConcat in os.listdir(dataRootPath):
			# if dateToConcat == '2017-05-22':
			# 	continue
			dateFolderPath = dataRootPath + "/" + dateToConcat
			generateListFile(dateFolderPath)
			concatMediaFiles(dateToConcat)

		f_error.close()

