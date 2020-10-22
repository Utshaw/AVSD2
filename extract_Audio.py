import subprocess
import sys


TEMP_AUDIO_FILE="temp.aac"

def getAudio(filename):
    exe = subprocess.Popen(["ffmpeg","-i",filename,"-vn", "-acodec","copy", "-y", TEMP_AUDIO_FILE], stdout=subprocess.PIPE)
    run = exe.communicate()[0]

# def main(timestamp,duration,output, filename="temp.aac",):
def main(timestamp,duration,output, filename="temp.aac",):
    test = subprocess.Popen(["ffmpeg","-ss",timestamp,"-t", duration, "-i",filename,output], stdout=subprocess.PIPE)
    output = test.communicate()[0]
    
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])