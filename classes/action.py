class Action(object):
    def __init__(self, name, args, preconditions, add_effects, delete_effects):
        self.name = name
        self.args = args
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.delete_effects = delete_effects

    def replace_with_objects(self, objects):
        objects_mapping = {}
        for i in range(len(self.args)):
            objects_mapping[self.args[i]] = objects[i]

        preconditions = [precondition.replace_with_objects(objects_mapping) for precondition in self.preconditions]
        add_effects = [add_effect.replace_with_objects(objects_mapping) for add_effect in self.add_effects]
        delete_effects = [delete_effect.replace_with_objects(objects_mapping) for delete_effect in self.delete_effects]

        return Action(name=self.name, args=objects, preconditions=preconditions, add_effects=add_effects, delete_effects=delete_effects)

    def __str__(self):
        return self.name \
               + ' ' + ' '.join([str(a) for a in self.args])
