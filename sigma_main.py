def sigma_main(X,y,beta,distribution='norm',loc=0,scale=1,a=None,c=None,s=None,W=0.5,c1=0.8,c2=0.9,n_iterations=10000,target_error =1,n_particles=20)
   
    count=0
    n_iterations = n_iterations
    target_error = target_error
    n_particles = n_particles
    distribution = distribution
    loc=loc
    scale=scale
    a=a
    c=c
    s=s
    W=W
    c1=c1
    search_space = Space(1, target_error, n_particles)
    particles_vector = [Particle() for _ in range(search_space.n_particles)]
    search_space.particles = particles_vector
    search_space.print_particles()

    iteration = 0
    while(iteration < n_iterations):
        search_space.set_pbest()    
        search_space.set_gbest()

        if(abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
            break

        search_space.move_particles()
        iteration += 1
    #the final transfer     
    sigma_final=binarysearch(beta=beta, X=X, y=y, sigma_upper=search_space.gbest_position[0], sigma_lower= search_space.gbest_position[1], distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s)
    
    return sigma_final

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
    sigma=sigma_main(X=X,y=y,beta=beta,distribution='norm',loc=0,scale=1,a=None,c=None,s=None,W=0.5,c1=0.8,c2=0.9,n_iterations=10000,target_error =1,n_particles=20)
    print(sigma)

