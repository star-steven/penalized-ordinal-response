import pandas as pd
def delta(y):
    '''
    Input: y --pd.Series with length n. Takes value from 1,..., K.
    Output: delta --pd.DataFrame with shape n times K. 
    the (i, j) elements of delta is 1 if y_i == j otherwise 0.
    '''
    if isinstance(y, pd.Series):
        categories = y.unique() #unique returns an array, in order of apperance
        categories.sort() #sort inplace
    else:
        raise Exception('Type error for y!')
    delta = pd.DataFrame(0, index=range(1, len(y) + 1), 
            columns=range(1, 1 + categories.shape[0]))
    for i in range(len(y)):
        delta[y[i]][i+1] = 1
    return delta
        

if __name__ == '__main__': 
    import pandas as pd 
    import numpy as np 
    y = pd.Series([2, 1, 4, 2, 3, 1, 2, 2, 3, 4, 2, 1])
    delta = delta(y) 
    print(delta)
