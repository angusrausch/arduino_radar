from time import sleep
from random import randint

class simulate:
    def __init__(self, rate):
        self.heading = 90
        self.direction = 1
        self.rate = rate
    
    def simulate(self):
        sleep(0.01)
        if self.heading <= -90: self.direction = 0.2
        elif self.heading >= 90: self.direction = -0.2
        self.heading += self.direction

        seen_object = self.generate_objects()
        return self.heading, seen_object
    
    def generate_objects(self):
        if randint(0, self.rate * 10) == 1:
            return randint(50, 400)
        return None
