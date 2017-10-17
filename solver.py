#!/usr/bin/env python
# Author: Sean La

import getopt
import sys
import cvxpy as cvx
import numpy as np
import itertools

# Global variables for problem_specs dict keys
NUM_STATES = 'num_states'
NUM_ACTIONS = 'num_actions'
TRANS_MATRIX = 'trans_matrix'
INITIAL_PROB = 'initial_prob'
REWARDS = 'rewards'
COSTS = 'costs'
PART_CONST = 'part_const'
MAX_CONTRACT = 'max_contract'

class ActionMatrix:
    '''
    Wrapper that holds a matrix that depends on the agent's actions
    '''
    def __init__(self,matrix,num_states):
        self.matrix = matrix
        self.num_states = num_states
    def for_policy(self,policy):
        '''
        Returns the matrix given a specific policy
        '''
        num_states = self.num_states
        policy_matrix = np.zeros( (num_states,num_states) )
        matrix = self.matrix
        for i in range(num_states):
            for j in range(num_states):
                policy_matrix[i,j] = matrix[i,j,policy[i]]
        return policy_matrix

def get_possible_policies(problem_specs):
    num_states = problem_specs[NUM_STATES]
    num_actions = problem_specs[NUM_ACTIONS]
    action_list = [action for action in range(num_actions)]
    # Cartesian product of the action_list with itself num_states times is equivalent to finding all possible policies
    policies = [policy for policy in itertools.product(action_list, repeat = num_states)]
    return policies 

def get_optimal_contracts_for_policies(policies, problem_specs):
    contracts = {}
    for policy in policies:
        contract = determine_optimal_contract(policy, problem_specs)
        contracts[policy] = contract
    return contracts

def determine_optimal_contract(policy, problem_specs):
    num_states = problem_specs[NUM_STATES]
    # trans_matrix is a num_states x num_states x num_actions size array
    trans_prob = problem_specs[TRANS_MATRIX].for_policy(policy)
    initial_prob = problem_specs[INITIAL_PROB]
    # rewards is a num_states x num_states size matrix
    rewards = problem_specs[REWARDS]
    # trans_matrix is a num_states x num_states x num_actions size array
    costs = problem_specs[COSTS].for_policy(policy)
    # agent participation constraint
    part_const = problem_specs[PART_CONST]
    # maximum contracts vector
    max_contract = problem_specs[MAX_CONTRACT]
    max_cont = max_contract[0]
    initial_prob = np.hstack((initial_prob,initial_prob))

    ## Construct the objective
    contracts = cvx.Variable(num_states,1)
    contracts_matrix = contracts
    # equivalent to repmat as in matlab
    for i in range(num_states-1):
        contracts_matrix = cvx.hstack(contracts_matrix,contracts) 
    # contruct the principals reward objective function
    principals_reward = rewards-contracts_matrix
    principals_reward = cvx.mul_elemwise(trans_prob,principals_reward)
    # at this step, we have the expected value of the principals reward among ending states
    principals_reward = cvx.mul_elemwise(initial_prob,principals_reward)
    # now, we have the expected value of the principal's reward among both initial and ending states
    principals_reward = cvx.sum_entries(principals_reward)
    # the objective is to maximize the principal's reward
    objective = cvx.Maximize(principals_reward)

    ## Construct the constraints
    # First, we need to make sure the contracts we use don't surpass the maximum allowed contracts in value
    constraints = [contracts < max_contract]
    # Next, construct the agent's participation constraint
    agents_reward = contracts_matrix - costs
    agents_reward = cvx.mul_elemwise(trans_prob,agents_reward)
    agents_reward = cvx.mul_elemwise(initial_prob,agents_reward)
    agents_reward = cvx.sum_entries(agents_reward)
    constraints.append(agents_reward > part_const)

    problem = cvx.Problem(objective,constraints)
    problem.solve()
    return problem
 
def get_test_problem_specs():
    num_actions = 2
    actions = [ "action_%d" % (action) for action in range(num_actions) ]
    num_states = 2
    problem_specs = {NUM_ACTIONS: num_actions, NUM_STATES: num_states} 
    policies = get_possible_policies(problem_specs)
    trans_matrix = np.zeros( (num_states,num_states,num_actions) )
    for i in range(num_actions):
        trans_matrix[:,:,i] = [[0.5,0.5],[0.3,0.7]]
    trans_matrix = ActionMatrix(trans_matrix,num_states)

    rewards = np.array([[5,5],[1,1]])
    costs = np.zeros( (num_states,num_actions,num_states) )
    for i in range(num_actions):
        costs[:,:,i] = np.array([ [2,2],[3,3] ])
    costs = ActionMatrix(costs,num_states) 

    part_const = 2
    max_contract = np.array([3,3])
    initial_prob = np.array([0.5,0.5])
    initial_prob.shape = (2,1)

    problem_specs = {
        NUM_ACTIONS: num_actions,
        NUM_STATES: num_states,
        TRANS_MATRIX: trans_matrix,
        REWARDS: rewards,
        COSTS: costs,
        PART_CONST: part_const,
        MAX_CONTRACT: max_contract,
        INITIAL_PROB: initial_prob,
        }

    return problem_specs

def read_config_file(config_path):
    return None

def print_solution(solution):
    return None

def write_solution(solution,output_path):
    return None

def main(argv):
    help_message = "Description: Repeated Moral Hazard Relationship in Large-Scale Shortest Path Problem"
    usage_message = "Usage: %s [-h help and usage] [-t test] [-i configuration file] [-o output path]" % (sys.argv[0])
    options = "hti:o:"

    try:
        opts, args = getopt.getopt(sys.argv[1:],options)
    except:
        print("Error: unable to read command line arguments.")
        sys.exit(1)

    if len(sys.argv) == 1:
        print(help_message)
        print(usage_message)
        sys.exit(1)

    config_path = None
    output_path = None
    do_test = False

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            print(usage_message)
            sys.exit(0)
        elif opt == '-t':
            do_test = True
        elif opt == '-i':
            config_path = arg
        elif opt == '-o':
            output_path = arg 

    opts_incomplete = False

    if not do_test:
        if config_path is None:
            print("Error: please provide a configuration file.")
            opts_incomplete = True
        if output_path is None:
            print("Error: please specify a path for the output file.")
            opts_incomplete = True 
    if opts_incomplete:
        print(usage_message)
        sys.exit(1)

    if (do_test):
        problem_specs = get_test_problem_specs()
    else:
        problem_specs = read_config_file(config_path)
    possible_policies = get_possible_policies(problem_specs)
    optimal_contracts = get_optimal_contracts_for_policies(possible_policies,problem_specs)
    '''
    solution = determine_optimal_policy_and_contract(optimal_contracts)
    print_solution(solution)
    '''
    if (not do_test):
        write_solution(solution,output_path)

if __name__ == "__main__":
    main(sys.argv)
