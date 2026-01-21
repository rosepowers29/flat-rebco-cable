# necessary imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser

R_CABLE = 5.8e-5

def get_tape_current(infile):
    # fill these with the input data
    V_tot = np.array(infile['CH3'])
    V_tape = np.array(infile['CH5']) # should I be averaging channel 5 and channel 6??
    I_input = np.array(infile['CURRENT'])

    I_cable = V_tot / R_CABLE
    I_tape = I_input - I_cable

    return I_tape, V_tape

# parse input files
parser = ArgumentParser()
parser.add_argument("-i", "--infiles", dest = "infiles", nargs = '+')
args = parser.parse_args()


for infile in args.infiles:
    # sep lets us read in a tab-separated textfile as a csv
    csv_in = pd.read_csv(infile, sep = "\t")
    I_tape, V_tape = get_tape_current(csv_in)
    csv_in['TAPE_CURRENT'] = I_tape
    csv_in['TAPE_VOLTAGE'] = V_tape
    csv_in.to_csv(infile+'-cleaned.txt', sep='\t')
