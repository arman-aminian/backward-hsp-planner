from utils.constants import OUTER_SEP, INNER_SEP
from classes.parser import Parser
from classes.action import Action
from classes.predicate import Predicate
import random
import numpy as np
import itertools
from utils.functions import calculate_delta2
from utils.functions import deep_str
from utils.functions import key_sort


def check_relevancy(act: Action, goal_list: list) -> bool:
    flag = False
    # as we do not have any negative precond or negative goal, so just we care about add effects
    for add_eff in act.add_effects:
        for g in goal_list:
            if add_eff == g:
                flag = True
                break
        if flag:
            break
    if not flag:
        return False
    # check whether negative effects delete a goal
    for del_eff in act.delete_effects:
        for g in goal_list:
            if del_eff == g:
                return False
    return True


def gamma_inverse(act: Action, goals: list) -> list:
    for add_eff in act.add_effects:
        if add_eff in goals:
            goals.remove(add_eff)
    for precond in act.preconditions:
        goals.append(precond)
    return goals


def calc_delta_state(new_goals):
    all_pairs = list(itertools.combinations(new_goals, 2))
    maximum = 0
    for pair in all_pairs:
        k = delta2_mapping[deep_str(sorted(pair, key=key_sort))]
        if k > maximum:
            maximum = k
    return maximum


def backward_search(init, goals, actions, trajectory, depth=0):
    if depth > 6:
        return False
    cur_goals = goals
    # check if init state satifies cur_goals
    flag = False
    for goal in cur_goals:
        # print('here')
        for pred in init:
            if goal == pred:
                flag = True
                break
        if flag:
            # check the next goal
            flag = False
        else:
            break
    else:
        # print('problem sloved :))')
        return trajectory

    relevant_actions = []
    for act in actions:
        if check_relevancy(act, cur_goals):
            relevant_actions.append(act)

    # calculate delta 2 for every state will be reach after applying an action
    delta_of_states = np.zeros(len(relevant_actions))
    for ind, act in enumerate(relevant_actions):
        new_goals = gamma_inverse(act, cur_goals.copy())
        delta_state = calc_delta_state(new_goals)
        delta_of_states[ind] = delta_state

    # act_index = np.argmin(delta_of_states)
    # np.delete(delta_of_states, act_index)
    # relevant_actions.remove(act)

    while len(relevant_actions) > 0:
        act_index = np.argmin(delta_of_states)
        delta_of_states = np.delete(delta_of_states, act_index)

        act = relevant_actions[act_index]
        relevant_actions.remove(act)
        new_goals = gamma_inverse(act, cur_goals.copy())

        # check new_goals is superset of old goals
        flag = False

        for old_goal in cur_goals:
            for new_goal in new_goals:
                if old_goal == new_goal:
                    flag = True
                    break
            if not flag:
                # new goals are superset of old goals and we struggled in a loop, so test the next relevant action
                flag = True
                break
            else:
                flag = False
        # if loop did not detected
        if flag:
            new_trajectory = trajectory.copy()
            new_trajectory.insert(0, act)

            path = backward_search(init, new_goals, actions, new_trajectory, depth + 1)
            if not path:
                continue
            return path

    return False


p = Parser('./problems/domain.txt', './problems/simple.txt', OUTER_SEP, INNER_SEP)
p.parse()

trajectory = []
delta2_mapping = calculate_delta2(p)

t = backward_search(p.init_state, p.goals, p.ground_actions, trajectory)
for i, act in enumerate(t):
    print(str(i) + ': (' + str(act) + ')')
