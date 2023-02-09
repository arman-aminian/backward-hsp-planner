class Action(object):
    def __init__(self, name, args, preconditions, add_effects, delete_effects):
        self.name = name
        self.args = args
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.delete_effects = delete_effects

    def __str__(self):
        return self.name + '\nargs:' + self.args \
               + '\npreconditions:' + self.preconditions\
               + '\nadd effects:' + self.add_effects\
               + '\ndelete effects:' + self.delete_effects
