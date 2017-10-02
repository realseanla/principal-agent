#!usr/bin/env python
# Author: Sean La

import getopt
import sys
import cvxpy as cvx
import numpy as np

def get_possible_policies(num_states, num_actions):
    action_list = ['action_%d' % (action) for action in range(num_actions)]
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
    num_states = problem_specs['num_states']
    # trans_matrix is a num_states x num_states x num_actions size array
    prob = problem_specs['trans_matrix']
    initial_prob = problem_specs['initial_prob']
    # rewards is a num_states x num_states size matrix
    rewards = problem_specs['rewards']
    # trans_matrix is a num_states x num_states x num_actions size array
    costs = problem_specs['costs']
    # agent participation constraint
    part_const = problem_specs['part_const']
    # maximum contracts vector
    max_contract = problem_specs['max_contract']
    # Create the contract vector
    contracts = Variable(num_states)

    # Create the objective function
    principal_util = [ prob[:,policy[i],i]*(reward[i,:]-contracts) for i in range(num_states) ]
    objective = cvx.Maximize(initial_prob*principal_util) 
    # Construct the constraints
    agent_util = [ prob[:,policy[i],i]*(contracts-costs[i,:]) for i in range(num_states) ]
    constraints = [ initial_prob*agent_util > part_const, contracts < max_contract ]
    solution = cvx.Problem(objectice,constraints)

    return solution
        
def main(argv):
    help_message = "Description: Repeated Moral Hazard Relationship in Large-Scale Shortest Path Problem"
    usage_message = "Usage: %s [-h help and usage]" % (sys.argv[0])
    options = "hi:o:"

    try:
        opts, args = getopt.getopt(sys.argv[1:],options)
    except:
        print("Error: unable to read command line arguments.")
        sys.exit(1)

    if len(sys.argv) == 1:
        print(help_message)
        print(usage_message)
        sys.exit(1)

    problem_specs = {'trans': trans_matrix, 'rewards': rewards, 'costs': costs, 'agent_part': agent_part, \
                     'max_contract': max_contract, 'num_states': num_states, 'num_actions': num_actions, \
                     'lambda': lmbda }

    possible_policies = get_possible_policies(num_states, num_actions)
    optimal_contracts = get_optimal_contracts_for_policies(possible_policies, problem_specs)
    solution = determine_optimal_policy_and_contract(optimal_contracts)

if __name__ == "__main__":
    main(sys.argv)
