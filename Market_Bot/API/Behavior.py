# A behavior stores a function/operator and a condition. The behavior object can
# also store a target (which will be used to evaulate the expression in get_result).


class Behavior:
    def __init__(self, function, condition, target, func_name=None):
        self.key = 0
        self.function = function
        self.condition = condition
        self.target = target
        self.name = func_name

    # Sets the internal dataset of the behavior object. This is done by
    # running the internal function/operator over the 'input_array'
    # and then setting the result to 'data'
    def set_data(self, input_array):
        # TODO Error handling
        self.data = self.function(input_array)
        return self.data

    # Gets the result of the comparison expression at the desired index
    # against the target. If an index is not supplied, then evaluate the function as is. If an external target is not supplied, the internal
    # target will be used
    def get_result(self, index=None, target=None):
        # TODO Error handling
        if(index == None):
            result = self.function()
        else:
            result = self.data[index]

        if(target == None):
            target = self.target

        switch = {
            "greater_than": result > target,
            "less_than": result < target,
            "equal_to": result == target,
            "greater_than_or_equal_to": result >= target,
            "less_than_or_equal_to": result <= target
        }
        return switch[self.condition]
