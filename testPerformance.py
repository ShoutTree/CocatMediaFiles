import os
import datetime
import subprocess


timeBegin = datetime.datetime.now()
cmd = 'ffmpeg -v error -i \"/Volumes/MultiOS_Use/Temp/360videos/2017-05-30/07/30.mp4\" -f null - 2>&1'

t = os.popen(cmd).read()

# t = subprocess.call(cmd, shell=True, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))

# t=subprocess.call(cmd, shell=True)

# t = subprocess.check_output(cmd, shell=True)

if (t.find('atom not found') >= 0) or (t.find('error reading header') >= 0):
	print 'file cannot open: '
timeEnd = datetime.datetime.now()

print 'os.popen ' + cmd + ' cost:\n', str(timeEnd-timeBegin)
