import random
import tkinter
import math 
random.seed()

def plot(xvals, yvals):
    # This is a function for creating a simple scatter plot.  You will use it,
    # but you can ignore the internal workings.
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=400, bg='white') #was 350 x 280
    c.grid()
    #create x-axis
    c.create_line(50,350,650,350, width=3)
    for i in range(5):
        x = 50 + (i * 150)
        c.create_text(x,355,anchor='n', text='%s'% (.5*(i+2) ) )
    #y-axis
    c.create_line(50,350,50,50, width=3)
    for i in range(5):
        y = 350 - (i * 75)
        c.create_text(45,y, anchor='e', text='%s'% (.25*i))
    #plot the points
    for i in range(len(xvals)):
        x, y = xvals[i], yvals[i]
        xpixel = int(50 + 300*(x-1))
        ypixel = int(350 - 300*y)
        c.create_oval(xpixel-3,ypixel-3,xpixel+3,ypixel+3, width=1, fill='red')
    root.mainloop()

#Constants: setting these values controls the parameters of your experiment.
injurycost = 10 #Cost of losing a fight  
displaycost = 5 #Cost of displaying   
foodbenefit = 8 #Value of the food being fought over   
init_hawk = 0
init_dove = 0
init_defensive = 0
init_evolving = 150

class World:
    def __init__(self):
        self.current_exisisting_birds = []
    def update(self): #time pass for everything in the world
        for item in self.current_exisisting_birds:
            item.update() 
    def free_food(self, n):
        i = 1
        while i <= n:
            bird_lucky = random.choice(self.current_exisisting_birds)
            bird_lucky.eat() 
            i += 1 ### i forgot! 
    def conflict(self,n): #x copy list-- random.sample
        i = 1
        while i <= n:
            bird_ls = random.sample(self.current_exisisting_birds, 2) 
            bird_1, bird_2 = bird_ls[0], bird_ls[1]
            bird_2.encounter(bird_1) 
            i += 1
    def status(self):
        dove, hawk, defensive = 0, 0, 0
        for item in self.current_exisisting_birds:
            if item.species == "Dove":
                dove += 1
            elif item.species == "Hawk":
                hawk += 1
            elif item.species == "Defensive":
                defensive += 1
        dove = str(dove)
        hawk = str(hawk)
        defensive = str(defensive)
        print("dove: " + dove + " hawk: " + hawk + " defensive: " + defensive)
    def evolvingPlot(self):
        xvals, yvals= [], []
        for item in self.current_exisisting_birds: #evolving birds == exisiting birds?
            xvals.append(item.w)
            yvals.append(item.aggression)
        return plot(xvals, yvals) 

class Bird:
    def __init__(self, world):
        world.current_exisisting_birds.append(self)
        self.world_in = world
        self.current_health = 100
    def eat(self):
        self.current_health += foodbenefit
    def injured(self):
        self.current_health -= injurycost
    def display(self):
        self.current_health -= displaycost
    def die(self):
        (self.world_in).current_exisisting_birds.remove(self) 
    def update(self): #time pass 1
        self.current_health -= 1
        if self.current_health <= 0:
            self.die() 

class Dove(Bird):
    species = "Dove"
    def update(self): 
        Bird.update(self)
        if self.current_health >= 200:
            self.current_health -= 100 
            new_dove = Dove(self.world_in)
    def defend_choice(self):
        return False  
    def encounter(self, bird_found_food):
        if bird_found_food.defend_choice() == True:
            bird_found_food.eat()
        else:
            self.display()
            bird_found_food.display()
            random.choice([self,bird_found_food]).eat()

class Hawk(Bird):
    species = "Hawk"
    def update(self): #is it right?
        Bird.update(self)
        if self.current_health >= 200:
            self.current_health -= 100 
            new_hawk = Hawk(self.world_in)
    def defend_choice(self):
        return True 
    def encounter(self, bird_found_food):
        if bird_found_food.defend_choice() == False:
            self.eat()
        else:
            two_birds = [self,bird_found_food]
            winner = random.choice(two_birds)
            winner.eat()
            two_birds.remove(winner)
            two_birds[0].injured()

class Defensive(Bird):
    species = "Defensive"
    def update(self): #is it right?
        Bird.update(self)
        if self.current_health >= 200:
            self.current_health -= 100 
            new_defensive = Defensive(self.world_in)
    def defend_choice(self):
        return True 
    def encounter(self, bird_found_food):
        Dove.encounter(self, bird_found_food) #world? __init__?

class Evolving(Bird): 
    species = "Evolving"
    def __init__(self, world, aggression = None, w = None): 
        world.current_exisisting_birds.append(self)
        if aggression == None:
            self.aggression = random.uniform(0,1)
            self.w = random.uniform(1, 3)
        else:
            self.w = w + random.uniform(-0.1, 0.1) # add when new bird 
            if self.w > 3:
                self.w = 3
            elif self.w < 1:
                self.w = 1
            self.aggression = aggression + random.uniform(-0.05,0.05)
            if self.aggression > 1:
                self.aggression = 1
            elif self.aggression < 0:
                self.aggression = 0
        self.world_in = world
        self.current_health = 100
    def update(self):
        self.current_health -= (0.4 + 0.6 * self.w)
        if self.current_health <= 0:
            self.die() 
        if self.current_health >= 200:
            self.current_health -= 100 
            new = Evolving(self.world_in, self.aggression, self.w) #beginning, should be default value
    def defend_choice(self):
        self.probability = self.aggression * 100
        number = random.choice(range(1, 101))
        if number <= self.probability:
            return True 
        else:
            return False 
    def encounter(self, bird_found_food):
        w1 = self.w 
        w2 = bird_found_food.w 
        if bird_found_food.defend_choice() == True: #other fights
            if self.defend_choice() == True: #fight
                probability_self_win = math.ceil(w1 / (w1 + w2) * 100) 
                number = random.choice(range(1, 101))
                if number <= probability_self_win: #self win
                    self.eat()
                    bird_found_food.injured() 
                else: #other wins
                    bird_found_food.eat()
                    self.injured()
            else: # x fight
                bird_found_food.eat() 
        else: #other x fight
            if self.defend_choice() == True:
                self.eat()
            else:
                self.display()
                bird_found_food.display()
                random.choice([self,bird_found_food]).eat() 









            
########
# The code below actually runs the simulation.  You shouldn't have to do anything to it.
########

w = World()

for i in range(init_dove):
    Dove(w)
for i in range(init_hawk):
    Hawk(w)

for i in range(init_defensive):
    Defensive(w)

for i in range(init_evolving):
    Evolving(w)

for t in range(10000):
    w.free_food(10) 
    w.conflict(50)
    w.update()
w.status()

w.evolvingPlot()  #This line adds a plot of evolving birds. Uncomment it when needed.



