import decimal
import json
from TemporalFeatures import Features as ft
from Behavior import Behavior
from BehaviorGroup import BehaviorGroup


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
        # create the function based on the value of key 'function' with the inputs in key 'inputs'
        def function(input_array):
            return FunctionBuilder(jsonString['function'])(input_array, jsonString['inputs'])

        if('inputs' in jsonString):
            if('interval' in jsonString['inputs']):
                jsonString['inputs']['interval'] = int(
                    jsonString['inputs']['interval'])
            if('wg' in jsonString['inputs']):
                jsonString['inputs']['wg'] = float(jsonString['inputs']['wg'])

        behavior = Behavior(
            function, jsonString['condition'], jsonString['target'], jsonString['function'])
        return behavior
    group = jsonString['group']
    condition = jsonString['group_condition']
    collection = []
    for item in group:
        collection.append(ParseBehaviorGroup(item))
    behavior_group = BehaviorGroup(collection, condition)
    return behavior_group


def ParseBehavior(jsonString):
    # the string is of a behavior not a behavior group
    # create the function based on the value of key 'function' with the inputs in key 'inputs'
    def function(input_array):
        return FunctionBuilder(jsonString['function'])(
            input_array, jsonString['inputs'])

    if('inputs' in jsonString):
        if('interval' in jsonString['inputs']):
            jsonString['inputs']['interval'] = int(
                jsonString['inputs']['interval'])
        if('wg' in jsonString['inputs']):
            jsonString['inputs']['wg'] = float(jsonString['inputs']['wg'])

    behavior = Behavior(
        function, jsonString['condition'], jsonString['target'], jsonString['function'])
    return behavior


def FunctionBuilder(function_name):
    switch = {
        "moving_average": lambda input_array, inputs: ft.moving_average(input_array, inputs['interval']),
        "resistance": lambda input_array, inputs: ft.resistance(input_array, inputs['interval']),
        "support": lambda input_array, inputs: ft.support(input_array, inputs['interval']),
        "resistance_trendline": lambda input_array, inputs: ft.resistance_trendline(input_array, inputs['interval'], inputs['wg']),
        "support_trendline": lambda input_array, inputs: ft.support_trendline(input_array, inputs['interval'], inputs['wg']),
        "moving_variance": lambda input_array, inputs: ft.moving_variance(input_array, inputs['interval']),
        "moving_deviation": lambda input_array, inputs: ft.moving_deviation(input_array, inputs['interval']),
        "moving_tdssd": lambda input_array, inputs: ft.moving_tdssd(input_array, inputs['interval'], inputs['isMetric']),
        "moving_max": lambda input_array, inputs: ft.moving_max(input_array, inputs['interval']),
        "moving_min": lambda input_array, inputs: ft.moving_min(input_array, inputs['interval']),
        "linear_regression_forecast": lambda input_array, inputs: ft.linear_regression_forecast(input_array, inputs['window'], inputs['interval']),
        "momentum": lambda input_array, inputs: ft.momentum(input_array, inputs['interval']),
        "dx_max": lambda input_array, inputs: ft.dx_max(input_array, inputs['interval']),
        "dx_min": lambda input_array, inputs: ft.dx_min(input_array, inputs['interval']),
        "difference": lambda input_array, inputs: ft.difference(input_array, inputs['order'], inputs['interval']),
        "average_difference": lambda input_array, inputs: ft.average_difference(input_array, inputs['order'], inputs['interval']),
        "average_difference_percent": lambda input_array, inputs: ft.average_difference_percent(input_array, inputs['order'], inputs['interval']),
        "derivative_ratio_max": lambda input_array, inputs: ft.derivative_ratio_max(input_array, inputs['interval']),
        "derivative_ratio_min": lambda input_array, inputs: ft.derivative_ratio_min(input_array, inputs['interval']),
        "difference_ratio": lambda input_array, inputs: ft.difference_ratio(input_array, order, inputs['interval']),
        "movement_ratio": lambda input_array, inputs: ft.movement_ratio(input_array, inputs['output_type']),
    }

    if(function_name in switch):
        return switch[function_name]
    else:
        return
