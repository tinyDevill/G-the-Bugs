import pygame
from gameobject import Player, Platform, create_platforms
from screen import load_assets, Camera, draw_background, draw_objects

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("G The Bugs Draft")
        
        self.clock = pygame.time.Clock()
        self.FPS = 45
        self.zoom = 1.5

        # Load assets
        self.background, self.platform_img, self.wall_img = load_assets(self.WIDTH, self.HEIGHT)

        # Game objects
        self.player = Player(
            50, self.HEIGHT - 100, 50, 50,
            pygame.image.load("assets/player.png").convert_alpha()
        )

        self.platforms = create_platforms(self.WIDTH, self.HEIGHT, self.platform_img, self.wall_img)
        self.camera = Camera(int(self.WIDTH / self.zoom), int(self.HEIGHT / self.zoom), self.zoom)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        original_x = self.player.rect.x
        
        if keys[pygame.K_LEFT]:
            self.player.move(dx=-self.player.speed)
        if keys[pygame.K_RIGHT]:
            self.player.move(dx=self.player.speed)
        if keys[pygame.K_SPACE]:
            self.player.jump()

        self.check_horizontal_collisions(original_x)

    def check_horizontal_collisions(self, original_x):
        collided = False
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                if self.player.rect.x < original_x:
                    self.player.rect.left = platform.rect.right
                else:
                    self.player.rect.right = platform.rect.left
                collided = True
        return collided
    
    def check_vertical_collisions(self):
        self.player.on_ground = False
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity_y > 0:
                    self.player.rect.bottom = platform.rect.top
                    self.player.velocity_y = 0
                    self.player.on_ground = True
                elif self.player.velocity_y < 0:
                    self.player.rect.top = platform.rect.bottom
                    self.player.velocity_y = 0
                return True
        return False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()
            self.player.apply_gravity()
            self.check_vertical_collisions()
            self.camera.update(self.player, self.WIDTH, self.HEIGHT)

            # Rendering
            self.screen.fill((255, 255, 255))  # Clear screen
            
            draw_background(
                self.screen,
                self.background,
                self.camera.rect,
                self.WIDTH,
                self.HEIGHT
            )
            
            draw_objects(
                self.screen,
                self.player,
                self.platforms,
                self.camera.rect,
                self.zoom
            )
            
            # Update display
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
