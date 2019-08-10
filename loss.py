def loss(beta, sigma, X, y, distribution='norm', loc=0, scale=1, 
        a=None, c=None, s=None):
    '''
    Input: beta --pd.Series. with length p + 1, including the intercept beta_0;
        sigma --scaler. > 0;
        X --pd.DataFrame. with shape n times p + 1, the elements of its first
            column are all 1;
        y --pd.Series. with length n
    Output: loss --scaler. the negative log likelihood.
    '''
    n = X.shape[0]
    gammas = threshold(y, distribution, a=a, c=c, s=s)
    K = len(gammas)
    fitvalues = np.dot(X, beta) #return an array with shape (n, )
    tmp = np.tile(gammas, n) #repeat gammas n times
    tmp = tmp.reshape(n, K) #transform tmp1 to a matrix with shape (n, K)
    #subtract each column of tmp by fitvalues. 
    #Remark: in numpy, substract each column of a matrix by a vector only works if
    #the trailing axes have the same dimension. The shape of tmp is (n, K), and
    #the shape of fitvalues is (n, ). So we need transport tmp. You can also think
    #numpy can do "matrix - vector' by row
    #the sahpe of upper is (n, K), which is the elment in the parentheses of F_0
    upper = ((tmp.T - fitvalues).T) / sigma
    
    x=np.array([-1.0 * np.inf])
    x2 = gammas[:-1]
    lower_gammas = np.concatenate([x, x2])
    tmp = np.tile(lower_gammas, n)
    tmp = tmp.reshape(n, K)
    lower = ((tmp.T - fitvalues).T) / sigma

    if distribution == 'norm':
        upper = st.norm.cdf(upper)
        lower = st.norm.cdf(lower)
    elif distribution == 'weibull':
        upper = st.exponweib.cdf(upper, a=a, c=c, loc=loc, scale=scale)
        lower = st.exponweib.cdf(lower, a=a, c=c, loc=loc, scale=scale)
    elif distribution == 'log':
        upper = st.lognorm.cdf(upper, s=s, loc=loc, scale=scale)
        lower = st.lognorm.cdf(lower, s=s, loc=loc, scale=scale)
    else:
        raise Exception('unvalid input for parameter distribution.')
    prob_y = upper - lower #probability of y equals to k
    log_prob_y = np.log(prob_y) #matrix with shape (n, K)
    deltah = np.array(delta(y))
    loss = deltah * log_prob_y
    loss = loss.sum()
    loss = -1.0 * loss
    return loss

if __name__ == '__main__': #test the function 
    import pandas as pd 
    import numpy as np 
    import scipy.stats as st
    from threshold import threshold
    from delta import delta
    y = pd.Series([2, 1, 4, 2, 3, 1, 2, 2, 3, 4, 2, 1])
    n = len(y)
    X = np.random.rand(n, 5)
    X = pd.DataFrame(X)
    beta = np.random.rand(5)
    beta = pd.Series(beta)
    sigma = 2
    lossh = loss(beta, sigma, X, y, distribution='norm') 
    print(X)
    print(lossh)
    len(y)   



