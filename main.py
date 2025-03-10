from argparse import ArgumentParser
import pygame
import math

# Local
import simulateRadar

class app:
    width = 500
    height = 300
    objects = {}
    max_range = 400

    def __init__(self, args):
        if args.simulated:
            simulation = simulateRadar.simulate(args.simulated)

        pygame.init()
        self.canvas = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        pygame.display.set_caption("Radar")

        self.background = pygame.Surface((self.width, self.height))  # Static background surface
        self.draw_background(self.background)

        self.previous_end = None  
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True

            if args.simulated:
                heading, seen_object = simulation.simulate()
            else:
                heading = 180

            self.canvas.blit(self.background, (0, 0)) 
            self.draw_radar_line(heading)
            self.remove_outdated_objects(heading)

            if seen_object:
                self.objects.update({heading: seen_object}) 

            for key, value in self.objects.items():
                self.draw_object(value, key)

            pygame.display.update()

    def draw_background(self, surface):
        surface.fill((0, 0, 0)) 
        center = (self.width / 2, self.height)
        radius = self.width / 2 * 0.95
        thickness = self.width / 200
        color = (13, 82, 2)

        pygame.draw.line(surface, color, center, (self.width/2, self.height - radius))
        for i in range(4):
            pygame.draw.circle(surface, color, center, radius, int(thickness))
            
            radius -= self.width / 2 * 0.95 / 4

    def draw_radar_line(self, heading):
        center = (self.width / 2, self.height)
        radius = self.width / 2 * 0.95
        thickness = self.width / 150
        end_point = self.find_line_end(heading, center, radius)

        if self.previous_end:
            pygame.draw.line(self.canvas, (0, 0, 0), center, self.previous_end, int(thickness)) 

        pygame.draw.line(self.canvas, (60, 255, 20), center, end_point, int(thickness)) 
        self.previous_end = end_point 

    def find_line_end(self, heading, center, radius):
        end_x = center[0] + radius * math.sin(math.radians(heading))
        end_y = center[1] - radius * math.cos(math.radians(heading))
        return (end_x, end_y)

    def draw_object(self, distance, heading):
        radius = self.width / 2 * 0.95
        corrected_distance = distance * (radius / self.max_range)
        center = (self.width / 2, self.height)
        item_position = self.find_line_end(heading, center, corrected_distance)
        pygame.draw.circle(self.canvas, (60, 255, 20), item_position, 7)

    def remove_outdated_objects(self, heading):
        try:
            self.objects.pop(heading)
        except KeyError:
            pass # Expected Behaviour 

if __name__ == "__main__":
    parser = ArgumentParser(description="SSH Config helper & send proxy keys")
    parser.add_argument("-d", "--debug", action="store_true", help="Set debug for output")
    parser.add_argument("-S", "--simulated", type=int, default=100, help="Simulates inputs")
    args = parser.parse_args()
    app(args)
