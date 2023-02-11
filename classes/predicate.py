class Predicate(object):
    def __init__(self, name, n_args, args=None):
        self.name = name
        self.n_args = n_args
        if args is None:
            self.args = [''] * n_args
        else:
            self.args = args

    def replace_with_objects(self, objects_mapping):
        args = [objects_mapping[arg] for arg in self.args]
        return Predicate(name=self.name,
                         n_args=self.n_args,
                         args=args)

    def __str__(self):
        return self.name + '(' + ', '.join([arg for arg in self.args]) + ')'

    def __hash__(self):
        return hash(self.name + " ".join(self.args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if other.name != self.name:
            return False
        if other.n_args != self.n_args:
            return False
        for i in range(len(self.args)):
            if self.args[i] != other.args[i]:
                return False
        return True