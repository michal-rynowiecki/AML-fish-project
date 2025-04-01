import os
import subprocess
import argparse
import pathlib
import ipdb

image_types = ['.png', '.jpg', '.jpeg']
video_types = ['.avi', '.mp4']

def extractFrames(args):
    main_dir = args["inputFolder"]
    output_dir = args["outputFolder"]

    for sub_dir, dirs, files in os.walk(main_dir):
        for filename in files:
            if os.path.splitext(filename)[1].lower() in video_types:
                videoFile = os.path.join(os.path.abspath(sub_dir), filename)

                if output_dir != '':
                    fileFolder = output_dir
                else:
                    fileFolder = os.path.splitext(videoFile)[0]
                pathlib.Path(os.path.abspath(fileFolder)).mkdir(exist_ok=True, parents=True)

                fileprefix = os.path.join(fileFolder, os.path.splitext(filename)[0])

                cmd_command = ["ffmpeg", "-i", videoFile, "-vf", "scale=960:540", "-sws_flags", "bicubic", "{}-%04d.png".format(fileprefix), "-hide_banner"]
                subprocess.call(cmd_command)

                # Create a .txt file with the names of all the image files in the respective folder
                dirContent = os.listdir(fileFolder)
                for fi in dirContent:
                    if os.path.splitext(fi)[1] in image_types:
                        with open("{}".format(os.path.join(fileFolder, "inputList.txt")), "a") as f:
                            f.write("{}\n".format(fi))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description = "Takes a set of videos and extracts the frames into separate folders")
    ap.add_argument("-in", "--inputFolder", type=str, required = True, help="Path to the main folder containing all the videos")
    ap.add_argument("-out", "--outputFolder", type=str, required = False, help="Path the image output folder. NOTE: if no outputfolder argument is provided, the images will be placed in folders corresponding to their respective video-names; if an argument IS given, all images will be placed in a folder with the provided argument name.", default='')

    args = vars(ap.parse_args())

    extractFrames(args)
