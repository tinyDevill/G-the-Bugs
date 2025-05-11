import pygame
import sys
import math
from character import Player  # Mengimpor Player dari character.py
from enemy import Enemy
from gameobject import Platform, create_platforms
from screen import load_assets, Camera, draw_background, draw_objects, draw_darkness_with_light

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("G The Bugs Draft")

        self.clock = pygame.time.Clock()
        self.FPS = 45
        self.zoom = 1.5
        self.state = "menu"
        self.font = pygame.font.Font(None, 36)
        self.jump_requested = False  

        # Load assets
        self.background, self.platform_img, self.wall_img, self.start_button_img, self.exit_button_img = load_assets(self.WIDTH, self.HEIGHT)

        # Game objects
        self.player = Player(
            50, self.HEIGHT - 100, 50, 50,
            pygame.image.load("assets/image/player.png").convert_alpha()
        )

        self.enemy = Enemy(
            300, self.HEIGHT - 150, 50, 50, pygame.image.load("assets/image/enemy.png").convert_alpha()
        )

        self.platforms = create_platforms(self.WIDTH, self.HEIGHT, self.platform_img, self.wall_img)
        self.camera = Camera(int(self.WIDTH / self.zoom), int(self.HEIGHT / self.zoom), self.zoom)

        # Light animation
        self.light_angle = 0

        # Initialize health
        self.health = 3  # Initialize player's health

    def update_enemy(self):
        damage = self.enemy.update(self.player.rect)
        if damage > 0:
            self.player.take_damage(damage)  # Pemain terkena serangan musuh
            self.health -= damage  # Kurangi health pemain ketika terkena serangan musuh

    def handle_input(self):
        keys = pygame.key.get_pressed()
        original_x = self.player.rect.x

        if keys[pygame.K_LEFT]:
            self.player.move(dx=-self.player.speed)
        if keys[pygame.K_RIGHT]:
            self.player.move(dx=self.player.speed)

        self.check_horizontal_collisions(original_x)

    def check_horizontal_collisions(self, original_x):
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                if self.player.rect.x < original_x:
                    self.player.rect.left = platform.rect.right
                else:
                    self.player.rect.right = platform.rect.left

    def check_vertical_collisions(self):
        self.player.on_ground = False
        collided = False
        for platform in self.platforms:
            if platform.is_wall:  # Skip tembok untuk tabrakan vertikal
                continue
            if self.player.rect.colliderect(platform.rect):
                collided = True
                if self.player.velocity_y > 0:
                    self.player.rect.bottom = platform.rect.top
                    self.player.velocity_y = 0
                    self.player.on_ground = True
                elif self.player.velocity_y < 0:
                    self.player.rect.top = platform.rect.bottom
                    self.player.velocity_y = 0
        return collided

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.state == "menu":
                        play_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2-40, 200, 50)
                        exit_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2+40, 200, 50)
                        if play_rect.collidepoint(mouse_pos):
                            self.state = "playing"
                        elif exit_rect.collidepoint(mouse_pos):
                            running = False
                    elif self.state == "paused":
                        resume_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2-40, 200, 50)
                        exit_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2+40, 200, 50)
                        if resume_rect.collidepoint(mouse_pos):
                            self.state = "playing"
                        elif exit_rect.collidepoint(mouse_pos):
                            running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = "paused" if self.state == "playing" else "playing"
                # Pengecekan SPACE di sini (hanya trigger saat ditekan)
                    if event.key == pygame.K_SPACE and self.state == "playing":
                        self.jump_requested = True                    

            if self.state == "playing":
                self.handle_input()
                self.player.apply_gravity()
                self.check_vertical_collisions()
                self.camera.update(self.player, self.WIDTH, self.HEIGHT)
                self.update_enemy()  # Update enemy behavior
                if self.jump_requested:
                    if self.player.on_ground:
                        self.player.jump()
                    self.jump_requested = False

            if self.state == "menu":
                self.screen.blit(self.background, (0, 0))
                play_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2-40, 200, 50)
                exit_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2+40, 200, 50)
                # Draw transparent rectangles for menu buttons
                play_overlay = pygame.Surface((play_rect.width, play_rect.height), pygame.SRCALPHA)
                play_overlay.fill((0, 0, 0, 0))  # 100 = alpha for transparency
                self.screen.blit(play_overlay, play_rect.topleft)

                exit_overlay = pygame.Surface((exit_rect.width, exit_rect.height), pygame.SRCALPHA)
                exit_overlay.fill((0, 0, 0, 0))
                self.screen.blit(exit_overlay, exit_rect.topleft)
                # Center the images in the rects
                play_img_rect = self.start_button_img.get_rect(center=play_rect.center)
                exit_img_rect = self.exit_button_img.get_rect(center=exit_rect.center)
                self.screen.blit(self.start_button_img, play_img_rect.topleft)
                self.screen.blit(self.exit_button_img, exit_img_rect.topleft)

            elif self.state in ("playing", "paused"):
                draw_background(self.screen, self.background, self.camera.rect, self.WIDTH, self.HEIGHT)
                draw_objects(self.screen, self.player, self.platforms, self.camera.rect, self.zoom)

                # Update radius cahaya
                self.light_angle += 0.05
                pulse = math.sin(self.light_angle) * 8  # denyut
                light_radius = int(120 + pulse)

                draw_darkness_with_light(self.screen, self.player, self.camera.rect, self.zoom, light_radius)

                # Draw enemy
                self.enemy.draw(self.screen, self.camera.rect, self.zoom)

                if self.state == "paused":
                    overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 128))
                    self.screen.blit(overlay, (0, 0))
                    resume_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2-40, 200, 50)
                    exit_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2+40, 200, 50)
                    pygame.draw.rect(self.screen, (0, 200, 0), resume_rect)
                    pygame.draw.rect(self.screen, (200, 0, 0), exit_rect)
                    text_resume = self.font.render("Resume", True, (255,255,255))
                    text_exit_pause = self.font.render("Exit", True, (255,255,255))
                    self.screen.blit(text_resume, (resume_rect.x+50, resume_rect.y+15))
                    self.screen.blit(text_exit_pause, (exit_rect.x+70, exit_rect.y+15))

            # Draw player's health on screen
            health_text = self.font.render(f"Health: {self.health}", True, (255, 0, 0))
            self.screen.blit(health_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()
