def binarysearch(beta, X, y, sigma_upper, sigma_lower, distribution='norm', loc=0, scale=1, a=None, c=None, s=None):
    global count
    count=count+1
    sigma_a = sigma_upper
    sigma_b = sigma_lower
    c = (sigma_a+sigma_b)/2
    f_a = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=sigma_a) 
    f_b = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=sigma_b) 
    f_c = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=c) 
    if f_c == 0:
        print(c)
        return c
    elif count>10000:
        raise Exception('unvalid input for parameter sigma_upper and sigma_lower.')        
    else: 
        if f_a*f_c <0:
            binarysearch(beta=beta, X=X, y=y, sigma_upper=a, sigma_lower=c, distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s)
        if f_b*f_c <0:
            binarysearch(beta=beta, X=X, y=y, sigma_upper=c, sigma_lower=b, distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s)
if __name__ == '__main__': #test the function 
    import pandas as pd 
    import numpy as np 
    count = 0
    y = pd.Series([2, 1, 4, 2, 3, 1, 2, 2, 3, 4, 2, 1])
    n = len(y)
    X = np.random.rand(n,5)
    X = pd.DataFrame(X)
    beta = np.random.rand(5)
    beta = pd.Series(beta)
    mid = binarysearch(beta=beta,X=X,y=y,distribution='norm', sigma_upper=100, sigma_lower=0.01) 
    print(X)
    print(mid)
