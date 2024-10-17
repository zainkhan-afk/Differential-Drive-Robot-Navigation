import pygame

class Car:
    def __init__(self, x, y, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation

class Renderer:
    def __init__(self, width = 1000, height = 700, title = "Delaunay Triangulation"):
        self.width  = width
        self.height = height
        self.title = title
        
        self.background_color = (0, 0, 0)
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def draw_car(self, car):
        car_width, car_height = 50, 30
        car_color = (255, 0, 0)  # Red color

        # Create a surface for the car
        car_surface = pygame.Surface((car_width, car_height), pygame.SRCALPHA)
        car_surface.fill(car_color)

        # Rotate the car surface based on the car's rotation
        rotated_surface = pygame.transform.rotate(car_surface, -car.rotation)

        # Get the new rectangle after rotation and set its center to the car's (x, y) position
        car_rect = rotated_surface.get_rect(center=(car.x, car.y))

        # Blit the rotated surface onto the screen at the correct position
        self.screen.blit(rotated_surface, car_rect.topleft)


    def draw_path(self):
        pass

    def render(self, car):
        self.draw_path()
        self.draw_car(car)

    def clear(self):
        self.screen.fill(self.background_color)



if __name__ == "__main__":
    c = Car(100, 100, 0)
    renderer = Renderer()

    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        renderer.clear()
        renderer.render(c)

        c.x += 5


        if c.x > renderer.width:
            c.x = 0
            c.rotation += 5

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
        