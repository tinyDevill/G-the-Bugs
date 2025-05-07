import pygame
import sys
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
        self.state = "menu"  # State: menu, playing, paused
        self.font = pygame.font.Font(None, 36)

        # Load assets
        self.background, self.platform_img, self.wall_img, self.light_img = load_assets(self.WIDTH, self.HEIGHT)  # Perbaikan penutup kurung
        
        # Scale light image sesuai zoom awal
        self.scaled_light = pygame.transform.scale(
            self.light_img,
            (int(self.light_img.get_width() * self.zoom), 
            int(self.light_img.get_height() * self.zoom))  # Perbaikan sintaks tuple
        )
        
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
                
                # Handle mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.state == "menu":
                        # Cek klik tombol menu
                        play_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2-40, 200, 50)
                        exit_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2+40, 200, 50)
                        if play_rect.collidepoint(mouse_pos):
                            self.state = "playing"
                        elif exit_rect.collidepoint(mouse_pos):
                            running = False
                    elif self.state == "paused":
                        # Cek klik tombol pause
                        resume_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2-40, 200, 50)
                        exit_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2+40, 200, 50)
                        if resume_rect.collidepoint(mouse_pos):
                            self.state = "playing"
                        elif exit_rect.collidepoint(mouse_pos):
                            running = False
                
                # Handle tombol pause
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.state == "playing":
                            self.state = "paused"
                        elif self.state == "paused":
                            self.state = "playing"

            # Update game state
            if self.state == "playing":
                self.handle_input()
                self.player.apply_gravity()
                self.check_vertical_collisions()
                self.camera.update(self.player, self.WIDTH, self.HEIGHT)

            # Rendering
            if self.state == "menu":
                # Draw menu
                self.screen.blit(self.background, (0, 0))
                # Tombol
                play_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2-40, 200, 50)
                exit_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2+40, 200, 50)
                pygame.draw.rect(self.screen, (0, 200, 0), play_rect)
                pygame.draw.rect(self.screen, (200, 0, 0), exit_rect)
                # Text
                text_play = self.font.render("Play", True, (255,255,255))
                text_exit = self.font.render("Exit", True, (255,255,255))
                self.screen.blit(text_play, (play_rect.x+70, play_rect.y+15))
                self.screen.blit(text_exit, (exit_rect.x+70, exit_rect.y+15))
            
            elif self.state in ("playing", "paused"):
                # Draw game
                draw_background(self.screen, self.background, self.camera.rect, self.WIDTH, self.HEIGHT)
                draw_objects(self.screen, self.player, self.platforms, self.camera.rect, self.zoom, self.light_img)
                
                if self.state == "paused":
                    # Overlay gelap
                    overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 128))
                    self.screen.blit(overlay, (0, 0))
                    # Tombol
                    resume_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2-40, 200, 50)
                    exit_rect = pygame.Rect(self.WIDTH//2-100, self.HEIGHT//2+40, 200, 50)
                    pygame.draw.rect(self.screen, (0, 200, 0), resume_rect)
                    pygame.draw.rect(self.screen, (200, 0, 0), exit_rect)
                    # Text
                    text_resume = self.font.render("Resume", True, (255,255,255))
                    text_exit_pause = self.font.render("Exit", True, (255,255,255))
                    self.screen.blit(text_resume, (resume_rect.x+50, resume_rect.y+15))
                    self.screen.blit(text_exit_pause, (exit_rect.x+70, exit_rect.y+15))

            pygame.display.flip()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()
