def sigma_main(X,y,beta,distribution='norm',loc=0,scale=1, W=0.5, c1=0.8, c2=0.9, niterations=10000, targeterror=1, nbirds=20, a=None, c=None, s=None):
    
    count=0
    n_iterations = niterations
    target_error = targeterror
    n_birds = nbirds
    distribution = distribution
    loc=loc
    scale=scale
    a=a
    c=c
    s=s
    W=W
    c1=c1
    c2=c2
    fly = Fly(0, target_error, n_birds)
    birds_vector = [Bird() for _ in range(fly.n_birds)]
    fly.birds = birds_vector
    fly.print_birds()

    iteration = 0
    while(iteration < n_iterations):
        fly.set_pbest()    
        fly.set_gbest()

        if(abs(fly.gbest_value - fly.target) <= fly.target_error):
            break

        fly.move_birds()
        iteration += 1
    #the final transfer     
    sigma_final=binarysearch(beta=beta, X=X, y=y, sigma_upper=fly.gbest_position[0], sigma_lower= fly.gbest_position[1], distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s)
    
    return sigma_final

if __name__ == '__main__': #test the function 
    import pandas as pd 
    import numpy as np 
    import random
    count = 0
    y = pd.Series([2, 1, 4, 2, 3, 1, 2, 2, 3, 4, 2, 1])
    n = len(y)
    X = np.random.rand(n,5)
    X = pd.DataFrame(X)
    beta = np.random.rand(5)
    beta = pd.Series(beta)
    sigma=sigma_main(X=X, y=y, beta=beta, distribution='norm', loc=0, scale=1, W=0.5, c1=0.8, c2=0.9, niterations=100, targeterror =1, nbirds=20, a=None, c=None, s=None)
    print(sigma)


