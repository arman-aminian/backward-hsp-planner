import itertools
from classes.predicate import Predicate


def print_list_of_predicates(predicates):
    for predicate in predicates:
        print(predicate)


def deep_str(pre):
    if type(pre) is list:
        return str([str(p) for p in pre])
    return str(pre)


def get_all_ground_predicates(predicates, objects):
    ground_predicates = []
    for pre in predicates:
        objects_permutations = list(itertools.permutations(objects, pre.n_args))
        objects_mapping = {}
        for permutation in objects_permutations:
            pre = Predicate(pre.name, pre.n_args, args=['a' + str(i) for i in range(pre.n_args)])
            for i in range(len(pre.args)):
                objects_mapping[pre.args[i]] = permutation[i]

            ground_predicates.append(pre.replace_with_objects(objects_mapping))
    return ground_predicates


key_sort = lambda x: str(x)


def is_applicable(init_state, preconditions):
    for state in preconditions:
        if state not in init_state:
            return False
    return True


def calculate_delta2(p):
    delta2_init = [sorted(t, key=key_sort) for t in list(itertools.combinations([pre for pre in p.init_state], 2))] + [
        pre for pre in p.init_state]

    ground_predicates = get_all_ground_predicates(p.predicates, p.objeects)
    str_ground_predicates = [pre for pre in ground_predicates] + [sorted(t, key=key_sort) for t in (
        itertools.combinations([pre for pre in ground_predicates], 2))]

    delta2_mapping = {}
    for pre in str_ground_predicates:
        delta2_mapping[deep_str(pre)] = float('inf')
    for pre in delta2_init:
        delta2_mapping[deep_str(pre)] = 0

    U = set(p.init_state)

    while (True):
        Uprim = set(U)
        for action in p.ground_actions:
            if not is_applicable(Uprim, action.preconditions):
                continue
            for pred in action.add_effects:
                Uprim.add(pred)

            max_delta2 = -1
            for pred in [pre for pre in action.preconditions] + [sorted(t, key=key_sort) for t in (
            itertools.combinations([pre for pre in action.preconditions], 2))]:
                if delta2_mapping[deep_str(pred)] > max_delta2:
                    max_delta2 = delta2_mapping[deep_str(pred)]
                    if max_delta2 == 0:

            for pred in [pre for pre in action.add_effects] + [sorted(t, key=key_sort) for t in (
            itertools.combinations([pre for pre in action.add_effects], 2))]:
                delta2_mapping[deep_str(pred)] = min(delta2_mapping[deep_str(pred)], 1 + max_delta2)

            for p1 in U - set(action.add_effects):
                for p2 in set(action.add_effects) - U:
                    pair = sorted((p1, p2), key=key_sort)
                    delta2_mapping[deep_str(pair)] = min(delta2_mapping[deep_str(pair)], 1 + max_delta2)

        if Uprim == U:
            break
        U = set(Uprim)

    return delta2_mapping