class Parser(object):
    def __init__(self, domain_path, outer_sep, inner_sep):
        self.domain_path = domain_path
        self.outer_sep = outer_sep
        self.inner_sep = inner_sep

    def parse_domain(self):
        with open(self.domain_path, 'r') as f:
            domain = f.read()
            domain = domain.strip().split(self.outer_sep)

        predicates = domain[0].split(self.inner_sep)
        predicates = [(p.split(':')[0], p.split(':')[1]) for p in predicates[1:]]
        return predicates
