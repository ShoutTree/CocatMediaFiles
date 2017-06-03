import os,sys
import print_progress
import datetime

# dateToConcat = "2017-01-01"
LIST_FILE_NAME = "temp_mylist.txt"
ERROR_FILE_NAME = "error.txt"
FILE_EXT = ".mp4"
f_error = None

def countFilesNum(dir):
	count = 0
	for entry in os.listdir(dir):
		path = dir + "/" + entry
		if os.path.isfile(path):
			if path.endswith(FILE_EXT):
				count = count + 1
		elif os.path.isdir(path):
			count = count + countFilesNum(path)
	return count

def generateListFile(dir, filesNum):
	global f_error
	f_list_file = open(LIST_FILE_NAME, "w+")

	checkedFilesNum = 0;

	for i in range(0, 24):
		hour = "%02d" % i
		hourStr = str(hour)
		hourFolderPath = dir + "/" + hourStr
		if os.path.isdir(hourFolderPath):
			for j in range(0, 59):
				minute = "%02d" % j
				minuteStr = str(minute)
				minuteFilePath = hourFolderPath + "/" + minuteStr + FILE_EXT
				if os.path.isfile(minuteFilePath) and minuteFilePath.endswith(FILE_EXT):					
					t=os.popen('ffmpeg -v error -i ' + '\"' + minuteFilePath + '\"' + ' -f null - 2>&1').read()
					if (t.find('atom not found') >= 0):
						print 'file cannot open: ' + minuteFilePath
						f_error.write('file cannot open: ' + minuteFilePath + "\n")
					else:
						f_list_file.write("file " + "\'" + minuteFilePath + "\'" + "\n")

					checkedFilesNum = checkedFilesNum + 1

					print_progress.print_progress(checkedFilesNum, filesNum, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
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
		f_error = open(ERROR_FILE_NAME, "w+")

		dataRootPath = sys.argv[1]
		for dateToConcat in os.listdir(dataRootPath):
			print 'dateToConcat:', dateToConcat
			# if dateToConcat == '2017-05-22':
			# 	continue
			dateFolderPath = dataRootPath + "/" + dateToConcat
			filesNum = countFilesNum(dateFolderPath)
			if filesNum <= 0:
				print 'date ' + dateToConcat + ' has no files of extention ' + FILE_EXT
			else:
				print 'total files Num for date ' + dateToConcat + ' is ' + str(filesNum)
				print_progress.print_progress(0, filesNum, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)

				timeBegin = datetime.datetime.now()

				generateListFile(dateFolderPath, filesNum)
				concatMediaFiles(dateToConcat)

				timeEnd = datetime.datetime.now()
				print("process date " + dateToConcat + "Cost:", str(timeEnd-timeBegin))

		f_error.close()

