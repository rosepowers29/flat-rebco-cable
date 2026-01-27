# necessary imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from pathlib import Path

R_CABLE = 5.8e-5

def get_tape_current(infile):
    # get keys
    keys = infile.columns
    # find current and voltage channels
    if 'CH3' in keys:
        chV_tot = 'CH3'
        chV_tape = 'CH6'
    elif 'CH4' in keys:
        chV_tot = 'CH4'
        chV_tape = 'CH6'
    elif 'CH5' in keys:
        chV_tot = 'CH5'
        chV_tape = 'CH6'
    else:
        return None
    # fill these with the input data
    V_tot = np.array(infile[chV_tot])
    V_tape = np.array(infile[chV_tape])
    I_input = np.array(infile['CURRENT'])

    try:
        I_cable = V_tot / R_CABLE
        I_tape = I_input - I_cable
    except Exception:
        return None

    return I_tape, V_tape

# parse input files
parser = ArgumentParser()
parser.add_argument("-i", "--infiles", dest = "infiles", nargs = '+')
args = parser.parse_args()


for infile in args.infiles:
    # sep \t lets us read in a tab-separated textfile as a csv
    csv_in = pd.read_csv(infile, sep = "\t")
    try:
        I_tape, V_tape = get_tape_current(csv_in)
    except Exception:
        continue
    csv_in['TAPE_CURRENT'] = I_tape
    csv_in['TAPE_VOLTAGE'] = V_tape
    csv_in.to_csv(Path(infile).stem+'-cleaned.txt', sep='\t')
