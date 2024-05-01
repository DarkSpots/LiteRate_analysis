import csv, sys
import os, glob
import time
import argparse
import numpy as np
from numpy import *
import multiprocessing

run = 1
settings = "-n 12000000 -s 1000 -p 100000 -rev_se 1"

def my_job(arg):
    cmd = "cd /home/silvestr/Documents/LiteRate/; "
    cmd = cmd + "python3 LiteRateForward.py -d %s -model_BDI 1 -calc_adequacy 0 %s" % (arg, settings)
    if run:
        os.system(cmd)
    else:
        print(cmd)
        

datasets = glob.glob("time2event/*")
CPUs = 50

if __name__ == '__main__': 
    pool = multiprocessing.Pool(CPUs)
    pool.map(my_job, datasets)
    pool.close()
