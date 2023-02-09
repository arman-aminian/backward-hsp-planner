class Predicate(object):
    def __init__(self, name, n_args, args=None):
        self.name = name
        self.n_args = n_args
        if args is None:
            self.args = [''] * n_args
        else:
            self.args = args

    def __str__(self):
        return self.name + ":" + str(self.n_args) + ' : ' + ', '.join([arg for arg in self.args])
