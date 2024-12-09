import pygame
import math


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and Throw with Weight")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


GRAVITY = 0.8
FRICTION = 0.99  
BOUNCE = 0.3 

class GameObject:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass  
        self.vel_x = 0  
        self.vel_y = 0  
        self.dragging = False  
        self.offset_x = 0  
        self.offset_y = 0  

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        if not self.dragging:
            self.vel_y += GRAVITY * self.mass  
        
        self.vel_x *= FRICTION  
        self.vel_y *= FRICTION
        
        self.x += self.vel_x  
        self.y += self.vel_y

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vel_x *= -BOUNCE
        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.vel_x *= -BOUNCE
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vel_y *= -BOUNCE
        if self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.vel_y *= -BOUNCE

    def handle_drag(self, mouse_x, mouse_y):
        if self.dragging:
            self.x = mouse_x - self.offset_x
            self.y = mouse_y - self.offset_y

    def start_drag(self, mouse_x, mouse_y):
        if (self.x - self.radius <= mouse_x <= self.x + self.radius and
            self.y - self.radius <= mouse_y <= self.y + self.radius):
            self.dragging = True
            self.offset_x = mouse_x - self.x
            self.offset_y = mouse_y - self.y

    def stop_drag(self):
        if self.dragging:
            self.dragging = False

    def apply_force(self, force_x, force_y):
        self.vel_x += force_x / self.mass
        self.vel_y += force_y / self.mass

    def collide(self, other):
        dist_x = self.x - other.x
        dist_y = self.y - other.y
        distance = math.sqrt(dist_x**2 + dist_y**2)

        if distance < self.radius + other.radius:
            normal_x = dist_x / distance
            normal_y = dist_y / distance

            relative_velocity_x = self.vel_x - other.vel_x
            relative_velocity_y = self.vel_y - other.vel_y

            dot_product = relative_velocity_x * normal_x + relative_velocity_y * normal_y

            if dot_product > 0: 
                return

            restitution = BOUNCE
            impulse = (2 * dot_product) / (self.mass + other.mass)

            self.vel_x -= impulse * other.mass * normal_x
            self.vel_y -= impulse * other.mass * normal_y

            other.vel_x += impulse * self.mass * normal_x
            other.vel_y += impulse * self.mass * normal_y

ball1 = GameObject(200, 300, 30, RED, 0.1)
ball2 = GameObject(600, 300, 30, BLUE, 2)

running = True
clock = pygame.time.Clock()

last_mouse_x, last_mouse_y = 0, 0

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            ball1.start_drag(event.pos[0], event.pos[1])
            ball2.start_drag(event.pos[0], event.pos[1])

        if event.type == pygame.MOUSEBUTTONUP:
            if ball1.dragging:
                ball1.stop_drag()
                mouse_x, mouse_y = event.pos
                force_x = (mouse_x - last_mouse_x) * 0.3
                force_y = (mouse_y - last_mouse_y) * 0.3
                ball1.apply_force(force_x, force_y)

            if ball2.dragging:
                ball2.stop_drag()
                mouse_x, mouse_y = event.pos
                force_x = (mouse_x - last_mouse_x) * 0.3
                force_y = (mouse_y - last_mouse_y) * 0.3
                ball2.apply_force(force_x, force_y)

        if event.type == pygame.MOUSEMOTION:
            if ball1.dragging:
                ball1.vel_x = 0
                ball1.vel_y = 0
                ball1.handle_drag(event.pos[0], event.pos[1])
            if ball2.dragging:
                ball2.vel_x = 0
                ball2.vel_y = 0
                ball2.handle_drag(event.pos[0], event.pos[1])

    ball1.update()
    ball2.update()

    ball1.collide(ball2)

    ball1.draw(screen)
    ball2.draw(screen)

    pygame.display.flip()

    last_mouse_x, last_mouse_y = pygame.mouse.get_pos()

    clock.tick(60)

pygame.quit()
