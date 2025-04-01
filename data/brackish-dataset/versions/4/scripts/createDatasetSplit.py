import os
import argparse
import numpy as np


def createDatasetSplit(args):
    '''
    Takes an imagelist as input and splits it into training/validation/test splits, according to the provided percentages.
    Outputs separate txt files for each split containing the image paths to the images in the splits.

    Input:
        args: Dict containing the following elements
            - inputFile: Path to the input imagelist
            - seed: Seed for the numpy random number generator
            - trnSplit: Percentage of data used for training set (value between 0 and 1)
            - valSplit: Percentage of data used for validation set (value between 0 and 1)
            - tstSplit: Percentage of data used for test set (value between 0 and 1)
    '''

    # Set Numpy RNG if seed is provided
    if args["seed"]:
        np.random.seed(args["seed"])


    # Read data split values
    trn_split = args["trnSplit"]
    val_split = args["valSplit"]
    tst_split = args["tstSplit"]

    # Check that the data_splits actually add up to 1.0
    data_split_sum = trn_split+val_split+tst_split
    assert  data_split_sum == 1.0, "INVALID DATA SPLIT, {}".format(data_split_sum)


    # Read input imagelist
    text_file = open(args["inputFile"], "r")
    filenames = text_file.read().split('\n')
    text_file.close()

    # Remove empty line in the end of imagelist file if present
    if filenames[-1] == "":
        filenames = filenames[:-1]
    number_of_files = len(filenames)

    # Check that there are no duplicate frames
    assert number_of_files == len(set(filenames)), "Dublicate filenames in the provided imagelist"

    filenames = np.asarray(filenames)


    # Randomize the files, without replacement
    indecies = list(np.random.choice(number_of_files, number_of_files, replace = False))

    # Check that there are no duplicate indecies 
    assert number_of_files == len(set(indecies)), "Dublicate indecies generated"

    # Determine the amount of iamge for each split
    trn_amount = int(number_of_files*trn_split)
    val_amount = int(number_of_files*val_split)
    tst_amount = number_of_files-trn_amount-val_amount

    print("Trn: {}\nVal: {}\nTst: {}".format(trn_amount, val_amount, tst_amount))


    # Save the filenames for each split into txt files
    
    with open("train.txt", "w") as f:
        for ind in indecies[:trn_amount]:
            f.write("{}\n".format(filenames[ind]))

    with open("valid.txt", "w") as f:
        for ind in indecies[trn_amount:trn_amount+val_amount]:
            f.write("{}\n".format(filenames[ind]))

    with open("test.txt", "w") as f:
        for ind in indecies[trn_amount+val_amount:]:
            f.write("{}\n".format(filenames[ind]))




if __name__ == "__main__":
    ap = argparse.ArgumentParser(
            description = "Takes a an annotation csv file and analyze it")
    ap.add_argument("-inputFile", "--inputFile", type=str, default = "/Users/alteafogh/Documents/ITU/AML/AML-fish-project/data/brackish-dataset/versions/4/annotations/files/ann.txt",
                    help="Path to the image list file")
    ap.add_argument("-seed", "--seed", type=int, default = 1234567890,
                    help="Seed for the numpy RNG")
    ap.add_argument("-trnSplit", "--trnSplit", type=float, default = 0.8,
                    help="Percentage of data used for training. Should be between 0 and 1")
    ap.add_argument("-valSplit", "--valSplit", type=float, default = 0.1,
                    help="Percentage of data used for validation. Should be between 0 and 1")
    ap.add_argument("-tstSplit", "--tstSplit", type=float, default = 0.1,
                    help="Percentage of data used for testing. Should be between 0 and 1")
    
    args = vars(ap.parse_args())
    
    createDatasetSplit(args)