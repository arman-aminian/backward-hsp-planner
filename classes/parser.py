from classes.predicate import Predicate
from classes.action import Action
import itertools


class Parser(object):
    def __init__(self, domain_path, problem_path, outer_sep, inner_sep):
        self.domain_path = domain_path
        self.problem_path = problem_path
        self.outer_sep = outer_sep
        self.inner_sep = inner_sep
        self.line_sep = '\n'
        self.predicates = []
        self.actions = []
        self.objects = []
        self.init_state = []
        self.goals = []
        self.ground_actions = []

    def read_predicates(self, domain):
        predicates = domain[0].split(self.line_sep)
        predicates = [Predicate(p.split(':')[0], int(p.split(':')[1])) for p in predicates[1:]]
        return predicates

    def parse_predicates(self, n_predicates, predicates_lines):
        idx = 0
        predicates = []
        for i in range(n_predicates):
            predicate_name = predicates_lines[idx].lower()
            predicate_n_args = -1
            for pred in self.predicates:
                if pred.name == predicate_name:
                    predicate_n_args = pred.n_args
            predicate_args = predicates_lines[idx + 1:idx + 1 + predicate_n_args]
            predicates.append(Predicate(name=predicate_name, n_args=predicate_n_args, args=predicate_args))
            idx = idx + predicate_n_args + 1

        return predicates

    def parse_action(self, operator_lines):
        preconditions_idx = [i for i in range(len(operator_lines)) if 'Preconditions' in operator_lines[i]][0]
        add_effects_idx = [i for i in range(len(operator_lines)) if 'Add-Effects' in operator_lines[i]][0]
        delete_effects_idx = [i for i in range(len(operator_lines)) if 'Delete-Effects' in operator_lines[i]][0]

        action_name = operator_lines[0]

        n_args = int(operator_lines[1].split(':')[1])
        args = operator_lines[2:preconditions_idx]

        n_preconditions = int(operator_lines[preconditions_idx].split(':')[1])
        preconditions = self.parse_predicates(n_preconditions, operator_lines[preconditions_idx + 1:add_effects_idx])

        n_add_effects = int(operator_lines[add_effects_idx].split(':')[1])
        add_effects = self.parse_predicates(n_add_effects, operator_lines[add_effects_idx + 1:delete_effects_idx])

        n_delete_effects = int(operator_lines[delete_effects_idx].split(':')[1])
        delete_effects = self.parse_predicates(n_delete_effects, operator_lines[delete_effects_idx + 1:])

        return Action(action_name, args, preconditions, add_effects, delete_effects)

    def read_operators(self, domain):
        actions = domain[1].split(self.inner_sep)
        actions[0] = self.line_sep.join(actions[0].split(self.line_sep)[1:])
        actions = [self.parse_action(action_lines.split(self.line_sep)) for action_lines in actions]
        return actions

    def read_objects(self, objects_lines):
        return [obj.lower() for obj in objects_lines.split(self.line_sep)[1:]]

    def read_init_state(self, init_state_lines):
        init_state_lines = init_state_lines.split(self.line_sep)
        n_predicates = int(init_state_lines[0].split(':')[1])
        return self.parse_predicates(n_predicates, init_state_lines[1:])

    def read_goals(self, goals_lines):
        goals_lines = goals_lines.split(self.line_sep)
        n_predicates = int(goals_lines[0].split(':')[1])
        return self.parse_predicates(n_predicates, goals_lines[1:])

    def create_ground_actions(self):
        ground_actions = []
        for action in self.actions:
            objects_permutations = list(itertools.permutations(self.objects, len(action.args)))
            for objects_permutation in objects_permutations:
                ground_actions.append(action.replace_with_objects(
                    list(objects_permutation))
                )
        return ground_actions

    def parse_domain(self):
        with open(self.domain_path, 'r') as f:
            domain = f.read()
            domain = domain.strip().split(self.outer_sep)

        self.predicates = self.read_predicates(domain)
        self.actions = self.read_operators(domain)

    def parse_problem(self):
        with open(self.problem_path, 'r') as f:
            problem = f.read()
            problem = problem.strip().split(self.outer_sep)

        self.objects = self.read_objects(problem[0])
        self.init_state = self.read_init_state(problem[1])
        self.goals = self.read_goals(problem[2])
        self.ground_actions = self.create_ground_actions()


if __name__ == '__main__':
    p = Parser('../problems/domain.txt', '\n\n\n', '\n\n')
    print(p.parse_domain())
