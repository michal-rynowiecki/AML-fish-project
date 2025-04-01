import os
import argparse

def createImageList(args):
    rootdir = args["inputFolder"]
    outputdir = os.path.abspath(args["outputFolder"])
    (_,_, curr_txt_files) = next(os.walk(outputdir))

    for root, _, files in os.walk(rootdir):
        for filename in files:
            filename_parts = os.path.splitext(filename)
            if filename_parts[-1] == ".png":
                txt_file = os.path.join(outputdir,filename_parts[0]+".txt")

                if os.path.basename(txt_file) not in curr_txt_files:
                    with open(txt_file, "w"):
                        pass

if __name__ == "__main__":
    ap = argparse.ArgumentParser( description = "Creates empty YOLO detection files for frames with no detections in it")
    ap.add_argument("-inputFolder", "--inputFolder", type=str, help="Path to the main folder holding all images")
    ap.add_argument("-outputFolder", "--outputFolder", type=str, help="Path to the output folder for the yolo .txt files")

    args = vars(ap.parse_args())

    createImageList(args)
