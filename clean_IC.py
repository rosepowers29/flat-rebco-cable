# necessary imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from pathlib import Path

#R_CABLE = 5.8e-5
RESISTIVITY = 0.00025 #ohm / m
RESIST_IAN = 0.0004 #ohm / m

def get_tape_current(infile, res):
    # get keys
    keys = infile.columns
    # find current and voltage channels
    if 'CH3' in keys:
        chV_tot = 'CH3'
    elif 'CH4' in keys:
        chV_tot = 'CH4'
    else:
        return None
    # fill these with the input data
    V_tot = np.array(infile[chV_tot])
    V_tot = abs(V_tot)
    I_input = np.array(infile['CURRENT'])

    try:
        I_cable = V_tot / res
        I_tape = I_input - I_cable
    except Exception:
        return None

    return I_tape

def get_resistance(resistivity, d_tap):
    # calculate cable resistance given resistivity value and tap spacing
    d_tap_m = d_tap / 1000 #entered in mm, change to meters
    res = resistivity * d_tap
    return res

# parse input files
parser = ArgumentParser()
parser.add_argument("-i", "--infiles", dest = "infiles", nargs = '+')
parser.add_argument("-d", "--dtap", type = float, dest = "d_tap") # comes in mm
parser.add_argument("-r", "--ian", dest = "is_ian", default = False)
args = parser.parse_args()


for infile in args.infiles:
    # sep \t lets us read in a tab-separated textfile as a csv
    csv_in = pd.read_csv(infile, sep = "\t")
    if args.is_ian:
        restv = RESIST_IAN
    else:
        restv = RESISTIVITY
    # get cable resistance
    res = get_resistance(restv, args.d_tap)
    try:
        I_tape = get_tape_current(csv_in, res)
    except Exception:
        print("exception")
        print(infile)
        continue
    csv_in['TAPE_CURRENT'] = I_tape
    csv_in.to_csv(Path(infile).stem+'-cleaned.txt', sep='\t')
