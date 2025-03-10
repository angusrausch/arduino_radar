from argparse import ArgumentParser
import math
import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

# Local
import simulateRadar
import parseSerial

class app:
    width = 1000
    height = 600
    objects = {}
    max_range = 400

    def __init__(self, args):
        if args.simulated:
            simulation = simulateRadar.simulate(args.simulated)
        else:
            self.parser = parseSerial.parser(reverse=args.revere, comport=args.comport, baudrate=args.baudrate)
        
        pygame.init()

        self.canvas = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        pygame.display.set_caption("Radar")

        self.background = pygame.Surface((self.width, self.height))  # Static background surface
        self.draw_background(self.background)

        self.previous_end = None  
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise KeyboardInterrupt()

                if args.simulated:
                    heading, seen_object = simulation.simulate()
                else:
                    heading, seen_object = self.parser.read_serial()
                if args.debug:
                    print(f"Heading: {heading}, Distance: {seen_object}")
                self.canvas.blit(self.background, (0, 0)) 
                self.draw_radar_line(heading)
                self.remove_outdated_objects(heading)

                if seen_object:
                    self.objects.update({heading: seen_object}) 

                for key, value in self.objects.items():
                    self.draw_object(value, key)

                pygame.display.update()
        except KeyboardInterrupt:
            print("\nRadar closing")

    def draw_background(self, surface):
        surface.fill((0, 0, 0))  
        center = (self.width / 2, self.height - 5)
        radius = self.width / 2 * 0.95
        thickness = max(1, self.width // 200)
        color = (13, 82, 2)
        
        font = pygame.font.Font(None, int(self.width / 20))

        for heading in range(-90, 91, 30):
            line_end = self.find_line_end(heading, center, radius + 20)
            
            pygame.draw.line(surface, color, center, line_end, max(1, thickness // 2))

            text_surface = font.render(str(heading), True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(center=self.find_line_end(heading, center, radius + 30))
            surface.blit(text_surface, text_rect)

        for i in range(4):
            pygame.draw.circle(surface, color, center, int(radius), int(thickness))
            radius -= self.width / 2 * 0.95 / 4  # Reduce radius for next circle

    def draw_radar_line(self, heading):
        center = (self.width / 2, self.height - 5)
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
        center = (self.width / 2, self.height - 5)
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
    parser.add_argument("-S", "--simulated", type=int, help="Simulates inputs")
    parser.add_argument("-r", "--revere", action="store_true", help="Reverser servo heading")
    parser.add_argument("-B", "--baudrate", type=int, default=9600, help="Use custom baudrate")
    parser.add_argument("-C", "--comport", type=str, default="/dev/tty.usbmodem101", help="Use custom comport")
    args = parser.parse_args()
    app(args)
