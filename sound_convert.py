#sound_convert.py
#Auther: Masafumi Hiura
#Last update: 14/09/2021 ver 1.0
#This code convert wav file to other format file by operating ffmpeg.
#You need to download "ffmpeg" and place on the folder of this module or the folder of being path set.
#Support format
##mp3, flac, ogg, wma
#You can set folder for input information(wav file folder).
#This case, This code seek wav files in wav file folder, and convert one by one.
#Usage: sound_convert.py <source wav file/folder>  <convert format name>

import subprocess
from subprocess import PIPE
import sys
import os
import glob
import shutil

class sound:
    def __init__(self, sfile):
        self.exportfile = ""
        self.sfile = os.path.abspath(sfile)
        # validate input source file strings
        if os.path.exists(self.sfile):
            # set "done" folder
            if (os.path.isdir(self.sfile)):  # arg = directory
                if self.sfile[-1:] == os.sep: #if last string of path is os separator then cut the string.
                    self.sfile = self.sfile[:-1]
                self.dstdir = self.sfile + os.sep + 'done'
                self.dstfile = self.dstdir

            elif (os.path.isfile(self.sfile)):  # arg = file
                self.dstdir = os.path.dirname(self.sfile) + os.sep + 'done'
                self.dstfile = self.dstdir + os.sep + os.path.basename(self.sfile)[:-len(os.path.splitext(self.sfile)) - 2]

            # "done" directory exists or not. if not, make "done" directory.
            if os.path.exists(self.dstdir):
                pass
            else:
                try:
                    os.mkdir(self.dstdir)
                    os.mkdir(self.dstdir + os.sep + 'wav')
                    print("make done directory.")
                except OSError as e:
                    print(e)
                    sys.exit(1)
            self.ret = True
        else:
            print("File / Directory Not Found -> " + self.sfile)
            self.ret = False


    def check_environment(self):
        #check ffmpeg exists or not.
        if os.path.exists("ffmpeg"):
            ret = True
        elif os.path.exists("ffmpeg.exe"):
            ret = True
        else:
            print("ffmpeg is Not Found. you need to place ffmpeg on the same folder with sound_convert.py.")
            print(" or set the path of ffmpeg.")
            ret = False

        return ret

    def get_parameter(self):
        if self.fmt == "mp3":
            self.parameter = "-vn -ac 2 -ar 44100 -ab 256k -acodec libmp3lame -f mp3"
            return True

        elif self.fmt == "flac":
            self.parameter = "-vn -ar 44100 -ac 2 -acodec flac -f flac"
            return True

        elif self.fmt == "ogg":
            self.parameter = "-vn -ac 2 -ar 44100 -ab 128k -acodec libvorbis -f ogg"
            return True

        elif self.fmt == "wav":
            self.parameter = "-vn -ac 2 -ar 44100 -acodec pcm_s16le -f wav"
            return True

        elif self.fmt == "wma":
            self.parameter = "-vn -ac 2 -ar 44100 -ab 128k -acodec wmav2 -f asf"
            return True

        else:
            return False

    def ExtentionByName(self, name):
        if name == "mp3":
            self.fmt = "mp3"
            return True

        elif name == "flac":
            self.fmt = "flac"
            return True

        elif name == "ogg":
            self.fmt = "ogg"
            return True

        elif name == "wav":
            self.fmt = "wav"
            return True

        elif name == "wma":
            self.fmt = "wma"
            return True

        else:
            return False

    def export(self):
        print("ffmpeg -i " + self.sfile + " " + self.parameter + " " + self.exportfile)
        proc = subprocess.run("ffmpeg -i " + self.sfile + " " + self.parameter + " " + self.exportfile, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        return proc.stdout


def main():
    if len(sys.argv) < 3:
        print("Usage: sound_convert.py <source wav file/folder>  <convert format name>")
    else:
        sfile = sys.argv[1]
        fmtname = sys.argv[2]
        print(fmtname)
        cls_sound = sound(sfile)
        if(cls_sound.ret):
            if(cls_sound.check_environment()):
                if(cls_sound.ExtentionByName(fmtname)):
                    if(cls_sound.get_parameter()):
                        if (os.path.isdir(cls_sound.sfile)):
                            # multi file mode
                            files = glob.glob(cls_sound.sfile + os.sep + "*.wav")
                            for file in files:
                                print("source file = " + file)
                                cls_sound.sfile = file
                                print("destination file = " + cls_sound.dstfile + os.sep + os.path.basename(file)[:-len(os.path.splitext(os.path.basename(file)))-2] + "." + cls_sound.fmt)
                                cls_sound.exportfile = cls_sound.dstfile + os.sep + os.path.basename(file)[:-len(os.path.splitext(os.path.basename(file)))-2] + "." + cls_sound.fmt
                                print("ffmpeg run")
                                print(cls_sound.export())
                                print("Done.")
                                # the wave file that convert process has end is moved to wav folder.
                                if os.path.isfile(self.dstdir + os.sep + 'wav' + os.sep + os.path.basename(self.sfile)):
                                    print("wav file is already exist.")
                                    print("wav file do not move.")
                                else:
                                    try:
                                        shutil.move(self.sfile, self.dstdir + os.sep + 'wav' + os.sep)
                                    except OSError as e:
                                        print(e)

                        else:
                            # single file mode
                            print("source file = " + sfile)
                            print("destination file = " + cls_sound.dstfile + "." + cls_sound.fmt)
                            cls_sound.exportfile = cls_sound.dstfile + "." + cls_sound.fmt
                            print("ffmpeg run")
                            print(cls_sound.export())
                            print("Done.")
                    else:
                        print("error from get_parameter. format-> " + fmtname)
                else:
                    print("error from ExtentionByName. format-> " + fmtname + " is not supported.")
            else:
                print("environment error. check above messages.")
        else:
            print("source-> " + sfile + " is incorrect. check above messages.")

if __name__ == '__main__':
    main()
