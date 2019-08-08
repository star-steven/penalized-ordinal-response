impot scipy.stats as st
from thrshold import threshold
from delta import delta
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
    gammas = threshold(y, distribution)
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
    
    tmp = np.tile([0] + gammas[:-1], n)
    tmp = tmp.reshape(n, K)
    lower = ((tmp.T - fitvalues).T) / sigma

    if distribution == 'norm':
        upper = st.norm.cdf(upper)
        lower = st.norm.cdf(lower)
    else if distribution == 'weibull':
        upper = st.exponweib.cdf(upper, a=a, c=c, loc=loc, scale=scale)
        lower = st.exponweib(lower, a=a, c=c, loc=loc, scale=scale)
    else if distribution == 'log':
        upper = st.lognorm.cdf(upper, s=s, loc=loc, scale=scale)
        lower = st.lognorm.cdf(lower, s=s, loc=loc, scale=scale)
    else:
        raise Exception('unvalid input for parameter distribution.')
    prob_y = upper - lower #probability of y equals to k
    log_prob_y = np.log(prob_y) #matrix with shape (n, K)
    delta = delta(y)
    loss = delta * log_prob_y
    loss = loss.sum()
    loss = -1.0 * loss
    return loss



