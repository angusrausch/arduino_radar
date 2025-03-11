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
    width = 1500
    height = 900
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
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)

        self.input_rect = pygame.Rect(10, 10, 140, 32)
        self.button_rect = pygame.Rect(160, 10, 80, 32)
        self.input_text = ""
        self.input_active = False

        self.background = pygame.Surface((self.width, self.height))
        self.draw_background(self.background)

        self.previous_end = None  
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise KeyboardInterrupt()
                    self.handle_input(event)

                if args.simulated:
                    heading, seen_object = simulation.simulate(self.max_range)
                else:
                    heading, seen_object = self.parser.read_serial()
                if args.debug:
                    print(f"Heading: {heading}, Distance: {seen_object}")
                self.canvas.blit(self.background, (0, 0)) 
                self.canvas.fill((0, 0, 0))
                self.remove_outdated_objects(heading)

                if seen_object and seen_object < self.max_range:
                    self.objects.update({heading: seen_object}) 

                for key, value in self.objects.items():
                    self.draw_object(value, key)
                self.draw_background(self.canvas)
                self.draw_radar_line(heading)
                self.draw_ui()
                pygame.display.update()
        except KeyboardInterrupt:
            print("\nRadar closing")

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.input_active = True
                if not self.input_text: 
                    self.input_text = str(self.max_range)
            else:
                self.input_active = False

            if self.button_rect.collidepoint(event.pos):
                self.set_max_range()

        elif event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN: 
                self.set_max_range()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isdigit():
                self.input_text += event.unicode

    def draw_ui(self):
        pygame.draw.rect(self.canvas, pygame.Color('white') if self.input_active else pygame.Color('gray'), self.input_rect, 2)
        
        txt_surface = self.font.render(self.input_text if self.input_active else str(self.max_range), True, pygame.Color('white'))
        self.canvas.blit(txt_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        pygame.draw.rect(self.canvas, pygame.Color('blue'), self.button_rect)
        btn_surface = self.font.render("Set", True, pygame.Color('white'))
        self.canvas.blit(btn_surface, (self.button_rect.x + 10, self.button_rect.y + 5))

    def set_max_range(self):
        if self.input_text.isdigit():
            self.max_range = int(self.input_text)
            self.input_text = ""
        else:
            self.input_text = ""

    def draw_background(self, surface):
        center = (self.width / 2, self.height - 5)
        radius = self.width / 2 * 0.95
        thickness = max(1, self.width // 400)
        color = (13, 82, 2)

        font = pygame.font.Font(None, int(self.width / 40))

        for heading in range(-90, 91, 30):
            line_end = self.find_line_end(heading, center, radius + 20)
            
            pygame.draw.line(surface, color, center, line_end, max(1, thickness))

            text_surface = font.render(str(heading), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.find_line_end(heading, center, radius + 30))
            surface.blit(text_surface, text_rect)

        font = pygame.font.Font(None, int(self.width / 60))
        for temp_radius, r in zip(
            range(0, int(radius) + 1, int(radius / 4)), 
            range(0, int(self.max_range) + 1, int(self.max_range / 4))
        ):
            pygame.draw.circle(surface, color, center, int(temp_radius), int(thickness))
            text_surface = font.render(str(r), True, (255, 255, 255)) if r < self.max_range*(3/4)+1 else font.render(str(self.max_range), True, (255, 255, 255))
            text_location = (self.width / 2, self.height - temp_radius)
            text_rect = text_surface.get_rect(center=(text_location))
            surface.blit(text_surface, text_rect)

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
        if distance > self.max_range: return
        radius = self.width / 2 * 0.95
        object_close_distance = (distance / self.max_range) * radius
        center = (self.width / 2, self.height - 5)
        color = (180, 20, 20)
        object_close = ((self.find_line_end(heading-0.5, center, object_close_distance), self.find_line_end(heading+0.5, center, object_close_distance)))
        object_far = ((self.find_line_end(heading-0.5, center, radius), self.find_line_end(heading+0.5, center, radius)))
        pygame.draw.polygon(self.canvas, color, [object_close[0], object_close[1], object_far[1], object_far[0]])

    def remove_outdated_objects(self, heading):
        try:
            self.objects.pop(heading)
        except KeyError:
            pass

if __name__ == "__main__":
    parser = ArgumentParser(description="Radar UI for Arduino Radar")
    parser.add_argument("-d", "--debug", action="store_true", help="Set debug for output")
    parser.add_argument("-S", "--simulated", type=int, help="Simulates inputs")
    parser.add_argument("-r", "--revere", action="store_true", help="Reverser servo heading")
    parser.add_argument("-B", "--baudrate", type=int, default=9600, help="Use custom baudrate")
    parser.add_argument("-C", "--comport", type=str, default="/dev/tty.usbmodem101", help="Use custom comport")
    args = parser.parse_args()
    app(args)
