def beta_gradient(beta, sigma, X, y, distribution, loc=0, scale=1, a=None, c=None, s=None):
    '''
    Input: beta --pd.Series. with length p + 1, including the intercept beta_0;
        sigma --scaler. > 0;
        X --pd.DataFrame. with shape n times p + 1, the elements of its first
            column are all 1;
        y --pd.Series. with length n
    Output: gradient --np.array with shape (p+1, ). the gradient of beta.
    '''
    n = X.shape[0]
    gammas = threshold(input=y, distribution=distribution,a=a,c=c,s=s)
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
    
    x=np.array([-1*np.inf])
    x2 = gammas[:-1]
    lower_gammas = np.concatenate([x,x2])
    tmp = np.tile(lower_gammas,n)
    tmp = tmp.reshape(n, K)
    lower = ((tmp.T - fitvalues).T) / sigma

    if distribution == 'norm':
        upper = st.norm.cdf(x=upper, loc=loc, scale=scale)
        upper_gradient_about_fitvalues = st.norm.pdf(x=upper, loc=loc, scale=scale)
        lower = st.norm.cdf(x=lower, loc=loc, scale=scale)
        lower_gradient_about_fitvalues = st.norm.pdf(x=lower, loc=loc, scale=scale)
    elif distribution == 'weibull':
        upper = st.exponweib.cdf(x=upper, a=a, c=c, loc=loc, scale=scale)
        upper_gradient_about_fitvalues = st.exponweib.pdf(x=upper, a=a, c=c, loc=loc, scale=scale)
        lower = st.exponweib.cdf(x=lower, a=a, c=c, loc=loc, scale=scale)
        lower_gradient_about_fitvalues = st.exponweib.pdf(x=lower, a=a, c=c, loc=loc, scale=scale)
    elif distribution == 'log':
        upper = st.lognorm.cdf(x=upper, s=s, loc=loc, scale=scale)
        upper_gradient_about_fitvalues = st.lognorm.pdf(x=upper, s=s, loc=loc, scale=scale)
        lower = st.lognorm.cdf(x=lower, s=s, loc=loc, scale=scale)
        lower_gradient_about_fitvalues= st.lognorm.pdf(x=lower,s=s, loc=loc, scale=scale)
    else:
        raise Exception('unvalid input for parameter distribution.')
    prob_y = upper - lower #probability of y equals to k
    prob_y_gradient_about_fitvalues = upper_gradient_about_fitvalues - lower_gradient_about_fitvalues
    product = prob_y_gradient_about_fitvalues / prob_y
    product = -1.0 * product / sigma
    deltah = np.array(delta(y))
    product = deltah * product
    fitvalues_gradient = X.values
    prob_yi = [x[x != 0][0] for x in np.array(product)]
    gradient = map(lambda x, y: x * y, prob_yi, fitvalues_gradient)
    gradient = np.array(list(gradient))
    gradient = np.sum(gradient, axis=0)
    gradient = -1.0 * gradient
    return gradient
if __name__ == '__main__': #test the function 
    import pandas as pd 
    import numpy as np 
    y = pd.Series([2, 1, 4, 2, 3, 1, 2, 2, 3, 4, 2, 1])
    n = len(y)
    X = np.random.rand(n,5)
    X = pd.DataFrame(X)
    beta = np.random.rand(5)
    beta = pd.Series(beta)
    sigma=2
    gradient = beta_gradient(beta=beta,sigma=sigma,X=X,y=y,distribution='log', s=1) 
    print(X)
    print(gradient)
    len(y)   

