#!/usr/bin/env python3

import getopt
import sys
import numpy as np

def create_config(states,actions,output_path):
    '''
    Creates a CSV configuration files at output_path, given the number of states and actions.
    '''
    # Make a template for the matrix
    matrix = ""
    for i in range(1,states+1):
        matrix += (",%d" % i)
    matrix += "\n"
    for i in range(1,states+1):
        matrix += ("%s" % i) + (",-" * states)
        matrix += "\n"
    # Create the tsv file
    with open(output_path,'w') as tsv:
        tsv.write("States,%d\n" % states)
        tsv.write("Actions,%d\n" % actions)
        tsv.write("Agent Reservation Utility,-\n")
        tsv.write("REWARDS\n")
        tsv.write(matrix)
        costs_labels = ["COSTS - ACTION %d\n" % i for i in range(1,actions+1)]
        for label in costs_labels:
            tsv.write(label)
            tsv.write(matrix)
        trans_probs_labels = ["TRANS PROB - ACTION %d\n" % i for i in range(1,actions+1)]
        for label in trans_probs_labels:
            tsv.write(label)
            tsv.write(matrix)

def main(argv):
    '''
    The main function.
    '''
    help_message = "Determines the optimal set of contracts for a given instance of a multistate moral hazard problem."
    usage_message = "Usage: [-h help and usage] [-c <create config file at given path>] [-i input config file] [-a number of actions] [-s number of states]"
    options = "hc:i:a:s:"

    if len(argv) == 1:
        print(help_message)
        print(usage_message)
        sys.exit(0)

    try:
        opts, args = getopt.getopt(argv[1:],options)
    except getopt.GetoptError:
        print("Error: unable to read command line arguments.")
        sys.exit(1)
    
    input_path = None
    output_path = None
    num_states = None
    num_actions = None
    
    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            print(usage_message)
        elif opt == '-c':
            output_path = arg
        elif opt == '-i':
            input_path = arg
        elif opt == '-a':
            num_actions = int(arg)
        elif opt == '-s':
            num_states = int(arg)

    opts_incomplete = False

    if input_path is not None and output_path is not None:
        print("Error: only one of -i or -c can be specified.")
        opts_incomplete = True
    if output_path is not None and (num_states is None or num_actions is None):
        print("Error: please specify the number of states and the number of actions for the model.")
        opts_incomplete = True
    if opts_incomplete:
        print(usage_message)
        sys.exit(1)

    if output_path is not None:
        create_config(num_states,num_actions,output_path) 
        print("Created configuration file at %s" % (output_path))
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
