import itertools
from classes.predicate import Predicate


def print_list_of_predicates(predicates):
    for predicate in predicates:
        print(predicate)


def get_all_ground_predicates(predicates):
    ground_predicates = []
    for pre in predicates:
        objects_permutations = list(itertools.permutations(p.objects, pre.n_args))
        objects_mapping = {}
        for permutation in objects_permutations:
            pre = Predicate(pre.name, pre.n_args, args=['a' + str(i) for i in range(pre.n_args)])
            for i in range(len(pre.args)):
                objects_mapping[pre.args[i]] = permutation[i]

            ground_predicates.append(pre.replace_with_objects(objects_mapping))
