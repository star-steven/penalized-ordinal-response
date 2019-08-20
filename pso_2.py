class Bird():
    def __init__(self):
        self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([0,0])

    def __str__(self):
        f_a = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=self.position[0]) 
        f_b = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=self.position[1]) 
        print("I am at ", self.position, " gradient value is ", [f_a,f_b])
    
    def move(self):
        self.position = self.position + self.velocity


class Fly():

    def __init__(self, target, target_error, n_birds):
        self.target = target
        self.target_error = target_error
        self.n_birds = n_birds
        self.birds = []
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random()*50, random.random()*50])

    def print_birds(self):
        for bird in self.birds:
            bird.__str__()
   
    def fitness(self, bird):
        f_a = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=bird.position[0]) 
        f_b = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=bird.position[1]) 
        if f_a*f_b ==0:
            return 0
        elif f_a*f_b>0:
            return float('inf')
        else:
            return abs(bird.position[0]-bird.position[1])

    def set_pbest(self):
        for bird in self.birds:
            fitness_cadidate = self.fitness(bird)
            if(bird.pbest_value > fitness_cadidate):
                bird.pbest_value = fitness_cadidate
                bird.pbest_position = bird.position
            

    def set_gbest(self):
        for bird in self.birds:
            best_fitness_cadidate = self.fitness(bird)
            if(self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = bird.position

    def move_birds(self):
        for bird in self.birds:
            global W
            new_velocity = (W*bird.velocity) + (c1*random.random()) * (bird.pbest_position - bird.position) + \
                            (random.random()*c2) * (self.gbest_position - bird.position)
            bird.velocity = new_velocity
            bird.move()
            
