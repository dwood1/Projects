class BehaviorGroup():
    def __init__(self, group, group_condition):
        self.group = group
        self.group_condition = group_condition

    # Sets the internal dataset of each behavior object in the group.
    def set_data(self, input_array):
        # TODO Error handling
        if(self.group != None):
            for behavior in self.group:
                behavior.set_data(input_array)

    # Gets the result of the comparison expression at the desired index for each behavior in the group
    # against the target. If an index is not supplied, then evaluate the function as is. If an external target is not supplied, the internal
    # target will be used
    def get_result(self, index=None, target=None):
        # TODO Error handling
        if(self.group != None):
            if(self.group_condition == "and"):
                for behavior in self.group:
                    if(not behavior.get_result(index, target)):
                        return False
                return True
            else:
                for behavior in self.group:
                    if(behavior.get_result(index, target)):
                        return True
                return False
