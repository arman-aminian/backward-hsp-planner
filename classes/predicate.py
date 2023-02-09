class Predicate(object):
    def __init__(self, name, n_args):
        self.name = name
        self.n_args = n_args
        self.args = [''] * n_args

    def __str__(self):
        return self.name + ":" + self.n_args + ' : ' + [arg for arg in self.args]
