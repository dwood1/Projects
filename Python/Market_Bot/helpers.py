import decimal, json

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def ParseBehaviorGroup(jsonString):
    if('group' not in jsonString):
        # the string is of a behavior not a behavior group
        #TODO -- create the function based on the value of key 'function' with the inputs in key 'inputs'
        behavior = Behavior(jsonString['function'], jsonString['condition'], jsonString['target'])
        return behavior
    group = jsonString['group']
    condition = jsonString['condition']
    collection = []
    for item in group:
        collection.append(ParseBehaviorGroup(item))
    behavior_group = BehaviorGroup(collection, condition)
    return behavior_group