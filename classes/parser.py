from classes.predicate import Predicate
from classes.action import Action


class Parser(object):
    def __init__(self, domain_path, outer_sep, inner_sep):
        self.domain_path = domain_path
        self.outer_sep = outer_sep
        self.inner_sep = inner_sep
        self.line_sep = '\n'
        self.predicates = []

    def read_predicates(self, domain):
        predicates = domain[0].split(self.line_sep)
        predicates = [Predicate(p.split(':')[0], int(p.split(':')[1])) for p in predicates[1:]]
        return predicates

    def parse_predicates(self, n_predicates, predicates_lines):
        idx = 0
        predicates = []
        print(predicates_lines)
        for i in range(n_predicates):
            print(idx)
            print(predicates_lines[idx])
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

    def parse_domain(self):
        with open(self.domain_path, 'r') as f:
            domain = f.read()
            domain = domain.strip().split(self.outer_sep)

        self.predicates = self.read_predicates(domain)
        return self.parse_predicates(3, domain[1].split(self.line_sep)[5:10])


if __name__ == '__main__':
    p = Parser('../problems/domain.txt', '\n\n\n', '\n\n')
    print(p.parse_domain())
