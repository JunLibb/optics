# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 10:33:58 2021

@author: APPO
"""

from lt import *
import argparse
import numpy as np
import pandas as pd
import win32com.client as client
import clr
import System
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='Etendue of receiver')
    parser.add_argument("--r", "-r", "-Receiver",type=str, default="Receiver_DMD",
                        help="Receiver Name")

    args = parser.parse_args()
    receiver = args.r
    print("Receiver:",receiver)
    test = Receiver(src=receiver)
    
    
if __name__ == "__main__":
    main()
