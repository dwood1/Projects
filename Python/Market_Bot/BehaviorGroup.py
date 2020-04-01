class BehaviorGroup():
    def __init__(self, group, condition):
        self.group = group
        self.condition = condition
        
    def get_result(self):    
        if(self.condition = "and"):
            for behavior in group:
                if(not behavior.get_result())
                    return False
            return True
        else:    
            for behavior in group:
                if(behavior.get_result())
                    return True
            return False
            