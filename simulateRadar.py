from time import sleep
from random import randint

class simulate:
    remaining = None
    def __init__(self, rate):
        self.heading = 90
        self.direction = 1
        self.rate = rate
    
    def simulate(self, max_range):
        sleep(0.01)
        if self.heading <= -90: self.direction = 1
        elif self.heading >= 90: self.direction = -1
        self.heading += self.direction

        seen_object = self.generate_objects(max_range)
        return self.heading, seen_object
    
    def generate_objects(self, max_range):
        if self.remaining:
            degrees_remaining = self.remaining[0] - 1
            distance = self.remaining[1]
            self.remaining = (degrees_remaining, distance) if degrees_remaining > 0 else None
            return distance
        try:
            if randint(1, self.rate) == 1:
                distance = randint(min(50, int(max_range/8)), max_range)
                width = randint(2, 30)
                self.remaining = (width, distance)
                return distance
        except ValueError:
            return None
        return None
