class Behavior:
    def __init__(self, function, condition, target):
        self.function = function
        self.condition = condition
        self.target = target
        
    def get_result(self):
        switch = {
                "greater_than":self.function() > self.target,
                "less_than":self.function() < self.target,
                "equal_to":self.function() == self.target,
                "greater_than_or_equal_to":self.function() >= self.target,
                "less_than_or_equal_to":self.function() <= self.target
            }
        return switch[self.condition]
    
    def test():
        func = lambda : 5+7
        condit = "greater_than_or_equal_to"
        targ = 5
        beh = Behavior(func, condit, targ)
        print("Expected: True -- Result: "+beh.get_result())
    

        