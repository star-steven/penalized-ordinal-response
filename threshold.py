import scipy.stats as st 
import numpy as np
import pandas as pd
import random
def threshold(y, distribution, loc=0, scale=1, a=None, c=None, s=None):
    '''
    input: y --pd.Series/list/np.array with length n. Take value with the order from 1,..., K.
    Output: threshold --list with length k. 
    the (i-1)_th and the i_th elements of threshold are the threshold of K .
    '''
    y = np.array(y)
    n = y.shape[0]
    m = y.max()
    density = np.zeros(m)
    for k in range(1, m+1):
        index = np.where(y == k)
        index = np.array(index )
        total = index.shape[1]
        density[k-1] = total / n
        density_new = density.cumsum()#take the porb of sample to verify the thresholds
    if distribution == 'norm':    
        threshold = st.norm.ppf(loc=loc, scale=scale, q=density_new)
    elif distribution == 'weibull':
        threshold = st.exponweib.ppf(a=a, c=c, loc=loc, scale=scale, q=density_new)
    elif distribution == 'log':
        threshold = st.lognorm.ppf(loc=loc, scale=scale, s=s, q=density_new)
    else :
        raise Exception('Type error for y!')
    return threshold 
if __name__ == '__main__': #test the function 
    import pandas as pd 
    import numpy as np 
    y = pd.Series([2, 1, 4, 2, 3, 1, 2, 2, 3, 4, 2, 1])
    threshold = threshold(y,distribution='log',s=1) 
    print(threshold)
    len(y)
