class Particle():
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


class Space():

    def __init__(self, target, target_error, n_particles):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random()*50, random.random()*50])

    def print_particles(self):
        for particle in self.particles:
            particle.__str__()
   
    def fitness(self, particle):
        f_a = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=particle.position[0]) 
        f_b = sigma_gradient(beta=beta,X=X,y=y,distribution=distribution, loc=loc, scale=scale, a=a, c=c, s=s, sigma=particle.position[1]) 
        if f_a*f_b ==0:
            return 0
        elif f_a*f_b>0:
            return float('inf')
        else:
            return abs(particle.position[0]-particle.position[1])

    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = self.fitness(particle)
            if(particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position
            

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = self.fitness(particle)
            if(self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position

    def move_particles(self):
        for particle in self.particles:
            global W
            new_velocity = (W*particle.velocity) + (c1*random.random()) * (particle.pbest_position - particle.position) + \
                            (random.random()*c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()
            
