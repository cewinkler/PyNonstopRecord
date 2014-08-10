import subprocess, sys, os.path

if len(sys.argv) == 1:
	print("No filename specified")
	exit()

Filename = sys.argv[1]
Seconds = 0
Count = 0

if sys.argv[2] is not None:
	Seconds = sys.argv[2]

def main():
	global Filename, Count, Seconds

	validate_filename()
	print("Recording to file: " + Filename + "_x.wav")
	if Seconds > 0:
		print("Recording for " + str(Seconds) + " seconds.")
	record()
	exit()

def record():
	global Filename
	global Count
	returnCode = subprocess.call(get_record_string(), shell=True)
	if returnCode == 0:
		print("Successfully completed recording")
		return
	else:
		print("Recording was interrupted...")
		Count += 1
		record()

def get_record_string():
	global Seconds
	recstring = "arecord -D plughw:1 --rate 140000"
	if Seconds > 0:
		recstring = recstring + " --duration " + str(Seconds)
	recstring += recstring + " " + get_filename()
	return recstring

def does_file_exist(file):
	return os.path.isfile("/home/"+file+"_0.wav") 
	
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
	global Filename
	global Count

	return "/home/"+Filename+"_"+str(Count)+".wav"

if __name__ == "__main__":
	main()
