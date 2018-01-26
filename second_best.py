#!/usr/bin/env python3

import getopt
import sys
import os
import cplex
import numpy

k_NUM_ACTIONS = "NUM_ACTIONS"
k_NUM_STATES = "NUM_STATES"
k_TRANS_PROB = "TRANS_PROB"
k_INIT_PROB = "INIT_PROB"
k_P_REWARD = "PRINCIPAL_REWARD"
k_A_COST = "AGENT_COST"

def create_config(output_prefix):
    '''
    Create TSV configuration file
    '''
    return None

def read_config(input_path):
    '''
    Read TSV configuration file
    '''
    model = {}
    return model

def main(argv):
    '''
    main function
    '''
    help_message = ""
    usage_message = ""
    options = "h"

    try:
        opts,args = getopt.getopt(argv[1:],options)
    except getopt.GetoptError:
        print("Error: unable to read command line arguments.")
        sys.exit(1)

    if len(argv) == 1:
        print(help_message)
        print(usage_message)
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            print(usage_message)
            sys.exit(0)
        elif opt == '-t':
            unit_tests()
            sys.exit(0)

    opts_incomplete = False

    if opts_incomplete:
        print(usage_message)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
