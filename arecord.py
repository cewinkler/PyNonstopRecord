import subprocess, sys, os.path

if len(sys.argv) == 1:
	print("No filename specified")
	exit()

Filename = sys.argv[1]
Count = 0

def main():
	global Filename
	global Count

	validate_filename()
	print("Recording to file: " + Filename + "_x.wav")
	record()
	exit()

def record():
	global Filename
	global Count
	returnCode = subprocess.call("arecord -D plughw:1  --rate 140000 " + get_filename(), shell=True)
	if returnCode == 0:
		print("Successfully completed recording")
		return
	else:
		print("Recording was interrupted...")
		Count += 1
		record()
	print("Return code: " + str(returnCode))

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
