import subprocess, sys, os.path
from datetime import datetime

if len(sys.argv) == 1:
	print("No filename specified")
	exit()

Filename = sys.argv[1]
Seconds = 0
Count = 0
Start = datetime.now()

if sys.argv[2] is not None:
	Seconds = int(sys.argv[2])

def main():
	global Filename, Count, Seconds

	validate_filename()
	print("Recording to file: " + Filename + "_x.wav")
	if Seconds > 0:
		print("Recording for " + str(Seconds) + " seconds.")
	Start = datetime.now()
	record()
	exit()

def record():
	global Filename, Count, Start, Seconds
	duration = 0
	if Seconds > 0:
		duration = Seconds - (datetime.now()-Start).seconds
	returnCode = subprocess.call(get_record_string(duration), shell=True)
	if returnCode == 0:
		print("Successfully completed recording")
		print("Total restarts: " + str(Count))
		return
	else:
		print("Recording was interrupted...")
		Count += 1
		record()

def get_record_string(duration):
	recstring = "arecord -D plughw:1 --rate 140000"
	if Seconds > 0:
		recstring = recstring + " --duration " + str(duration)
	recstring += recstring + " " + get_filename()
	return recstring

def does_file_exist(file):
	return os.path.isfile("/home/pi/"+file+"_0.wav") 
	
def validate_filename():
	global Filename
	if does_file_exist(Filename) is False:
		return
	append = 1
	print("Filename '"+Filename+"' is not valid... Appending a number.")
	while does_file_exist(Filename + str(append)) is True:
		append += 1
	Filename = Filename + str(append)
	return

def get_filename():
	global Filename, Count

	return "/home/pi/"+Filename+"_"+str(Count)+".wav"

if __name__ == "__main__":
	main()
