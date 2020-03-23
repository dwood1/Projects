
# 
__all__ = ['test',
           'average',
           'variance',
           'standard_deviation'          
           ]

def test():
    print('Test Successful')

#-------------------------Mathematical Operators------------------------------#

def average(input_array):
    # time: O(n), space: O(1)
    return sum(input_array) / len(input_array)

def variance(input_array):
    # time: O(n), space: O(n)
    x_bar = average(input_array)
    x2_bar = average([x**2 for x in input_array])
    return x2_bar - x_bar**2
    
def covariance(x_array, y_array=[]):
    # time: O(n), space: O(n)
    l_x = len(x_array)
    x_bar = average(x_array)
    if(y_array == []):
        y_bar = (l_x-1)/2     
        xy_bar = average([x_array[i]*i for i in range(l_x)])
        return (xy_bar - (x_bar*y_bar))
    elif(l_x != len(y_array)):
        print("The arrays must be the same length!")
        return []
    else:
        loop_xy = zip(x_array, y_array)
        y_bar = average(y_array)
        xy_bar = average([x*y for x, y in loop_xy])
        return (xy_bar - (x_bar*y_bar))

def standard_deviation(input_array):
    # time: O(n), space: O(n)
    n = len(input_array)
    avg = average(input_array)
    return (average([(input_array[i] - avg)**2 
                     for i in range(n)]))**(0.5)
    
def sample_average(input_array):
    # time: O(n), space: O(1)
    return sum(input_array) / (len(input_array)-1)
    
def sample_variance(input_array):
    # time: O(n), space: O(n)
    n = len(input_array)
    sAvg = sample_average(input_array)
    return sample_average([(input_array[i] - sAvg)**2 
                     for i in range(n)])
    
def sample_standard_deviation(input_array):
    # time: O(n), space: O(n)
    n = len(input_array)
    sAvg = sample_average(input_array)
    return (sample_average([(input_array[i] - sAvg)**2 
                     for i in range(n)]))**(0.5)
    
def time_dependent_sample_standard_deviation(input_array):
    # time: O(n), space: O(n)
    n = len(input_array)   
    return sample_average([((i/(n-2))*(input_array[n-1] - input_array[i]))**2 for i in range(n-1)])**(0.5)

#------------------------------Temporal Features------------------------------#
    
#-----------------------------------------------------------------------------#
#----------------Finance------------------------------------------------------#
#-----------------------------------------------------------------------------#
    
def resistance(input_array, interval):
    # time: O(n), space: O(n)
    output_array = [x for x in input_array]
    l = len(input_array)
    if(l > interval+2):
        li = [0 for x in range(interval)]
        for t in range(interval+2, l):
            del li[0]
            currMax = max(li)
            #identify inflextion point (or local maxima)
            if(input_array[t-1] > input_array[t-2] and input_array[t] < input_array[t-1]):
                currRes = input_array[t-1]
                li.append(currRes)
                if(currRes > currMax):    
                    output_array[t] = currRes
                else:
                    output_array[t] = currMax
            else:
                li.append(li[-1])
                output_array[t] = currMax
    return output_array
            
def support(input_array, interval):
    # time: O(n), space: O(n)
    output_array = [x for x in input_array]
    l = len(input_array)
    if(l > interval+2):
        li = [0 for x in range(interval)]
        for t in range(interval+2, l):
            del li[0]
            currMin = min(li)
            #identify inflextion point (or local minima)
            if(input_array[t-1] < input_array[t-2] and input_array[t] > input_array[t-1]):
                currRes = input_array[t-1]
                li.append(currRes)
                if(currRes < currMin):    
                    output_array[t] = currRes
                else:
                    output_array[t] = currMin
            else:
                li.append(li[-1])
                output_array[t] = currMin
    return output_array      

def resistance_trendline(input_array, interval, wf):
    # time: O(n*i), space: O(n*i)
    output_array = [i for i in input_array]
    l = len(input_array)
    for t in range(l):
        if(t-interval >= 0):
            temp_list = [i for i in input_array[t-interval:t]]
            temp_max = max(temp_list)
            r_0 = temp_list.index(temp_max)
            if(1-(r_0/interval) >= wf):
                slope_list = [(temp_max - temp_list[i])/(r_0 - i) for i in range(r_0+1, interval)]
                slope_max = max(slope_list)            
                b = temp_max - slope_max*r_0
                output_array[t] = slope_max*interval + b                 
            else:
                slope_list = [(temp_max - temp_list[i])/(r_0 - i) for i in range(0, r_0)]
                slope_max = min(slope_list)            
                b = temp_max - slope_max*r_0
                output_array[t] = slope_max*interval + b
    return list(output_array)

def support_trendline(input_array, interval, wf):
    # time: O(n*i), space: O(n*i)
    output_array = [i for i in input_array]
    l = len(input_array)
    for t in range(l):
        if(t-interval >= 0):
            temp_list = [i for i in input_array[t-interval:t]]
            temp_min = min(temp_list)
            r_0 = temp_list.index(temp_min)
            if(1-(r_0/interval) >= wf):
                slope_list = [(temp_min - temp_list[i])/(r_0 - i) for i in range(r_0+1, interval)]
                slope_max = min(slope_list)            
                b = temp_min - slope_max*r_0                
                output_array[t] = slope_max*interval + b
            else:
                slope_list = [(temp_min - temp_list[i])/(r_0 - i) for i in range(0, r_0)]
                slope_max = max(slope_list)            
                b = temp_min - slope_max*r_0                
                output_array[t] = slope_max*interval + b
    return list(output_array)

#-----------------------------------------------------------------------------#
#------------Data Science-----------------------------------------------------#
#-----------------------------------------------------------------------------#
    
def moving_average(input_array, interval):
    # time: O(n), space: O(n)
    output_array = [x for x in input_array]
    output_array[interval-1] = average([input_array[interval-x-1] for x in range(interval)])
    for t in range(interval, len(input_array)):
        output_array[t] = output_array[t-1] + ((input_array[t] - input_array[t-interval]) / interval)
    return output_array

def moving_variance(input_array, interval):
    # time: O(n*i), space: O(n*i)
    output_array = [0 for x in input_array]
    l = len(input_array)
    for t in range(l):
        if(t-interval >= 0):
            output_array[t] = variance(input_array[t-interval:t+1])
    return list(output_array)

def moving_deviation(input_array, interval):
    # time: O(n*i), space: O(n*i)
    output_array = [0 for x in input_array]
    l = len(input_array)
    for t in range(l):
        if(t-interval >= 0):
            output_array[t] = standard_deviation(input_array[t-interval:t+1])
    return list(output_array)

def moving_tdssd(input_array, interval):
    # time: O(n*i), space: O(n*i)
    l = len(input_array)
    output_array = [0 for x in input_array]
    for t in range(l):
        if(t-interval >= 0):
            output_array[t] = time_dependent_sample_standard_deviation(input_array[t-interval:t+1])
    return output_array


def moving_max(input_array, interval):
    # time: O(n*i), space: O(n*i)
    output_array = [x for x in input_array]
    l = len(input_array)
    curr_max = input_array[0]
    max_index = 0
    for t in range(l): 
        if(input_array[t] >= curr_max):
            curr_max = input_array[t]
            max_index = t
        elif((t-max_index) > interval):
            loop_list = [x for x in input_array[t-interval+1:t+1]]
            curr_max = max(loop_list)
            max_index = loop_list.index(curr_max)
        output_array[t] = curr_max
    return output_array

def moving_min(input_array, interval):
    # time: O(n*i), space: O(n*i)
    output_array = [x for x in input_array]
    curr_min = output_array[0]
    min_index = 0
    for t in range(len(input_array)):
        if(input_array[t] <= curr_min):
            curr_min = input_array[t]
            min_index = t
        elif((t-min_index) > interval):
            loop_list = [x for x in input_array[t-interval+1:t+1]]
            curr_min = max(loop_list)
            min_index = loop_list.index(curr_min)
        output_array[t] = curr_min
    return output_array

def linear_regression_forecast(input_array, window=-1, interval=1): 
    # time: O(n*i), space: O(n*i)   
    output_array = [x for x in input_array]
    y_bar = (interval/2)
    l = len(input_array)
    if(window == -1):
        window = l-1 
    for t in range(l):
        if(t-window >= 0):
            x = input_array[t-window:t+1]
            cov = covariance(x)
            var = variance(x)
            a_hat = cov/var
            b_hat = average(x) - a_hat*y_bar
            output_array[t] = (a_hat)*(interval)+(b_hat)
    return output_array

def theta_forecast(input_array, window=-1, interval=1):
    print("not implemented")

def momentum(input_array, interval):
    output_array = [0 for x in input_array]
    mov_avg = moving_average(input_array, interval)
    for t in range(1, len(input_array)):
        output_array[t] = (mov_avg[t] - mov_avg[t-1])
    return output_array
    

#--------------------------------Derivative-----------------------------------#

def dx_max(input_array, interval):
    output_array = [1 for i in input_array]
    l = len(input_array)
    for t in range(l):
        if(t-interval >= 0):    
            temp_list = [input_array[i+1] - input_array[i] for i in range(t-interval, t)]
            output_array[t] = max(temp_list)
    return output_array
            
def dx_min(input_array, interval):
    output_array = [1 for i in input_array]
    l = len(input_array)
    for t in range(l):
        if(t-interval >= 0):    
            temp_list = [input_array[i+1] - input_array[i] for i in range(t-interval, t)]
            output_array[t] = min(temp_list)
    return output_array   

def difference(input_array, order=1, interval=1):
    if(order > 1):
        temp_array = difference(input_array, order-1, interval)
        output_array = [0 for x in input_array]
        l = len(input_array)
        for t in range(l):
            if(t-interval >= 0):
                output_array[t] = temp_array[t] - temp_array[t-interval]
    else:
        output_array = [0 for x in input_array]
        l = len(input_array)
        for t in range(l):
            if(t-interval >= 0):
                output_array[t] = input_array[t] - input_array[t-interval]
    return list(output_array)

def average_difference(input_array, order=1, interval=1):
    if(order > 1):
        temp_array = average_difference(input_array, order-1, interval)
        output_array = [0 for x in input_array]
        l = len(input_array)
        for t in range(l):
            if(t-interval >= 0):
                output_array[t] = average([temp_array[i] - temp_array[i-1] for i in range(t-interval+1, t+1)])
    else:
        output_array = [0 for x in input_array]
        l = len(input_array)
        for t in range(l):
            if(t-interval >= 0):
                output_array[t] = average([input_array[i] - input_array[i-1] for i in range(t-interval+1, t+1)])
    return list(output_array)

def average_difference_percent(input_array, order=1, interval=1):
    if(order > 1):
        temp_array = average_difference(input_array, order-1, interval)
        output_array = [1 for x in input_array]
        l = len(input_array)
        for t in range(l):
            if(t-interval >= 0):
                print(t)
                output_array[t] = average([temp_array[i]/temp_array[i-1] for i in range(t-interval+1, t+1)])
    else:
        output_array = [1 for x in input_array]
        l = len(input_array)
        for t in range(l):
            if(t-interval >= 0):
                output_array[t] = average([input_array[i]/input_array[i-1] for i in range(t-interval+1, t+1)])
    return list(output_array)

def derivative_ratio_max(input_array, interval):
    output_array = [1 for i in input_array]
    l = len(input_array)
    for t in range(l):
        if(t-interval >= 0):    
            temp_list = [input_array[i+1] / input_array[i] for i in range(t-interval, t)]
            output_array[t] = max(temp_list)
    return output_array
            
def derivative_ratio_min(input_array, interval):
    output_array = [1 for i in input_array]
    l = len(input_array)
    for t in range(l):
        if(t-interval >= 0):    
            temp_list = [input_array[i+1] / input_array[i] for i in range(t-interval, t)]
            output_array[t] = min(temp_list)
    return output_array   

def difference_ratio(input_array, order=1, interval=1):
    if(order > 1):
        temp_array = difference_ratio(input_array, order-1, interval)
        output_array = [1 for x in input_array]
        l = len(input_array)
        for t in range(l):
            if(t-interval >= 0):
                output_array[t] = temp_array[t]/temp_array[t-interval]
    else:
        output_array = [1 for x in input_array]
        l = len(input_array)
        for t in range(l):
            if(t-interval >= 0):
                output_array[t] = input_array[t]/input_array[t-interval]
    return list(output_array)

def movement_ratio(input_array, output_type="PERCENT"):
    output_array = [0 for i in input_array]
    l = len(input_array)
    for t in range(1, l):
#        if(output_type==" ")
        output_array[t] = (input_array[t]-input_array[t-1])/input_array[t-1]
        if(output_type=="PERCENT"): output_array[t] = output_array[t]*100
    return output_array

#-----------------------------------------------------------------------------#
def normalize(input_array, range_interval=(0, 1)):
    max_int = max(input_array)
    min_int = min(input_array)
    output_array = [((range_interval[1]-range_interval[0])*(x-min_int)/(max_int-min_int))+range_interval[0] for x in input_array]
    return output_array


def max_profit(input_array, k):
    l = len(input_array)
    PR = [[0 for j in range(l)] for i in range(k)]
    for i in range(1, k):
        for j in range(1, l):
            prev_transac_max = max([-input_array[x] + PR[i-1][x] for x in range(j)])
            PR[i][j] = max([PR[i][j-1], input_array[j] + prev_transac_max])
    return PR[k-1][l-1]


#------------------------------ Tests --------------------------------------------#
