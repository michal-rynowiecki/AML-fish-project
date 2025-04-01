import os
import argparse


def createImageList(args):
    '''
    Takes a path to an image folder and saves all absolute paths as separate lines in a txt file
    
    Input:
        args: Dict containing the following elements
            - inputFolder: Path to the input image folder
            - outputFile: Filepath to the output imagelist file
    '''

    rootdir = args["inputFolder"]
    with open(args["outputFile"], "w") as f:
        for root, _, files in os.walk(rootdir):
            for filename in files:
                if os.path.splitext(filename)[-1] == ".png":
                    f.write("{}\n".format(os.path.join(os.path.abspath(root), filename)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
            description = "Takes a set root dir and creates a list of all images in this dir. Writing with absolute path")
    ap.add_argument("-inputFolder", "--inputFolder", type=str, default= "/Users/alteafogh/Documents/ITU/AML/AML-fish-project/data/brackish-dataset/versions/4/annotations/annotations_YOLO",
                    help="Path to the main folder holding all images")
    ap.add_argument("-outputFile", "--outputFile", type=str, default = "imagelist.txt",
                    help="Path to the output file")
    
    args = vars(ap.parse_args())
    
    createImageList(args)